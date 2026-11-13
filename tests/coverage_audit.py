"""Coverage assertions for the published exam case bank."""
from collections import Counter
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"PRIME":100,"PROTEIN":100,"BILLARD":100,"DIVIDE":100,"ALKANE":20}
manifest=json.loads((ROOT/"docs/assets/test-manifest.json").read_text(encoding="utf-8"))
for name,total in EXPECTED.items():
    root=ROOT/"tests/generated"/name
    rows=json.loads((root/"manifest.json").read_text(encoding="utf-8"))["cases"]
    assert len(rows)==total
    values=[(root/row["id"]/(name+".INP")).read_text(encoding="utf-8") for row in rows]
    duplicates=len(values)-len(set(values))
    assert duplicates==0, f"{name}: duplicate inputs waste test capacity ({duplicates})"
    families=dict(Counter(row["family"] for row in rows))
    print(name, "COUNT",len(values),"DUPLICATES",duplicates,"FAMILIES",json.dumps(families,sort_keys=True),flush=True)
    if name=="PRIME":
        nums=[int(x.strip()) for x in values]
        assert 1 in nums and 10**14 in nums and 8 in nums
        assert min(nums)>=1 and max(nums)<=10**14
    if name=="PROTEIN":
        assert any(len(x.strip())==99999 for x in values)
        assert len([row for row in rows if row["family"]=="all-64-codons"])==64
        assert all(len(x.strip())%3==0 and set(x.strip())<={"A","C","T","G"} for x in values)
    if name=="BILLARD":
        cases=[list(map(int,x.split())) for x in values]
        assert all(len(a)==7 and a[0]>=2 and a[1]>=2 and 1<=a[-1]<=10**9 for a in cases)
        assert {(a[4],a[5]) for a in cases}=={(i,j) for i in (-1,0,1) for j in (-1,0,1)}
        assert any(a[-1]==10**9 for a in cases)
    if name=="DIVIDE":
        lengths=[int(x.split()[0]) for x in values]
        assert 1 in lengths and 100000 in lengths
        assert all(1<=len(x.split())-1<=100000 for x in values)
    if name=="ALKANE":
        assert sorted(int(x) for x in values)==list(range(1,21))
print("COVERAGE_AUDIT_DONE",flush=True)
