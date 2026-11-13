"""Create deterministic, independently-oracled official-boundary test packs.
Run on WIN11-181 with Python 3.13 portable; no external dependencies.
"""
from __future__ import annotations
import csv, hashlib, itertools, json, math, random, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"tests"/"generated"
DOWNLOAD=ROOT/"docs"/"downloads"
R=random.Random(20261113); MOD=1_000_000_007
NAMES=["PRIME","PROTEIN","BILLARD","DIVIDE","ALKANE"]
CODON={}
for key,vals in {
"Ser":"UCA UCU UCC UCG","Thr":"ACA ACU ACC ACG",
"Arg":"CGA CGU CGC CGG","Gly":"GGA GGU GGC GGG",
"Tyr":"UAU UAC","His":"CAU CAC","Pro":"CCU CCA CCC CCG"
}.items():
    for triplet in vals.split(): CODON[triplet]=key
ALKANE=[0,1,1,1,2,3,5,9,18,35,75,159,355,802,1858,4347,10359,24894,60523,148284,366319]
def prime(n):
    if n<2:return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%p==0:return n==p
    d=n-1; s=0
    while not d&1:s+=1;d//=2
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a%n==0:continue
        x=pow(a,d,n)
        if x in (1,n-1):continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1:break
        else:return False
    return True
