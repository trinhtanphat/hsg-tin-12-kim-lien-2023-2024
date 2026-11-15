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
- Bộ hồi quy mới **1.207/1.207 PASS** đã chạy thực tế trên WIN11-181 ngày 14/11/2026 từ commit `15c36be6`, gồm 13 đối chứng viết tay bổ sung so với 1.194 khẳng định lịch sử. 5/5 binary C++17 biên dịch thành công.
- Bộ kiểm thử sinh công khai 420 trường hợp vốn đã dùng PROTEIN 99.999 ký tự cho stress; thay đổi này chủ yếu sửa **test runner hồi quy** và minh bạch phạm vi.
- QA trên máy WIN11-181 hoặc môi trường C++17 được chỉ định; không sử dụng GitHub Actions.
- Chưa có bằng chứng từ máy chấm bí mật của nhà trường; không tuyên bố AC chính thức.


## Đối chứng thực chạy trên Linux ngày 14/11/2026

Bản `solutions/PROTEIN.cpp` dùng để biên dịch đã được đối chiếu **Git blob SHA `30a2e3823c06b07aeb62a1fe1dbf870425f61be3`** với tệp trên nhánh kiểm toán (không chỉ dựa trên việc sao chép nội dung).

| Trình biên dịch | Kết quả | Các ca kiểm thử |
|---|---:|---|
| GNU G++ 14.2.0 (C++17, `-O2 -Wall -Wextra -Wpedantic`) | **379/379 PASS** | 13 viết tay + 64 bộ ba + 300 chuỗi DNA hợp lệ ngẫu nhiên + 99.999 ký tự + I/O tệp |
| Clang++ 17.0.0 (cùng flags) | **379/379 PASS** | Cùng 379 trường hợp |

Đây là **QA trọng tâm trên Linux**, độc lập với bộ hồi quy toàn repo vừa chạy trên **WIN11-181: 1.207/1.207 PASS** và ngân hàng dữ liệu **420/420 PASS** (SHA-256, ZIP CRC, C++17 output). Cả hai không thay thế AC từ hệ thống chấm trường. Xem [QA_EVIDENCE.md](QA_EVIDENCE.md).


## Phát hiện lỗi nhập/xuất có thể gây WA (14/11/2026)

**Tái hiện thực tế trên WIN11-181 từ chương trình trước bản sửa I/O:**

- Khi không có `PROTEIN.INP`, cấp stdin `AGT` → stdout `Ser`.
- Khi `PROTEIN.INP` chứa `TCT` và đồng thời cấp stdin `AGT`, chương trình trước đó tự động `freopen` sang tệp, stdout rỗng và `PROTEIN.OUT` chứa `Unk`.
- Đây là lỗi **ưu tiên nguồn nhập/xuất** nếu hệ thống chấm dựa trên stdin/stdout trong thư mục có tệp `PROTEIN.INP` cũ; không chứng minh thuật toán ánh xạ codon sai trên dữ liệu hợp lệ.

**Cách khắc phục trong `solutions/PROTEIN.cpp`:** ưu tiên stdin, chỉ đọc tệp khi stdin EOF; luôn in stdout, đồng thời ghi `PROTEIN.OUT` nếu tệp `PROTEIN.INP` tồn tại. Cờ `-DPROTEIN_FORCE_FILE_IO` chọn chế độ tệp khi chạy tương tác. Bổ sung hai test hồi quy (xung đột đầu vào + chế độ tệp không có stdin), và cô lập stdin=DEVNULL khi kiểm thử file-only. Các kết quả 1.207 PASS lịch sử vẫn thuộc commit `15c36be6`; bản mới phải được chạy lại trước khi công bố số liệu PASS tiếp theo.

**Giới hạn:** Chưa có URL/ID bài chấm và log WA thật từ người dùng, nên chưa xác nhận máy chấm đang sử dụng trường hợp này. Nếu vẫn WA sau sửa, cần xem kết quả chấm thực tế và đối chiếu checker; không được suy từ test nội bộ rằng đã AC chính thức.


### Kết quả kiểm thử bản sửa I/O trên WIN11-181

- Commit kiểm tra: `89f8d56844cbe70c4ccfdd4856528bff40f9c6ef`.
- Zig C++17 0.13.0 + Python 3.13.9 portable; toàn bộ **1.209/1.209 assertions PASS**, **5/5 C++17 compiled**. Số 1.209 gồm 2 test mới về ưu tiên stdin và chế độ file-only.
- `tests/coverage_audit.py` **PASS**, xác nhận 100+100+100+100+20=420 đầu vào duy nhất và các biên ràng buộc.
- `tests/check_generated.py` **420/420 PASS** cùng kiểm tra SHA-256 manifest, ZIP CRC và đầu ra thực của các chương trình C++17; tiến trình PowerShell trả mã 0.
- Không chạy GitHub Actions; không thay đổi production hay Session 2.
- **Quan trọng:** vẫn chưa có log WA/AC thật từ nền tảng chấm. Kết quả PASS nội bộ xác nhận lỗi I/O tái hiện đã được sửa trong môi trường thử, **không chứng nhận AC chính thức**.


