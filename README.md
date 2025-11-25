# Retail Insights Assistant

This repository contains an end-to-end sample implementation of a Retail Insights Assistant — a GenAI-enabled tool for summarizing sales CSVs and answering conversational Q&A about sales data.

Core features:
- Upload a CSV and run Summarization Mode or Conversational Q&A Mode (Streamlit UI).
- Modular LLM client (supports Gemini/OpenAI via environment keys) with a local fallback for offline demo.
- Multi-agent design: language-to-query resolution agent, data extraction agent, and validation agent.
- Data layer using pandas + DuckDB for efficient querying, with a scalable architecture design documented in slides.

Run locally:
1. Create a venv, install requirements
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Run Streamlit app
```
streamlit run app/streamlit_app.py
```

Provide OPENAI_API_KEY or GEMINI_API_KEY in a `.env` file for LLM-backed answers. You already added `GEMINI_API_KEY` — good.

Note about installing dependencies on Python 3.12 / Linux:
- Some packages (notably `duckdb` pins or `faiss-cpu`) may fail to install with strict pins. If pip errors when installing `duckdb` try updating requirements as shown and re-run `pip install -r requirements.txt`.
- `faiss-cpu` is optional and often fails to build on some platforms. If you need RAG/embedding features install `faiss-cpu` or `faiss-gpu` later using prebuilt wheels or `conda`.

If you hit install failures, try these steps (copy/paste):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `faiss-cpu` fails, install embeddings separately:

```bash
# Install sentence-transformer first
pip install -U sentence-transformers
# For FAISS with pip (sometimes unavailable), prefer conda:
conda install -c pytorch faiss-cpu -y
# or use a prebuilt wheel if available for your platform
```

Files:
- `app/streamlit_app.py` — Streamlit UI
- `src/retail_insights/` — core python modules (agents, llm client, data layer, QA, summarizer)
- `sample_data/sample_sales.csv` — sample dataset
- `docs/architecture_presentation.pptx` — architecture slides

Next steps: You can run tests and generate the presentation locally.

Run tests (requires pytest):
```
pip install pytest
pytest -q
```

Generate presentation (requires python-pptx):
```
python docs/generate_presentation.py
```

Troubleshooting Streamlit port access ("localhost refused to connect")
-----------------------------------------------------------------

If you start Streamlit and still can't open the Local URL in your browser:

1) Start Streamlit bound to all interfaces in case you are in a container/remote environment:

```bash
# helper script (executable by default in repo)
./scripts/start_streamlit.sh
# or manually:
streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

2) Check the process and port from the machine where Streamlit runs:

```bash
# check listener
ss -ltnp | grep 8501 || sudo lsof -i :8501

# try a local HTTP check on the host
curl -v http://127.0.0.1:8501 || curl -v http://<CONTAINER_IP>:8501
```

3) If Streamlit is in a devcontainer / Codespace / remote VM, confirm port 8501 is forwarded in the remote environment to your host. In VS Code Remote - Containers and Codespaces you can use the "Forward Port" feature or add the port in the devcontainer config. If the port is forwarded you can use the Network or External URL printed by Streamlit.

4) If you need external access while debugging, tools such as ngrok can expose the port to a public URL:

```bash
# install ngrok and run
ngrok http 8501
```

If you want environment-specific steps (codespace, devcontainer, cloud VM), tell me which environment you're running in and I'll add exact forward/open steps to the README.

Running in GitHub Codespaces (exact steps)
----------------------------------------

1) Remove any committed `.env` file from the repo (do not store secrets in the repository). If you accidentally committed a key already, remove it and rotate the key immediately. To remove it from the repository tracking (but keep local copy):

```bash
# removes from git tracking but leaves the file on disk
git rm --cached .env || true
git commit -m "Remove .env from repo; keep local only" || true
```

2) Use the Codespaces secrets (set the GEMINI_API_KEY / OPENAI_API_KEY in the Codespace repo secrets) — this keeps the key safe and accessible in the Codespace environment.

3) The repository includes a `.devcontainer/devcontainer.json` that will automatically forward port 8501 and run `pip install -r requirements.txt` in the Codespace after creation; after the container is ready, start Streamlit with the helper script to bind to 0.0.0.0:

```bash
chmod +x ./scripts/start_streamlit.sh
./scripts/start_streamlit.sh
```

4) In the Codespaces Ports view, ensure port 8501 is forwarded and marked "Open in Browser" or "Open in preview". If you prefer automatic forwarding, use the "Forward Port" button in the Codespaces UI (or use the Network URL printed by Streamlit).

If you want, I can also add an optional start-up task to automatically run the Streamlit server when the Codespace is created (not recommended for security reasons since it may expose an interactive app automatically). Let me know if you want that.

