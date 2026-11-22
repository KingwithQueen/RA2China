"""Read-only comparison of RA2's configured Windows x86 Ninja graphs.

Usage: python -B tools/verify_static_contract_graph.py DEFAULT_BUILD OPT_IN_BUILD
       python -B tools/verify_static_contract_graph.py --self-test

Both directories must already contain CMake's Release Ninja metadata, generated
with RA2_ENABLE_STATIC_CONTRACTS respectively OFF and ON and with the same x86
toolchain. This checks the known CMake/MSVC graph shape, not arbitrary Ninja
syntax, source contents, build results, or what regeneration might produce.
Snapshot source paths need not exist. No graph command or included file path
from the metadata is executed or opened.
"""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path, PureWindowsPath
import re
import shlex
import stat
import sys


OPTION = "RA2_ENABLE_STATIC_CONTRACTS"
TARGET = "ra2_static_contracts"
PRODUCTION = "ra2"
LINK = "C_EXECUTABLE_LINKER__ra2_Release"
CONTRACTS = {
    "ra2/tools/crew_percent_static_contract.c",
    "ra2/tools/ground_movement_static_contract.c",
}
VARS = {"ninja_required_version", "CONFIGURATION", "cmake_ninja_workdir"}
UTILITIES = {"CUSTOM_COMMAND", "RERUN_CMAKE", "VERIFY_GLOBS", "CLEAN", "HELP"}
COMPILE_KEYS = {
    "CONFIG", "DEFINES", "FLAGS", "INCLUDES", "OBJECT_DIR", "OBJECT_FILE_DIR",
    "TARGET_COMPILE_PDB", "TARGET_PDB", "TARGET_SUPPORT_DIR",
}
CONTRACT_FLAGS = (
    "/DWIN32 /D_WINDOWS /O2 /Ob2 /DNDEBUG -std:c17 -MT /W4 /WX /std:c17 /utf-8"
)
META = ("CMakeCache.txt", "compile_commands.json", "build.ninja", "CMakeFiles/rules.ninja")
FILE_LIMIT = 2 * 1024 * 1024


class GraphError(ValueError):
    """The input disagrees with the known graph shape."""


def need(condition, message):
    if not condition:
        raise GraphError(message)


def compiler_rule(target):
    return f"C_COMPILER__{target}_unscanned_Release"


def fence(target):
    return f"cmake_object_order_depends_target_{target}"


def local_windows_path(value, name, *, compact=True):
    need(isinstance(value, str) and "\r" not in value and "\n" not in value,
         f"invalid {name} path")
    p = PureWindowsPath(value)
    need(p.is_absolute() and re.fullmatch(r"[A-Za-z]:", p.drive) and ".." not in p.parts,
         f"invalid {name} path")
    if compact:
        need(re.fullmatch(r"[A-Za-z]:\\[A-Za-z0-9_.\\-]+", str(p)),
             f"{name} path requires unsupported Ninja escaping")
    return p


def fields(text, wanted):
    result = {}
    for line in text.splitlines():
        m = re.fullmatch(r"([^#/:][^:=]*):([A-Z_]+)=(.*)", line)
        if m and m[1] in wanted:
            key, value = m[1], m[3]
            need(key not in result, "duplicate CMake cache field")
            result[key] = value
    need(set(result) == wanted, "missing CMake cache fields")
    return result


def assignment(line):
    key, separator, value = line.partition(" = ")
    need(separator and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key),
         "unsupported Ninja assignment")
    return key, value


@dataclass
class Edge:
    outputs: tuple
    rule: str
    inputs: tuple
    attrs: dict


def ninja_words(text):
    # Retain the literal escapes in names; never evaluate Ninja variables.
    words, piece = [], []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "$":
            need(i + 1 < len(text) and text[i + 1] in " :$", "unsupported Ninja path escape")
            piece.append(text[i:i + 2])
            i += 2
            continue
        if ch in " \t":
            if piece:
                words.append("".join(piece))
                piece.clear()
        else:
            piece.append(ch)
        i += 1
    if piece:
        words.append("".join(piece))
    return words


