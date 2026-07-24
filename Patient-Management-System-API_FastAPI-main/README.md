# 🏥 Patient Management System

A full-stack Patient Management System built with **FastAPI** (backend) and **Streamlit** (frontend). It allows you to add, view, edit, delete, and sort patient records with automatic BMI and health verdict calculation.

---

## 🖥️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Pydantic |
| Frontend | Streamlit |
| Database | JSON File (`patients.json`) |
| Language | Python 3.8+ |

---

## 📁 Project Structure

```
my_project/
│
├── main.py            ← FastAPI backend (REST API)
├── app.py             ← Streamlit frontend (UI)
├── patients.json      ← Local JSON database
└── README.md          ← Project documentation
```

---

## ⚙️ Installation & Setup

### Step 1 — Clone or Download the Project
Place all files in the same folder.

### Step 2 — Create the Database File
Create a file named `patients.json` in the project folder with this content:
```json
{}
```

### Step 3 — Install Required Libraries
Open a terminal in the project folder and run:
```bash
pip install fastapi uvicorn streamlit requests
```

---

## ▶️ Running the Project

You need **two terminals open at the same time**.

### Terminal 1 — Start FastAPI Backend
```bash
uvicorn main:app --reload
```
✅ Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Terminal 2 — Start Streamlit Frontend
```bash
streamlit run app.py
```
✅ Expected output:
```
Local URL:  http://localhost:8501
Network URL: http://192.168.x.x:8501
```
The browser will open automatically.

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI Backend | http://127.0.0.1:8000 |
| API Docs (Swagger) | http://127.0.0.1:8000/docs |
| API Docs (Redoc) | http://127.0.0.1:8000/redoc |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home message |
| GET | `/about` | About the API |
| GET | `/view` | Get all patients |
| GET | `/patient/{patient_id}` | Get a single patient |
| GET | `/sort?sort_by=bmi&order=asc` | Sort patients |
| POST | `/create` | Add a new patient |
| PUT | `/edit/{patient_id}` | Update a patient |
| DELETE | `/delete/{patient_id}` | Delete a patient |

---

## 📋 Features

- ✅ View all patients in a card-based dashboard
- ✅ Search patient by ID
- ✅ Add new patient with full validation
- ✅ Edit existing patient details
- ✅ Delete a patient record
- ✅ Sort patients by height, weight, or BMI
- ✅ Auto-calculated BMI and health verdict
- ✅ Summary metrics (total patients, average BMI, etc.)

---

## 🧮 BMI & Verdict Logic

| BMI Range | Verdict |
|-----------|---------|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal |
| 25.0 – 29.9 | Overweight |
| 30 and above | Obese |

> BMI Formula: `weight (kg) / height (m)²`

---

## 📝 Sample Patient Data

You can add this to `patients.json` to test the app quickly:

```json
{
    "P001": {
        "name": "John Doe",
        "city": "Mumbai",
        "age": 30,
        "gender": "male",
        "height": 1.75,
        "weight": 70.0,
        "bmi": 22.86,
        "verdict": "Normal"
    },
    "P002": {
        "name": "Jane Smith",
        "city": "Delhi",
        "age": 25,
        "gender": "female",
        "height": 1.60,
        "weight": 85.0,
        "bmi": 33.2,
        "verdict": "Obese"
    }
}
```

---

## 🐛 Known Bug Fixes Required in `main.py`

Before running, fix these two bugs in your `main.py`:

**Bug 1 — Wrong verdict label:**
```python
# ❌ Wrong
elif self.bmi < 30:
    return 'Normal'

# ✅ Fix
elif self.bmi < 30:
    return 'Overweight'
```

**Bug 2 — Wrong exclude syntax:**
```python
# ❌ Wrong
existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

# ✅ Fix
existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})
```

---

## ⚠️ Important Notes

- Both terminals must stay **open and running** at the same time
- `patients.json` must exist **before** starting FastAPI
- All files must be in the **same folder**
- FastAPI runs on port **8000**, Streamlit runs on port **8501**

---

## 👨‍💻 Author

Built with FastAPI + Streamlit | Python Full Stack Project
