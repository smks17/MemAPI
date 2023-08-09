# MemAPI

A simple API application to get information system memory usage that is recorded at any specific period.

## Usage

Fist, init the Python environment:

```console
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
```

Then set your secret key (and sql url if it's needed) in `app/config.py`.

Then run the API server:

```console
    uvicorn app.main:app --host <Your-IP> --port <Your-Port> --reload
```

## Test
To run the test in the python environment use ```pytest``` command.

## API
- /users/register

    Signing up and creating a new user.

- /users/token

    Logging up and creating a new token to work with the API.

- /users/me

    Getting a token and return user of token.

- memory/info

    reading the last n memory information from database.

For more information see `/docs`

# فارسی
این ریپو یک API اپلیکیشن ساده است برای گرفتن  اطلاعات فظای حافظه که در دیتابیس که در هر دوره زمانی خاص ذخیره می شود.

## استفاده

ابتدا محیط کاری خود را برای اجرای برنامه آماده می کنیم:

```console
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
```

سپس سرور را اجرا می کنیم:

```console
    uvicorn app.main:app --reload
```

## Test
برای تست کردن برنامه هم می توانید از کامند ```pytest``` استفاده کنید.

## API
- /users/register:

    برای ساخت یک اکانت جدید (موقت) است. وروردی اش به صورت پارامتر فرستاده می شود.

- /users/token

    برای ورود با اکانت و گرفتن توکن است. ورودی به صورت body فرستاده می شود

- /users/me

    برای چک کردن توکن است. ورودی به صورت security key فرستاده می شود

- memory/info
    برای گرفتن اطلاعات مموری است.

برای اطلاعات بیشتر به `docs/` مراجعه کنید.