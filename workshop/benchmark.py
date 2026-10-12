"""Reproducible retrieval microbenchmark; no LLM, no external API."""
import json,time,platform,statistics,csv
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT=Path(__file__).parent

def build():
 docs=[]; queries=[]; edges={}; owners={}
 for i in range(8):
  s=f'svc-{i}'; dep=f'db-{i}'; team=f'team-{i}'
  def add(id,text,kind): docs.append(dict(id=id,text=text,kind=kind,entity=s))
  add(f'inc-{i}',f'{s}: Incident connection pool exhausted, timeout during traffic spike. Mitigation: reduce concurrency and enable backpressure. Runbook: connection pool timeout.', 'incident')
  add(f'dep-{i}',f'{s} depends_on {dep}. Dependency confirmed in deployment manifest.', 'edge')
  add(f'own-{i}',f'{dep} owned_by {team}. Current escalation team for database.', 'edge')
  add(f'old-{i}',f'{s}: owner was legacy-{i} until 2026-09-30. Historical ownership entry.', 'history')
  add(f'new-{i}',f'{s}: current owner is platform-{i} since 2026-10-01. Supersedes legacy-{i}.', 'state')
  add(f'noise-{i}',f'{s}: connection pool timeout investigation draft. No verified mitigation; outdated hypothesis: increase concurrency.', 'draft')
  edges[s]=[f'dep-{i}',f'own-{i}']; owners[s]=f'new-{i}'
  queries.extend([
   dict(id=f'q-inc-{i}',type='similarity',entity=s,text=f'{s} connection pool exhausted timeout traffic spike mitigation',gold=[f'inc-{i}']),
   dict(id=f'q-path-{i}',type='path',entity=s,text=f'{s} dependency database escalation team',gold=[f'dep-{i}',f'own-{i}']),
   dict(id=f'q-now-{i}',type='current',entity=s,text=f'{s} current owner',gold=[f'new-{i}'])])
 return docs,queries,edges,owners

def run():
 docs,qs,edges,owners=build(); byid={d['id']:d for d in docs}
 start=time.perf_counter(); v=TfidfVectorizer(token_pattern=r"(?u)\b[\w-]+\b"); X=v.fit_transform([d['text'] for d in docs]); build_ms=(time.perf_counter()-start)*1000
 def retrieve(method,q,k=2):
  if method=='full': return [d['id'] for d in docs]
  if method=='graph': return edges[q['entity']] if q['type']=='path' else ([owners[q['entity']]] if q['type']=='current' else [])
  if method=='hybrid' and q['type']!='similarity': return retrieve('graph',q)
  scores=(X@v.transform([q['text']]).T).toarray().ravel()
  return [docs[i]['id'] for i in np.argsort(-scores,kind='stable')[:k]]
 rows=[]
 for method in ['full','vector','graph','hybrid']:
  for q in qs:
   ids=retrieve(method,q); lat=[]
   for _ in range(50):
    t=time.perf_counter_ns(); retrieve(method,q); lat.append((time.perf_counter_ns()-t)/1e6)
   gold=set(q['gold']); got=set(ids)
   context='\n'.join(byid[i]['text'] for i in ids)
   rows.append(dict(method=method,query=q['id'],type=q['type'],recall=len(gold&got)/len(gold),precision=len(gold&got)/len(got) if got else 0,complete=int(gold<=got),context_bytes=len(context.encode()),latency_median_ms=statistics.median(lat),latency_p95_ms=float(np.percentile(lat,95)),retrieved=ids,gold=q['gold']))
 summary=[]
 for method in ['full','vector','graph','hybrid']:
  r=[r for r in rows if r['method']==method]
  summary.append(dict(method=method,complete=sum(x['complete'] for x in r),queries=len(r),recall=statistics.mean(x['recall'] for x in r),precision=statistics.mean(x['precision'] for x in r),context_bytes=round(statistics.mean(x['context_bytes'] for x in r)),latency_median_ms=statistics.median(x['latency_median_ms'] for x in r)))
 sweep=[]
 for k in [1,2,4,8]:
  out=[retrieve('vector',q,k) for q in qs]
  sweep.append(dict(k=k,complete=sum(set(q['gold'])<=set(ids) for q,ids in zip(qs,out)),context_bytes=round(statistics.mean(len('\n'.join(byid[i]['text'] for i in ids).encode()) for ids in out))))
 result=dict(sweep=sweep,metadata=dict(python=platform.python_version(),platform=platform.platform(),documents=len(docs),queries=len(qs),repetitions=50,vector_build_ms=build_ms,csr_bytes=X.data.nbytes+X.indices.nbytes+X.indptr.nbytes,scope='Warm in-process retrieval; excludes LLM, network, extraction, graph planning; byte counts are NOT tokens.'),summary=summary,rows=rows,documents=docs,queries=qs)
 (ROOT/'results.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 with (ROOT/'results.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(summary,indent=2))
 return result
if __name__=='__main__':run()
