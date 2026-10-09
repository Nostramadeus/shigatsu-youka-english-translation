import io, os, glob
src='orig/データベース'
for p in glob.glob(src+'/*.tsv')+glob.glob(src+'/人物/*.tsv')+glob.glob(src+'/実況/*.tsv'):
    rel=os.path.relpath(p,src).replace(os.sep,'/')
    out='notes/_db/'+rel.replace('/','__')
    io.open(out,'w',encoding='utf-8').write(io.open(p,encoding='cp932',errors='replace').read())
rows=[l.rstrip('\n').split('\t') for l in io.open('notes/_db/シナリオデータベース.tsv',encoding='utf-8')]
hdr=rows[0]
for i,h in enumerate(hdr): print(i,h,'|',rows[1][i] if i<len(rows[1]) else '', '|', rows[2][i] if i<len(rows[2]) else '')
