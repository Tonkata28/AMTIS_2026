# AMTIS 2026 — Stock-Trading Simulator

![Python](https://img.shields.io/badge/Python-FastAPI-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

> **About this repository:** This is my **completed, post-competition solution**. The version I built live during the 7-hour AMTIS 2026 competition was less complete and lives in a separate private repo. This repository is the cleaned-up and finished build of the same task, kept public as a reference.

---

## About

**AMTIS 2026** (*"Аз мога тук и сега"*) is a national IT competition. The challenge was to build a **stock-trading simulator** — a web server that lets users trade stocks against changing market prices and tracks the results.

I competed **solo** with a 7-hour time limit to produce a working solution. This repo is where I rebuilt and finished it properly afterwards, using the same problem statement.

---

## What it does

- Simulates buying and selling of stocks with changing prices
- Exposes the simulation through a Python web server
- Serves a web interface for interacting with the simulator
- Based on the official competition task (see `tickets_and_problem_desc/`)

---

## Tech stack

| Layer      | Technology          |
| ---------- | ------------------- |
| Server     | Python (FastAPI)    |

---

## Project structure

```
AMTIS_2026/
├── amtis_server/             # Python server and trading/simulation logic
├── tickets_and_problem_desc/ # Original competition problem statement and task tickets
└── LICENSE
```

---

## Getting started

```bash
# 1. Clone the repo
git clone https://github.com/Tonkata28/AMTIS_2026.git
cd AMTIS_2026/amtis_server

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies and run the server
pip install -r requirements.txt
uvicorn main:app --reload
```

> Adjust the run command to match your entry file (e.g. `uvicorn app:app`).

---

## License

Released under the [MIT License](LICENSE). © 2026 Antonio Simeonov
