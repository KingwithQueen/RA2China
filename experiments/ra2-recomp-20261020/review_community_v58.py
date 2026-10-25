"""Read public fixed-revision references; retain hashes/line anchors, no imported engine bodies."""
from run_batch_v58 import *
import tempfile
def fetch(url):
 assert url.startswith(('https://api.github.com/repos/','https://raw.githubusercontent.com/'))
 with tempfile.NamedTemporaryFile(dir=R/'temp',prefix='community-ref-v58-',suffix='.dat',delete=False) as f:cache=Path(f.name)
 assert cache.resolve().parent==(R/'temp').resolve()
 try:
  command="$ErrorActionPreference='Stop'; Invoke-WebRequest -Uri $env:RA2_LOCAL_REFERENCE_URL -OutFile $env:RA2_LOCAL_REFERENCE_DESTINATION"
  subprocess.run(['pwsh','-NoProfile','-Command',command],check=True,timeout=45,env=dict(os.environ,RA2_LOCAL_REFERENCE_URL=url,RA2_LOCAL_REFERENCE_DESTINATION=str(cache)),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  return cache.read_bytes()
 finally:cache.unlink(missing_ok=True)
def commit(repo,branch):return json.loads(fetch('https://api.github.com/repos/'+repo+'/commits/'+branch))['sha']
sources=[]
def source(repo,rev,path,patterns):
 url='https://raw.githubusercontent.com/'+repo+'/'+rev+'/'+path;raw=fetch(url);lines=raw.decode('utf-8-sig').splitlines()
 anchors={name:[i+1 for i,l in enumerate(lines) if needle in l][:12] for name,needle in patterns.items()}
 sources.append(dict(repository=repo,revision=rev,path=path,url='https://github.com/'+repo+'/blob/'+rev+'/'+path,raw_url=url,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),line_anchors=anchors))
g='08a5f602fe1bcf8ec69e68ecd709bd7de9ee3944'
source('r-melvin/gagarin',g,'match/_layout/astar_00746000.h',{'astar_attempt_path':'AttemptPath','global_instance':'Instance'})
source('r-melvin/gagarin',g,'match/movement/foot_class_find_path_methods.cpp',{'foot_find_path':'FootClass::FindPath','astar_dispatch':'DAT_0087E8B8.FindPath'})
source('r-melvin/gagarin',g,'match/movement/unit_class_astar_attempt_methods.h',{'bridge_flag':'0x140','map_height':'0x1C8','astar_instance':'0x87E8B8'})
ea=commit('electronicarts/CnC_Remastered_Collection','master')
source('electronicarts/CnC_Remastered_Collection',ea,'REDALERT/FINDPATH.CPP',{'los_edge_search':'The path algorithm works','optimize_moves':'FootClass::Optimize_Moves','deleted_slot_marker':'#define\tEMPTY','passability':'Passable_Cell'})
ph=commit('Phobos-developers/Phobos','develop')
source('Phobos-developers/Phobos',ph,'README.md',{'engine_extension':'extend','yuris_revenge':'Revenge'})
assert any(s['line_anchors'].get('astar_attempt_path') for s in sources)
write(S/'community-reference-review.json',dict(passed=True,client_date='2026-10-25',sources=sources,private_project_uploaded=False,third_party_engine_code_imported=False,reference_only=True,acceptance_authority='Locked original Red Alert 2 1.006 plus finite functional/effect comparison',findings=[
 dict(project='gagarin',target='Yuri Revenge gamemd.exe 1.001',useful='AStar/Foot FindPath dispatch names and alternate bridge-layer flag provide version-aware search/navigation cues.',limit='The three inspected files cover declarations/wrappers and one caller, not this project local path algorithm or a proved 1.006 address mapping.'),
 dict(project='EA Red Alert source',target='Earlier Red Alert engine',useful='Separates candidate passability checks from path publication and names empty direction slots -2; useful for service naming and successful-only publication.',limit='Its LOS/edge-follow search and command-pair optimizer differ from current layered search and local turn/segment rules. No thresholds, address constants or replacement engine body adopted.'),
 dict(project='Phobos',target='Yuri Revenge engine extension',useful='Further index for extension hooks and established terminology.',limit='An extension of the retail engine, not an interchangeable standalone C17 RA2 1.006 engine.')],application='Use candidate validation and publication names to organize the existing independently reconstructed C17 code. Keep turn-origin versus segment-point threat checks, control-word arithmetic and bridge-level reads grounded in original probes.'))
print(dict(passed=True,references=len(sources),gagarin=g,ea=ea,phobos=ph,third_party_code_imported=False))
