## Social-Media-and-Network-Analysis-of-Russia-Ukraine-War

This repository gathers the code, notebooks and data artifacts used for Assignment 2: collecting and analysing social media (YouTube + Reddit) data about the Russia–Ukraine war. The content includes data collection scripts, preprocessing notebooks, and network analysis notebooks and outputs.

TABLE OF CONTENTS
- Project summary
- Repo layout (important files)
- Quick start (run locally)
- Notebooks & scripts (detailed)
- Environment variables and secrets (how to provide keys)
- Development notes and troubleshooting
- License & contact

Project summary
---------------
The repository demonstrates a small data engineering + analysis pipeline:

- Data Collection: scripts and notebooks that use the YouTube Data API and Reddit API (PRAW) to collect videos, comments, posts and comments.
- Processing: Jupyter notebooks that clean and preprocess the collected data.
- Network Analysis: notebooks and CSVs containing network measures and community analysis results.

This repo is intended for research / educational use. If you reuse scripts, obey the platforms' API terms and rate limits.

Repo layout (top-level)
-----------------------
Key folders and files you will likely use:

- `Data Collection/` — scripts and notebooks that collect raw data (YouTube + Reddit). Examples: `youtube_api.py`, `youtube_data.py`, `reddit_data.ipynb`.
- `Data/` — saved JSON/CSV datasets produced by collection and processing steps (committed sample data).
- `Processing/` — notebooks for cleaning and preparing data for analysis.
- `Network Analysis/` — notebooks and result CSVs for graph construction and centrality/community analysis.
- `requirements.txt` — Python dependencies to install.
- `.env.example` — example environment file showing required variables (copy to `.env`).

Quick start (recommended)
-------------------------
1. Clone the repo and change directory to the project root.

2. Create and activate a virtual environment (Windows, cmd.exe):

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install Python dependencies:

```cmd
pip install -r requirements.txt
```

4. Create a local `.env` file from the template and add your keys (do NOT commit the file):

```cmd
copy .env.example .env
```

Open `.env` and replace placeholders with real keys. Required variables (examples):

- `YOUTUBE_API_KEY` — Google Cloud API key with YouTube Data API enabled
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT` — PRAW credentials

5. Run a collection script to verify setup (example):

```cmd
python "Data Collection\youtube_api.py"
```

The scripts and notebooks now read keys from environment variables (via `python-dotenv`). If a required variable is missing, the script/notebook will raise a clear error telling you which variable is missing.

Notebooks & scripts (details)
-----------------------------
- `Data Collection/youtube_api.py` — script that searches YouTube, fetches video metadata and top-level comments, and writes JSON/CSV outputs. Uses `YOUTUBE_API_KEY` from the environment.
- `Data Collection/youtube_data.py` — alternative/supplementary YouTube collector.
- `Data Collection/reddit_data.ipynb` — notebook that collects submissions and comments using `praw`. It has been updated to load credentials from `.env`.

How environment variables are used
---------------------------------
The repository uses `python-dotenv` to load `.env` at runtime (only for local development). That means you should:

1. Create `.env` from `.env.example` locally.
2. Put your actual API keys in `.env` (DO NOT commit this file).

Example `.env` (already provided as `.env.example`):

```
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY_HERE
REDDIT_CLIENT_ID=YOUR_REDDIT_CLIENT_ID_HERE
REDDIT_CLIENT_SECRET=YOUR_REDDIT_CLIENT_SECRET_HERE
REDDIT_USER_AGENT=your_app_name/0.1 by your_reddit_username
```

Security and publishing guidance
--------------------------------
- Never commit `.env` or real API keys. `.gitignore` in this repo excludes `.env`.
- If you need to share reproducible examples, use `.env.example` or GitHub Secrets (for CI) instead of exposing tokens.

Development notes & troubleshooting
----------------------------------
- Missing imports / unresolved packages: install `requirements.txt` in a virtualenv as shown above.
- If you get API quota errors from YouTube/Reddit, watch your requests per minute and use smaller limits when running collection jobs.
- Notebooks can be large; if GitHub renders slowly, open them locally (VS Code / Jupyter Lab).
