"""Real source-code retrieval: imports → reexports → definition, installed sklearn."""
import ast,inspect,json,time,statistics,hashlib,importlib.util
from pathlib import Path
import sklearn
import sklearn.feature_extraction.text as text
import sklearn.preprocessing as preprocessing
import sklearn.preprocessing._data as pdata
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
R=Path(__file__).parent

def run():
 modules=[text,preprocessing,pdata];docs=[];gold=[];sources=[];links={}
 for module in modules:
  source=inspect.getsource(module);lines=source.splitlines();tree=ast.parse(source)
  sources.append(dict(module=module.__name__,sha256=hashlib.sha256(source.encode()).hexdigest(),line_count=len(lines)))
  for node in tree.body:
   hit=(isinstance(node,ast.ImportFrom) and any(a.name=='normalize' for a in node.names)) or (isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name=='normalize')
   if hit:
    # Import node fully, definition plus first docstring lines. No execution inference.
    start=node.lineno;end=min(node.end_lineno,start+15) if isinstance(node,ast.FunctionDef) else node.end_lineno
    id=f'{module.__name__}:{start}-{end}'
    docs.append(dict(id=id,module=module.__name__,line_start=start,line_end=end,text='\n'.join(lines[start-1:end]),gold=True));gold.append(id)
    target=None
    if isinstance(node,ast.ImportFrom):
     imported=importlib.util.resolve_name('.'*node.level+(node.module or ''),module.__package__) if node.level else node.module
     target=imported+'.normalize'
    links[module.__name__+'.normalize']=dict(target=target,document=id)
  for start in range(0,len(lines),40):
   docs.append(dict(id=f'{module.__name__}:chunk-{start+1}',module=module.__name__,line_start=start+1,line_end=min(start+40,len(lines)),text='\n'.join(lines[start:start+40]),gold=False))
 # Gold fragments and regular chunks overlap; diagnostic benchmark requires exact annotated evidence IDs.
 v=TfidfVectorizer(token_pattern=r'(?u)\b[\w.-]+\b');X=v.fit_transform([d['text'] for d in docs])
 query='sklearn.feature_extraction.text normalize import sklearn.preprocessing normalize definition'
 def vector(k):
  scores=(X@v.transform([query]).T).toarray().ravel();return [docs[i]['id'] for i in np.argsort(-scores,kind='stable')[:k]]
 def graph():
  current='sklearn.feature_extraction.text.normalize';visited=set();ids=[]
  while current in links and current not in visited:
   visited.add(current);node=links[current];ids.append(node['document']);current=node['target']
  return ids
 rows=[]
 for label,fn in [('vector@3',lambda:vector(3)),('vector@8',lambda:vector(8)),('graph',graph)]:
  ids=fn();times=[]
  for _ in range(100):
   t=time.perf_counter_ns();fn();times.append((time.perf_counter_ns()-t)/1e6)
  byid={d['id']:d for d in docs}
  # Source coverage, not exact ID: full fragment must be inside a returned range in same module.
  covered=[]
  for target in [byid[g] for g in gold]:
   if any(byid[i]['module']==target['module'] and byid[i]['line_start']<=target['line_start'] and byid[i]['line_end']>=target['line_end'] for i in ids):covered.append(target['id'])
  rows.append(dict(method=label,retrieved=ids,covered=covered,complete=len(covered)==len(gold),recall=len(covered)/len(gold),context_bytes=len('\n'.join(byid[i]['text'] for i in ids).encode()),median_ms=statistics.median(times)))
 result=dict(sklearn=sklearn.__version__,sources=sources,documents=docs,query=query,gold=gold,rows=rows,graph_links=links,notes='Actual installed source; AST extraction of explicit imports/reexports for known symbol normalize in three modules. Known start module/symbol, no query interpretation. Does not resolve dynamic imports or arbitrary Python. Chunk and evidence fragments overlap; coverage uses source ranges. Single diagnostic query; no LLM.')
 (R/'real-source-results.json').write_text(json.dumps(result,indent=2));print(json.dumps(rows,indent=2));return result
if __name__=='__main__':run()
