Freelance Marketplace API (DRF)
Freelancerlar va mijozlar o'rtasida loyihalar va takliflar almashinuvi uchun mo'ljallangan platforma backend API si.

📋 Loyiha haqida
Ushbu loyiha - bu freelance marketplace platformasining backend qismi bo'lib, unda ikki xil rol mavjud:

Client (Mijoz): Loyiha yaratadi, freelancer takliflarini ko'radi va tanlaydi, baho beradi

Freelancer: Loyihalarni ko'radi, taklif yuboradi, tanlangan loyihani bajaradi

Platforma orqali mijozlar o'z loyihalarini joylashtiradi, freelancerlar esa ularga takliflar yuboradi. Mijoz eng yaxshi taklifni tanlab, freelancer bilan shartnoma tuzadi va loyihani boshlaydi.

🛠 Texnologiyalar
Python 3.10+

Django 4.2+

Django REST Framework 3.14+

PostgreSQL (ishlab chiqishda SQLite)

JWT Authentication (djangorestframework-simplejwt)

Swagger (drf-yasg)

Git

📁 Model lar va ularning vazifalari
User (Custom User Model)
Foydalanuvchi ma'lumotlarini saqlaydi. Django'ning standart User modelidan farqli o'laroq, role maydoni qo'shilgan.

role: client yoki freelancer

bio: Foydalanuvchi haqida qisqacha ma'lumot

Project
Mijoz tomonidan joylangan loyihalarni saqlaydi.

status: open, in_progress, completed, cancelled

budget: Loyiha uchun ajratilgan byudjet

deadline: Loyihaning tugash muddati

Bid
Freelancerlar tomonidan loyihalar uchun yuborilgan takliflar.

price: Taklif qilingan narx

message: Taklif haqida qo'shimcha ma'lumot

status: pending, accepted, rejected

Contract
Mijoz freelancer tanlaganidan keyin tuziladigan shartnoma.

agreed_price: Kelishilgan narx

status: active, finished, cancelled

finished_at: Tugash sanasi

Review
Loyiha tugagach, mijoz tomonidan freelancerga beriladigan baho.

rating: 1-5 gacha bo'lgan baho

comment: Izoh

🔐 Authentication
Tizim JWT (JSON Web Token) orqali autentifikatsiya qiladi. Quyidagi endpointlar mavjud:

Endpoint	Method	Tavsif
/api/auth/register/	POST	Yangi foydalanuvchi ro'yxatdan o'tadi
/api/auth/login/	POST	Tizimga kirish va token olish
/api/auth/logout/	POST	Tizimdan chiqish (token blacklist)
🔌 API Endpointlar
📊 Project API
Endpoint	Method	Ruxsat	Tavsif
/api/projects/	GET	Barcha (open)	Barcha open loyihalarni ko'rish
/api/projects/	POST	Client	Yangi loyiha yaratish
/api/projects/{id}/	GET	Barcha	Loyiha detallarini ko'rish
💰 Bid API
Endpoint	Method	Ruxsat	Tavsif
/api/projects/{project_id}/bids/	POST	Freelancer	Loyihaga taklif yuborish
/api/projects/{project_id}/bids/	GET	Client	Loyihaga kelgan takliflarni ko'rish
/api/bids/{id}/accept/	POST	Client	Taklifni qabul qilish
📝 Contract API
Endpoint	Method	Ruxsat	Tavsif
/api/contracts/	GET	Client/Freelancer	O'z shartnomalarini ko'rish
/api/contracts/{id}/	GET	Client/Freelancer	Shartnoma detallari
/api/contracts/{id}/complete/	POST	Client	Shartnomani tugatish
⭐ Review API
Endpoint	Method	Ruxsat	Tavsif
/api/contracts/{contract_id}/reviews/	POST	Client	Baho yozish
/api/reviews/	GET	Barcha	Barcha baholarni ko'rish
📚 Swagger Dokumentatsiya
API ni sinab ko'rish va hujjatlashtirish uchun Swagger interfeysi mavjud:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

📮 Postman Collection
API ni test qilish uchun Postman collection tayyorlangan:

📎 Postman Collection: Freelance Marketplace API

Collection ichida barcha endpointlar va ularni test qilish uchun misollar mavjud.

🧪 Test foydalanuvchilar
Tizimni tekshirish uchun quyidagi test foydalanuvchilar yaratilgan:

Client
Username: client1

Password: client123

Freelancer
Username: freelancer1

Password: freelancer123

⚙️ O'rnatish va ishga tushirish
1. Repositoryni clone qilish
bash
git clone https://github.com/justazic/freelancer_marketplace_drf.git
cd freelancer_marketplace_drf
2. Virtual environment yaratish
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
3. Kerakli kutubxonalarni o'rnatish
bash
pip install -r requirements.txt

4. Ma'lumotlar bazasini yaratish va migratsiya qilish
bash
python manage.py makemigrations
python manage.py migrate


7. Serverni ishga tushirish
bash
python manage.py runserver
8. Admin panelga kirish (ixtiyoriy)
bash
python manage.py createsuperuser
So'ngra http://localhost:8000/admin/ orqali admin panelga kiring.

🔒 Permissionlar
Tizimda quyidagi permissionlar mavjud:

Client uchun
✅ Loyiha yaratish

✅ O'z loyihalariga kelgan takliflarni ko'rish

✅ Taklifni qabul qilish

✅ Shartnomani tugatish

✅ Baho yozish

Freelancer uchun
✅ Open loyihalarni ko'rish

✅ Loyihalarga taklif yuborish (bitta loyihaga faqat bitta taklif)

✅ O'z shartnomalarini ko'rish

Barcha foydalanuvchilar uchun
✅ Ro'yxatdan o'tish va tizimga kirish

✅ O'z profilingizni ko'rish

🔍 Filter va Search imkoniyatlari
Project list API da quyidagi imkoniyatlar mavjud:

Search: ?search=python - Loyiha nomi bo'yicha qidirish

Budget filter: ?min_budget=100&max_budget=1000 - Byudjet oralig'i bo'yicha filtr

Pagination: ?page=2&page_size=10 - Sahifalash

🌐 GitHub Repository
Loyiha ikki xil implementatsiyada mavjud:

DRF (API) versiyasi: freelancer_marketplace_drf

Django MVT (Template) versiyasi: freelancer_marketplace_django (alohida repository)

📝 Xulosa
Ushbu loyiha orqali quyidagi bilimlar tekshirilgan:

✅ Django ORM va modellar

✅ Django REST Framework

✅ JWT Authentication

✅ Permissionlar va biznes logika

✅ Relationlar bilan ishlash

✅ API dizayn

✅ Swagger dokumentatsiya

✅ Postman collection

Loyiha to'liq funksional bo'lib, real freelance marketplace platformasining backend qismini taqdim etadi.

Muallif: justazic
Repository: https://github.com/justazic/freelancer_marketplace_drf.git
Postman Collection: https://documenter.getpostman.com/view/51312918/2sBXihoXUF