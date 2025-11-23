# Chemical Equipment Parameter Visualizer

A hybrid Web and Desktop application for visualizing and analyzing chemical equipment data. This project was built as part of an Intern Screening Task.

It consists of a **Django Backend** that processes CSV data, a **React Web Frontend** for browser-based analytics, and a **PyQt5 Desktop Application** for local usage.

## 🚀 Key Features
* **Hybrid Architecture:** Single Django backend serving both Web (React) and Desktop (PyQt5) frontends.
* **Data Analysis:** Parses CSV files to calculate total count, parameter averages, and equipment type distribution.
* **Visualization:** Interactive Pie charts (Web) and Bar charts (Desktop).
* **History Management:** Stores the last 5 uploads with clickable summaries to reload past analytics.
* **PDF Reporting:** Generates downloadable PDF reports of the analysis.
* **Authentication:** Basic Authentication required for uploading and viewing sensitive data.

## 🛠️ Tech Stack
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python Django + DRF | API, CSV Parsing, PDF Generation  |
| **Web Frontend** | React.js + Chart.js | Responsive Web Dashboard  |
| **Desktop Frontend** | PyQt5 + Matplotlib | Native Desktop Interface  |
| **Data Handling** | Pandas | Data processing & analytics  |
| **Database** | SQLite | Storing upload history  |

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