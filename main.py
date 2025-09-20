from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict
import smtplib
import random
from email.mime.text import MIMEText
import hashlib
import shutil
import os

app = FastAPI()

# Statik fayllar uchun papkalarni tayyorlash
if not os.path.exists("avatars"):
    os.makedirs("avatars")
if not os.path.exists("videos"):
    os.makedirs("videos")

# Statik fayllarni ulash
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Email sozlamalar
SENDER_EMAIL = "muham20021202@gmail.com"
APP_PASSWORD = "kxnx qmzg qtbc guhm"
ADMIN_EMAIL = "muham20021202@gmail.com"

# Modellar
class Lesson(BaseModel):
    id: int
    category: str
    title: str
    description: str
    subtitle: str
    answer: str
    video_url: str

class RegisterInput(BaseModel):
    name: str
    email: str
    password: str

class VerifyInput(BaseModel):
    code: str

class Comment(BaseModel):
    name: Optional[str] = None
    email: str
    message: str

class UserOutput(BaseModel):
    email: str
    image: str
    name: Optional[str] = None
lessons = [
    Lesson(
        id=1,
        category={"uz": "Word darslari", "rus": "Уроки Word", "eng": "Word lessons"},
        title={"uz": "Word kirish", "rus": "Введение в Word", "eng": "Introduction to Word"},
        description={
            "uz": "Word dasturiga kirish va Glavnaya bo'limi",
            "rus": "Введение в программу Word и раздел Главная",
            "eng": "Introduction to Word program and Home section"
        },
        subtitle={
            "uz": "Word nima uchun kerak?",
            "rus": "Зачем нужен Word?",
            "eng": "Why do we need Word?"
        },
        answer={
            "uz": "Microsoft Word matn yaratish, tahrirlash va formatlash uchun kerak",
            "rus": "Microsoft Word нужен для создания, редактирования и форматирования текста",
            "eng": "Microsoft Word is used for creating, editing, and formatting text"
        },
        video_url="https://player.vimeo.com/video/1118563974"
    ),
    Lesson(
        id=2,
        category={"uz": "Word darslari", "rus": "Уроки Word", "eng": "Word lessons"},
        title={"uz": "Vstavka bo'limi bilan tanishish", "rus": "Знакомство с разделом Вставка", "eng": "Introduction to Insert section"},
        description={
            "uz": "Vstavka bo'limi haqida.",
            "rus": "О разделе Вставка.",
            "eng": "About the Insert section."
        },
        subtitle={
            "uz": "Vstavka bo'limi bizga nima uchun kerak?",
            "rus": "Зачем нам раздел Вставка?",
            "eng": "Why do we need the Insert section?"
        },
        answer={
            "uz": "Hujjatni boyitish, rasm, jadval va boshqa elementlarni qo‘shish uchun kerak.",
            "rus": "Чтобы обогатить документ: добавить изображения, таблицы и другие элементы.",
            "eng": "To enrich the document: add images, tables, and other elements."
        },
        video_url="https://player.vimeo.com/video/1118566162"
    ),
    Lesson(
        id=3,
        category={"uz": "Word darslari", "rus": "Уроки Word", "eng": "Word lessons"},
        title={"uz": "Dizayn Maket vid bo'limlari", "rus": "Разделы Дизайн, Макет и Вид", "eng": "Design, Layout, and View sections"},
        description={
            "uz": "Dizayn va Maket vid bo'limlari haqida",
            "rus": "О разделах Дизайн, Макет и Вид",
            "eng": "About Design, Layout, and View sections"
        },
        subtitle={
            "uz": "Dizayn va Maket va vid bo'limida nimalar o'rganamiz?",
            "rus": "Что изучаем в разделах Дизайн, Макет и Вид?",
            "eng": "What do we learn in Design, Layout, and View sections?"
        },
        answer={
            "uz": "Dizayn bo‘limida interfeys, shrift, tugmalar... Maket bo‘limida esa joylashuv va o‘lchamlar sozlanadi",
            "rus": "В Дизайне — интерфейс, шрифты, кнопки... В Макете — расположение и размеры",
            "eng": "In Design — interface, fonts, buttons... In Layout — positioning and sizes"
        },
        video_url="https://player.vimeo.com/video/1118567468"
    ),
    Lesson(
        id=4,
        category={"uz": "Excel darslari", "rus": "Уроки Excel", "eng": "Excel lessons"},
        title={"uz": "Excelga kirish", "rus": "Введение в Excel", "eng": "Introduction to Excel"},
        description={
            "uz": "Excel dasturiga kirish.",
            "rus": "Введение в программу Excel.",
            "eng": "Introduction to Excel program."
        },
        subtitle={
            "uz": "Excel nima uchun kerak?",
            "rus": "Зачем нужен Excel?",
            "eng": "Why do we need Excel?"
        },
        answer={
            "uz": "Excel maʼlumotlarni tartiblash, hisoblash va tahlil qilish uchun kerak.",
            "rus": "Excel нужен для упорядочивания, вычисления и анализа данных.",
            "eng": "Excel is used for organizing, calculating, and analyzing data."
        },
        video_url="https://onlinetech.onrender.com/videos/excal-1.mp4"
    ),
     Lesson(
        id=5,
        category={"uz": "Excel darslari", "rus": "Уроки Excel", "eng": "Excel lessons"},
        title={"uz": "Excelda summ min max funksiyalari", "rus": "Функции SUMM, MIN, MAX в Excel", "eng": "SUM, MIN, MAX functions in Excel"},
        description={
            "uz": "Excelda summ min max funksiyalari",
            "rus": "Функции SUMM, MIN, MAX в Excel",
            "eng": "SUM, MIN, MAX functions in Excel"
        },
        subtitle={
            "uz": "Excelda summ min max funksiyalari nima uchun kerak?",
            "rus": "Для чего нужны функции СУММ, МИН и МАКС в Excel?",
            "eng": "What are the SUM, MIN, and MAX functions in Excel used for?"
        },
        answer={
            "uz": "Excel da Summ->sonlarni bir-biriga qo'shishlik uchun,Min->Sonlarining ichidan eng pastini olib beradi,Max->Sonlarning ichidan eng balandini olib beradi",
            "rus": "СУММ → используется для сложения чисел.МИН → возвращает наименьшее число из диапазона.МАКС → возвращает наибольшее число из диапазона.",
            "eng": "SUM → is used to add numbers together.MIN → returns the smallest number from a range.MAX → returns the largest number from a range."
        },
        video_url="https://vimeo.com/manage/videos/1120360780"
    ),
      Lesson(
        id=6,
        category={"uz": "Excel darslari", "rus": "Уроки Excel", "eng": "Excel lessons"},
        title={"uz": "Excelda summ min max funksiyalari", "rus": "Функции SUMM, MIN, MAX в Excel", "eng": "SUM, MIN, MAX functions in Excel"},
        description={
            "uz": "Excelda Agar funksiyasi",
            "rus": "функция ЕСЛИ в Excel",
            "eng": "the IF function in Excel."
        },
        subtitle={
            "uz": "Excelda Agar funksiyasi nima uchun kerak?",
            "rus": "Для чего нужна функция ЕСЛИ в Excel?",
            "eng": "What is the IF function in Excel used for?"
        },
        answer={
            "uz": "Excalda Agar funksiyasi shart berishlik uchun ishlatiladi",
            "rus": "Функция ЕСЛИ в Excel используется для задания условия.",
            "eng": "The IF function in Excel is used for giving conditions."
        },
        video_url="https://vimeo.com/manage/videos/1120362544"
    ),
]


