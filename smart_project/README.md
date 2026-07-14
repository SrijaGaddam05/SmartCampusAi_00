# SmartCampusAI

SmartCampusAI is a production-grade, responsive, and secure AI-powered campus management dashboard application developed using Python and Streamlit. It incorporates advanced styling principles, a modern Glassmorphism layout, role-based page access, a thread-safe JSON file database, and Google Gemini AI assistance.

---

## 🌟 Key Features

1. **Aesthetic UI**: Custom Glassmorphism styles, dark theme setting, linear glowing gradients, and responsive layouts.
2. **Secure Credentials Portal**: Form-based validation and registration with automatic login, password length constraints, duplicate checks, and SHA-256 password hashing.
3. **Dynamic custom sidebar**: Unified navigation using `streamlit-option-menu` with conditional page restrictions depending on user roles (Admin, Faculty, Student).
4. **Interactive Analytics**: Enrollment comparisons and weekly attendance metrics rendered with Plotly, plus downloadable CSV database exports.
5. **Robust Attendance logging**: Multi-student checkbox forms organized by date and department with automatic present/absent stats.
6. **Gemini AI chatbot**: Advanced chat queries powered by `gemini-1.5-flash` with graceful fallback (API Key Not Found warnings) if config keys are missing.
7. **Thread-Safe local DB**: File-backed JSON databases (`users.json`, `students.json`, etc.) wrapped with write locks to guarantee data integrity.

---

## 📁 Folder Structure

```
SmartCampusAI/
├── .streamlit/
│   └── config.toml          # Custom theme and page settings
├── assets/
│   ├── styles.css           # Global glassmorphism stylesheet
│   ├── logo.png             # Programmatic campus logo
│   └── background.jpg       # Gradient background asset
├── database/
│   ├── users.json           # Credentials database
│   ├── students.json        # Student profiles
│   ├── faculty.json         # Faculty registries
│   ├── attendance.json      # Logs of attendance
│   ├── settings.json        # Global options
│   └── activity.json        # Portal activity logs
├── modules/
│   ├── helpers.py           # Reusable UI cards and logging wrappers
│   ├── authentication.py    # Login, registration, and auth gates
│   ├── sidebar.py           # Custom option menu navigation controller
│   ├── dashboard.py         # Metrics panels, quick actions, feed
│   ├── analytics.py         # Visualizations and data downloaders
│   ├── profile.py           # Profile modification details and password reset
│   ├── settings.py          # Customize theme selection and notifications
│   └── chatbot.py           # AI Assistant and Gemini chat loops
├── utils/
│   ├── config.py            # Loads and gets environment variables
│   ├── database.py          # Thread-safe JSON CRUD operations
│   ├── security.py          # Password hashing operations
│   ├── validators.py        # Syntax and database validation
│   ├── image_generator.py   # Pillow static assets script
│   ├── db_seeder.py         # Seed file populator
│   └── verifier.py          # Core system test verifier
├── pages/
│   ├── Home.py              # Main dashboard routing panel
│   ├── Students.py          # Student management portal
│   ├── Faculty.py           # Faculty directory portal
│   ├── Attendance.py        # Attendance log editor
│   ├── Timetable.py         # Agendas weekly scheduler
│   ├── AI_Assistant.py      # Virtual assistant portal
│   ├── Analytics.py         # Comparative metrics portal
│   ├── Profile.py           # Profile updates portal
│   └── Settings.py          # Preferences portal
├── app.py                   # Main gateway page (Login/Register controller)
├── requirements.txt         # Package dependencies mapping
├── .env.example             # Template for API credentials
└── README.md                # Documentation guide
```

---

## 🛠️ Local Setup & Installation

### 1. Clone Project
```bash
git clone <repository-url>
cd SmartCampusAI
```

### 2. Configure Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows PowerShell
.\venv\Scripts\Activate.ps1
# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Populate Static Assets and Seed Database
The project contains automatic seeding tools. Run them once to set up testing accounts:
```bash
python utils/image_generator.py
python utils/db_seeder.py
```

### 4. Set Environment Variables
Copy `.env.example` into a new `.env` file and insert your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 5. Launch the Application
Run the Streamlit server command:
```bash
streamlit run app.py
```

---

## 🔐 Credentials for Testing

Use these pre-seeded logins to check user access levels:

| Account Type | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Faculty | `turing` | `faculty123` |
| Student | `alice` | `student123` |

---

## 🚀 Deployment Instructions

### Streamlit Cloud
1. Push this project code directly to a GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and create a new app.
3. Select your repository, branch, and specify `app.py` as the entry file path.
4. Open the **App Settings** -> **Secrets** panel and insert your environment keys:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy**!
