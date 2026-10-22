"""只观察原版启动异常；外部调试事件全部交还 Windows，不改游戏数据或异常处置。"""
import ctypes as C
from ctypes import wintypes as W
import importlib.util
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence/movement-prepare-v3/startup-debug'
OUT.mkdir(exist_ok=False)
k32 = C.WinDLL('kernel32', use_last_error=True)


class ExceptionRecord(C.Structure):
    _fields_ = [('code', W.DWORD), ('flags', W.DWORD), ('record', C.c_void_p), ('address', C.c_void_p),
                ('count', W.DWORD), ('info', C.c_size_t * 15)]


class ExceptionInfo(C.Structure):
    _fields_ = [('record', ExceptionRecord), ('first', W.DWORD)]


class DebugUnion(C.Union):
    _fields_ = [('exception', ExceptionInfo), ('raw', C.c_byte * 160)]


class DebugEvent(C.Structure):
    _fields_ = [('kind', W.DWORD), ('pid', W.DWORD), ('tid', W.DWORD), ('data', DebugUnion)]


k32.WaitForDebugEvent.argtypes = [C.POINTER(DebugEvent), W.DWORD]
k32.ContinueDebugEvent.argtypes = [W.DWORD, W.DWORD, W.DWORD]
k32.ReadProcessMemory.argtypes = [W.HANDLE, C.c_void_p, C.c_void_p, C.c_size_t, C.POINTER(C.c_size_t)]
k32.ReadProcessMemory.restype = W.BOOL


def memory(process, address, size):
    output = C.create_string_buffer(size)
    read = C.c_size_t()
    if not k32.ReadProcessMemory(process, address, output, size, C.byref(read)):
        return b''
    return output.raw[:read.value]


os.environ['RA2_TARGET'] = 'game'
spec = importlib.util.spec_from_file_location('playtest', ROOT / 'ra2/tools/playtest.py')
test = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test)
game = Path(test.farm(str(OUT / 'game')))
cmd = json.loads((ROOT / 'evidence/movement-prepare-v3/runs/retry-path-rerun/original/command.json').read_text(encoding='utf-8'))
for flag, value in [('--game', game), ('--exe', game / 'game.exe'), ('--state-log', OUT / 'state.jsonl')]:
    cmd[cmd.index(flag) + 1] = str(value)
(OUT / 'command.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2), encoding='utf-8')
events = []
with (OUT / 'run.log').open('w', encoding='utf-8') as log:
    process = subprocess.Popen(cmd, cwd=ROOT / 'ra2', stdout=log, stderr=subprocess.STDOUT, creationflags=2)
    while True:
        event = DebugEvent()
        if not k32.WaitForDebugEvent(C.byref(event), 10000):
            if process.poll() is not None:
                break
            continue
        status = 0x10002
        if event.kind == 1:
            record = event.data.exception.record
            entry = {'code': hex(record.code), 'address': hex(record.address or 0), 'first': event.data.exception.first,
                     'parameters': [hex(v) for v in record.info[:record.count]]}
            if record.code == 0xE06D7363 and record.count >= 3:
                obj, throw = record.info[1], record.info[2]
                entry['object_bytes'] = memory(process._handle, obj, 64).hex()
                data = memory(process._handle, throw, 16)
                entry['throw_bytes'] = data.hex()
                if len(data) == 16:
                    array = int.from_bytes(data[12:16], 'little')
                    types = memory(process._handle, array, 8)
                    if len(types) == 8:
                        first_type = int.from_bytes(types[4:8], 'little')
                        catch = memory(process._handle, first_type, 28)
                        if len(catch) == 28:
                            descriptor = int.from_bytes(catch[4:8], 'little')
                            entry['type'] = memory(process._handle, descriptor + 8, 128).split(b'\0')[0].decode('ascii', errors='replace')
            events.append(entry)
            status = 0x10002 if record.code == 0x80000003 else 0x80010001
        k32.ContinueDebugEvent(event.pid, event.tid, status)
        if event.kind == 5:
            break
    code = process.wait(timeout=10)
result = {'exit_code': code, 'events': events}
(OUT / 'exceptions.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