def edges(text):
    result = {}
    order = []
    globals_seen = {}
    defaults = []
    includes = []
    active = None
    for line in text.split("\n"):
        if not line or line.lstrip().startswith("#"):
            continue
        need(not line.endswith("$") and "\x00" not in line, "unsupported Ninja continuation")
        if line.startswith("  "):
            need(active is not None, "orphaned Ninja edge assignment")
            key, value = assignment(line[2:])
            need(key not in active.attrs, "duplicate Ninja edge attribute")
            need(key not in {"LAUNCHER", "CODE_CHECK", "command"}, "unexpected command override")
            active.attrs[key] = value
            continue
        active = None
        if line.startswith("build "):
            left, sep, right = line[6:].partition(": ")
            need(sep and left and right, "invalid Ninja build edge")
            out = tuple(x for x in ninja_words(left) if x != "|")
            rule, *inputs = ninja_words(right)
            need(out and "$" not in rule, "unknown Ninja rule reference")
            active = Edge(out, rule, tuple(inputs), {})
            for name in out:
                need(name not in result, "duplicate Ninja edge output")
                result[name] = active
            order.append(active)
        elif line.startswith("default "):
            defaults.append(line)
        elif line.startswith("include "):
            includes.append(line)
        else:
            key, value = assignment(line)
            need(key in VARS and key not in globals_seen, "unsupported Ninja global statement")
            globals_seen[key] = value
    need(defaults == ["default all"] and includes == [r"include CMakeFiles\rules.ninja"],
         "unsupported Ninja graph entry point or include")
    need(set(globals_seen) == VARS and globals_seen["CONFIGURATION"] == "Release",
         "unsupported Ninja configuration")
    return result, order


def rules(text, enabled):
    seen = {}
    current = None
    prefix = False
    for line in text.split("\n"):
        if not line or line.lstrip().startswith("#"):
            continue
        need(not line.endswith("$") and "\x00" not in line, "unsupported Ninja rule continuation")
        if line.startswith("rule "):
            name = line[5:]
            need(re.fullmatch(r"[A-Za-z0-9_]+", name) and name not in seen,
                 "unsupported or duplicate Ninja rule")
            current = seen[name] = {}
        elif line.startswith("  ") and current is not None:
            key, value = assignment(line[2:])
            need(key not in current, "duplicate rule attribute")
            current[key] = value
        else:
            need(not prefix and not seen and line.startswith("msvc_deps_prefix = "),
                 "unsupported Ninja rule statement")
            prefix = True  # May be localized; it is never decoded as a command.
    expected = UTILITIES | {LINK, compiler_rule(PRODUCTION)}
    if enabled:
        expected.add(compiler_rule(TARGET))
    need(prefix and set(seen) == expected, "unexpected Ninja rule set")
    return seen


