# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | **82,83%** (994/1.200); phạm vi pilot 92,26% (906/982) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | **27,12%** (48/177); phạm vi pilot 21,09% (27/128) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | **4,25%** (51/1.200); phạm vi pilot 3,97% (39/982) |
| Dùng | Nhóm tự đề xuất: % yêu cầu của nhóm trợ lý được mở bằng trợ lý | Số `request_id` có `agent_suggestion_shown`, chia số `refund_request_created` của `arm = tro_ly` | Không cần tính |
| An toàn | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần | Số đơn có `so_tien_da_hoan` khác `so_tien_dung`, chia số đơn trong `audit_sample_checked` | Không cần tính |

Chỉ số chính trong đợt chạy thử là 82,83%. Đợt chạy thử không có nhóm đối chứng nên con số này không cho biết tác động của trợ lý so với mức 0,70.

## Danh sách event

Mỗi event có `trace_id` để nối với trace của agent.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | request_id, loai, so_tien, arm, trace_id | Khi khách gửi |
| `input_validation_failed` | Agent | request_id, truong_loi, trace_id | Khi đầu vào không hợp lệ |
| `agent_run_completed` | Agent | attempt, tokens_in, tokens_out, tool_calls, status, trace_id | Sau mỗi lần chạy, kể cả lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | request_id, staff_id, so_tien_de_xuat, trace_id | Khi gợi ý hiện ra |
| `staff_review_decision` | Nhân viên | quyet_dinh (giu/sua/bo), phut_xem_lai đo thật, trace_id | Khi bấm gửi, sửa hoặc bỏ |
| `staff_rework_completed` | Nhân viên | phut_lam_lai đo thật, ly_do, trace_id | Khi làm lại xong |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, so_tien, ket_qua, trace_id | Khi ghi sổ |
| `handoff_to_staff` | Agent | reason, tom_tat, trace_id | Khi chuyển nhân viên |
| `ticket_closed` | Hệ thống ticket | request_id, closed_at, trace_id | Khi đóng |
| `ticket_reopened` | Khách | request_id, reopened_at, reason, trace_id | Khi mở lại |
| `audit_sample_checked` | Kế toán | so_tien_da_hoan, so_tien_dung, phien_ban_bang_gia, trace_id | Hằng tuần |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, event dùng để tính:

- Chính: `refund_request_created`, `ticket_closed`, `ticket_reopened`.
- Bỏ qua gợi ý: `staff_review_decision`.
- Lỗi lọt đến khách: `refund_request_created`, `ticket_reopened`.
- % yêu cầu mở bằng trợ lý: `refund_request_created`, `agent_suggestion_shown`.
- % đơn hoàn sai tiền: `audit_sample_checked`.
- Chi phí mỗi việc thành công: `agent_run_completed`, `staff_review_decision`, `staff_rework_completed`, `ticket_closed`.

## E2 · Rủi ro kinh tế

Số lấy từ `bang_chi_phi.md`, đều là **simulated**.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | +51,8%, lên 6.787 đ [simulated] | Tỉ lệ làm lại theo tuần > 7% (đợt chạy thử: 4,89% trong phạm vi) | Thu hẹp về noi_dia, rà 20 trace làm lại | PM trợ lý hoàn phí |
| Phải giữ xem lại 100% | 11.743 đ = 0,98×; 12.415 đ = 1,03× nếu làm lại 15,3 phút [simulated] | Sửa + bỏ ≥ 15% (đợt chạy thử: 21,09%); % xem lại > 64% từ tuần 3 | Chỉ giảm xem lại khi đạt ngưỡng; không đạt thì áp dụng luật dừng chi phí | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Cố định +1.185 đ/việc ở 45.000 yêu cầu/tháng, +2.370 đ/việc ở một nửa, +11.852 đ/việc ở 10% [simulated] | Số việc thành công theo tuần < 50% kế hoạch | Không mở rộng pilot, xem lại hợp đồng chi phí cố định | PM trợ lý hoàn phí |
