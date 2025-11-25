#!/usr/bin/env bash
# Helper to start Streamlit bound to all interfaces and the default port
# Use this when you run in containers or remote workspaces where you need external access
python -m streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port 8501