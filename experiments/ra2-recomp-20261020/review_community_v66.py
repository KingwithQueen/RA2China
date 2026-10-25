"""Recheck two pinned public source bodies in memory; never send local project data."""
from run_batch_v66 import *
from urllib.request import urlopen,Request
review=read(S/'community-reference-review.json');checks=[]
for item in [review['sources'][1],review['sources'][3]]:
 with urlopen(Request(item['raw_url'],headers={'User-Agent':'RA2-local-source-reference-check'}),timeout=45) as response:body=response.read()
 assert len(body)==item['bytes'] and hashlib.sha256(body).hexdigest()==item['sha256'],item['path']
 checks.append(dict(repository=item['repository'],revision=item['revision'],path=item['path'],url=item['url'],bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),content_matches_locked_review=True))
write(S/'community-current-use.json',dict(passed=True,locked_review_sha256=sha(S/'community-reference-review.json'),rechecked=checks,reference_only=True,third_party_engine_code_imported=False,private_project_uploaded=False,application='Keep path requests, passability/search and successful publication separated. These older-engine/YR wrappers provide terminology only; they do not establish RA2 1.006 global FIFO, wait thresholds or addresses. Recovery timer and callback order remain grounded in native 1.006 probes.',cache_files_written=0))
print(dict(passed=True,rechecked=len(checks),cache_files_written=0))
