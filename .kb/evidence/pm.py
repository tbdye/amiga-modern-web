import fitz,re,sys,json
sys.stdout.reconfigure(encoding='utf-8')
def lines(f):
    d=fitz.open(f); out=[]
    for pi,p in enumerate(d):
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                t=''.join(s['text'] for s in l['spans']).strip()
                if t: out.append((pi,round(l['bbox'][0],1),round(l['bbox'][1],1),round(l['bbox'][2],1),t))
    return out
f=sys.argv[1]
L=lines(f)
pairs=[x for x in L if re.fullmatch(r'\d+ \d+',x[4])]
print(len(pairs))
xs=sorted(set(round(x[1]) for x in pairs)); print('pair x',xs)
for x in L:
    if x[4] in('Net Name','J1','J2') : print(x)
cx=float(sys.argv[2]);
mid=[x for x in L if abs((x[1]+x[3])/2-cx)<12 and re.fullmatch(r'[\d ]+',x[4])]
mid.sort(key=lambda x:x[2])
print([ (x[2],x[4]) for x in mid if not re.fullmatch(r'\d+ \d+',x[4])])
# sections by y gap
ys=[x[2] for x in mid];
print('first',mid[0][4],mid[0][2],'last',mid[-1][4],mid[-1][2])
