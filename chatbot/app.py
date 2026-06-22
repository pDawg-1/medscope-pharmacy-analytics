from flask import Flask, request, render_template_string
import snowflake.connector
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)


# -----------------------------
# Snowflake connection
# -----------------------------
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )


def run_query_one(sql):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def run_query_all(sql):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


# -----------------------------
# Helper functions
# -----------------------------
DRUG_ALIASES = {
    "metformin": "Metformin",
    "januvia": "Januvia",
    "januiva": "Januvia",
    "janivia": "Januvia",
    "ozempic": "Ozempic",
    "trulicity": "Trulicity",
    "farxiga": "Farxiga",
    "insulin glargine": "Insulin Glargine",
    "insulin": "Insulin Glargine",
    "prednisone": "Prednisone",
    "losartan": "Losartan",
    "lisinopril": "Lisinopril",
    "amlodipine": "Amlodipine",
    "hydrochlorothiazide": "Hydrochlorothiazide",
    "atorvastatin": "Atorvastatin",
    "rosuvastatin": "Rosuvastatin",
    "albuterol inhaler": "Albuterol Inhaler",
    "albuterol": "Albuterol Inhaler",
    "omeprazole": "Omeprazole",
    "pantoprazole": "Pantoprazole",
    "sertraline": "Sertraline",
    "montelukast": "Montelukast",
    "amoxicillin": "Amoxicillin",
    "azithromycin": "Azithromycin",
    "apixaban starter pack": "Apixaban Starter Pack",
    "apixaban": "Apixaban Starter Pack",
    "clopidogrel": "Clopidogrel",
    "cyclobenzaprine": "Cyclobenzaprine",
    "cefdinir": "Cefdinir",
}


def extract_drug_name(question):
    q = question.lower()
    for alias, official_name in DRUG_ALIASES.items():
        if alias in q:
            return official_name
    return None


def safe_sql_text(value):
    return value.replace("'", "''")


def format_money(value):
    if value is None:
        return "$0.00"
    return f"${float(value):,.2f}"


