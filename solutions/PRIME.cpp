// Bai 1: Tich ba so nguyen to (dem thua so nguyen to co boi so).
#include <bits/stdc++.h>
using namespace std;

int main() {
    if (FILE *f = fopen("PRIME.INP", "r")) {
        fclose(f);
        freopen("PRIME.INP", "r", stdin);
        freopen("PRIME.OUT", "w", stdout);
    }
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;
    int count = 0;
    while (n % 2 == 0 && n > 1) {
        ++count;
        n /= 2;
    }
    for (long long d = 3; d <= n / d && count <= 3; d += 2) {
        while (n % d == 0) {
            ++count;
            n /= d;
            if (count > 3) break;
        }
    }
    if (n > 1) ++count;
    cout << (count == 3 ? "YES" : "NO") << '\n';
}
