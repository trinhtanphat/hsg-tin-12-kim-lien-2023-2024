# Kiểm toán PROTEIN: đặc tả, đối chứng độc lập và lỗi phạm vi test (14/11/2026)

## Kết luận
- Chưa xác nhận một sai lệch kết quả **trên miền đề gốc** của `solutions/PROTEIN.cpp`. Không tự ý đổi logic dịch mã khi chưa có testcase phản ví dụ hợp lệ.
- Đã phát hiện **một lỗi về phạm vi kiểm thử**: `tests/run_tests.py` cũ dùng `"ATCG" * 25000` (100.000 ký tự), nhưng đề yêu cầu chiều dài DNA chia hết cho 3. `100000 % 3 == 1`. Test đó không thuộc miền đề chính thức.
- Thay stress test bằng `"ATCG" * 24999 + "ATC"`, dài **99.999 ký tự**, là chiều dài hợp lệ lớn nhất.
- Chương trình có chủ đích không dịch nhóm cuối thiếu 3 nucleotide nếu thử đầu vào ngoài đặc tả. Điều này không chứng minh có lỗi bài thi.

## Đặc tả cần giữ nguyên
1. Đầu vào là DNA **mạch khuôn (template)** gồm A/T/C/G, độ dài chia hết cho 3 và không quá 100.000.
2. Phiên mã bổ sung: `A→U`, `T→A`, `C→G`, `G→C`; sau đó chia thành các bộ ba *từ trái qua phải*.
3. Chỉ **24 codon** được đề cung cấp có kết quả `Ser/Thr/Arg/Gly/Tyr/His/Pro`. Các codon còn lại in đúng chữ **`Unk`**, không thêm tên amino acid dựa trên bảng mã sinh học chuẩn.
4. Đầu ra không có dấu gạch nối ở đầu hoặc cuối, dấu `-` chỉ đặt giữa hai amino acid.

## 13 ca đối chứng viết tay (không suy đáp án từ bảng `CODONS` trong test runner)

| DNA input | mRNA bổ sung | Expected output | Mục đích |
|---|---|---|---|
| `AGT` | UCA | `Ser` | Ser |
| `TGT` | ACA | `Thr` | Thr |
| `GCT` | CGA | `Arg` | Arg |
| `CCT` | GGA | `Gly` | Gly |
| `ATA` | UAU | `Tyr` | Tyr |
| `GTA` | CAU | `His` | His |
| `GGA` | CCU | `Pro` | Pro |
| `TCT` | AGA | `Unk` | Không thêm codon Arg ngoài đề |
| `TCC` | AGG | `Unk` | Không thêm codon Arg ngoài đề |
| `TCA` | AGU | `Unk` | Không thêm codon Ser ngoài đề |
| `ACT` | UGA | `Unk` | Không tự thêm STOP |
| `AGTTCA` | UCA-AGU | `Ser-Unk` | Codon không xác định ở cuối |
| `GTAGGA` | CAU-CCU | `His-Pro` | Đa codon, dấu nối đúng |

Ghi chú: cột mRNA của hai ca đa codon dùng dấu `-` để minh họa ranh giới codon, không phải ký tự đầu vào.

## Cách chạy lại QA
```powershell
python tests/run_tests.py
python tests/generate_cases.py
python tests/coverage_audit.py
python tests/check_generated.py
```

- Hồi quy gồm kiểm tra 64 bộ ba, ngẫu nhiên **hợp lệ** (độ dài bội 3), chuỗi dài hợp lệ 99.999, 13 ca đối chứng viết tay, và nhóm **ngoài đặc tả** riêng.
- Số khẳng định dự kiến của `run_tests.py` là **1.207** (trước đó 1.194; bổ sung 13), nhưng chỉ được ghi là PASS sau khi chạy thực tế.
- Bộ kiểm thử sinh công khai 420 trường hợp vốn đã dùng PROTEIN 99.999 ký tự cho stress; thay đổi này chủ yếu sửa **test runner hồi quy** và minh bạch phạm vi.
- QA trên máy WIN11-181 hoặc môi trường C++17 được chỉ định; không sử dụng GitHub Actions.
- Chưa có bằng chứng từ máy chấm bí mật của nhà trường; không tuyên bố AC chính thức.