# -----------------------------
# Chatbot response logic
# -----------------------------
def get_bot_response(question):
    q = question.lower().strip()
    drug_name = extract_drug_name(q)

    try:
        # -----------------------------
        # Drug availability
        # Example: Is Metformin available in CVS?
        # -----------------------------
        if drug_name and ("available" in q or "cvs" in q):
            drug = safe_sql_text(drug_name)
            pharmacy_filter = "%CVS%" if "cvs" in q else "%"

            row = run_query_one(f"""
                SELECT
                    COUNT(*) AS prescription_count,
                    ROUND(SUM(total_cost), 2) AS total_cost,
                    ROUND(SUM(insurance_covered), 2) AS insurance_covered,
                    ROUND(SUM(out_of_pocket), 2) AS out_of_pocket
                FROM MEDSCOPE_DB.ANALYTICS.VW_PATIENT_PRESCRIPTION_LOOKUP
                WHERE drug_name ILIKE '%{drug}%'
                  AND pharmacy_name ILIKE '{pharmacy_filter}';
            """)

            if row and row[0] and row[0] > 0:
                pharmacy_text = "CVS Pharmacy" if "cvs" in q else "the pharmacy records"
                return (
                    f"Yes, {drug_name} appears in {pharmacy_text} prescription records. "
                    f"There are {int(row[0]):,} matching prescriptions, with total drug cost of "
                    f"{format_money(row[1])}, insurance coverage of {format_money(row[2])}, "
                    f"and patient out-of-pocket cost of {format_money(row[3])}."
                )

            return f"No matching {drug_name} prescriptions were found for that pharmacy."

        # -----------------------------
        # Who prescribed a drug?
        # Examples:
        # Who prescribed Januvia?
        # Who all prescribed Metformin?
        # Which doctors prescribed Metformin?
        # -----------------------------
        elif drug_name and (
            "who" in q
            or "doctor" in q
            or "doctors" in q
            or "prescribed" in q
            or "prescriber" in q
        ) and "why" not in q:
            drug = safe_sql_text(drug_name)

            rows = run_query_all(f"""
                SELECT
                    doctor_name,
                    specialty,
                    COUNT(*) AS prescription_count
                FROM MEDSCOPE_DB.ANALYTICS.VW_PATIENT_PRESCRIPTION_LOOKUP
                WHERE drug_name ILIKE '%{drug}%'
                  AND doctor_name IS NOT NULL
                GROUP BY doctor_name, specialty
                ORDER BY prescription_count DESC
                LIMIT 8;
            """)

            if rows:
                doctor_lines = [
                    f"{doctor} ({specialty}) — {int(count)} prescriptions"
                    for doctor, specialty, count in rows
                ]

                return (
                    f"{drug_name} was prescribed by these doctors in the dataset:\n\n"
                    + "\n".join(doctor_lines)
                )

            return f"I could not find doctors who prescribed {drug_name} in the dataset."

        # -----------------------------
        # Why was a drug prescribed?
        # Examples:
        # Why was Januvia prescribed?
        # What diagnosis was Januvia prescribed for?
        # -----------------------------
        elif drug_name and ("why" in q or "diagnosis" in q or "reason" in q):
            drug = safe_sql_text(drug_name)

            rows = run_query_all(f"""
                SELECT
                    standardized_diagnosis,
                    COUNT(*) AS prescription_count
                FROM MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL
                WHERE drug_name ILIKE '%{drug}%'
                  AND standardized_diagnosis IS NOT NULL
                GROUP BY standardized_diagnosis
                ORDER BY prescription_count DESC
                LIMIT 5;
            """)

            if rows:
                top_diagnosis = rows[0][0]

                diagnosis_lines = [
                    f"{diagnosis} — {int(count)} prescriptions"
                    for diagnosis, count in rows
                ]

                return (
                    f"Based on the prescription dataset, {drug_name} was mainly prescribed for "
                    f"{top_diagnosis}. The diagnosis breakdown is:\n\n"
                    + "\n".join(diagnosis_lines)
                )

            return f"I could not find diagnosis information explaining why {drug_name} was prescribed."

        # -----------------------------
        # KPI questions
        # -----------------------------
        elif "total drug cost" in q:
            row = run_query_one("""
                SELECT total_drug_cost
                FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;
            """)
            return f"The total drug cost is {format_money(row[0])}."

        elif "total prescriptions" in q or "prescription count" in q:
            row = run_query_one("""
                SELECT total_prescriptions
                FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;
            """)
            return f"The total number of prescriptions is {int(row[0]):,}."

        elif "average prescription cost" in q or "average cost" in q:
            row = run_query_one("""
                SELECT average_prescription_cost
                FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;
            """)
            return f"The average prescription cost is {format_money(row[0])}."

        elif "most prescribed drug" in q:
            row = run_query_one("""
                SELECT most_prescribed_drug
                FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;
            """)
            return f"The most prescribed drug is {row[0]}."

        elif "highest cost drug" in q or "most expensive drug" in q or "highest total cost drug" in q:
            row = run_query_one("""
                SELECT drug_name, total_drug_cost
                FROM MEDSCOPE_DB.ANALYTICS.VW_DRUG_COST_ANALYSIS
                ORDER BY total_drug_cost DESC
                LIMIT 1;
            """)
            return f"The highest-cost drug is {row[0]}, with a total cost of {format_money(row[1])}."

        elif "doctor prescribed the most" in q or "top prescribing doctor" in q or "most prescriptions doctor" in q:
            row = run_query_one("""
                SELECT doctor_name, total_prescriptions
                FROM MEDSCOPE_DB.ANALYTICS.VW_DOCTOR_PRESCRIBER_ANALYSIS
                ORDER BY total_prescriptions DESC
                LIMIT 1;
            """)
            return f"The top prescribing doctor is {row[0]}, with {int(row[1]):,} prescriptions."

        elif "highest prescriptions month" in q or "month had the highest" in q:
            row = run_query_one("""
                SELECT year_month, total_prescriptions
                FROM MEDSCOPE_DB.ANALYTICS.VW_MONTHLY_PRESCRIPTION_TREND
                ORDER BY total_prescriptions DESC
                LIMIT 1;
            """)
            return f"The month with the highest prescriptions is {row[0]}, with {int(row[1]):,} prescriptions."

        elif "insurance covered" in q:
            row = run_query_one("""
                SELECT SUM(insurance_covered)
                FROM MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL;
            """)
            return f"The total insurance-covered amount is {format_money(row[0])}."

        elif "out of pocket" in q or "patient paid" in q:
            row = run_query_one("""
                SELECT SUM(out_of_pocket)
                FROM MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL;
            """)
            return f"The total patient out-of-pocket amount is {format_money(row[0])}."

        elif "total patients" in q:
            row = run_query_one("""
                SELECT total_patients
                FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;
            """)
            return f"The total number of patients is {int(row[0]):,}."

        elif "total doctors" in q:
            row = run_query_one("""
                SELECT total_doctors
                FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;
            """)
            return f"The total number of doctors is {int(row[0]):,}."

        # -----------------------------
        # Fallback
        # -----------------------------
        else:
            return (
                "I can answer questions about total drug cost, total prescriptions, average cost, "
                "most prescribed drug, top prescribing doctor, highest prescription month, insurance coverage, "
                "out-of-pocket cost, total patients, total doctors, drug availability, who prescribed a drug, "
                "and why a drug was prescribed."
            )

    except Exception as e:
        return f"Connection or query error: {str(e)}"


