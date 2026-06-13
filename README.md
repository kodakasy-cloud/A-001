# 🔐 My Flet App

A desktop/mobile application built with **Flet**, focused on **security, organization, and secure data storage**, using local encryption to protect user information.

---

# ✨ Features

* 🔑 Local authentication
* 🛡️ Sensitive data encryption
* 💰 Financial management
* 📅 Event management
* 🔒 Secure vault for storing information
* 💾 Local database storage
* 🔄 Future-ready automatic update system

---

# 📂 Project Structure

```text
my_flet_app/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
└── src/
    ├── main.py
    │
    ├── database/
    │   ├── __init__.py
    │   └── local_db.py
    │
    ├── security/
    │   ├── __init__.py
    │   └── crypto.py
    │
    ├── views/
    │   ├── modules/
    │   │   ├── vault_views.py
    │   │   ├── events_views.py
    │   │   └── finance_views.py
    │   │
    │   ├── __init__.py
    │   ├── login_view.py
    │   └── home_view.py
    │
    └── utils/
        └── updater.py
```

---

# 🏗️ Architecture

## 🔥 main.py

Application entry point.

Responsibilities:

* Initialize Flet
* Configure the main window
* Load startup views
* Manage the application lifecycle

---

## 🗄️ database/

Responsible for local data storage.

### local_db.py

Features:

* Create tables
* Insert records
* Update data
* Delete records
* Query information

Suggested technology:

* SQLite

---

## 🛡️ security/

Handles application security.

### crypto.py

Features:

* Encrypt data before storage
* Decrypt data when loading
* Manage encryption keys

---

## 🖥️ views/

Responsible for the graphical user interface.

### login_view.py

Local authentication screen.

Features:

* User login
* Credential validation
* Access control

### home_view.py

Main dashboard.

Features:

* Module navigation
* Display key information

---

## 📦 modules/

Independent application modules.

### 🔒 vault_views.py

Secure storage system.

Possible features:

* Password management
* Protected notes
* Encrypted documents

### 📅 events_views.py

Event management system.

Possible features:

* Calendar
* Reminders
* Scheduling
* Task tracking

### 💰 finance_views.py

Financial management system.

Possible features:

* Income tracking
* Expense tracking
* Reports and analytics
* Categories and budgeting

---

## 🛠️ utils/

Helper utilities and support tools.

### updater.py

Future update management system.

Possible features:

* Check for new versions
* Download updates
* Automatic update installation

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/my_flet_app.git
```

## 2. Navigate to the project folder

```bash
cd my_flet_app
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Configure the `.env` file

Example:

```env
SECRET_KEY=your_super_secret_key
```

## 7. Run the application

```bash
python src/main.py
```

---

# 🔒 Security

This project follows security best practices:

* Data is encrypted before storage
* Encryption keys are stored in `.env`
* Sensitive files are excluded from Git tracking
* Clear separation between UI, database, and security layers

---

# 📈 Roadmap

* ☁️ Cloud backup support
* 🔐 Two-Factor Authentication (2FA)
* 📊 Advanced analytics dashboard
* 🌙 Light & Dark themes
* 🔄 Automatic updates
* 📱 Android and iOS versions
* 🖥️ Native desktop packaging

---

# 👨‍💻 Technologies

* Python 3.12+
* Flet
* SQLite
* Cryptography
* python-dotenv

---

# 📄 License

This project is intended for educational and personal use.

All rights reserved.