TEMP_USERS: Dict[str, dict] = {}
USERS = []
comments: Dict[int, List[Comment]] = {}

# Darslar
@app.get("/lessons", response_model=List[Lesson])
def get_lessons():
    return lessons

@app.get("/lessons/{lesson_id}", response_model=Lesson)
def get_lesson_by_id(lesson_id: int):
    for lesson in lessons:
        if lesson.id == lesson_id:
            return lesson
    raise HTTPException(status_code=404, detail="Bunday IDdagi dars topilmadi")

# Ro'yxatdan o'tish
@app.post("/register")
def register(user: RegisterInput):
    if user.email in TEMP_USERS:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan.")
    verify_code = str(random.randint(100000, 999999))
    TEMP_USERS[user.email] = {
        "password": user.password,
        "code": verify_code,
        "name": user.name
    }
    msg = MIMEText(f"Sizning tasdiqlash kodingiz: {verify_code}")
    msg["Subject"] = "Tasdiqlash kodi"
    msg["From"] = SENDER_EMAIL
    msg["To"] = user.email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
    return {"message": "Kod yuborildi"}

# Email orqali tasdiqlash
@app.post("/verify")
def verify_code(data: VerifyInput):
    for email, user_data in TEMP_USERS.items():
        if user_data["code"] == data.code:
            email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
            image_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon"
            USERS.append({
                "email": email,
                "password": user_data["password"],
                "image": image_url,
                "name": user_data.get("name")
            })
            del TEMP_USERS[email]
            return {"message": "Tasdiqlandi va ro'yxatdan o'tdingiz", "image": image_url}
    raise HTTPException(status_code=400, detail="Kod noto‘g‘ri")

# Avatar yuklash
# Avatar yuklash
@app.post("/upload-avatar")
async def upload_avatar(email: str = Form(...), image: UploadFile = File(...)):
    filename = f"avatars/{email.replace('@', '_')}.png"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    file_url = f"https://backendthree-sc1q.onrender.com/avatars/{email.replace('@', '_')}.png"
    return {"message": "Rasm saqlandi", "image": file_url}


# Komment qo'shish
@app.post("/lessons/{lesson_id}/comments")
def add_comment(lesson_id: int, comment: Comment):
    lesson_ids = [lesson.id for lesson in lessons]
    if lesson_id not in lesson_ids:
        raise HTTPException(status_code=404, detail="Bunday IDdagi dars topilmadi")
    if lesson_id not in comments:
        comments[lesson_id] = []
    comments[lesson_id].append(comment)
    comment_name = comment.name if comment.name else "Ism ko'rsatilmagan"
    admin_body = f"""🔔 Yangi izoh keldi!

🆔 Dars ID: {lesson_id}
👤 Ism: {comment_name}
📧 Email: {comment.email}

💬 Xabar:
{comment.message}

➡️ Ushbu emailga "Reply" qilsangiz, foydalanuvchiga javob yuboriladi.
"""
    user_body = f"""Salom {comment_name},

Izohingiz uchun rahmat! Tez orada sizga javob beramiz.

Hurmat bilan,  
Bilim ol jamoasi
"""
    admin_msg = MIMEText(admin_body)
    admin_msg["Subject"] = f"Dars {lesson_id} uchun yangi izoh"
    admin_msg["From"] = SENDER_EMAIL
    admin_msg["To"] = ADMIN_EMAIL
    admin_msg["Reply-To"] = comment.email
    user_msg = MIMEText(user_body)
    user_msg["Subject"] = "Izohingiz qabul qilindi"
    user_msg["From"] = SENDER_EMAIL
    user_msg["To"] = comment.email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(admin_msg)
        server.send_message(user_msg)
    return {"message": "Izoh saqlandi va email yuborildi"}

# Ro'yxatdan o'tgan foydalanuvchilarni olish
@app.get("/users", response_model=List[UserOutput])
def get_users():
    return USERS
