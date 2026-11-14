"""Offline C++17 QA: compile all five tasks, sample, random differential, edge, stress.
No third-party libraries and no GitHub Actions required.
"""
from __future__ import annotations

import itertools
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["PRIME", "PROTEIN", "BILLARD", "DIVIDE", "ALKANE"]
MOD = 1_000_000_007
CASES = 0


def verify(ok: bool, msg: str) -> None:
    global CASES
    CASES += 1
    if not ok:
        raise AssertionError(msg)


def compile_all(target: Path) -> dict[str, Path]:
    # zig c++ is a portable C++17 compiler usable on Windows without MSVC/MSYS2.
    zig = os.environ.get("ZIG_EXE") or shutil.which("zig")
    cxx = os.environ.get("CXX")
    if cxx:
        compiler = [cxx]
    elif shutil.which("g++"):
        compiler = [shutil.which("g++")]
    elif shutil.which("clang++"):
        compiler = [shutil.which("clang++")]
    elif zig:
        compiler = [zig, "c++"]
    else:
        raise RuntimeError("Missing C++17 compiler. Set CXX or ZIG_EXE, or install g++/clang++.")
    results = {}
    for name in SOURCES:
        dest = target / (name + (".exe" if os.name == "nt" else ""))
        subprocess.run(
            [*compiler, "-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic",
             str(ROOT / "solutions" / (name + ".cpp")), "-o", str(dest)],
            check=True, capture_output=True, text=True,
        )
        results[name] = dest
    return results


def run(binary: Path, data: str, timeout: int = 15) -> str:
    # Do not inherit any matching .INP from the caller's working directory.
    with tempfile.TemporaryDirectory(prefix="kim-lien-run-") as cwd:
        p = subprocess.run([str(binary)], input=data, text=True, capture_output=True,
                           timeout=timeout, cwd=cwd, check=True)
    return p.stdout.strip()


def prime_reference(n: int) -> str:
    count = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            count += 1
            n //= d
        d += 1
    count += int(n > 1)
    return "YES" if count == 3 else "NO"


CODONS = {
    **{x: "Ser" for x in ("UCA", "UCU", "UCC", "UCG")},
    **{x: "Thr" for x in ("ACA", "ACU", "ACC", "ACG")},
    **{x: "Arg" for x in ("CGA", "CGU", "CGC", "CGG")},
    **{x: "Gly" for x in ("GGA", "GGU", "GGC", "GGG")},
    **{x: "Tyr" for x in ("UAU", "UAC")},
    **{x: "His" for x in ("CAU", "CAC")},
    **{x: "Pro" for x in ("CCU", "CCA", "CCC", "CCG")},
}


def protein_reference(dna: str) -> str:
    trans = str.maketrans({"A": "U", "T": "A", "C": "G", "G": "C"})
    mrna = dna.translate(trans)
    return "-".join(CODONS.get(mrna[i:i + 3], "Unk")
                    for i in range(0, len(mrna) - 2, 3))


def billiard_reference(m: int, n: int, x: int, y: int,
                        vx: int, vy: int, t: int) -> str:
    # Simulate unit spatial steps, independently on each coordinate.
    def bounce(length: int, pos: int, vel: int) -> int:
        direction = -1 if vel < 0 else 1
        for _ in range(abs(vel) * t):
            if pos == 0 and direction == -1:
                direction = 1
            if pos == length and direction == 1:
                direction = -1
            pos += direction
        return pos
    return f"{bounce(m, x, vx)} {bounce(n, y, vy)}"


def divide_reference(nums: list[int]) -> int:
    answer = 0
    for mask in range(1, 1 << len(nums)):
        digits = "".join(str(x) for i, x in enumerate(nums) if mask >> i & 1)
        if int(digits) % 11 == 0:
            answer += 1
    return answer % MOD


ALKANE = [None, 1, 1, 1, 2, 3, 5, 9, 18, 35, 75,
          159, 355, 802, 1858, 4347, 10359, 24894, 60523, 148284, 366319]


