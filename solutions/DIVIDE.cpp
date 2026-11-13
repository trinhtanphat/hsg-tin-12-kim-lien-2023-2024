// Bai 4: Dem cac day con khong rong, giu nguyen thu tu, ghep lai chia het cho 11.
#include <bits/stdc++.h>
using namespace std;

int main() {
    if (FILE *f = fopen("DIVIDE.INP", "r")) {
        fclose(f);
        freopen("DIVIDE.INP", "r", stdin);
        freopen("DIVIDE.OUT", "w", stdout);
    }
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    const long long MOD = 1'000'000'007LL;
    int n;
    if (!(cin >> n)) return 0;
    array<long long, 11> dp{};
    dp[0] = 1;  // Day rong, tru 1 khi in dap an.
    for (int i = 0; i < n; ++i) {
        long long x;
        cin >> x;
        int digits = 0;
        for (long long y = x; y > 0; y /= 10) ++digits;
        // 10^digits mod 11 = (-1)^digits mod 11.
        const int power = digits % 2 == 0 ? 1 : 10;
        const int remainder = static_cast<int>(x % 11);
        auto next = dp;  // Khong chon phan tu thu i.
        for (int r = 0; r < 11; ++r) {
            const int nr = (r * power + remainder) % 11;
            next[nr] = (next[nr] + dp[r]) % MOD;
        }
        dp = next;
    }
    cout << (dp[0] + MOD - 1) % MOD << '\n';
}
