"""Offline C++17 QA: compile all five tasks, sample, random differential, edge, stress.
No third-party libraries and no GitHub Actions required.
"""
from __future__ import annotations

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
    compiler = next((shutil.which(c) for c in ("g++", "clang++") if shutil.which(c)), None)
    if not compiler:
        raise RuntimeError("Missing g++ or clang++; install a C++17 compiler.")
    results = {}
    for name in SOURCES:
        dest = target / (name + (".exe" if os.name == "nt" else ""))
        subprocess.run(
            [compiler, "-std=c++17", "-O2", "-Wall", "-Wextra", "-Wpedantic",
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

        for dna in ["A", "AT", "AGT", "AGTA", "AGTAG", "TTT", "GGG", "CCC"]:
            verify(run(bins["PROTEIN"], dna + "\n") ==
                   protein_reference(dna), f"PROTEIN edge {dna}")
        for _ in range(200):
            dna = "".join(rng.choices("ATCG", k=rng.randint(1, 180)))
            verify(run(bins["PROTEIN"], dna + "\n") ==
                   protein_reference(dna), f"PROTEIN random {dna}")
        long_dna = "ATCG" * 25000
        verify(run(bins["PROTEIN"], long_dna + "\n") ==
               protein_reference(long_dna), "PROTEIN 100000 chars")

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
        n = 100000
        verify(int(run(bins["DIVIDE"], f"{n}\n" + "11 " * n + "\n")) ==
               (pow(2, n, MOD) - 1) % MOD, "DIVIDE 100000 all divisible")

        for n in range(1, 21):
            verify(int(run(bins["ALKANE"], f"{n}\n")) == ALKANE[n], f"ALKANE OEIS n={n}")

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
                           capture_output=True)
            output = (work / (name + ".OUT")).read_text(encoding="utf-8").strip()
            verify(output == expected, f"{name} INP/OUT mode")

    print(f"PASS: {CASES}/{CASES} assertions; 5 C++17 programs compiled successfully")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL after {CASES} assertions: {exc}", file=sys.stderr)
        raise
