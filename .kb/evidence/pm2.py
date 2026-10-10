import fitz,re,sys,json
sys.stdout.reconfigure(encoding='utf-8')
TOL=float(sys.argv[4]) if len(sys.argv)>4 else 14
def extract(f,cx):
    d=fitz.open(f); L=[]
    for b in d[0].get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                t=s['text'].strip()
                if t: L.append((s['bbox'][0],s['bbox'][1],s['bbox'][2],s['bbox'][3],t))
    nums=[]
    for x in L:
        if abs((x[0]+x[2])/2-cx)<TOL and re.fullmatch(r'[\d ]+',x[4]):
            toks=x[4].split()
            if len(toks)==2:
                w=(x[2]-x[0])/2
                nums.append((int(toks[0]),x[0],x[0]+w*0.8,x[1],x[3])); nums.append((int(toks[1]),x[2]-w*0.8,x[2],x[1],x[3]))
            else: nums.append((int(toks[0]),x[0],x[2],x[1],x[3]))
    res={}
    sec=0; prev=None
    nums.sort(key=lambda n:(n[3],n[0]))
    for n,x0,x1,y0,y1 in nums:
        if n in(1,) : sec+=1
        yc=(y0+y1)/2
        row=[x for x in L if abs((x[1]+x[3])/2-yc)<1.6 and not re.fullmatch(r'[\d ]+',x[4])]
        if n%2: cand=[x for x in row if x[2]<=x0+1]; cand.sort(key=lambda x:-x[2])
        else: cand=[x for x in row if x[0]>=x1-1]; cand.sort(key=lambda x:x[0])
        res.setdefault(sec,{})[n]=cand[0][4] if cand else None
    return res
r=extract(sys.argv[1],float(sys.argv[2]))
for s in r: print(s,len(r[s]),r[s].get(7),r[s].get(29),r[s].get(140))
json.dump(r,open(sys.argv[3],'w'),indent=0)
