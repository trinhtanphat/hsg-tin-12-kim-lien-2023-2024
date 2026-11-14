# Bằng chứng kiểm thử độc lập (13/11/2026)

## Môi trường và kết quả

- **Máy chạy kiểm thử:** `WIN11-181`, Windows 11, qua Private Commander (không đóng tab, không thay đổi production).
- **Thời điểm hoàn tất:** 13/11/2026, 15:07:38 GMT+7.
- **C++ toolchain:** Zig `0.17.1`, portable, `zig c++` dùng chuẩn C++17. Bản tải từ `https://ziglang.org/download/index.json`, SHA-256 ZIP **b03f477a1943673e02aca0f570e8030dffd536ce1f45cbc4d3326ec31159562e** được xác minh trước khi giải nén.
- **Python:** portable `3.13.17`, tải từ `python.org` (ZIP SHA-256 `9e35319bffedab8b36ad44d8f377cb4f1733bcec257a0b6d04d94f01486ddb38`).
- **Lệnh thực thi tại thư mục repository:** `$env:ZIG_EXE='C:\Temp\HSG-KimLien-2023-2024\toolchain\zig-x86_64-windows-0.17.1\zig.exe'; & 'C:\Temp\HSG-KimLien-2023-2024\toolchain\python\python.exe' tests/run_tests.py`.
- **Stdout thực tế:** `PASS: 1194/1194 assertions; 5 C++17 programs compiled successfully`.
- **Quy trình điều khiển:** đã kiểm tra mã thoát của PowerShell = `0` và dòng `WIN11_181_QA_PASS` sau khi Python kết thúc.

## Phạm vi kiểm thử (1.194 khẳng định)

- **5** ví dụ chính thức từ ba trang ảnh đề.
- **161** kiểm tra PRIME: trường hợp biên và đối chiếu phân tích thừa số ngẫu nhiên.
- **273** kiểm tra PROTEIN: các chuỗi ngắn, 200 chuỗi ngẫu nhiên, đầy đủ **64** bộ ba DNA và đầu vào `100.000` ký tự.
- **201** kiểm tra BILLARD: mô phỏng va chạm từng bước độc lập và một trường hợp số lớn.
- **521** kiểm tra DIVIDE: đối chiếu exhaustive và brute-force, dữ liệu cực đại `n=100.000`.
- **28** kiểm tra ALKANE: 20 kết quả đối chiếu OEIS và **8 kiểm tra liệt kê cây bằng mã Prüfer** với `n=1..8` (độc lập với công thức hàm sinh của lời giải).
- **5** kiểm tra chế độ `*.INP → *.OUT` (ngoài stdin/stdout).

**Tổng: 5 + 161 + 273 + 201 + 521 + 28 + 5 = 1.194**, đúng với bộ đếm của `tests/run_tests.py` (mỗi lần gọi `verify()` tương ứng một kiểm tra).

## Biên dịch chéo trong môi trường QA Linux

- GNU G++ `14.2.0`: `1194/1194 PASS`.
- Clang++ `17.0.0`: `1194/1194 PASS`.
- Cả 5 chương trình chỉ dùng header C++17 chuẩn (không còn phụ thuộc `bits/stdc++.h`).

## Giới hạn xác minh

- Đây là **QA tự xây dựng và kiểm tra độc lập**, chưa phải kết quả nộp hệ thống chấm của Sở GD&ĐT.
- Một số test bổ sung cố tình vượt ngoài ràng buộc đề (DNA không chia hết 3, `|v|>1`) để thử độ ổn định; không thay thế các ràng buộc chính thức.
- Không sử dụng GitHub Actions và không đụng Session 2, production hay các dịch vụ tunnel.


## Đính chính bổ sung ngày 14/11/2026 — PROTEIN

Hồ sơ PASS 1.194/1.194 ngày 13/11 là **kết quả lịch sử**, không bị sửa hoặc đổi nhãn thành một lần chạy mới. Trong `tests/run_tests.py` phiên bản đó có stress test `"ATCG" * 25000` dài 100.000 ký tự; độ dài này **không chia hết cho 3**, nên chỉ phù hợp kiểm thử chịu lỗi ngoài phạm vi đề, không phù hợp làm trường hợp stress hợp lệ của đề gốc.

Bản cập nhật thay bằng chuỗi **99.999 ký tự** và bổ sung 13 đối chứng viết tay, tách nhóm trường hợp ngoài đặc tả. Kết quả QA mới phải lấy từ log thực chạy sau thay đổi, không suy từ số PASS cũ. Chi tiết: [PROTEIN_AUDIT.md](PROTEIN_AUDIT.md).
