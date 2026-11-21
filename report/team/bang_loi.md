# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

> **Trạng thái: đủ hai bộ nhãn, đồng thuận 20/20 = 100%.** Nhóm có 1 thành viên; lab coach cho phép dùng AI gắn nhãn. Bộ 1 do Claude Code gắn sau khi đã đọc bảng tham khảo. Bộ 2 do một agent Claude mới gắn, chỉ nhận đề 20 ca và định nghĩa 5 loại, không dùng công cụ nào nên không thấy đáp án hay bộ 1. Vì cả hai đều là AI cùng họ mô hình, tỉ lệ này có thể cao hơn đồng thuận giữa hai người.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Claude Code (đã đọc bảng tham khảo) · Người gắn nhãn 2: agent Claude mới, gắn mù (0 lần dùng công cụ). Nguyễn Trần Anh Khôi chịu trách nhiệm cho kết quả.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Do người dùng | Có | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Hệ thống | Có | Hệ thống |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 20 / 20 = 100%

Phân bố nhãn: Do người dùng 4 · Hệ thống 5 · Ngữ cảnh 4 · Giới hạn hệ thống 4 · Ngầm 3.

## Quy tắc phân biệt cho các ca không trùng

Hai bộ nhãn trùng cả 20 ca nên không có ca phải thống nhất. Quy tắc cho các ca dễ lẫn:

- **Ca 6, 9 là do người dùng:** gốc lỗi là khách chọn sai mục hoặc nhập sai mã; việc trợ lý thiếu gợi ý chỉ là chỗ cần cải thiện.
- **Ca 8, 15 là hệ thống, không phải ngầm:** sai đã lộ ra qua trích dẫn nhìn thấy được hoặc nhân viên bắt được.
- **Ca 12 là ngầm:** kết quả đúng nhưng chi phí gấp 3 lần suốt 3 tuần mà không ai nhận ra.
- **Ca 13 là giới hạn hệ thống:** yêu cầu nằm ngoài phạm vi, dù trợ lý xử lý giới hạn đó chưa tốt.
- **Ca 18 là ngữ cảnh:** số tiền đúng chính sách, chỉ giả định khách hiểu cách tính là không khớp.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed` theo `trace_id`; cảnh báo khi quá 2% số yêu cầu/ngày | Nhận diện mã sàn TMĐT và tra sang mã vận đơn; không tra được thì hướng dẫn kèm ảnh | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tin "đã hoàn" không có `refund_ledger_write` ok cùng `trace_id`; ngưỡng 0 ca | Chỉ báo "đã hoàn" khi sổ cái trả ok; lỗi 503 sau 3 lần thì báo "đang xử lý" và chuyển nhân viên | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Tỉ lệ `ticket_reopened` lý do số tiền mà kiểm tra thấy đúng, theo tuần; cảnh báo khi quá 1% số yêu cầu | Mẫu tin nhắn luôn ghi cách tính: 30.000 đ × 50% = 15.000 đ | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Event `handoff_to_staff` với `reason = thieu_du_lieu`, theo loại yêu cầu, báo cáo hằng tuần | Giữ cách chuyển kèm tóm tắt; đưa quoc_te ra khỏi pilot (1,88× [simulated]) | PM trợ lý hoàn phí |
| 17 | Ngầm | `audit_sample_checked`: kiểm tra mẫu 100 đơn/tuần so với bảng giá hiện hành; ngưỡng 1% đơn lệch | Xoá bộ nhớ đệm khi có bảng giá mới, ghi phiên bản bảng giá vào trace | Kế toán trưởng |
