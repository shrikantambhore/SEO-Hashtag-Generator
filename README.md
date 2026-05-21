# 🏢 RealLaunch — AI SEO & Social Content Generator

An internal Streamlit app that generates **SEO titles, meta descriptions, keywords, and platform-specific hashtags** for every new real estate project launch — powered by [Grok (xAI)](https://x.ai/).

---

## What it generates

| Output | Details |
|---|---|
| SEO Titles | 3 options, each with a distinct angle |
| Meta Descriptions | 3 options, 150–160 chars, CTA-driven |
| Primary Keywords | 5–7 high-intent, location-aware |
| Secondary Keywords | 6–8 supporting terms |
| Long-tail Keywords | 5–7 buyer-intent phrases |
| Instagram Hashtags | 20–25 discovery-optimised tags |
| LinkedIn Hashtags | 10–12 professional/investment tags |
| X (Twitter) Hashtags | 8–10 concise, campaign-ready tags |
| Caption Keywords | 10–12 plain phrases for social copy |

---

## Project Structure

```
realestate-seo-app/
├── app.py                        # Streamlit UI
├── prompts.py                    # Prompt builders + Grok call wrappers
├── grok_client.py                # Grok API client (OpenAI-compatible)
├── utils.py                      # Validation, constants, formatters
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example      # Copy → secrets.toml and add your key
```

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_ORG/realestate-seo-app.git
cd realestate-seo-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Grok API key

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and replace the placeholder with your real key:

```toml
GROK_API_KEY = "xai-your-actual-key-here"
```

> Get your key from [console.x.ai](https://console.x.ai/)

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Deploying on Streamlit Community Cloud

### Step 1 — Push to GitHub

Make sure `.streamlit/secrets.toml` is in `.gitignore` (it already is). Then:

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2 — Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select your GitHub repo and set **Main file path** to `app.py`
4. Click **Deploy**

### Step 3 — Add the API key securely

In the Streamlit Cloud dashboard:

1. Open your deployed app → **⋮ menu → Settings → Secrets**
2. Paste:

```toml
GROK_API_KEY = "xai-your-actual-key-here"
```

3. Save. The app will restart and pick up the key automatically.

---

## Updating the app

```bash
git add .
git commit -m "Your change description"
git push
```

Streamlit Cloud auto-redeploys on every push to `main`.

---

## Environment variable alternative

If you prefer not to use `secrets.toml`, you can set the key as an environment variable:

```bash
export GROK_API_KEY="xai-your-key-here"
streamlit run app.py
```

The app checks `st.secrets` first, then `os.environ`.

---

## Customisation notes

| File | What to change |
|---|---|
| `utils.py` | Add cities, project types, or configurations to the constants |
| `prompts.py` | Adjust prompt wording, output schema, or add new generation types |
| `grok_client.py` | Switch model (`grok-3` → `grok-3-mini` for speed) or adjust temperature |
| `app.py` | Add new UI sections, tabs, or export features |

---

## Suggested Future Improvements

- **PDF / DOCX export** — one-click download of all generated content per project
- **Project history** — save past generations to a local SQLite or Supabase DB
- **Batch mode** — upload a CSV of projects and generate content for all at once
- **Google Sheets integration** — push outputs directly to a launch tracker sheet
- **CMS integration** — auto-populate WordPress / Webflow SEO fields via API
- **Content brief generator** — extend output to include blog post outlines
- **Competitor keyword analysis** — add a Serper/SerpAPI call to benchmark against competing projects

---

## Requirements

- Python 3.10+
- Streamlit 1.35+
- A valid Grok API key (xAI account)
