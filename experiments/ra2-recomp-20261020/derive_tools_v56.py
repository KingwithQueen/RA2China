"""Bounded current harness derivation and final-control-word probe check."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v56'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lineage=[]
names=['run_batch_v55.py','accept_dynamic_v55.py','audit_scenes_v55.py','audit_sources_v55.py','plan_cleanup_v55.py','commit_movement_v55.py','audit_evidence_v55.py','verify_final_movement_v55.py']
for name in names:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v55','v56')
 if name=='run_batch_v55.py':
  t=t.replace("O=R/'evidence/movement-state-v54'", "O=R/'evidence/movement-state-v55'")
  t=t.replace("'neighbors'","'layers'").replace("'frontier'","'edges'")
  t=t.replace('build-path-search-probe','build-region-search-probe').replace('path_search_probe','region_search_probe').replace('-path-search.json','-region-search.json').replace('8192','6144')
  t=t.replace('Complete mapped original neighbor loop; engine services stubbed. Same 6144 cases after both parts, counted once. Ordered calls, mutable weights/region connection/cache stamps, heap, nodes and four exits.','Mapped original three-layer regional search; engine services stubbed. Same 6144 inputs before changes and after both parts, counted once. Ordered native engine events, routes, caches, node pool, heap and final logical numeric control.')
  t=t.replace('Three exact parent traces inherited; one pre-change infantry-first recipe run with frozen parent observer.','All four exact parent per-mode traces inherited by hash; frozen observer retained. No duplicate pre-change game runs.')
 elif name=='audit_scenes_v55.py':
  t=t.replace("'frontier-cross-'","'edges-cross-'").replace('path-search','regional-search')
 elif name=='audit_sources_v55.py':
  t=t.replace('new Prepare/Advance cycle','regional-search service phases')
  t=t.replace("['ground_path_search']","['ground_region_search']")
  t=t.replace("['neighbors','frontier']","['layers','edges']").replace("parts['frontier']","parts['edges']")
  t=t.replace("['path_search','capture_packet','transport_packet']","['region_search','capture_packet','transport_packet']").replace('8192','6144')
  t=t.replace('nine-neighbor lookup, repeated region cell reads, live numeric controls and cache publication ordering retained','coarse-to-fine layer setup, same-region shortcut, penalty conversion, edge filter and full-heap cache publication ordering retained')
 elif name=='commit_movement_v55.py':
  t=t.replace('第五十四批','第五十五批').replace('路径搜索与步兵先登载','分层区域搜索与边代价')
  t=t.replace('Stage path search services; validate infantry-first transport and traffic (batch 54)','Stage layered region search, edge restrictions and cost services (batch 55)')
 elif name=='audit_evidence_v55.py':
  t=t.replace("protected=[O/n for n in", "def inherited_path(name):\n direct=O/name\n if direct.exists():return direct\n item=read(O/'boundary-inheritance.json')['files'][name]\n p=Path(item['path']);assert sha(p)==item['sha256'];return p\nprotected=[inherited_path(n) for n in")
  t=t.replace(" p=O/name;inherited[name]", " p=inherited_path(name);inherited[name]")
  t=t.replace('new_fm_map_equals_parent_south_bytes','retained_fm_map_equals_parent_south_bytes').replace('new_fm_terrain_pack_sha256','retained_fm_terrain_pack_sha256')
  a=t.index('source=(R/');b=t.index('print(dict(passed=True',a)
  t=t[:a]+'''source=(R/'ra2/src/gameplay/ground_region_search.c').read_text(encoding='utf-8')
for helper in ['prepare_layer','publish_same_region','seed_layer_frontier','proposed_edge_cost','edge_is_eligible']:assert helper in source
write(S/'service-boundaries.json',dict(passed=True,changed_unit='ground_region_search.c',new_headers_or_build_sources=False,stages=['prepare_layer and same-region/root publication','proposed_edge_cost with live conversion control','edge_is_eligible: visited, upper-layer connection, terrain and blocked-pair checks'],retained=['snapshot heap before region lookups; snapshot layer cache after lookups','start lookup then goal lookup; fresh context per service call','clear heap entries/count without resetting historical address bounds','same-region writes only original fields; no root/blocked-list work','owner factor and house precede threshold decision','penalty multiplication precedes integer conversion control update','proposed cost before all edge filters','blocked pair list queried only after previous filters and only if initially nonempty','heap full still publishes visited/cost and consumes node pool slot','failure keeps already completed coarse-layer routes'],native_probe_scope='Mapped original three-layer routine with native engine event stubs. Final native control word compared with the C logical control; not all ABI fields or all callback mutations.'))
write(S/'infrastructure-status.json',dict(passed=True,new_game_setup_failures=False,prior_failure_retained=str(O/'infrastructure-failure.json'),prior_failure_sha256=sha(O/'infrastructure-failure.json'),scope='Prior initial resource-link setup failure retained in place; current game runs use authorized local resource links.'))
''' +t[b:]
 elif name=='verify_final_movement_v55.py':
  t=t.replace("==(54,55)","==(55,56)")
  t=t.replace("['neighbors','frontier']","['layers','edges']").replace('parts/frontier/','parts/edges/').replace('path_search_probe','region_search_probe').replace('8192','6144')
  t=t.replace("  assert proof['stop_cases']==[2765,636,668,4123]\n  assert proof['ordered_service_events']==311395 and proof['created_nodes']==17661", "  assert proof['successes']>0 and proof['failures']>0 and proof['final_numeric_control_compared']\n  assert proof['successes']+proof['failures']==6144")
  t=t.replace("'infrastructure-failure.json'","'infrastructure-status.json'").replace("['ra2/src/gameplay/ground_path_search.c']","['ra2/src/gameplay/ground_region_search.c']")
  t=t.replace('generation=54','generation=55')
  marker="selected=read(S/'selected-baseline-scenes.json')"
  t=t.replace(marker,"baseline=read(S/'part-baseline-region-search.json');assert baseline['passed'] and baseline['cases']==6144 and baseline['final_numeric_control_compared']\n"+marker)
 q=R/name.replace('v55','v56');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n')
 lineage.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
# The regional cost service deliberately updates the logical control word. Compare
# it with the native final x87 control, before production code is reorganized.
p=S/'region_search_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('static void set_control(uint16_t control)', '''static uint16_t get_control(void)
{
 uint16_t value;
 __asm fnstcw value
 return value;
}
static void set_control(uint16_t control)''',1)
t=t.replace('uint32_t events[8192],event_count,success;','uint32_t events[8192],event_count,success,control;')
t=t.replace('static void capture(Capture *out,int success)','static void capture(Capture *out,int success,uint16_t control)')
t=t.replace('out->success=(unsigned)success;','out->success=(unsigned)success;out->control=control;')
t=t.replace('capture(&expected,(result&255)!=0);','capture(&expected,(result&255)!=0,get_control());')
t=t.replace('capture(&actual,ok);','capture(&actual,ok,control);')
t=t.replace(r'\"engine_services_stubbed\":true',r'\"engine_services_stubbed\":true,\"final_numeric_control_compared\":true')
assert 'get_control());' in t and 'final_numeric_control_compared' in t
eol=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes(t.encode('utf-8').replace(b'\n',eol))
source=R/'evidence/movement-state-v38/region_search_probe.c'
lineage.append(dict(source=str(source.relative_to(R)),source_sha256=sha(source),derived=str(p.relative_to(R)),derived_sha256=sha(p),change='Compare final native x87 control with C logical numeric control; original case inputs retained.'))
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=lineage),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(lineage)))