def factor(n,out):
    if n==1:return
    if prime(n):out.append(n);return
    if n%2==0:out.append(2);factor(n//2,out);return
    while True:
        x=R.randrange(2,n-1);y=x;c=R.randrange(1,n-1);d=1
        while d==1:
            x=(x*x+c)%n;y=(y*y+c)%n;y=(y*y+c)%n
            d=math.gcd(abs(x-y),n)
        if d!=n:break
    factor(d,out);factor(n//d,out)
def prime_answer(n):
    factors=[];factor(n,factors)
    return "YES" if len(factors)==3 else "NO"
def protein_answer(dna):
    comp=str.maketrans("ATCG","UAGC")
    rna=dna.translate(comp)
    return "-".join(CODON.get(rna[i:i+3],"Unk") for i in range(0,len(rna),3))
def billiard_answer(m,n,x,y,vx,vy,t):
    def axis(length,p,v):
        r=(p+v*t)%(length*2)
        return length-abs(r-length)
    ans=(axis(m,x,vx),axis(n,y,vy))
    if t<=150:  # independent step-by-step oracle (small times)
        X,Y=x,y;dx,dy=vx,vy
        for _ in range(t):
            if X+dx<0 or X+dx>m:dx=-dx
            if Y+dy<0 or Y+dy>n:dy=-dy
            X+=dx;Y+=dy
        assert (X,Y)==ans,(m,n,x,y,vx,vy,t,ans,(X,Y))
    return f"{ans[0]} {ans[1]}"
def divide_answer(a):
    dp=[0]*11;dp[0]=1
    for val in a:
        place=(-1 if len(str(val))%2 else 1)
        rem=val%11; nxt=dp[:]
        for i,ways in enumerate(dp):
            j=(i*place+rem)%11
            nxt[j]=(nxt[j]+ways)%MOD
        dp=nxt
    answer=(dp[0]-1)%MOD
    if len(a)<=14:
        brute=0
        for mask in range(1,1<<len(a)):
            r=0
            for i,v in enumerate(a):
                if mask>>i&1:r=(r*pow(10,len(str(v)),11)+v)%11
            if r==0:brute+=1
        assert answer==brute%MOD,(a,answer,brute)
    return str(answer)
CASES={x:[] for x in NAMES}
SEEN={x:set() for x in NAMES}
def add(name,raw,expected,label):
    if name=="PROTEIN":assert len(raw.strip())%3==0 and 3<=len(raw.strip())<=100000
    if name=="PRIME":assert 1<=int(raw)<=10**14
    if name=="ALKANE":assert 1<=int(raw)<=20
    inp=raw.strip()+"\n"
    if inp in SEEN[name]:return  # all published cases must be distinct
    SEEN[name].add(inp)
    CASES[name].append((inp,str(expected).strip()+"\n",label))
# PRIME: four official score bands, repeated factors, large semiprimes and n=1.
base=[1,2,3,4,6,8,12,16,18,27,30,36,49,64,125,121,999983,1000000,
      1000001,10**14,9999999967,1000000000000,99999999999999,
      99999999999991,99999999999989,2**46,3**29,5**20]
for n in base:
    if n<=10**14:add("PRIME",str(n),prime_answer(n),"edge")
while len(CASES["PRIME"])<100:
    family=len(CASES["PRIME"])%5
    if family==0:n=R.randint(1,10**6)
    elif family==1:n=R.randint(10**6+1,10**14)
    elif family==2:
        p,q,r=R.choice([2,3,5,7,11,13,17,23,97,1009,10007,100003]),R.choice([2,3,5,7,11,13,17,97,1009]),R.choice([2,3,5,7,11,97,1009])
        n=p*q*r
    elif family==3:n=R.choice([2,3,5,7,11])**R.randint(1,12)
    else:n=R.randint(10**6+1,10**14)
    if 1<=n<=10**14:add("PRIME",str(n),prime_answer(n),["small","large","YES-products","power","large"][family])
# PROTEIN: every single codon + full length limit + His/Unk score group.
dna_sample="AGTAGGGTAGCACCT"
add("PROTEIN",dna_sample,protein_answer(dna_sample),"official-sample")
reverse={"U":"A","A":"T","G":"C","C":"G"}
for codon in map("".join,itertools.product("UACG",repeat=3)):
    dna="".join(reverse[x] for x in codon)
    add("PROTEIN",dna,CODON.get(codon,"Unk"),"all-64-codons")
while len(CASES["PROTEIN"])<100:
    index=len(CASES["PROTEIN"]);length=R.choice([1,2,3,4,8,32,100,333,33333])
    if index==95:length=33333
    if index%3==0:
        pool=["CAC","CAU","AAA","AAG","GGG","UUU"]
        dna="".join(reverse[x] for x in "".join(R.choices(pool,k=length)))
    elif index%3==1:
        dna="".join(R.choices("ATCG",k=length*3))
    else:
        unit=R.choice(["ATC","CGA","AAA","GGG","TTA","AGT"])
        dna=unit*length
    add("PROTEIN",dna,protein_answer(dna),"long-stress" if len(dna)>3000 else "mixed-translation")
# BILLARD: legal velocities are ONLY -1,0,+1 according to original statement.
add("BILLARD","11 7 2 4 1 1 14",billiard_answer(11,7,2,4,1,1,14),"official-sample")
for m,n in [(2,2),(2,100),(100,2),(100,100),(11,7),(97,89)]:
    for vx,vy in itertools.product((-1,0,1),repeat=2):
        x=1 if m==2 else R.randint(1,m-1)
        y=1 if n==2 else R.randint(1,n-1)
        t=R.choice([1,2,3,13,100,10**7,10**9])
        arg=f"{m} {n} {x} {y} {vx} {vy} {t}"
        add("BILLARD",arg,billiard_answer(m,n,x,y,vx,vy,t),"velocities-and-edges")
while len(CASES["BILLARD"])<100:
    m=R.randint(2,100);n=R.randint(2,100)
    x=R.randint(1,m-1);y=R.randint(1,n-1)
    vx=R.choice((-1,0,1));vy=R.choice((-1,0,1))
    t=R.choice([1,2,3,6,12,59,149,10**7,10**7+1,10**9])
    arg=f"{m} {n} {x} {y} {vx} {vy} {t}"
    add("BILLARD",arg,billiard_answer(m,n,x,y,vx,vy,t),"random-mixed")
# DIVIDE: independent O(11n) oracle; brute-force every subset for n<=14.
def add_divide(a,label):
    assert 1<=len(a)<=10**5 and all(1<=v<=10**9 for v in a)
    add("DIVIDE",str(len(a))+"\n"+" ".join(map(str,a)),divide_answer(a),label)
add_divide([1,2,1,2,1],"official-sample")
for a in ([1],[11],[22],[1,1],[11,11],[1,2],[1,2,1],[1,2,1,2,1],
          [10],[10,10],[100],[1000],[1000000000],[999999999],
          [11]*10,[1]*10,[10]*10,[2,22,222,2222],[101,1001,10001]):
    add_divide(a,"edge-and-concatenation")
for n in range(1,9):
    for seed in range(4):
        family=["uniform","mixed-digits","alternating","random"][seed]
        if seed==0:a=[R.choice([1,2,3,9,11,22,999])]*n
        elif seed==1:a=[R.choice([1,9,10,11,12,100,1000,10**9]) for _ in range(n)]
        elif seed==2:a=([1,11]*n)[:n]
        else:a=[R.randint(1,10**9) for _ in range(n)]
        add_divide(a,family)
for n in [10,11,12,13,14]:
    for _ in range(3):
        add_divide([R.randint(1,10**9) for _ in range(n)],"bruteforce-random")
# 100k max n; performance, modulo rollover, all-equal, 1-digit, mixed-length.
for name,a in [
    ("max-n-all11",[11]*100000),
    ("max-n-all1",[1]*100000),
    ("max-n-powers",([1,10,100,1000,10000]*20000)),
    ("max-n-random",[R.randint(1,10**9) for _ in range(100000)]),
]:
    if len(CASES["DIVIDE"])>=100:break
    add_divide(a,name)
while len(CASES["DIVIDE"])<100:
    n=R.choice([1,5,8,10,13,15,25,100,1000,10000])
    a=[R.randint(1,10**9) for _ in range(n)]
    add_divide(a,"varying-n-and-digit-length")
# ALKANE official dataset contains exactly twenty distinct possible inputs.
for n in range(1,21):add("ALKANE",str(n),str(ALKANE[n]),"all-valid-n")
# Emit per-case portable judge folders: 001/PRIME.INP, 001/PRIME.OUT, ...
# Zip each problem for direct download from GitHub Pages and GitHub repository.
DEST.mkdir(parents=True,exist_ok=True);DOWNLOAD.mkdir(parents=True,exist_ok=True)
manifest={"generator":"tests/generate_cases.py","seed":20261113,
          "official_constraints_only":True,"schema":"1.0","problems":{}}
for problem,cases in CASES.items():
    folder=DEST/problem;folder.mkdir(parents=True,exist_ok=True)
    records=[]
    for idx,(inp,out,family) in enumerate(cases,1):
        case=folder/f"{idx:03d}";case.mkdir(exist_ok=True)
        (case/f"{problem}.INP").write_text(inp,encoding="utf-8",newline="\n")
        (case/f"{problem}.OUT").write_text(out,encoding="utf-8",newline="\n")
        records.append({"id":f"{idx:03d}","family":family,
                        "input_sha256":hashlib.sha256(inp.encode()).hexdigest(),
                        "output_sha256":hashlib.sha256(out.encode()).hexdigest()})
    (folder/"manifest.json").write_text(json.dumps({"problem":problem,"count":len(cases),
       "cases":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    path=DOWNLOAD/f"{problem}_{len(cases)}_tests.zip"
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as out:
        for file in sorted(folder.rglob("*")):
            if file.is_file():
                name=file.relative_to(DEST).as_posix()
                info=zipfile.ZipInfo(name,date_time=(2026,11,13,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o644<<16
                out.writestr(info,file.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    manifest["problems"][problem]={"count":len(cases),"zip":f"downloads/{path.name}",
       "zip_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
       "families":sorted(set(r["family"] for r in records))}
outpath=ROOT/"docs"/"assets"/"test-manifest.json"
outpath.parent.mkdir(parents=True,exist_ok=True)
outpath.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("GENERATED_TEST_CASES", {k:len(v) for k,v in CASES.items()})
print("TOTAL_CASES",sum(map(len,CASES.values())))
print("MANIFEST",outpath)
