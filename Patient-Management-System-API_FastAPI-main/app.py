import streamlit as st
import requests

# ── Config ──────────────────────────────────────────────────────────────────
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Patient Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f2027, #203a43, #2c5364);
    border-right: 1px solid rgba(255,255,255,0.07);
}
[data-testid="stSidebar"] * { color: #e2eaf0 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; }

/* ── Main background ── */
.main { background: #f4f7fb; }

/* ── Page heading ── */
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.1rem;
    color: #1a2a3a;
    margin-bottom: 0.2rem;
}
.page-sub { color: #5f7a8a; font-size: 0.95rem; margin-bottom: 1.5rem; }

/* ── Cards ── */
.patient-card {
    background: #fff;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(30,60,90,0.07);
    border-left: 4px solid #2c7be5;
    transition: box-shadow .2s;
}
.patient-card:hover { box-shadow: 0 6px 24px rgba(44,123,229,0.14); }
.card-name { font-size: 1.15rem; font-weight: 600; color: #1a2a3a; }
.card-id   { font-size: 0.78rem; color: #8fa3b1; margin-bottom: .5rem; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
}
.badge-normal      { background:#d4edda; color:#155724; }
.badge-underweight { background:#fff3cd; color:#856404; }
.badge-overweight  { background:#fde2b5; color:#a85800; }
.badge-obese       { background:#f8d7da; color:#721c24; }

/* ── Metric boxes ── */
.metric-row { display:flex; gap:1rem; margin-bottom:1.2rem; flex-wrap:wrap; }
.metric-box {
    flex:1; min-width:120px;
    background:#fff;
    border-radius:12px;
    padding:1rem 1.2rem;
    box-shadow: 0 1px 8px rgba(30,60,90,0.07);
    text-align:center;
}
.metric-val { font-size:1.8rem; font-weight:700; color:#2c7be5; }
.metric-lbl { font-size:0.78rem; color:#8fa3b1; margin-top:2px; }

/* ── Success / error banners ── */
.stAlert { border-radius: 10px !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def badge(verdict: str) -> str:
    cls = {
        "Normal": "badge-normal",
        "Underweight": "badge-underweight",
        "Overweight": "badge-overweight",
        "Obese": "badge-obese",
    }.get(verdict, "badge-normal")
    return f'<span class="badge {cls}">{verdict}</span>'


def get_patients():
    try:
        r = requests.get(f"{BASE_URL}/view")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Could not connect to API: {e}")
        return {}


# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 Patient MS")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📋 View All Patients", "🔍 Search Patient", "➕ Add Patient",
         "✏️ Edit Patient", "🗑️ Delete Patient", "📊 Sort Patients"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("FastAPI backend on `localhost:8000`")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: VIEW ALL
# ════════════════════════════════════════════════════════════════════════════
if page == "📋 View All Patients":
    st.markdown('<div class="page-title">All Patients</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Complete patient registry</div>', unsafe_allow_html=True)

    data = get_patients()
    if not data:
        st.info("No patients found in the database.")
    else:
        # Summary metrics
        patients = list(data.values())
        total = len(patients)
        avg_bmi = round(sum(p.get("bmi", 0) for p in patients) / total, 1) if total else 0
        verdicts = [p.get("verdict", "") for p in patients]

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">{total}</div><div class="metric-lbl">Total Patients</div></div>
            <div class="metric-box"><div class="metric-val">{avg_bmi}</div><div class="metric-lbl">Avg BMI</div></div>
            <div class="metric-box"><div class="metric-val">{verdicts.count("Normal")}</div><div class="metric-lbl">Normal</div></div>
            <div class="metric-box"><div class="metric-val">{verdicts.count("Obese")}</div><div class="metric-lbl">Obese</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Cards
        cols = st.columns(2)
        for i, (pid, p) in enumerate(data.items()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="patient-card">
                    <div class="card-id">ID: {pid}</div>
                    <div class="card-name">{p.get('name','—')}</div>
                    <div style="color:#5f7a8a;font-size:0.85rem;margin:.3rem 0;">
                        {p.get('gender','').capitalize()} · {p.get('age','')} yrs · {p.get('city','')}
                    </div>
                    <div style="margin-top:.4rem;">
                        <b>BMI:</b> {p.get('bmi','—')} &nbsp;
                        {badge(p.get('verdict',''))}
                    </div>
                    <div style="font-size:0.82rem;color:#8fa3b1;margin-top:.3rem;">
                        Height: {p.get('height','')} m &nbsp;|&nbsp; Weight: {p.get('weight','')} kg
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE: SEARCH
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Search Patient":
    st.markdown('<div class="page-title">Search Patient</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Look up a patient by their ID</div>', unsafe_allow_html=True)

    pid = st.text_input("Patient ID", placeholder="e.g. P001")
    if st.button("Search", use_container_width=True):
        if not pid.strip():
            st.warning("Please enter a Patient ID.")
        else:
            try:
                r = requests.get(f"{BASE_URL}/patient/{pid.strip()}")
                if r.status_code == 200:
                    p = r.json()
                    st.success("Patient found!")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Name", p.get("name", "—"))
                    col1.metric("Age", p.get("age", "—"))
                    col2.metric("City", p.get("city", "—"))
                    col2.metric("Gender", p.get("gender", "—").capitalize())
                    col3.metric("BMI", p.get("bmi", "—"))
                    col3.metric("Verdict", p.get("verdict", "—"))
                    with st.expander("Raw data"):
                        st.json(p)
                elif r.status_code == 404:
                    st.error("Patient not found.")
                else:
                    st.error(f"Error {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: ADD PATIENT
# ════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Patient":
    st.markdown('<div class="page-title">Add New Patient</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Register a new patient in the system</div>', unsafe_allow_html=True)

    with st.form("add_form"):
        c1, c2 = st.columns(2)
        pid    = c1.text_input("Patient ID *", placeholder="P001")
        name   = c2.text_input("Full Name *")
        city   = c1.text_input("City *")
        age    = c2.number_input("Age *", min_value=1, max_value=119, value=25)
        gender = c1.selectbox("Gender *", ["male", "female", "other"])
        height = c2.number_input("Height (m) *", min_value=0.5, max_value=2.5, value=1.70, step=0.01, format="%.2f")
        weight = c1.number_input("Weight (kg) *", min_value=1.0, max_value=300.0, value=65.0, step=0.1)

        submitted = st.form_submit_button("➕ Create Patient", use_container_width=True)

    if submitted:
        if not pid.strip() or not name.strip() or not city.strip():
            st.warning("Please fill in all required fields.")
        else:
            payload = {
                "id": pid.strip(), "name": name.strip(), "city": city.strip(),
                "age": age, "gender": gender, "height": height, "weight": weight,
            }
            try:
                r = requests.post(f"{BASE_URL}/create", json=payload)
                if r.status_code == 201:
                    st.success("✅ Patient created successfully!")
                elif r.status_code == 400:
                    st.error("A patient with this ID already exists.")
                else:
                    st.error(f"Error {r.status_code}: {r.json().get('detail', r.text)}")
            except Exception as e:
                st.error(f"Connection error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: EDIT PATIENT
# ════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Edit Patient":
    st.markdown('<div class="page-title">Edit Patient</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Update existing patient information</div>', unsafe_allow_html=True)

    pid = st.text_input("Patient ID to edit", placeholder="e.g. P001")
    load_btn = st.button("Load Patient")

    if load_btn and pid.strip():
        try:
            r = requests.get(f"{BASE_URL}/patient/{pid.strip()}")
            if r.status_code == 200:
                st.session_state["edit_data"] = r.json()
                st.session_state["edit_id"] = pid.strip()
                st.success("Patient loaded. Edit below.")
            else:
                st.error("Patient not found.")
        except Exception as e:
            st.error(f"Connection error: {e}")

    if "edit_data" in st.session_state:
        p = st.session_state["edit_data"]
        with st.form("edit_form"):
            c1, c2 = st.columns(2)
            name   = c1.text_input("Name",   value=p.get("name", ""))
            city   = c2.text_input("City",   value=p.get("city", ""))
            age    = c1.number_input("Age",   min_value=1, max_value=119, value=int(p.get("age", 25)))
            gender_opts = ["male", "female", "other"]
            gender = c2.selectbox("Gender", gender_opts, index=gender_opts.index(p.get("gender", "male")))
            height = c1.number_input("Height (m)", min_value=0.5, max_value=2.5,
                                     value=float(p.get("height", 1.70)), step=0.01, format="%.2f")
            weight = c2.number_input("Weight (kg)", min_value=1.0, max_value=300.0,
                                     value=float(p.get("weight", 65.0)), step=0.1)
            save = st.form_submit_button("💾 Save Changes", use_container_width=True)

        if save:
            payload = {k: v for k, v in {
                "name": name, "city": city, "age": age,
                "gender": gender, "height": height, "weight": weight,
            }.items() if v}
            try:
                r = requests.put(f"{BASE_URL}/edit/{st.session_state['edit_id']}", json=payload)
                if r.status_code == 200:
                    st.success("✅ Patient updated successfully!")
                    del st.session_state["edit_data"]
                    del st.session_state["edit_id"]
                else:
                    st.error(f"Error: {r.json().get('detail', r.text)}")
            except Exception as e:
                st.error(f"Connection error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: DELETE PATIENT
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗑️ Delete Patient":
    st.markdown('<div class="page-title">Delete Patient</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Permanently remove a patient record</div>', unsafe_allow_html=True)

    pid = st.text_input("Patient ID to delete", placeholder="e.g. P001")
    st.warning("⚠️ This action cannot be undone.")

    if st.button("🗑️ Delete Patient", use_container_width=True):
        if not pid.strip():
            st.warning("Please enter a Patient ID.")
        else:
            try:
                r = requests.delete(f"{BASE_URL}/delete/{pid.strip()}")
                if r.status_code == 200:
                    st.success(f"✅ Patient {pid.strip()} deleted successfully.")
                elif r.status_code == 404:
                    st.error("Patient not found.")
                else:
                    st.error(f"Error {r.status_code}: {r.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE: SORT
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊 Sort Patients":
    st.markdown('<div class="page-title">Sort Patients</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">Sort the patient list by a chosen metric</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    sort_by = c1.selectbox("Sort By", ["height", "weight", "bmi"])
    order   = c2.selectbox("Order", ["asc", "desc"])

    if st.button("Sort", use_container_width=True):
        try:
            r = requests.get(f"{BASE_URL}/sort", params={"sort_by": sort_by, "order": order})
            if r.status_code == 200:
                patients = r.json()
                st.success(f"Showing {len(patients)} patients sorted by **{sort_by}** ({order})")

                # Table view
                rows = []
                for p in patients:
                    rows.append({
                        "Name": p.get("name", ""),
                        "Age": p.get("age", ""),
                        "City": p.get("city", ""),
                        "Gender": p.get("gender", "").capitalize(),
                        "Height (m)": p.get("height", ""),
                        "Weight (kg)": p.get("weight", ""),
                        "BMI": p.get("bmi", ""),
                        "Verdict": p.get("verdict", ""),
                    })
                st.dataframe(rows, use_container_width=True)
            else:
                st.error(f"Error {r.status_code}: {r.json().get('detail', r.text)}")
        except Exception as e:
            st.error(f"Connection error: {e}")