## Đối chiếu QTOJ p059 File IO — 15/11/2026

Người dùng cung cấp kết quả chấm trên QTOJ: **15/16 Accepted, test #14 Wrong Answer**, dù phiên bản cũ đã vượt 1209 kiểm thử nội bộ. Đã mở trực tiếp trang đề p059 (giao diện công khai, không truy cập hidden tests), đối chiếu bảng 24 codon và điều kiện `|DNA| <= 100000`, độ dài chia hết cho 3. **Không có bằng chứng mã codon sai.**

Nền tảng hiển thị **Chế độ I/O: File IO**, yêu cầu đọc `PROTEIN.INP` và ghi `PROTEIN.OUT`. Vì vậy bản mới ưu tiên file khi nó tồn tại, tránh xung đột với stdin phụ; và chỉ dùng stdin/stdout khi không tìm thấy `.INP`. Ở chế độ file, không ghi bản sao vào stdout. Đây là thay đổi về hợp đồng I/O, không thay đổi thuật toán.

Test bổ sung kiểm tra thứ tự ưu tiên khi đồng thời có file và stdin, chế độ file không có stdin, và dữ liệu dài tối đa hợp lệ **99.999 nucleotide**, với 16.667 `His` + 16.666 `Unk`, viết/đọc qua file.

**Quan trọng:** chưa có nội dung input/expected output của test #14 và chưa có lần chấm QTOJ AC mới. Vì vậy **không thể khẳng định nguyên nhân WA #14 đã được giải quyết** chỉ nhờ PASS nội bộ. Nếu vẫn WA, cần đề nghị người quản trị QTOJ rà soát expected output và tính hợp lệ của test #14, thay vì tự ý biến đổi bảng codon đã khớp đề.


## Đối chứng độc lập sau khi QTOJ vẫn WA test #14 (15/11/2026)

**Nguồn phản hồi:** người dùng xác nhận bản sau PR #7 vẫn **15/16 Accepted; test #14 Wrong Answer** tại `https://qtoj.org/problems/p059?tab=editor`. Trạng thái này **không phải AC**, dù 1.212 kiểm thử nội bộ từng PASS.

**Khảo sát thực tế:** trang bài p059 của QTOJ (trang công khai) tiếp tục chỉ định `File IO`, đầu vào chỉ có A/T/C/G, dài không quá 100.000 và chia hết cho 3, bảng mã gồm 24 codon, codon khác ra `Unk`. Mã `solutions/PROTEIN.cpp` ở main `02712af5f4e6ad2ddacb6303bc146c203e1eea52` khớp phần đặc tả đã công bố; chưa xác định trường hợp đúng đặc tả làm chương trình cho đáp án sai.

**Phương pháp kiểm tra mới:** `tests/p059_independent_qa.py` tạo bảng ánh xạ *DNA triplet → amino acid* độc lập (thay vì tái sử dụng bảng *mRNA → amino acid* của lời giải) và kiểm tra nguyên chuỗi output qua `PROTEIN.INP`/`PROTEIN.OUT`. Nó bao phủ 4.096 cặp hai codon liền nhau, 6 chuỗi thử dài 99.999 nucleotide (ngẫu nhiên, toàn Unk, toàn His, trộn His/Unk, luân phiên đủ codon, mẫu đề lặp), cùng fallback stdin và thứ tự ưu tiên file. Công cụ so sánh toàn bộ output theo ký tự, không chỉ hash, và thất bại tại ký tự đầu tiên khác nếu có.

**Kết quả chạy thực tế WIN11-181:** SHA QA `4b0fdafea6b2340cbe147b61387d33df79f4916b`, Python portable 3.13.9 + Zig C++17 0.13.0, `QA_EXIT=0`, tất cả nhóm kiểm thử **PASS**. Các SHA-256 ngắn và thời lượng từng ca hiển thị trong stdout; đây không phải tốc độ tương đương QTOJ.

**Kết luận kỹ thuật:** chưa tìm thấy lỗi thuật toán hay file-mode trong miền đặc tả được công khai. Kết quả WA duy nhất vẫn có thể xuất phát từ (a) test ẩn không khớp đặc tả, (b) expected output của bộ chấm không chính xác, (c) phiên bản mã được nộp chưa khớp GitHub, hoặc (d) hành vi checker/runner chưa quan sát được. **Không có bằng chứng để khẳng định nguyên nhân nào.** Không nên chỉnh bảng codon hoặc ràng buộc theo suy đoán chỉ để làm một test qua.

**Bằng chứng cần để truy nguyên:** mã submission và nguồn C++ đúng phiên bản được QTOJ chấm; nếu được phép, báo cáo từ quản trị viên về `PROTEIN.INP`/expected `PROTEIN.OUT` của test #14 hoặc nguyên nhân checker. Theo dõi [issue #6](https://github.com/trinhtanphat/hsg-tin-12-kim-lien-2023-2024/issues/6). Giữ issue **OPEN** cho tới khi có xác minh 16/16 hoặc phản ví dụ cụ thể.
