# Agents-only tool. Builds notes/_db/_reading-order.tsv from the scenario DB + line counts.
import io,collections,re
rows=[l.rstrip('\n').split('\t') for l in io.open('notes/_db/シナリオデータベース.tsv',encoding='utf-8')][1:]
sc=[r for r in rows if r[1]=='シナリオ']
by_title={r[5]:r for r in sc}
lc={l.split('\t')[0][:-4]:(int(l.split('\t')[1]),int(l.split('\t')[2])) for l in io.open('line-counts.tsv',encoding='utf-8').read().splitlines()[1:]}
hen=[l.split('\t')[1] for l in io.open('notes/_db/編.tsv',encoding='utf-8').read().splitlines()[1:] if l.strip()]
henidx={h:i for i,h in enumerate(hen)}
def ival(s):
    try: return int(float(s))
    except: return 0
# candidate lsb by char count (文字数1 alone, or 特殊4 = total when branching)
cands={}
for r in sc:
    want=[ival(r[23]), ival(r[28])]
    want=[w for w in want if w>0]
    best=[]
    for f,(l,c) in lc.items():
        d=min(abs(c-w)/w for w in want) if want else 9
        if d<0.04: best.append((d,f))
    cands[r[0]]=sorted(best)
# greedy one-to-one
assigned={}; used=set()
for r in sorted(sc,key=lambda r:(cands[r[0]][0][0] if cands[r[0]] else 9)):
    for d,f in cands[r[0]]:
        if f not in used:
            assigned[r[0]]=(f,d); used.add(f); break
# topological order by 罫線 predecessors
preds={r[0]:[by_title[t][0] for t in r[8:14] if t and t!='0' and t in by_title] for r in sc}
order=[]; seen=set()
def key(r): return (henidx.get(r[6],99), ival(r[7]), sc.index(r))
remaining=sorted(sc,key=key)
while remaining:
    prog=False
    for r in list(remaining):
        if all(p in seen for p in preds[r[0]]):
            order.append(r); seen.add(r[0]); remaining.remove(r); prog=True; break
    if not prog:
        r=remaining.pop(0); order.append(r); seen.add(r[0])
out=['order\tscenario\ttitle\then\tcol\tlsb\tmatch_err\tdb_chars\tlsb_lines\tlsb_chars\tpreds']
for i,r in enumerate(order,1):
    f,d=assigned.get(r[0],('?',9))
    l,c=lc.get(f,(0,0))
    out.append(f"{i}\t{r[0]}\t{r[5]}\t{r[6]}\t{r[7]}\t{f}\t{d:.3f}\t{r[23]}\t{l}\t{c}\t{','.join(preds[r[0]])}")
io.open('notes/_db/_reading-order.tsv','w',encoding='utf-8').write('\n'.join(out)+'\n')
print('assigned',len(assigned),'of',len(sc),'; unassigned:',[r[0] for r in sc if r[0] not in assigned])
print('unused lsb with text:',len([f for f in lc if f not in used]))
