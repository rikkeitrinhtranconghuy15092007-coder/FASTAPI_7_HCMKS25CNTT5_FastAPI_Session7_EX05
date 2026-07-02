# LUỒNG XỬ LÝ DỮ LIỆU CỦA API HỦY ĐƠN HÀNG

Khi Client (Frontend) gửi một yêu cầu hủy đơn hàng lên API `DELETE /orders/{order_id}`, dữ liệu và các lỗi (nếu có) sẽ đi qua bộ lọc **Global Exception Handler** toàn cục theo sơ đồ luồng dưới đây:

## 1. Sơ đồ tổng quan luồng đi của dữ liệu
Client Request ──> [Bộ lọc FastAPI] ──> [Hàm xử lý logic] ──> [Cơ sở dữ liệu]
                        │                       │
         (Lỗi Nhập liệu) │         (Lỗi Nghiệp vụ) │
                        ▼                       ▼
            ┌───────────────────────────────────────┐
            │     GLOBAL EXCEPTION HANDLER (Bộ lọc) │
            │  (Đóng gói dữ liệu lỗi thành 6 trường)│
            └───────────────────┬───────────────────┘
                                ▼
                        Client Response (JSON)

---

## 2. Các kịch bản xử lý chi tiết (Áp dụng khung 6 trường thống nhất)

### 📌 Kịch bản 1: Hủy đơn hàng thành công (Happy Path)
* **Luồng đi:** Client gửi `order_id = 1` ──> Hệ thống tìm thấy đơn hàng có trạng thái `PENDING` ──> Cập nhật trạng thái thành `CANCELLED` ──> Hàm tiện ích `send_response` đóng gói dữ liệu thành công.
* **Kết quả trả về Frontend:**
```json
{
  "statusCode": 200,
  "message": "Hủy đơn hàng thành công.",
  "data": { "id": 1, "code": "SP001", "status": "CANCELLED" },
  "error": null,
  "timestamp": "2026-07-02T15:00:00Z",
  "path": "/orders/1"
}