# -----------------------------
# Chat UI
# -----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>MedScope Analytics Chatbot</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            background: linear-gradient(135deg, #e8f3f6, #f8fbfc);
            color: #1f2937;
        }

        .app {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 28px;
        }

        .chat-shell {
            width: 1120px;
            height: 730px;
            background: #ffffff;
            border-radius: 26px;
            box-shadow: 0 24px 60px rgba(15, 46, 60, 0.18);
            display: grid;
            grid-template-columns: 330px 1fr;
            overflow: hidden;
            border: 1px solid #dbe7ec;
        }

        .sidebar {
            background: linear-gradient(180deg, #0f3d4a, #1f7a8c);
            color: white;
            padding: 30px;
        }

        .sidebar h2 {
            margin: 0;
            font-size: 28px;
            line-height: 1.2;
        }

        .sidebar p {
            color: #d7edf2;
            font-size: 14px;
            margin: 12px 0 24px;
            line-height: 1.5;
        }

        .chip {
            background: rgba(255,255,255,0.13);
            border: 1px solid rgba(255,255,255,0.25);
            color: white;
            padding: 13px;
            border-radius: 13px;
            margin-bottom: 10px;
            cursor: pointer;
            font-size: 14px;
            transition: 0.2s;
        }

        .chip:hover {
            background: rgba(255,255,255,0.24);
            transform: translateX(3px);
        }

        .chat-area {
            display: flex;
            flex-direction: column;
            background: #f8fbfc;
        }

        .topbar {
            padding: 28px 34px;
            background: white;
            border-bottom: 1px solid #e5edf1;
        }

        .topbar h1 {
            margin: 0;
            font-size: 32px;
            color: #103b4a;
        }

        .topbar p {
            margin: 7px 0 0;
            color: #64748b;
            font-size: 15px;
        }

        .messages {
            flex: 1;
            padding: 34px;
            overflow-y: auto;
        }

        .empty-state {
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #64748b;
            text-align: center;
        }

        .empty-icon {
            width: 78px;
            height: 78px;
            border-radius: 50%;
            background: #e7f5f8;
            color: #1f7a8c;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            margin-bottom: 18px;
        }

        .message {
            display: flex;
            margin-bottom: 20px;
        }

        .message.user {
            justify-content: flex-end;
        }

        .bubble {
            max-width: 78%;
            padding: 17px 20px;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.55;
            white-space: pre-line;
        }

        .user .bubble {
            background: #1f7a8c;
            color: white;
            border-bottom-right-radius: 5px;
            font-weight: 600;
        }

        .bot .bubble {
            background: white;
            color: #1f2937;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 5px;
            box-shadow: 0 8px 20px rgba(15, 46, 60, 0.06);
        }

        .bot-label {
            font-size: 12px;
            font-weight: 800;
            color: #1f7a8c;
            margin-bottom: 7px;
            letter-spacing: 0.2px;
        }

        .input-area {
            padding: 22px 34px;
            background: white;
            border-top: 1px solid #e5edf1;
        }

        form {
            display: flex;
            gap: 13px;
        }

        input {
            flex: 1;
            border: 1px solid #cbd5e1;
            border-radius: 15px;
            padding: 17px 19px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #1f7a8c;
            box-shadow: 0 0 0 4px rgba(31, 122, 140, 0.13);
        }

        button {
            background: #1f7a8c;
            color: white;
            border: none;
            border-radius: 15px;
            padding: 0 26px;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background: #145566;
        }

        .meta {
            margin-top: 9px;
            font-size: 12px;
            color: #94a3b8;
        }
    </style>
</head>

<body>
    <div class="app">
        <div class="chat-shell">

            <aside class="sidebar">
                <h2>MedScope Assistant</h2>
                <p>Ask business questions about prescription cost, drug utilization, insurance coverage, and provider activity.</p>

                <div class="chip" onclick="fillQuestion('What is the total drug cost?')">Total drug cost</div>
                <div class="chip" onclick="fillQuestion('What is the total prescriptions?')">Total prescriptions</div>
                <div class="chip" onclick="fillQuestion('What is the average prescription cost?')">Average prescription cost</div>
                <div class="chip" onclick="fillQuestion('What is the most prescribed drug?')">Most prescribed drug</div>
                <div class="chip" onclick="fillQuestion('Who prescribed Metformin?')">Who prescribed Metformin?</div>
                <div class="chip" onclick="fillQuestion('Who prescribed Januvia?')">Who prescribed Januvia?</div>
                <div class="chip" onclick="fillQuestion('Why was Januvia prescribed?')">Why was Januvia prescribed?</div>
                <div class="chip" onclick="fillQuestion('Is Metformin available in CVS?')">Metformin in CVS</div>
                <div class="chip" onclick="fillQuestion('Which month had the highest prescriptions?')">Highest prescription month</div>
            </aside>

            <main class="chat-area">
                <div class="topbar">
                    <h1>Analytics Chatbot</h1>
                    <p>Connected to Snowflake analytics views for controlled business Q&A.</p>
                </div>

                <div class="messages">
                    {% if question and answer %}
                        <div class="message user">
                            <div class="bubble">{{ question }}</div>
                        </div>

                        <div class="message bot">
                            <div class="bubble">
                                <div class="bot-label">MedScope Bot</div>
                                {{ answer }}
                            </div>
                        </div>
                    {% else %}
                        <div class="empty-state">
                            <div class="empty-icon">💬</div>
                            <h2>Start a conversation</h2>
                            <p>Ask about costs, prescriptions, doctors, drugs, pharmacy availability, or diagnosis-based insights.</p>
                        </div>
                    {% endif %}
                </div>

                <div class="input-area">
                    <form method="POST" id="chatForm">
                        <input id="questionInput" name="question" autocomplete="off" placeholder="Ask a question, for example: Who prescribed Metformin?" autofocus>
                        <button type="submit">Send</button>
                    </form>
                    <div class="meta">Queries are mapped to approved SQL statements for reliable Snowflake answers.</div>
                </div>
            </main>

        </div>
    </div>

    <script>
        const input = document.getElementById("questionInput");

        function fillQuestion(text) {
            input.value = text;
            input.focus();
        }
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    question = ""
    answer = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            answer = get_bot_response(question)

    return render_template_string(HTML_PAGE, question=question, answer=answer)


if __name__ == "__main__":
    app.run(debug=True)