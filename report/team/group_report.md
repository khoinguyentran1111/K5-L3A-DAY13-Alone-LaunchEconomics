# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: Alone
- Lớp: L3A
- Thành viên: Nguyễn Trần Anh Khôi (nhóm 1 người), xem `TEAM.md`

## 2. Mục tiêu và cách tiếp cận

Đánh giá trợ lý hoàn phí của LogiX-VN trên mẫu 1.200 yêu cầu và 1.624 lần chạy (dữ liệu giả lập), rồi đề xuất có nên mở pilot hay không. Mọi số được tính bằng `src/lab13.py`; các số chính được tính lại bằng một script độc lập không dùng pandas.

## 3. Giải pháp

- **A, B** ([bang_chi_phi.md](bang_chi_phi.md)): tính chi phí mỗi việc thành công từ trace, tách theo loại, cộng chi phí cố định, chạy độ nhạy.
- **C** ([bang_loi.md](bang_loi.md)): hai bộ nhãn do AI gắn với sự cho phép của lab coach, đồng thuận 20/20 = 100%; bảng khắc phục đủ 5 loại.
- **D** ([pilot_plan.yaml](pilot_plan.yaml)): chia theo nhân viên 20 + 20, chấp nhận mức chênh 6 điểm, kéo dài bước 50% thành 14 ngày để đủ 299 yêu cầu mỗi người.
- **E** ([chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)): đặc tả chỉ số, 11 event có `trace_id`, 3 rủi ro kinh tế, hồ sơ một trang.

## 4. Kết quả

- Chi phí mỗi việc thành công: **4.472 đ** [simulated], gấp 16,3 lần hoá đơn token và tool chia số yêu cầu.
- Phạm vi noi_dia + hang_nang, đã cộng cố định: **4.599 đ = 0,38×** của 12.000 đ [simulated].
- Con số bất lợi: xem lại 100% tốn **11.743 đ = 0,98×** [simulated]; pilot chỉ có power **0,64** nếu tác động thật là 5 điểm.
- Đề xuất: **Go có điều kiện** cho pilot noi_dia + hang_nang, quyết định ngày 2027-01-12.
- Kết quả hội đồng chấm nhóm Alone: **chưa có**.
- Phiếu nhóm Alone chấm HC2 (đã xác nhận): **25/30, Go có điều kiện**.

## 5. Khó khăn và cách xử lý

- Nhóm chỉ có 1 người nên nhiệm vụ C dùng AI gắn nhãn với sự cho phép của lab coach. Bộ 1 gắn sau khi đã đọc bảng tham khảo; bộ 2 do một agent mới gắn mù, không thấy đáp án hay bộ 1. Hai bộ trùng 20/20, nhưng cả hai cùng là AI nên tỉ lệ có thể cao hơn đồng thuận giữa hai người.
- Đã chạy lại `lab13.py` từ bản clone sạch trên GitHub trong môi trường Python mới và đạt ba phép thử; chưa chạy trên một máy vật lý khác.
- Duyệt chéo thực hiện trên bản clone repo HC2 (commit `82b663c`), chưa có buổi trình bày trực tiếp nên chưa ghi được câu trả lời của HC2. Không sao chép nội dung hay nhãn của HC2 vào bài Alone.
- Một tuần ở bước 50% chỉ được 215 yêu cầu mỗi người, thấp hơn mức 299. Kế hoạch kéo bước này thành 14 ngày (430 yêu cầu mỗi người).
- Chỉ số mở lại có độ trễ 7 ngày, nên luật an toàn dùng cohort đã đủ thời gian theo dõi, kèm một luật tức thời cho lỗi hoàn trùng.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Phút xem lại và làm lại là số giả lập; pilot cần thay bằng phút đo thật từ tuần 1.
- ICC 0,02 là giả định của đề. ICC cao hơn sẽ làm giảm cỡ mẫu hiệu dụng.
- Tỉ lệ sửa + bỏ 21,09% tính trên 128 ca được xem lại, nên còn dao động.

## 8. Tài liệu tham khảo

- Erol và cộng sự, *Cost-of-Pass: An Economic Framework for Evaluating Language Models*, arXiv:2504.13359.
- Google PAIR, *People + AI Guidebook*, chương "Errors + Graceful Failure".
- Tài liệu statsmodels, lớp `NormalIndPower`.
- Đề bài và hướng dẫn Lab 13 trong thư mục `docs/`.
