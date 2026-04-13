# AI Performance Tracker

I built this because I was curious — what if my computer could just *tell me* what's slowing it down?

This tool checks your CPU, RAM, and disk usage, grabs the top 10 processes eating your resources, and sends all of that to Google Gemini. The AI looks at it and gives you actual advice — like "close Brave, it's using 500MB of your RAM" or "your RAM is at 85%, here's what to do."

No background monitoring. No data stored. You run it, it tells you what's up, and it exits.

---

## What it does

- Reads your system stats using `psutil` (CPU %, RAM, Disk, top 10 processes)
- Bundles it into a JSON object
- Sends it to the Gemini API
- Prints the AI's advice in a clean terminal layout using `rich`

The whole thing runs in one shot — open terminal, type `python main.py`, done.

---

## Setup

**1. Clone it**
```bash
git clone https://github.com/sakshamtyagi767/AI-performance-tracker.git
cd AI-performance-tracker
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Copy `.env.example` to `.env` and paste your Gemini API key inside:
```
GEMINI_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)

**4. Run it**
```bash
python main.py
```

---

## What the output looks like

```
AI System Performance Tracker
────────────────────────────────────
Step 1/3 : Collecting system metrics...
Done! Metrics collected in 1.3s

CPU   8.5%  |  4 cores
RAM   6.6 GB used / 7.75 GB (85%)
Disk  92 GB used / 328 GB (28%)

Top 10 Processes
1. Antigravity.exe   — 630 MB RAM
2. MemCompression    — 450 MB RAM
3. MsMpEng.exe       — 242 MB RAM
...

Step 2/3 : Sending to Gemini AI...

Severity : MEDIUM  |  Health Score: 75/100
"System under moderate load, mostly from RAM usage"

Recommendations:
  [HIGH]   Close unused Brave tabs — saves ~500 MB RAM
  [MEDIUM] Adjust MemCompression  — saves ~50 MB RAM
  [LOW]    Monitor CPU core imbalance
```

---

## Running the tests

```bash
pytest tests/ -v
```

21 tests, all passing. They check that psutil returns valid data — correct types, sane ranges, JSON-serializable output before anything gets sent to the API.

---

## Files

```
ai-performance-tracker/
├── main.py          # runs everything in order
├── monitor.py       # collects system stats with psutil
├── ai_advisor.py    # sends data to Gemini, parses response
├── reporter.py      # prints everything nicely in the terminal
├── config.py        # loads API key from .env
├── tests/
│   └── test_monitor.py
├── .env.example     # copy this to .env and add your key
└── requirements.txt
```

---

## Note on the API key

The `.env` file is in `.gitignore` so it will never be committed to GitHub. The `.env.example` is safe to commit — it's just a template with no real key in it.

---

Built with Python 3.12 · psutil · google-genai · rich · python-dotenv
