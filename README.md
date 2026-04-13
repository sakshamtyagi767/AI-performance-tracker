# 🚀 AI System Performance Tracker

> **A Python CLI tool that monitors your PC's health and uses Google Gemini AI to deliver personalised performance optimisation advice — in seconds.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange?logo=google)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 What It Does

1. **Collects** real-time CPU, RAM, and Disk metrics using `psutil`
2. **Identifies** the top 10 most resource-hungry processes
3. **Sends** the data as JSON to the **Google Gemini API**
4. **Displays** AI-generated, actionable optimisation advice in your terminal

**No background monitoring. Runs once, shows results, exits cleanly.**

---

## 🖥️ Demo Output

```
🚀  AI System Performance Tracker
────────────────────────────────────────────────
Step 1/3 : Collecting system metrics... ✅
Step 2/3 : Sending data to Gemini AI...  ✅
Step 3/3 : Displaying AI recommendations...

🤖  AI Performance Analysis
  Severity  : HIGH
  Health    : 42/100
  Your system is under heavy load — Chrome and Slack are consuming most of your RAM.

📋 Recommendations
  #1 [HIGH] Close unused Chrome tabs
     Why   : Chrome is using 3.2 GB RAM across 12 processes
     Saves : ~2.5 GB RAM freed
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---------|---------|
| `psutil` | System metrics (CPU, RAM, Disk, Processes) |
| `google-generativeai` | Gemini API for AI-powered advice |
| `rich` | Beautiful terminal output |
| `python-dotenv` | Secure API key management |
| `pytest` | Unit testing |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-performance-tracker.git
cd ai-performance-tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key
```bash
# Copy the example file
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux

# Open .env and paste your key:
# GEMINI_API_KEY=your_actual_key_here
```
> Get a free API key at: https://aistudio.google.com/app/apikey

### 4. Run
```bash
python main.py
```

---

## 🧪 Run Unit Tests

```bash
pytest tests/ -v
```

---

## 📁 Project Structure

```
ai-performance-tracker/
│
├── main.py          # Entry point — orchestrates the pipeline
├── monitor.py       # psutil-based system metrics collector
├── ai_advisor.py    # Gemini API integration + response parser
├── reporter.py      # Rich terminal display module
├── config.py        # Settings & secure API key loader
│
├── tests/
│   └── test_monitor.py  # Unit tests for monitor module
│
├── requirements.txt
├── .env.example     # Safe to commit — template only
├── .gitignore       # Keeps .env and __pycache__ out of git
└── README.md
```

---

## 🔒 Security Note

Your API key is stored in a `.env` file which is listed in `.gitignore`.
**It will never be committed to GitHub.** The `.env.example` file (which is safe to commit) shows the format.

---

## 📄 License

MIT License — feel free to use, modify, and share.
