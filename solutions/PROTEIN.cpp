// Bai 2: DNA template -> mRNA -> amino acids; bo qua 1-2 nucleotide cuoi neu thieu bo ba.
#include <bits/stdc++.h>
using namespace std;

int main() {
    if (FILE *f = fopen("PROTEIN.INP", "r")) {
        fclose(f);
        freopen("PROTEIN.INP", "r", stdin);
        freopen("PROTEIN.OUT", "w", stdout);
    }
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string dna;
    if (!(cin >> dna)) return 0;
    auto complement = [](char c) -> char {
        switch (c) {
            case 'A': return 'U';
            case 'T': return 'A';
            case 'C': return 'G';
            case 'G': return 'C';
            default: return '?';
        }
    };
    const unordered_map<string, string> amino = {
        {"UCA", "Ser"}, {"UCU", "Ser"}, {"UCC", "Ser"}, {"UCG", "Ser"},
        {"ACA", "Thr"}, {"ACU", "Thr"}, {"ACC", "Thr"}, {"ACG", "Thr"},
        {"CGA", "Arg"}, {"CGU", "Arg"}, {"CGC", "Arg"}, {"CGG", "Arg"},
        {"GGA", "Gly"}, {"GGU", "Gly"}, {"GGC", "Gly"}, {"GGG", "Gly"},
        {"UAU", "Tyr"}, {"UAC", "Tyr"}, {"CAU", "His"}, {"CAC", "His"},
        {"CCU", "Pro"}, {"CCA", "Pro"}, {"CCC", "Pro"}, {"CCG", "Pro"}
    };

    bool first = true;
    for (size_t i = 0; i + 2 < dna.size(); i += 3) {
        string codon;
        for (int j = 0; j < 3; ++j) codon += complement(dna[i + j]);
        auto it = amino.find(codon);
        if (!first) cout << '-';
        first = false;
        cout << (it == amino.end() ? "Unk" : it->second);
    }
    cout << '\n';
}
