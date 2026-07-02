from fastapi import FastAPI, HTTPException, Path, Request, status
from fastapi.exceptions import RequestValidationError
from datetime import datetime

app = FastAPI()

orders_db = [
    {"id": 1, "code": "SP001", "status": "PENDING"},
    {"id": 2, "code": "SP002", "status": "DELIVERED"}
]

def send_response(status_code: int, message: str, path: str, data=None, error=None):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "path": path
    }

@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return send_response(422, "Dữ liệu nhập vào sai định dạng.", request.url.path, error=exc.errors())

@app.exception_handler(HTTPException)
async def http_error(request: Request, exc: HTTPException):
    return send_response(exc.status_code, exc.detail, request.url.path, error="HTTP Exception")

@app.exception_handler(Exception)
async def system_error(request: Request, exc: Exception):
    return send_response(500, "Hệ thống đang gặp sự cố. Thử lại sau!", request.url.path, error="Internal Server Error")


@app.delete("/orders/{order_id}")
def cancel_order(request: Request, order_id: int = Path(..., gt=0)):
    
    target_order = None
    for order in orders_db:
        if order["id"] == order_id:
            target_order = order
            break

    if target_order is None:
        raise HTTPException(status_code=404, detail="Đơn hàng không tồn tại.")

    if target_order["status"] == "DELIVERED":
        raise HTTPException(status_code=400, detail="Đơn hàng đã giao, không thể hủy!")

    if target_order["status"] == "PENDING":
        target_order["status"] = "CANCELLED"
        return send_response(200, "Hủy đơn hàng thành công.", request.url.path, data=target_order)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)