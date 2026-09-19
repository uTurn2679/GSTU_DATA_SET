# 🩸 GSTU Blood Donor Database & Badhon Network

A full-stack web application designed for **GSTU** and **Badhon Voluntary Blood Donors' Organization** to manage, search, and filter blood donor records efficiently.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-red)
![Database](https://img.shields.io/badge/Database-SQLite3-green)
![Styling](https://img.shields.io/badge/Styling-Tailwind%20CSS-38bdf8)

---

## 🌟 Key Features

- 🩸 **Donor Registration & Profile Management**: Register student & voluntary donors with institutional details.
- 🔍 **Advanced Search & Multi-Filters**: Filter donors by **Blood Group** (`A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`), **Department**, **Session**, **Badhon Membership**, and **Availability Status**.
- 📊 **Live Metrics Dashboard**: Quick count of Total Donors, Available Donors, Total Donations Made, and Badhon Members.
- ⚡ **Instant Auto-Submit Filters**: Real-time filtering with interactive badge pills and radio buttons.
- 📥 **CSV Dataset Export**: Download complete donor directory as a standard `.csv` file.
- 🛡️ **Null Value Handling**: Graceful fallback display (`N/A`) for missing last donation dates or donation counts.

---

## 📋 Stored Donor Fields

| Field Name | Description | Example |
| :--- | :--- | :--- |
| **Name** | Full Name of Donor | *Md. Rakibul Hasan* |
| **Department** | Academic Department | *CSE, EEE, BBA, Physics* |
| **Session** | Academic Batch / Session | *2020-21, 2021-22* |
| **Blood Group** | Blood Group Type | *A+, O+, B-, AB+* |
| **Phone** | Contact Phone Number | *01711223344* |
| **Last Donation Date** | Date of last blood donation | *2026-05-12* (or *N/A*) |
| **Total Donations** | Total blood donations count | *4 times* (or *N/A*) |
| **Member of Badhon** | Badhon Member badge | **Badhon Member** / Non-Member |
| **Availability Status** | Ready to donate status | **Available** / **Unavailable** |

---

## 💻 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone <YOUR-GITHUB-REPO-URL>
   cd "GSTU DATA SET"
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Seed Initial Database**:
   ```bash
   python seed_data.py
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🧪 Running Automated Unit Tests

Run the test suite to verify routing, filters, and CSV export functionality:
```bash
python test_app.py
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