def alkane_bruteforce(n: int) -> int:
    """Independent graph enumeration via Prufer codes (labeled trees, then canonicalize)."""
    if n <= 2:
        return 1

    def canonical(adj: list[list[int]]) -> str:
        degree = [len(near) for near in adj]
        leaves = [v for v in range(n) if degree[v] <= 1]
        remaining = n
        while remaining > 2:
            remaining -= len(leaves)
            new_leaves = []
            for v in leaves:
                degree[v] = 0
                for u in adj[v]:
                    if degree[u] > 0:
                        degree[u] -= 1
                        if degree[u] == 1:
                            new_leaves.append(u)
            leaves = new_leaves

        def encode(v: int, parent: int) -> str:
            branches = sorted(encode(u, v) for u in adj[v] if u != parent)
            return "(" + "".join(branches) + ")"

        # One center or two centers. Swapping the sides cannot change identity.
        return min(encode(c, -1) for c in leaves)

    types = set()
    for code in itertools.product(range(n), repeat=n - 2):
        degree = [1] * n
        for v in code:
            degree[v] += 1
        if max(degree) > 4:
            continue
        edges = [[] for _ in range(n)]
        for v in code:
            leaf = next(i for i in range(n) if degree[i] == 1)
            edges[leaf].append(v)
            edges[v].append(leaf)
            degree[leaf] -= 1
            degree[v] -= 1
        u, v = (i for i in range(n) if degree[i] == 1)
        edges[u].append(v)
        edges[v].append(u)
        types.add(canonical(edges))
    return len(types)


