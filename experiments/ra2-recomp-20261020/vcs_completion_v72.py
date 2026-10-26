"""Narrow review of external remote-tracking synchronization; never changes refs or config."""
from combat_batch_v72 import *
def expected_remote_hash(context):
    review=read(S/'vcs-sync-review.json')
    assert review['passed'] and review['initial_context_sha256']==sha(S/'vcs-context.json')
    assert review['initial_remote_refs_sha256']==context['remote_refs_sha256']
    assert review['local_parent_commit']==context['parent_commit'] and not review['remote_actions_performed_by_task']
    assert sha(P/'.git/config')==review['config_sha256']==context['config_sha256']
    refs=git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')
    actual=dict(line.split(' ',1) for line in refs.decode('utf-8').splitlines())
    assert actual==review['observed_refs'] and set(actual)=={'refs/remotes/origin/HEAD','refs/remotes/origin/主要'}
    assert all(value==context['parent_commit'] for value in actual.values())
    current=hashlib.sha256(refs).hexdigest();assert current==review['observed_remote_refs_sha256']
    return current

def reviewed_tools():
    review=read(S/'post-finalization-tool-review.json');assert review['passed']
    assert sha(S/'source-manifest.json')==review['initial_source_manifest_sha256']
    assert sha(S/'evidence-rollup.json')==review['initial_rollup_sha256']
    assert sha(S/'vcs-context.json')==review['initial_context_sha256']
    assert sha(R/'ra2/build-original-c/ra2.exe')==review['unchanged_exe_sha256']
    allowed={'verify_lifecycle_v72.py','commit_lifecycle_v72.py','vcs_completion_v72.py'}
    assert {Path(e['path']).name for e in review['tools']}==allowed
    original={e['path']:e['sha256'] for e in read(S/'source-manifest.json')};result={}
    for e in review['tools']:
        p=Path(e['path']);assert p.parent==R and p.name in allowed and sha(p)==e['sha256']==sha(Path(e['archive']))
        if e['previous_sha256'] is None:assert p.name=='vcs_completion_v72.py' and p.name not in original
        else:assert original[p.name]==e['previous_sha256']==sha(S/'final-source'/p.name)
        result[str(p)]=e
    for e in review['artifacts']:assert sha(Path(e['path']))==e['sha256']==sha(Path(e['archive']))
    return result
