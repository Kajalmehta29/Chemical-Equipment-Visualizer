# Chemical Equipment Parameter Visualizer

A hybrid Web and Desktop application for visualizing and analyzing chemical equipment data. [cite_start]This project was built as part of an Intern Screening Task[cite: 3].

[cite_start]It consists of a **Django Backend** that processes CSV data, a **React Web Frontend** for browser-based analytics, and a **PyQt5 Desktop Application** for local usage[cite: 13].

## 🚀 Key Features
* [cite_start]**Hybrid Architecture:** Single Django backend serving both Web (React) and Desktop (PyQt5) frontends[cite: 22].
* [cite_start]**Data Analysis:** Parses CSV files to calculate total count, parameter averages, and equipment type distribution[cite: 16].
* [cite_start]**Visualization:** Interactive Pie charts (Web) and Bar charts (Desktop)[cite: 17].
* [cite_start]**History Management:** Stores the last 5 uploads with clickable summaries to reload past analytics[cite: 18].
* [cite_start]**PDF Reporting:** Generates downloadable PDF reports of the analysis[cite: 19].
* [cite_start]**Authentication:** Basic Authentication required for uploading and viewing sensitive data[cite: 19].

## 🛠️ Tech Stack
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python Django + DRF | [cite_start]API, CSV Parsing, PDF Generation [cite: 13] |
| **Web Frontend** | React.js + Chart.js | [cite_start]Responsive Web Dashboard [cite: 13] |
| **Desktop Frontend** | PyQt5 + Matplotlib | [cite_start]Native Desktop Interface [cite: 13] |
| **Data Handling** | Pandas | [cite_start]Data processing & analytics [cite: 13] |
| **Database** | SQLite | [cite_start]Storing upload history [cite: 13] |

---

## 🔑 Login Credentials
To perform uploads or view detailed history, use the following demo credentials:

* **Username:** `admin`
* **Password:** `password123`

*(Note: You must create this superuser during the backend setup if running from scratch.)*

---

## ⚙️ Setup Instructions

### 1. Prerequisites
* Python 3.8 or higher
* Node.js & npm
* Git

### 2. Backend Setup (Django)
The backend must be running for both the Web and Desktop apps to work.

```bash
# 1. Navigate to the backend folder
cd backend

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create the Admin User (for the credentials above)
python manage.py createsuperuser
# Enter username: admin
# Enter password: password123

# 7. Start the Server
python manage.py runserver

## Open new terminal to run Web-frontend

# 1. Navigate to the web folder
cd frontend_web

# 2. Install dependencies
npm install

# 3. Start the application
npm start

## Open new terminal to run Desktop-frontend
# 1. Activate the environment (if not already active)
# Windows:
..\backend\venv\Scripts\activate
# Mac/Linux:
source ../backend/venv/bin/activate

# 2. Run the desktop application
python frontend_desktop/main.py