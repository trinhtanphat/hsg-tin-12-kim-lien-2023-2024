# Đề bài: tóm tắt đối chiếu 3 ảnh gốc (30/08/2023)

> Nội dung được biên tập lại từ **3 trang ảnh do người dùng cung cấp**; không phải bản PDF chính thức được xác nhận từ nhà trường. Mục đích là giữ đúng yêu cầu kỹ thuật, ràng buộc và những lỗi in ấn cần lưu ý khi chấm.

**Đơn vị:** Sở GD&ĐT Hà Nội — THPT Kim Liên. **Kỳ thi:** chọn đội tuyển thi học sinh giỏi thành phố Hà Nội lớp 12, năm học 2023–2024. **Môn:** Tin học. **Ngày:** 30/08/2023. **Thời gian:** 180 phút. **Thang điểm:** 20.

| STT | Bài | Điểm | Input | Output |
|---|---|---:|---|---|
| 1 | Tích ba số nguyên tố | 5 | PRIME.INP | PRIME.OUT |
| 2 | Tổng hợp amino acid | 5 | PROTEIN.INP | PROTEIN.OUT |
| 3 | Bàn bi-a | 4 | BILLARD.INP | BILLARD.OUT |
| 4 | Chia hết cho 11 | 3 | DIVIDE.INP | DIVIDE.OUT |
| 5 | Alkane | 3 | ALKANE.INP | ALKANE.OUT (*) |

`(*)` Trang 1 in nhầm tên file **kết quả** Bài 5 là `ALKANE.INP`; trang 3 yêu cầu `ALKANE.OUT`, được lấy làm chuẩn thực thi.

## Bài 1 — PRIME (5 điểm)

- **Input:** một số nguyên dương `n`, trong nhóm test lớn `n <= 10^14`.
- **Yêu cầu:** kiểm tra `n` có là tích của **đúng ba** số nguyên tố hay không. Có thể trùng nhau, ví dụ `12 = 2*2*3`, `8 = 2*2*2`.
- **Output:** `YES` hoặc `NO`.
- **Ví dụ:** `12` → `YES`.
- **Phân nhóm:** 25% mỗi nhóm `n<=10^6` và YES; `n<=10^6` và NO; `10^6<n<=10^14` và YES; `10^6<n<=10^14` và NO.

## Bài 2 — PROTEIN (5 điểm)

- **Input:** một dòng DNA gồm các ký tự `A, T, C, G`, độ dài **không quá `10^5` và chia hết cho 3** (ghi rõ tại trang 2).
- **Quy luật:** mỗi DNA mạch đơn được phiên mã bổ sung sang mRNA: `A→U`, `T→A`, `C→G`, `G→C`. Đọc các codon mRNA liên tiếp, mỗi codon gồm 3 ký tự.
- **Bảng mã theo đề:** `UCA/UCU/UCC/UCG→Ser`; `ACA/ACU/ACC/ACG→Thr`; `CGA/CGU/CGC/CGG→Arg`; `GGA/GGU/GGC/GGG→Gly`; `UAU/UAC→Tyr`; `CAU/CAC→His`; `CCU/CCA/CCC/CCG→Pro`; mọi codon khác → `Unk`.
- **Output:** các tên amino acid cách nhau bởi dấu `-`, không dấu cách.
- **Ví dụ:** `AGTAGGGTAGCACCT` → `Ser-Ser-His-Arg-Gly`.
- **Phân nhóm:** 25% test chỉ có `His` và `Unk`; 50% test có độ dài `<=10^3`; 25% không thêm ràng buộc.

## Bài 3 — BILLARD (4 điểm)

- **Input:** 7 số nguyên `m n x y v1 v2 t`, với `2<=m,n<=100`, `1<=x<m`, `1<=y<n`, `-1<=v1,v2<=1`, `1<=t<=10^9`.
- **Bàn:** hình chữ nhật trục tọa độ `0<=X<=m`, `0<=Y<=n`; bóng ở `(x,y)` khi thời gian `0`.
- **Chuyển động:** vận tốc không đổi giữa các lần va chạm, phản xạ đàn hồi ở thành (góc tới = góc phản xạ); va chạm góc đảo hướng cả hai thành phần.
- **Output:** `x' y'` tại thời điểm `t`.
- **Ví dụ:** `11 7 2 4 1 1 14` → `6 4`.
- **Phân nhóm:** 50% `t<=10^7`; 25% `10^7<t<=10^9` với `v1=0` hoặc `v2=0`; 25% còn lại.
- **Lỗi đánh máy của đề:** trang 2 liệt kê đỉnh thứ tư là `(n;0)` (không tạo thành hình chữ nhật). Theo hình minh họa, hình chữ nhật đúng phải có đỉnh `(0;n)`.

## Bài 4 — DIVIDE (3 điểm)

- **Input:** dòng đầu `1<=n<=10^5`; dòng tiếp gồm `n` số nguyên dương có giá trị `<=10^9`.
- **Yêu cầu:** chọn **ít nhất một** thẻ, giữ nguyên thứ tự ban đầu, ghép biểu diễn thập phân thành một số chia hết cho 11. Đếm **số tập vị trí** được chọn, không phải số giá trị khác nhau.
- **Output:** số cách modulo `10^9+7`.
- **Ví dụ:** `5\n1 2 1 2 1` → `9`.
- **Phân nhóm:** 25% `n<=10`, chỉ số một chữ số; 25% `n<=10`; 25% tất cả thẻ bằng nhau và một chữ số; 25% còn lại.

## Bài 5 — ALKANE (3 điểm)

- **Input:** một số nguyên dương `1<=n<=20`.
- **Yêu cầu:** đếm số cây **không gắn nhãn** có `n` đỉnh, tất cả bậc đỉnh `<=4`, tính mỗi lớp đẳng cấu đúng một lần. Đây là số đồng phân cấu tạo của alkane `C_n H_(2n+2)` theo mô hình mạch carbon không vòng.
- **Output:** một số nguyên dương duy nhất.
- **Ví dụ:** `5` → `3`.
- **Phân nhóm:** 20 test khác nhau, mỗi test 5% điểm của bài.

## Hướng dẫn sử dụng

Lời giải, chứng minh tính đúng đắn, độ phức tạp và cạm bẫy từng bài: [EDITORIAL.md](EDITORIAL.md). Đối chiếu các vấn đề in ấn: [DANH_GIA_DE.md](DANH_GIA_DE.md).

**Nguyên tắc ưu tiên:** ràng buộc đề gốc (nêu chính xác ở trên) khác với test thử robustness vượt phạm vi (như DNA dư ký tự hoặc vận tốc `|v|>1`); hai loại test được tách biệt trong phần mô tả QA.
