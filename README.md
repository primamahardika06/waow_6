# Flask CRUD Application

Aplikasi web CRUD (Create, Read, Update, Delete) sederhana yang dibangun dengan Flask dan MySQL untuk manajemen toko (customers, products, transactions).

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: bcrypt untuk hashing password
- **CORS**: Flask-CORS

## 📋 Fitur

- ✅ Autentikasi User (Login/Register)
- ✅ Manajemen Customers
- ✅ Manajemen Products  
- ✅ Manajemen Transactions
- ✅ Sales Reports
- ✅ Session Management
- ✅ RESTful API Endpoints

## 🚀 Instalasi dan Setup

### Prerequisites

Pastikan Anda telah menginstall:
- Python 3.7+
- MySQL Server (XAMPP/WAMP/MAMP)
- Git




### 1. Clone Repository

```bash
git clone https://github.com/primamahardika06/waow_6.git
cd repository-name
```

### 2. Setup file .env

```bash
# Untuk Windows
python -m venv venv
venv\Scripts\activate

# Untuk Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
```bash
# Jika file requirements.txt tidak tersedia, install manual:
pip install flask flask-cors pymysql bcrypt
```

### 4. Konfigurasi Database Shop
```bash
# config.py
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''  # Sesuaikan dengan password MySQL Anda
MYSQL_DATABASE = 'shop'
```

### 5. Jalankan program
```bash
python app.py
```