def json_fields(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate compile database field")
        result[key] = value
    return result


def argv(text):
    return tuple(shlex.split(text, posix=False))


def expect_edge(table, name, rule, inputs):
    node = table.get(name)
    need(node is not None and node.outputs == (name,) and node.rule == rule
         and node.inputs == inputs, f"unexpected dependency for {name}")
    return node


def graph_mode(parts, enabled):
    cache, database, ninja, rule_text = parts
    names = {"CMAKE_GENERATOR", "CMAKE_HOME_DIRECTORY", "CMAKE_CACHEFILE_DIR",
             "CMAKE_C_COMPILER", "CMAKE_BUILD_TYPE", "RA2_TARGET", OPTION}
    props = fields(cache, names)
    need(props["CMAKE_GENERATOR"] == "Ninja" and props["CMAKE_BUILD_TYPE"] == "Release"
         and props["RA2_TARGET"] == "game" and props[OPTION] == ("ON" if enabled else "OFF"),
         "expected Ninja Release game configuration with requested option state")
    project = local_windows_path(props["CMAKE_HOME_DIRECTORY"], "CMake source")
    build = local_windows_path(props["CMAKE_CACHEFILE_DIR"], "CMake build")
    compiler = local_windows_path(props["CMAKE_C_COMPILER"], "MSVC compiler", compact=False)
    need(project.name == "ra2" and compiler.name.lower() == "cl.exe"
         and compiler.parent.name.lower() == "x86", "expected an x86 MSVC RA2 graph")
    source = project.parent
    encoded = str(source).replace(":", "_", 1)

    def rebase(text):
        return text.replace(encoded + "\\", "<external-source>\\").replace(
            str(source) + "\\", "<source>\\")

    table, ordered = edges(ninja)
    commands = rules(rule_text, enabled)
    need(all(e.rule == "phony" or e.rule in commands for e in ordered), "undeclared Ninja rule")
    expected_command = (f'\u0024{{LAUNCHER}}\u0024{{CODE_CHECK}}"{compiler}"  /nologo '
                        "$DEFINES $INCLUDES $FLAGS /showIncludes /Fo$out /Fd$TARGET_COMPILE_PDB /FS -c $in")
    for target in ((PRODUCTION, TARGET) if enabled else (PRODUCTION,)):
        r = commands[compiler_rule(target)]
        need(r == {"deps": "msvc", "command": expected_command, "description": "Building C object $out"},
             f"unsupported compile command for {target}")
        need(not expect_edge(table, fence(target), "phony", ("||", ".")).attrs and "." not in table,
             "object order-only fence is not inert")
    need(not expect_edge(table, "all", "phony", ("ra2.exe",)).attrs and
         not expect_edge(table, "ra2", "phony", ("ra2.exe",)).attrs, "default target is not isolated")

    raw = json.loads(database, object_pairs_hook=json_fields)
    need(isinstance(raw, list) and 0 < len(raw) <= 4096, "unsupported compile database size")
    prod = {}
    contracts = {}
    output_names = set()
    for row in raw:
        need(isinstance(row, dict) and set(row) == {"directory", "file", "output", "command"}
             and all(isinstance(v, str) for v in row.values()), "unsupported compile database row")
        need(local_windows_path(row["directory"], "compile directory") == build, "compile directory differs")
        file = local_windows_path(row["file"], "compile input")
        output = local_windows_path(row["output"], "compile output")
        need(file.is_relative_to(source) and output.is_relative_to(build), "compile path outside snapshot metadata")
        rel = file.relative_to(source).as_posix()
        obj = str(output.relative_to(build))
        is_contract = rel in CONTRACTS
        t = TARGET if is_contract else PRODUCTION
        group = contracts if is_contract else prod
        need(rel not in group and obj not in output_names and (enabled or not is_contract), "duplicate or disabled compile row")
        if is_contract:
            want_obj = f"CMakeFiles\\{TARGET}.dir\\tools\\{file.name}.obj"
        elif file.is_relative_to(project):
            need(rel.startswith("ra2/src/") and rel.endswith(".c"), "unexpected project translation unit")
            want_obj = f"CMakeFiles\\ra2.dir\\{file.relative_to(project)}.obj"
        else:
            need(rel.startswith("pcrecomp/runtime/") and rel.endswith(".c"), "unexpected outside translation unit")
            want_obj = f"CMakeFiles\\ra2.dir\\{encoded}\\{file.relative_to(source)}.obj"
        need(obj == want_obj, "unexpected owned object path")
        edge = expect_edge(table, obj, compiler_rule(t), (str(file).replace(":", "$:", 1), "||", fence(t)))
        attrs = edge.attrs
        need(set(attrs) <= COMPILE_KEYS and attrs.get("CONFIG") == "Release" and
             attrs.get("OBJECT_DIR") == f"CMakeFiles\\{t}.dir" and
             attrs.get("OBJECT_FILE_DIR") == str(PureWindowsPath(obj).parent) and
             attrs.get("TARGET_COMPILE_PDB") == f"CMakeFiles\\{t}.dir\\",
             "unexpected compile edge attributes")
        rebuilt = (f'"{compiler}"', "/nologo", *argv(attrs.get("DEFINES", "")), *argv(attrs.get("INCLUDES", "")),
                   *argv(attrs.get("FLAGS", "")), "/Fo"+obj, "/Fd"+attrs["TARGET_COMPILE_PDB"], "/FS", "-c", str(file))
        need(argv(row["command"]) == rebuilt, "compile database disagrees with Ninja object command")
        if is_contract:
            need(not attrs.get("DEFINES") and attrs.get("FLAGS") == CONTRACT_FLAGS
                 and attrs.get("INCLUDES") == "-I"+str(project/"src/gameplay"),
                 "unexpected opt-in compile flags")
        group[rel] = (obj, rebase(row["command"]))
        output_names.add(obj)

    need(prod and set(contracts) == (CONTRACTS if enabled else set()), "missing or extra contract objects")
    object_edges = {x for e in ordered if e.rule in (compiler_rule(PRODUCTION), compiler_rule(TARGET)) for x in e.outputs}
    need(object_edges == output_names, "extra compile edge not in the database")
    link = table.get("ra2.exe")
    prod_objects = {item[0] for item in prod.values()}
    need(link is not None and link.outputs == ("ra2.exe",) and link.rule == LINK and
         len(link.inputs) == len(prod_objects) and set(link.inputs) == prod_objects and
         [e.outputs for e in ordered if e.rule == LINK] == [("ra2.exe",)],
         "production link must contain only its documented objects")
    need(link.attrs.get("PRE_LINK") == link.attrs.get("POST_BUILD") == "cd ." and
         "/machine:X86" in link.attrs.get("LINK_FLAGS", "").split() and link.attrs.get("TARGET_FILE") == "ra2.exe",
         "unsupported x86 production link edge")
    if enabled:
        objset = {item[0] for item in contracts.values()}
        target = table.get(TARGET)
        need(target is not None and target.outputs == (TARGET,) and target.rule == "phony"
             and len(target.inputs) == 2 and set(target.inputs) == objset and not target.attrs,
             "opt-in target must lead only to its two objects")
        allowed = objset | {TARGET, fence(TARGET)}
        need(all(e.outputs[0] in allowed or TARGET not in " ".join((*e.outputs, *e.inputs, *e.attrs.values()))
                 for e in ordered), "opt-in dependency leaked into another Ninja edge")
    else:
        need(TARGET not in ninja, "opt-in target present in the disabled graph")

    prod_signature = {k: (rebase(v[0]), v[1]) for k,v in prod.items()}
    link_signature = (tuple(rebase(x) for x in link.inputs),
                      {k:rebase(v) for k,v in link.attrs.items()}, commands[LINK])
    return prod_signature, link_signature, len(contracts), build


def verify(default_parts, opt_parts):
    default, default_link, n_off, original = graph_mode(default_parts, False)
    opt, opt_link, n_on, enabled = graph_mode(opt_parts, True)
    need(original != enabled, "supply distinct configured build directories")
    need(default == opt and default_link == opt_link, "enabling contracts changed the production graph")
    return dict(production_units=len(default), default_contract_units=n_off,
                opt_in_contract_units=n_on, opt_in_link_or_archive_edges=0)

def read_parts(directory):
    """Open only the four literal names under a caller-selected local directory."""
    root = Path(directory).absolute()
    need(re.fullmatch(r"[A-Za-z]:\\", root.anchor), "select local Windows graph directories")
    for parent in (*reversed(root.parents), root, root/"CMakeFiles"):
        st = parent.lstat()
        need(stat.S_ISDIR(st.st_mode) and not getattr(st, "st_file_attributes", 0) & 0x400,
             "graph directory cannot be a reparse point")
    parts = []
    for name in META:
        path = root/name
        st = path.lstat()
        need(stat.S_ISREG(st.st_mode) and not getattr(st, "st_file_attributes", 0) & 0x400
             and st.st_size <= FILE_LIMIT, "invalid metadata file or size")
        with path.open("rb") as stream:
            data = stream.read(FILE_LIMIT + 1)
        need(len(data) <= FILE_LIMIT and b"\0" not in data, "unsupported metadata bytes")
        # Rules may include a localized MSVC /showIncludes prefix.
        parts.append(data.decode("latin-1" if name.endswith(".ninja") else "utf-8-sig").replace("\r\n", "\n"))
    return tuple(parts)


def fixture(enabled, stem):
    """Deliberately small graph strings; no files, process commands, or game data."""
    compiler = r"E:\VS\Hostx64\x86\cl.exe"
    source = PureWindowsPath("D:/" + stem + "/snapshot")
    project = source/"ra2"
    directory = PureWindowsPath("D:/" + stem + "/build")
    cache = "\n".join((
        "CMAKE_GENERATOR:INTERNAL=Ninja",
        "CMAKE_BUILD_TYPE:STRING=Release",
        "CMAKE_HOME_DIRECTORY:INTERNAL="+project.as_posix(),
        "CMAKE_CACHEFILE_DIR:INTERNAL="+directory.as_posix(),
        "CMAKE_C_COMPILER:STRING="+compiler,
        "RA2_TARGET:STRING=game",
        OPTION+":BOOL="+("ON" if enabled else "OFF"),
    ))
    graph = ["ninja_required_version = 1.8", "CONFIGURATION = Release", r"include CMakeFiles\rules.ninja",
             "cmake_ninja_workdir = "+str(directory).replace(":", "$:", 1)+"\\"]
    rule_lines = ["msvc_deps_prefix = fixture only"]
    command = (f'\u0024{{LAUNCHER}}\u0024{{CODE_CHECK}}"{compiler}"  /nologo '
               "$DEFINES $INCLUDES $FLAGS /showIncludes /Fo$out /Fd$TARGET_COMPILE_PDB /FS -c $in")
    for target in ((PRODUCTION, TARGET) if enabled else (PRODUCTION,)):
        rule_lines.extend((f"rule {compiler_rule(target)}", "  deps = msvc", "  command = "+command,
                           "  description = Building C object $out"))
        graph.append(f"build {fence(target)}: phony || .")
    rule_lines.extend((f"rule {LINK}", "  command = fixture-link-metadata"))
    for name in sorted(UTILITIES):
        rule_lines.extend((f"rule {name}", "  command = fixture-ignored-metadata"))
    production = ("ra2/src/example.c", "pcrecomp/runtime/native32/fixture.c")
    entries = (*production, *sorted(CONTRACTS)) if enabled else production
    paths = {PRODUCTION: [], TARGET: []}
    rows = []
    for rel in entries:
        item = source/rel
        target = TARGET if rel in CONTRACTS else PRODUCTION
        owner = "CMakeFiles\\"+target+".dir"
        if target == TARGET:
            ext = "tools\\"+item.name
        elif item.is_relative_to(project):
            ext = str(item.relative_to(project))
        else:
            ext = str(source).replace(":", "_", 1)+"\\"+str(item.relative_to(source))
        output = owner+"\\"+ext+".obj"
        paths[target].append(output)
        include = "-I"+str(project/"src/gameplay")
        flags = CONTRACT_FLAGS
        graph.extend((
            f"build {output}: {compiler_rule(target)} " + str(item).replace(":", "$:", 1)+f" || {fence(target)}",
            "  CONFIG = Release", "  FLAGS = "+flags, "  INCLUDES = "+include,
            "  OBJECT_DIR = "+owner, "  OBJECT_FILE_DIR = "+str(PureWindowsPath(output).parent),
            "  TARGET_COMPILE_PDB = "+owner+"\\",
        ))
        rows.append(dict(directory=directory.as_posix(), file=item.as_posix(), output=(directory/output).as_posix(),
                         command=f'"{compiler}"  /nologo {include} {flags} /Fo{output} /Fd{owner}\\ /FS -c {item}'))
    graph.extend((f"build ra2.exe: {LINK} "+" ".join(paths[PRODUCTION]),
                  "  LINK_FLAGS = /machine:X86", "  TARGET_FILE = ra2.exe",
                  "  PRE_LINK = cd .", "  POST_BUILD = cd .",
                  "build all: phony ra2.exe", "build ra2: phony ra2.exe", "default all"))
    if enabled:
        graph.append(f"build {TARGET}: phony "+" ".join(paths[TARGET]))
    return (cache, json.dumps(rows), "\n".join(graph), "\n".join(rule_lines))


def self_test():
    off, on = fixture(False, "off-test"), fixture(True, "on-test")
    need(verify(off, on) == dict(production_units=2, default_contract_units=0, opt_in_contract_units=2,
                                 opt_in_link_or_archive_edges=0), "positive rebased fixture")
    need(ninja_words(r"E$:\Program$ Files\Tools | D$:\Source") ==
         [r"E$:\Program$ Files\Tools", "|", r"D$:\Source"], "literal path lexer")
    accepted = 2

    def edited(parts, index, before, after):
        values = list(parts)
        need(before in values[index], "broken self-test fixture")
        values[index] = values[index].replace(before, after, 1)
        return tuple(values)

    def trim_db(parts):
        rows = json.loads(parts[1])
        return parts[:1]+(json.dumps(rows[:-1]),)+parts[2:]

    def append_duplicate(parts):
        rows = json.loads(parts[1])
        return parts[:1]+(json.dumps(rows+[rows[0]]),)+parts[2:]

    victims = (
        ("all-leak", off, edited(on, 2, "build all: phony ra2.exe", "build all: phony ra2.exe "+TARGET)),
        ("missing-object", off, trim_db(on)),
        ("extra-object", off, append_duplicate(on)),
        ("contract-link", off, edited(on, 2, f"build {TARGET}: phony", f"build {TARGET}: {LINK}")),
        ("extra-opt-in-input", off, edited(on, 2, f"build {TARGET}: phony ", f"build {TARGET}: phony ra2.exe ")),
        ("production-input-drift", off, edited(on, 2, "build ra2.exe: "+LINK+" ", "build ra2.exe: "+LINK+" extra.obj ")),
        ("production-flags-drift", off, edited(on, 1, "/O2", "/Od")),
        ("order-fence-leak", off, edited(on, 2, f"build {fence(TARGET)}: phony || .",
                                        f"build {fence(TARGET)}: phony || ra2.exe")),
        ("unsupported-include", off, edited(on, 2, r"include CMakeFiles\rules.ninja", "include unknown.ninja")),
        ("unsupported-rule", off, edited(on, 3, "rule HELP", "rule NEW_RULE")),
        ("option-off-mismatch", edited(off, 0, OPTION+":BOOL=OFF", OPTION+":BOOL=ON"), on),
        ("duplicate-row-property", off, edited(on, 1, '"file":', '"file": "ignored", "file":')),
    )
    for label, default, opt in victims:
        try:
            verify(default, opt)
        except GraphError:
            continue
        raise GraphError(f"self-test unexpectedly accepted {label}")
    return dict(self_tests_passed=accepted+len(victims), rejected_fixtures=len(victims))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("default_build", nargs="?")
    parser.add_argument("opt_in_build", nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test and (args.default_build or args.opt_in_build):
        parser.error("--self-test does not take graph directories")
    if not args.self_test and not (args.default_build and args.opt_in_build):
        parser.error("provide the existing default and opt-in build directories")
    try:
        report = self_test() if args.self_test else verify(read_parts(args.default_build), read_parts(args.opt_in_build))
    except (ValueError, OSError) as exc:
        print(f"Graph verification failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
