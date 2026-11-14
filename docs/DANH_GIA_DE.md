# Đánh giá đề chọn đội tuyển HSG Tin học 12 Hà Nội (THPT Kim Liên, 30/08/2023)

## Khái quát

Đề có **5 bài, 20 điểm, 180 phút**. Chủ đề đa dạng: lý thuyết số, xử lý chuỗi, mô phỏng hình học, quy hoạch động và tổ hợp đồ thị. Bố cục đi từ bài cơ bản đến bài khó; phù hợp để thăm dò năng lực, nhưng **độ khó không tăng tương ứng với số điểm**.

| Bài | Điểm | Độ khó tương đối (/10) | Nhận xét phân loại |
| --- | ---: | ---: | --- |
| 1 PRIME | 5 | 2/10 | Kiểm tra phân tích thừa số; dễ đạt trọn điểm |
| 2 PROTEIN | 5 | 3/10 | Xử lý chuỗi và bảng chuyển mã; yêu cầu đọc đề cẩn thận |
| 3 BILLARD | 4 | 5/10 | Có mẹo phản xạ/trải gương; phân loại ở tư duy toán và dấu âm |
| 4 DIVIDE | 3 | 7/10 | DP theo số dư, cần nhận ra quy tắc nối số; khó hơn số điểm phản ánh |
| 5 ALKANE | 3 | 9/10 | Đếm cây không nhãn bậc ≤4; lý thuyết tổ hợp đồ thị khá sâu |

**Đánh giá tổng thể chủ quan: 7,5–8/10 về độ khó để giải trọn vẹn trong 180 phút** nếu học sinh chưa gặp trước các phép đếm cây không nhãn. Độ khó bài 5 vượt xa các bài đầu. Một học sinh nắm tốt thuật toán phổ thông có thể xử lý 4 bài đầu, nhưng để tự xây dựng bài 5 tổng quát là thử thách rất lớn.

## Điểm mạnh

- Phạm vi kỹ năng phong phú, có câu cơ bản giúp phân hóa tương đối rõ.
- Ràng buộc chia nhóm test khuyến khích lời giải từng phần.
- Bài 3 có cách rút gọn đẹp từ mô phỏng va chạm sang toán học modulo.
- Bài 4 có một trạng thái DP ngắn gọn mà mạnh (`11` phần dư), là dạng bài giỏi kiểm tra khả năng biến đổi vấn đề.
- Bài 5 có liên hệ hấp dẫn giữa hóa hữu cơ và đồ thị, có chiều sâu thuật toán.

## Các điểm cần sửa/giải thích trong đề gốc

1. **Tên file Bài 5 không thống nhất:** bảng trang 1 ghi đầu ra `ALKANE.INP`, mô tả chi tiết trang 3 ghi `ALKANE.OUT`. Nên sửa bảng thành `ALKANE.OUT`.
2. **Bài 3, tọa độ hình chữ nhật bị in sai:** trang 2 ghi đỉnh `(n;0)` thay vì `(0;n)`; vì hình chữ nhật có các đỉnh `(0;0), (m;0), (m;n), (0;n)`. Hình minh họa và các ràng buộc về `(x,y)` làm rõ ý định. Đây là lỗi cần đính chính trong đề.
3. **Bài 5, thuật ngữ hóa học:** cần nói rõ *chỉ đếm đồng phân cấu tạo liên kết mạch carbon, không xét đồng phân lập thể* (đề mô hình hóa bằng cây không hướng không nhãn nên suy ra được, nhưng nói thẳng tốt hơn).
4. **Phân phối điểm và mức khó:** hai bài 1+2 chiếm tới 10/20 điểm nhưng cơ bản hơn nhiều so với bài 4+5 chỉ 6/20 điểm. Nếu mục tiêu là chọn đội tuyển mạnh, cần cân nhắc độ phân hóa ở tốp trên.
5. **Bài 3, khi chạm góc:** diễn đạt hiện tại rằng vận tốc đổi hướng ngược lại là phù hợp với phản xạ lý tưởng, nhưng có thể ghi rõ đảo dấu cả hai thành phần vận tốc ở góc để tránh tranh cãi.
6. **Bài 2, không có lỗi ràng buộc về bộ ba:** trang 2 nói rõ độ dài xâu chia hết cho 3. Đây là ràng buộc cần giữ nguyên khi trích đề hoặc tạo bộ test chính thức. Vì độ dài tối đa là 100.000, chiều dài hợp lệ lớn nhất là **99.999**. Bộ kiểm thử hồi quy trước đây dùng 100.000 ký tự (ngoài miền đề) đã được điều chỉnh; xem [kiểm toán PROTEIN](PROTEIN_AUDIT.md).
7. **Bài 2, ranh giới bảng mã sinh học:** đề chỉ liệt kê **24 codon**, còn lại `Unk`; không được áp dụng toàn bộ bảng mã di truyền chuẩn để tự thêm Arg/Ser/Stop ngoài danh sách. Đây là đặc tả bài toán, khác mô hình sinh học đầy đủ và nên được lưu ý rõ khi dạy học.

## Gợi ý điều chỉnh thang điểm (tham khảo, không phải đáp án chính thức)

Có thể cân nhắc `PRIME 3`, `PROTEIN 3`, `BILLARD 4`, `DIVIDE 5`, `ALKANE 5` trên tổng 20 điểm, nếu muốn điểm số phản ánh tương đối độ khó của lời giải đầy đủ. Tuy vậy việc phân bổ thực tế còn phụ thuộc mục tiêu ra đề và tỷ lệ học sinh đạt từng nhóm test.

## Cách ôn luyện từ bộ đề

- Mới học: hoàn thiện PRIME và PROTEIN, kiểm tra ràng buộc nhập/xuất.
- Đã có nền tảng: luyện mẹo tọa độ phản xạ và xử lý số âm với BILLARD.
- Có tư duy DP: tự suy ra công thức modulo của phép ghép số và tối ưu DIVIDE xuống `11` trạng thái.
- Đội tuyển chuyên sâu: tìm hiểu cây không nhãn, đa tập qua hàm sinh/Pólya và định lý dissymmetry; so sánh đáp án ALKANE với [OEIS A000602](https://oeis.org/A000602).

> Các điểm khó là nhận xét sư phạm có tính đánh giá, không phải số liệu thống kê điểm thi hoặc kết quả chính thức của Sở GD&ĐT Hà Nội.
