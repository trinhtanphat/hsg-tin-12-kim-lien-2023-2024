# Bộ test HSG Tin học 12 Kim Liên 2023–2024 — 420 test

## Phạm vi theo đề chính thức
| Bài | Số test | Ràng buộc | Test đặc biệt |
| --- | ---: | --- | --- |
| PRIME | 100 | 1 ≤ n ≤ 10^14 | Phân bố YES/NO, lũy thừa, số nguyên tố lớn, cận tối đa |
| PROTEIN | 100 | DNA A/T/C/G, độ dài chia hết 3, ≤ 10^5 | Đầy đủ 64 bộ ba và 36 test hỗn hợp, gần 10^5 ký tự |
| BILLARD | 100 | 2 ≤ m,n ≤ 100, -1 ≤ v1,v2 ≤ 1, 1 ≤ t ≤ 10^9 | 9 tổ hợp vận tốc, t lớn, trục đứng yên, bàn hẹp |
| DIVIDE | 100 | 1 ≤ n ≤ 10^5, 1 ≤ ai ≤ 10^9 | Brute force ≤14 thẻ, n=10^5, nhiều số giống nhau, modulo |
| ALKANE | 20 | 1 ≤ n ≤ 20 | Đủ toàn bộ 20 giá trị hợp lệ, không lặp cho đủ 100 |

Tất cả **420 test đều nằm trong phạm vi đề gốc**, không lẫn test robust ngoài ràng buộc. Trường hợp bài Alkane **chỉ có 20 đầu vào khác nhau** là lý do chỉ sinh 20 test.

## Cấu trúc
- `tests/generated/PRIME/001/PRIME.INP` và `PRIME.OUT` tương ứng, tương tự cho 4 bài khác.
- `tests/generated/<NAME>/manifest.json` ghi từng test, loại trường hợp và SHA-256 hai tệp.
- `docs/assets/test-manifest.json` tổng hợp số lượng, SHA-256 từng gói ZIP và các nhóm dữ liệu.
- `docs/downloads/<NAME>_<n>_tests.zip` cho tải riêng từng bài trên GitHub Pages.

## Cách sinh và chạy lại độc lập
```powershell
python tests/generate_cases.py
python tests/check_generated.py
python tests/run_tests.py
```
Có thể dùng compiler g++ / clang++; khi Windows không có hai trình biên dịch này, đặt `ZIG_EXE` đến `zig.exe`. **Không bật GitHub Actions**.

## Đối chứng oracle
- **PRIME:** phân tích Pollard Rho + Miller–Rabin 64-bit độc lập với chia thử của C++.
- **PROTEIN:** ánh xạ DNA→mRNA, bảng đủ 64 codon; 40 bộ ba không định nghĩa trả Unk.
- **BILLARD:** mô phỏng từng bước khi t≤150, công thức phản xạ để xác nhận các trường hợp t lớn.
- **DIVIDE:** brute force tất cả tập con khi n≤14, DP số dư cho dữ liệu lớn.
- **ALKANE:** 20 giá trị trong dãy đối chứng; có thêm kiểm thử đếm cây Prüfer n≤8 trong `tests/run_tests.py`.

Lưu ý: bộ dữ liệu tự sinh và oracle độc lập không thay thế bộ test bí mật của hệ thống chấm chính thức.
