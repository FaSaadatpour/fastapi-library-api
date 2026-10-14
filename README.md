# FastAPI Library API

یک سیستم کتابداری ساده ساخته‌شده با **FastAPI**.  
داده‌ها در حافظه (in-memory) نگه‌داری می‌شوند و نیازی به دیتابیس نیست.

---

## ویژگی‌ها

- دریافت لیست تمام کتاب‌ها
- اضافه کردن کتاب جدید
- دریافت اطلاعات یک کتاب خاص
- به‌روزرسانی جزئی اطلاعات کتاب (PATCH)
- حذف کتاب

---

## نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.9 یا بالاتر

### مراحل

```bash
# کلون کردن ریپو
git clone https://github.com/YOUR_USERNAME/fastapi-library-api.git
cd fastapi-library-api

# ساخت محیط مجازی (پیشنهادی)
python -m venv venv
source venv/bin/activate          # در ویندوز: venv\Scripts\activate

# نصب وابستگی‌ها
pip install -r requirements.txt

# اجرای سرور
uvicorn main:app --reload
```

سرور روی آدرس زیر اجرا می‌شود:

```
http://127.0.0.1:8000
```

- مستندات تعاملی Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- مستندات ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

| Method | Endpoint          | توضیح                          |
|--------|-------------------|--------------------------------|
| GET    | `/books`          | دریافت لیست تمام کتاب‌ها      |
| POST   | `/books`          | اضافه کردن کتاب جدید          |
| GET    | `/books/{id}`     | دریافت اطلاعات یک کتاب خاص    |
| PATCH  | `/books/{id}`     | به‌روزرسانی جزئی اطلاعات کتاب |
| DELETE | `/books/{id}`     | حذف یک کتاب                   |

---

## نمونه درخواست‌ها

### اضافه کردن کتاب جدید

```bash
curl -X POST "http://127.0.0.1:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "شاهنامه",
    "author": "فردوسی",
    "year": 1010,
    "isbn": "978-964-00-0000-0"
  }'
```

### دریافت لیست کتاب‌ها

```bash
curl http://127.0.0.1:8000/books
```

### دریافت یک کتاب خاص

```bash
curl http://127.0.0.1:8000/books/1
```

### به‌روزرسانی کتاب

```bash
curl -X PATCH "http://127.0.0.1:8000/books/1" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 1011
  }'
```

### حذف کتاب

```bash
curl -X DELETE http://127.0.0.1:8000/books/1
```

---

## ساختار پروژه

```
fastapi-library-api/
├── main.py              # کد اصلی FastAPI
├── requirements.txt     # وابستگی‌ها
└── README.md            # این فایل
```

---

## مدل داده

هر کتاب دارای فیلدهای زیر است:

| فیلد        | نوع      | اجباری | توضیح                |
|-------------|----------|--------|----------------------|
| `id`        | int      | بله    | شناسه یکتا (خودکار)  |
| `title`     | string   | بله    | عنوان کتاب           |
| `author`    | string   | بله    | نویسنده              |
| `year`      | int      | خیر    | سال انتشار           |
| `isbn`      | string   | خیر    | شابک                 |
| `created_at`| datetime | بله    | زمان ایجاد (خودکار)  |

---

## نکات مهم

- داده‌ها فقط در حافظه سرور نگه‌داری می‌شوند. با ری‌استارت سرور، تمام داده‌ها پاک می‌شوند.
- برای استفاده در محیط واقعی، پیشنهاد می‌شود از دیتابیس (مثل SQLite، PostgreSQL یا MongoDB) استفاده کنید.
- این پروژه برای یادگیری و نمونه اولیه طراحی شده است.

---

## لایسنس

MIT License
