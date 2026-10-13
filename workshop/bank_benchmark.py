"""Retrieval benchmark on executable synthetic trading-support code and config."""
import ast,json,time,statistics,platform,hashlib,csv
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from bank_demo.registry import deployed_mechanism
R=Path(__file__).parent

def build():
 docs=[];nodes={};edges=[];asts={};names={}
 for path in sorted((R/'bank_demo').glob('*.py')):
  lines=path.read_text().splitlines();tree=ast.parse(path.read_text());module=path.stem;imports={}
  for n in tree.body:
   if isinstance(n,ast.ImportFrom) and n.level:
    for alias in n.names:imports[alias.asname or alias.name]=f'fn:{n.module}.{alias.name}'
  for n in tree.body:
   if not isinstance(n,ast.FunctionDef):continue
   id=f'fn:{module}.{n.name}';start=min([n.lineno]+[d.lineno for d in n.decorator_list]);text='\n'.join(lines[start-1:n.end_lineno]);doc=dict(id=id,text=text,kind='code',label=n.name,source=f'bank_demo/{path.name}:{start}-{n.end_lineno}',module=module)
   docs.append(doc);nodes[id]=doc;asts[id]=n;names[id]=imports
   for d in n.decorator_list:
    if isinstance(d,ast.Call) and isinstance(d.func,ast.Name) and d.func.id=='source':
     dataset=d.args[0].value;did='data:'+dataset
     if did not in nodes:
      item=dict(id=did,text=f'Datový zdroj {dataset}. V modelové platformě ho poskytuje {n.name}; zdrojová deklarace {doc["source"]}.',kind='dataset',label=dataset,source=doc['source']);docs.append(item);nodes[did]=item
     edges.append(dict(source=id,target=did,type='reads',evidence=doc['source']))
 for id,n in asts.items():
  for call in ast.walk(n):
   if isinstance(call,ast.Call) and isinstance(call.func,ast.Name):
    name=call.func.id;candidate=names[id].get(name,'fn:'+nodes[id]['module']+'.'+name)
    if candidate in nodes and candidate!=id:edges.append(dict(source=id,target=candidate,type='calls',evidence=nodes[id]['source']))
 for v in json.loads((R/'bank_demo/mechanisms.json').read_text()):
  doc=dict(id='cfg:'+v['id'],text=json.dumps(v,ensure_ascii=False),kind='config',label=v['id'],source='bank_demo/mechanisms.json');docs.append(doc);nodes[doc['id']]=doc
 for v in json.loads((R/'bank_demo/notes.json').read_text()):
  doc=dict(id=v['id'],text=v['text'],kind='document',label=v['id'],source='bank_demo/notes.json');docs.append(doc);nodes[doc['id']]=doc
 # Independently specified evidence requirements for the three concrete questions.
 queries=[
  dict(id='bank-report',type='lineage',title='Odkud se berou data pro týdenní report?',text='Odkud se berou data pro týdenní report platformy pro obchodníky na burze?',start='fn:report.generate_weekly_report',gold=['fn:report.generate_weekly_report','fn:pnl.calculate_weekly_pnl','fn:health.calculate_financial_health']+['data:'+s for s in ['portfolio_positions','market_closing_prices','reference_fx_rates','client_cashflows','margin_snapshots','client_profiles']]),
  dict(id='bank-feature',type='impact',title='Co ovlivní feature what-if margin?',text='Které části kódu ovlivní změna calculate_margin_buffer kvůli přidání nové feature what-if margin?',start='fn:health.calculate_margin_buffer',gold=['fn:health.calculate_financial_health','fn:report.generate_weekly_report','fn:api.get_trader_dashboard']),
  dict(id='bank-health',type='current',title='Jak se dnes počítá finanční zdraví klienta?',text='Jaký je současný mechanismus výpočtu finančního zdraví klienta?',start='fn:health.calculate_financial_health',gold=['cfg:health-v2','fn:registry.deployed_mechanism','fn:health.calculate_financial_health','fn:health.calculate_liquidity_component','fn:health.calculate_margin_buffer','fn:health.calculate_diversification'])]
 return docs,edges,queries

def traversal(start,edges,reverse=False):
 todo=[start];seen=set();out=[]
 while todo:
  n=todo.pop(0)
  if n in seen:continue
  seen.add(n);out.append(n)
  todo.extend(e['source'] if reverse else e['target'] for e in edges if (e['target'] if reverse else e['source'])==n)
 return out

def run():
 docs,edges,queries=build();byid={d['id']:d for d in docs};v=TfidfVectorizer(token_pattern=r'(?u)\b[\w.-]+\b');start=time.perf_counter();X=v.fit_transform([d['text'] for d in docs]);build_ms=(time.perf_counter()-start)*1000;rankings={}
 for q in queries:
  scores=(X@v.transform([q['text']]).T).toarray().ravel();order=np.argsort(-scores,kind='stable');rankings[q['id']]=[dict(id=docs[i]['id'],score=float(scores[i]),rank=n+1) for n,i in enumerate(order)]
 def retrieve(method,q,k=4):
  if method=='full':return [d['id'] for d in docs]
  if method=='vector':
   scores=(X@v.transform([q['text']]).T).toarray().ravel();return [docs[i]['id'] for i in np.argsort(-scores,kind='stable')[:k]]
  if q['type']=='current':
   # Hybrid: exact deployed registry + graph of the current implementation.
   active='cfg:'+deployed_mechanism('2026-10-13')['id']
   return [active,'fn:registry.deployed_mechanism']+traversal(q['start'],edges)
  return traversal(q['start'],edges,reverse=q['type']=='impact')
 rows=[]
 for q in queries:
  for method in ['full','vector','structure']:
   ids=retrieve(method,q);timings=[]
   for _ in range(50):
    t=time.perf_counter_ns();retrieve(method,q);timings.append((time.perf_counter_ns()-t)/1e6)
   gold=set(q['gold']);got=set(ids);rows.append(dict(query=q['id'],method=method,retrieved=ids,gold=q['gold'],complete=gold<=got,recall=len(gold&got)/len(gold),precision=len(gold&got)/len(got),context_bytes=len('\n'.join(byid[i]['text'] for i in ids).encode()),median_ms=statistics.median(timings),p95_ms=float(np.percentile(timings,95))))
 summary=[]
 for method in ['full','vector','structure']:
  a=[x for x in rows if x['method']==method];summary.append(dict(method=method,complete=sum(x['complete'] for x in a),queries=3,recall=statistics.mean(x['recall'] for x in a),precision=statistics.mean(x['precision'] for x in a),context_bytes=round(statistics.mean(x['context_bytes'] for x in a)),median_ms=statistics.median(x['median_ms'] for x in a)))
 result=dict(metadata=dict(date='2026-10-13',python=platform.python_version(),documents=len(docs),queries=3,repetitions=50,vector_build_ms=build_ms,scope='Synthetic banking code, actual AST extraction and execution. Known start symbols and intent. structure=current is registry + graph, not graph alone. No LLM, no product benchmark. Bytes not tokens.'),documents=docs,edges=edges,queries=queries,rankings=rankings,rows=rows,summary=summary)
 (R/'bank-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 with (R/'bank-results.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(summary,ensure_ascii=False,indent=2));return result
if __name__=='__main__':run()
