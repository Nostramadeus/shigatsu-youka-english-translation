# Agents-only tool. Builds read/chunkNN.txt (compact reading copies of the csv text, in .lsb ID order)
# and notes/_db/_file-order.tsv. Never split a file across chunks. Skips the navigator UI 0000001C.
import io,csv,os
TARGET=45000  # JP chars per chunk
lc=[(l.split('\t')[0][:-4],int(l.split('\t')[1]),int(l.split('\t')[2])) for l in io.open('line-counts.tsv',encoding='utf-8').read().splitlines()[1:]]
lc=[x for x in sorted(lc) if x[0]!='0000001C']
chunks=[]; cur=[]; curc=0
for f,l,c in lc:
    if cur and curc+c>TARGET:
        chunks.append(cur); cur=[]; curc=0
    cur.append((f,l,c)); curc+=c
if cur: chunks.append(cur)
order=['order\tlsb\tlines\tchars\tchunk']
n=0
for ci,ch in enumerate(chunks,1):
    out=[]
    for f,l,c in ch:
        n+=1; order.append(f'{n}\t{f}\t{l}\t{c}\t{ci:02d}')
        out.append(f'### FILE {f}.lsb  (order {n}, {l} lines, {c} chars)')
        rd=csv.reader(io.open(f'csv/{f}.csv',encoding='utf-8-sig')); next(rd)
        for r in rd:
            idx=r[0].split(':')[-2]+':'+r[0].split(':')[-1]
            t=r[3].replace('\r','').replace('\n','⏎')
            out.append(f'{idx}\t{t}')
        out.append('')
    io.open(f'read/chunk{ci:02d}.txt','w',encoding='utf-8').write('\n'.join(out))
io.open('notes/_db/_file-order.tsv','w',encoding='utf-8').write('\n'.join(order)+'\n')
print('chunks',len(chunks),'files',n)
for ci,ch in enumerate(chunks[:6],1): print(ci,len(ch),sum(c for _,_,c in ch),ch[0][0],'..',ch[-1][0])
