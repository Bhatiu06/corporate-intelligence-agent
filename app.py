import json
import requests
import streamlit as st
from duckduckgo_search import DDGS

# ----------------------------------------------------
# 🔑 EMBEDDED AQ KEY
# ----------------------------------------------------
AUTH_KEY = "AQ.Ab8RN6JgbeeoEr6J-Rdy_PE24hl_exdseT_L4V1AaGh8W0wATg"

# ----------------------------------------------------
# 🎨 COLORFUL, MODERN UI CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="Corporate Vision Intelligence",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 20%, #fdfbf7 0%, #edf2f7 60%, #f8fafc 100%);
    }

    .hero-card {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 40%, #ec4899 100%);
        padding: 35px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px -5px rgba(99, 102, 241, 0.35);
        text-align: center;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
    }
    .hero-desc {
        font-size: 1.05rem;
        opacity: 0.95;
        font-weight: 500;
    }

    .stTextInput > div > div > input {
        border-radius: 12px;
        padding: 12px 18px;
        border: 2px solid #cbd5e1;
        font-size: 1.1rem;
        background-color: #ffffff;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.15);
    }

    .stButton > button {
        background: linear-gradient(90deg, #4f46e5 0%, #06b6d4 100%);
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 700;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        width: 100%;
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.3);
    }

    .dossier-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 30px 35px;
        margin-top: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.04);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-card">
    <div class="hero-title">⚡ Corporate Vision & Intelligence</div>
    <div class="hero-desc">Autonomous research engine for live company leadership, products, future bets, and GDP economic footprint.</div>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# ⚡ SEARCH ENGINE
# ----------------------------------------------------
def search_company_fast(query: str, max_results: int = 4) -> str:
    results = []
    try:
        with DDGS(timeout=5) as ddgs:
            raw_results = ddgs.text(query, max_results=max_results)
            for r in raw_results:
                results.append(f"Title: {r.get('title')}\nDetails: {r.get('body')}\n")
    except Exception:
        pass
    return "\n---\n".join(results) if results else "No external search snippets available."


# ----------------------------------------------------
# 🌐 DYNAMIC API CALL (Auto-detects active models)
# ----------------------------------------------------
def get_working_headers(token: str):
    """Returns headers that work with the key."""
    return {
        "Content-Type": "application/json",
        "x-goog-api-key": token
    }


def call_gemini_api(prompt_text: str, token: str) -> str:
    # Modern active models suggested by the Google API error response
    models_to_try = [
        "gemini-3.1-pro-preview",
        "gemini-3.8-flash",
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash"
    ]

    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    headers = get_working_headers(token)
    last_error = ""

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)

            # If 401, retry with Bearer token header
            if resp.status_code == 401:
                alt_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
                resp = requests.post(url, headers=alt_headers, json=payload, timeout=30)

            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                last_error = f"{model_name} (Status {resp.status_code}): {resp.text}"
                # If 503 (busy) or 404 (wrong version), smoothly continue to next model
                continue
        except Exception as e:
            last_error = str(e)
            continue

    raise Exception(last_error)


# ----------------------------------------------------
# 📥 USER INPUT
# ----------------------------------------------------
col_search, col_btn = st.columns([4, 1.2])

with col_search:
    target_company = st.text_input(
        "Search Box",
        placeholder="Enter company name (e.g. Tata Motors, ASML, Reliance, NVIDIA)...",
        label_visibility="collapsed"
    )

with col_btn:
    analyze_click = st.button("🚀 Analyze Now")

# ----------------------------------------------------
# ⚙️ AGENT PIPELINE
# ----------------------------------------------------
if analyze_click:
    if not target_company.strip():
        st.warning("⚠️ Please enter a company name first.")
    else:
        with st.spinner("⚡ Fetching live corporate records & analyzing..."):
            search_query = f"{target_company} CEO MD founder products revenue GDP"
            search_data = search_company_fast(search_query, max_results=4)

            prompt = f"""
            You are a corporate intelligence analyst. Create a concise, structured intelligence dossier for '{target_company}'.
            Use the web context below, combined with your knowledge.

            WEB SEARCH CONTEXT:
            {search_data}

            Strictly format as:
            # 🏢 {target_company} — Corporate Intelligence Dossier
            ---
            ### 🏛️ Executive Snapshot
            | Attribute | Details |
            | :--- | :--- |
            | **Official Name** | (Official registered name) |
            | **Founded** | (Year or date) |
            | **Founders** | (Names) |
            | **Headquarters** | (City, Country) |
            | **Key Leadership** | **CEO:** [Name] <br> **MD / Chairperson:** [Name] |
            | **Listing** | [Public (Exchange: TICKER) or Private] |

            ---
            ### 🧭 About the Company & Mission
            > [2-3 sentences on market positioning, identity, and footprint]

            ---
            ### 📦 Core Offerings & Products
            * **[Product Segment 1]**: Brief description.
            * **[Product Segment 2]**: Brief description.
            * **[Product Segment 3]**: Brief description.

            ---
            ### 🎯 Strategic Focus & Future Bets
            * **Core Advantage**: Competitive moat.
            * **R&D & Tech Horizon**: Future investments (e.g., AI, green transition, automation).
            * **Expansion Focus**: Priority markets.

            ---
            ### 🌍 Role in GDP & Macroeconomic Footprint
            * **Revenue & Valuation**: Latest figures.
            * **Workforce**: Direct headcount & indirect job ecosystem.
            * **GDP Impact**: Contribution to domestic/global GDP, tax revenues, and export share.
            * **Supply Chain**: Critical vendor ecosystem reliance.
            """

            try:
                result_text = call_gemini_api(prompt, AUTH_KEY)
                st.markdown('<div class="dossier-card">', unsafe_allow_html=True)
                st.markdown(result_text)
                st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ API Response: {e}")