def main() -> None:
    rng = random.Random(20231130)
    with tempfile.TemporaryDirectory(prefix="kim-lien-hsg-") as td:
        base = Path(td)
        bins = compile_all(base)
        verify(run(bins["PRIME"], "12\n") == "YES", "PRIME sample")
        verify(run(bins["PROTEIN"], "AGTAGGGTAGCACCT\n") ==
               "Ser-Ser-His-Arg-Gly", "PROTEIN sample")
        verify(run(bins["BILLARD"], "11 7 2 4 1 1 14\n") == "6 4", "BILLARD sample")
        verify(run(bins["DIVIDE"], "5\n1 2 1 2 1\n") == "9", "DIVIDE sample")
        verify(run(bins["ALKANE"], "5\n") == "3", "ALKANE sample")

        for n in [1, 2, 4, 8, 16, 27, 30, 49, 121, 9999999967, 100000000000000]:
            verify(run(bins["PRIME"], f"{n}\n") == prime_reference(n), f"PRIME edge {n}")
        for _ in range(150):
            n = rng.randint(1, 10**9)
            verify(run(bins["PRIME"], f"{n}\n") == prime_reference(n), f"PRIME random {n}")

        # Official constraints: DNA contains A/T/C/G and length is a multiple of 3.
        for dna in ["AGT", "TTT", "GGG", "CCC"]:
            verify(run(bins["PROTEIN"], dna + "\n") ==
                   protein_reference(dna), f"PROTEIN valid edge {dna}")
        # Robustness only: these tails violate the official divisible-by-3 rule.
        for dna in ["A", "AT", "AGTA", "AGTAG"]:
            verify(run(bins["PROTEIN"], dna + "\n") ==
                   protein_reference(dna), f"PROTEIN out-of-spec tail {dna}")

        # Hand-checked expected values independent of CODONS/protein_reference.
        # AGA and AGG are Arg in the full genetic code but Unk in THIS exam.
        protein_regression_vectors = [
            ("AGT", "Ser"), ("TGT", "Thr"), ("GCT", "Arg"),
            ("CCT", "Gly"), ("ATA", "Tyr"), ("GTA", "His"),
            ("GGA", "Pro"), ("TCT", "Unk"), ("TCC", "Unk"),
            ("TCA", "Unk"), ("ACT", "Unk"),
            ("AGTTCA", "Ser-Unk"), ("GTAGGA", "His-Pro"),
        ]
        for dna, expected in protein_regression_vectors:
            verify(run(bins["PROTEIN"], dna + "\n") == expected,
                   f"PROTEIN hand-checked codon {dna}")

        for _ in range(200):
            dna = "".join(rng.choices("ATCG", k=3 * rng.randint(1, 60)))
            verify(run(bins["PROTEIN"], dna + "\n") ==
                   protein_reference(dna), f"PROTEIN random {dna}")
        # Every one of the 4^3 possible DNA codons, including all Unk codons.
        for triplet in map("".join, itertools.product("ATCG", repeat=3)):
            verify(run(bins["PROTEIN"], triplet + "\n") ==
                   protein_reference(triplet), f"PROTEIN all codons {triplet}")
        # Largest legal length <= 100000 divisible by 3 is 99999, not 100000.
        long_dna = "ATCG" * 24999 + "ATC"
        assert len(long_dna) == 99999 and len(long_dna) % 3 == 0
        verify(run(bins["PROTEIN"], long_dna + "\n") ==
               protein_reference(long_dna), "PROTEIN max legal 99999 chars")

        for _ in range(200):
            m, n = rng.randint(2, 20), rng.randint(2, 20)
            x, y = rng.randint(1, m - 1), rng.randint(1, n - 1)
            vx, vy, t = rng.randint(-6, 6), rng.randint(-6, 6), rng.randint(1, 40)
            inp = f"{m} {n} {x} {y} {vx} {vy} {t}\n"
            expected = billiard_reference(m, n, x, y, vx, vy, t)
            verify(run(bins["BILLARD"], inp) == expected, f"BILLARD random {inp!r}")
        big = "100 99 42 24 -1000000000 1000000000 1000000000\n"
        verify(run(bins["BILLARD"], big) == "42 74", "BILLARD large negative")

        for nums in [[11], [1], [1, 1], [11, 11], [1, 2, 1, 2, 1],
                     [1000000000, 1000000000], [11] * 12]:
            inp = f"{len(nums)}\n" + " ".join(map(str, nums)) + "\n"
            verify(int(run(bins["DIVIDE"], inp)) == divide_reference(nums), f"DIVIDE edge {nums}")
        for _ in range(150):
            nums = [rng.randint(1, 10**9) for _ in range(rng.randint(1, 10))]
            inp = f"{len(nums)}\n" + " ".join(map(str, nums)) + "\n"
            verify(int(run(bins["DIVIDE"], inp)) == divide_reference(nums), f"DIVIDE random {nums}")
        for length in range(1, 6):
            for tup in itertools.product((1, 2, 11), repeat=length):
                nums = list(tup)
                inp = f"{length}\n" + " ".join(map(str, nums)) + "\n"
                verify(int(run(bins["DIVIDE"], inp)) == divide_reference(nums),
                       f"DIVIDE exhaustive {nums}")
        n = 100000
        verify(int(run(bins["DIVIDE"], f"{n}\n" + "11 " * n + "\n")) ==
               (pow(2, n, MOD) - 1) % MOD, "DIVIDE 100000 all divisible")

        for n in range(1, 21):
            verify(int(run(bins["ALKANE"], f"{n}\n")) == ALKANE[n], f"ALKANE OEIS n={n}")

        # Independent constructive count: enumerate labeled trees through Prufer
        # sequences, canonicalize unrooted shapes, and enforce maximum degree 4.
        for size in range(1, 9):
            verify(alkane_bruteforce(size) == ALKANE[size],
                   f"ALKANE independent brute force n={size}")

        # Judge file mode, in addition to stdin mode.
        for name, input_data, expected in [
            ("PRIME", "12\n", "YES"),
            ("PROTEIN", "AGTAGGGTAGCACCT\n", "Ser-Ser-His-Arg-Gly"),
            ("BILLARD", "11 7 2 4 1 1 14\n", "6 4"),
            ("DIVIDE", "5\n1 2 1 2 1\n", "9"),
            ("ALKANE", "5\n", "3"),
        ]:
            work = base / ("file_" + name)
            work.mkdir()
            (work / (name + ".INP")).write_text(input_data, encoding="utf-8")
            subprocess.run([str(bins[name])], cwd=work, timeout=15, check=True,
                           capture_output=True, stdin=subprocess.DEVNULL)
            output = (work / (name + ".OUT")).read_text(encoding="utf-8").strip()
            verify(output == expected, f"{name} INP/OUT mode")

        # Judge collision regression: a stale official .INP must not steal
        # piped stdin from a stdout-based judge (historical WA reproducer).
        work = base / "protein_judge_collision"
        work.mkdir()
        (work / "PROTEIN.INP").write_text("TCT\n", encoding="utf-8")
        p = subprocess.run([str(bins["PROTEIN"])], input="AGT\n", text=True,
                           cwd=work, capture_output=True, timeout=15, check=True)
        verify(p.stdout.strip() == "Ser" and
               (work / "PROTEIN.OUT").read_text(encoding="utf-8").strip() == "Ser",
               "PROTEIN stdin wins over stale .INP; output mirrored")

        # The original file-only contract still works with stdin explicitly at EOF.
        work = base / "protein_official_file_only"
        work.mkdir()
        (work / "PROTEIN.INP").write_text("TCT\n", encoding="utf-8")
        p = subprocess.run([str(bins["PROTEIN"])], cwd=work,
                           stdin=subprocess.DEVNULL, capture_output=True,
                           text=True, timeout=15, check=True)
        verify(p.stdout.strip() == "Unk" and
               (work / "PROTEIN.OUT").read_text(encoding="utf-8").strip() == "Unk",
               "PROTEIN file-only judge fallback")

    print(f"PASS: {CASES}/{CASES} assertions; 5 C++17 programs compiled successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL after {CASES} assertions: {exc}", file=sys.stderr)
        raise
