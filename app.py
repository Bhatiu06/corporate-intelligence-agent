import os
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# ----------------------------------------------------
# 🔑 SECURE KEY RETRIEVAL (Reads from Streamlit Secrets)
# ----------------------------------------------------
AUTH_KEY = st.secrets.get("GROQ_API_KEY", "")

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
# ⚡ SEARCH ENGINE (Free DuckDuckGo)
# ----------------------------------------------------
def search_company_fast(query: str, max_results: int = 5) -> str:
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
# 🔍 LIVE GROQ MODEL DISCOVERY
# ----------------------------------------------------
def get_available_groq_models(client: Groq):
    """Dynamically queries Groq for active, non-deprecated chat models."""
    try:
        model_list = client.models.list()
        # Filter out whisper (audio), guard, or embedding models
        chat_models = [
            m.id for m in model_list.data 
            if not any(skip in m.id for skip in ["whisper", "guard", "embed", "safeguard", "vision"])
        ]
        if chat_models:
            return chat_models
    except Exception:
        pass
    # Fallback to standard active defaults if listing fails
    return ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]

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
    elif not AUTH_KEY:
        st.error("⚠️ GROQ_API_KEY is missing! Go to your Streamlit Cloud settings -> Secrets, and add: GROQ_API_KEY = \"gsk_...\"")
    else:
        with st.spinner("⚡ Fetching live corporate records & analyzing via Groq..."):
            search_query = f"{target_company} CEO MD founder products revenue GDP role"
            search_data = search_company_fast(search_query, max_results=5)

            system_instruction = """
            You are a senior corporate intelligence analyst and macro-economist.
            Generate a concise, beautifully structured intelligence dossier for the requested company.
            Combine the provided online search context with your knowledge base.
            Strictly follow the Markdown format requested by the user.
            """

            prompt = f"""
            Generate a full corporate intelligence dossier for '{target_company}'.

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

            st.markdown('<div class="dossier-card">', unsafe_allow_html=True)
            placeholder = st.empty()
            full_text = ""
            success = False
            last_err = ""

            try:
                client = Groq(api_key=AUTH_KEY)
                active_models = get_available_groq_models(client)

                for model_id in active_models:
                    try:
                        stream = client.chat.completions.create(
                            model=model_id,
                            messages=[
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3,
                            stream=True
                        )
                        for chunk in stream:
                            content = chunk.choices[0].delta.content or ""
                            full_text += content
                            placeholder.markdown(full_text + " ▌")
                        
                        placeholder.markdown(full_text)
                        success = True
                        break
                    except Exception as e:
                        last_err = str(e)
                        continue

                if not success:
                    st.error(f"⚠️ Groq Error: {last_err}")
            except Exception as client_err:
                st.error(f"⚠️ Connection Error: {client_err}")

            st.markdown('</div>', unsafe_allow_html=True)
