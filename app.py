import os
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# ----------------------------------------------------
# 🔑 SECURE KEY RETRIEVAL (Reads from Streamlit Secrets)
# ----------------------------------------------------
AUTH_KEY = st.secrets.get("GROQ_API_KEY", "")

# ----------------------------------------------------
# 🎨 GIDC CORPORATE THEME & RESPONSIVE UI
# ----------------------------------------------------
st.set_page_config(
    page_title="Corporate Vision & Intelligence Engine",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* GIDC Slate Industrial Background */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #EEF2F6 100%);
        color: #0F172A;
    }

    /* GIDC Executive Header Banner */
    .gidc-hero {
        background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 65%, #B45309 100%);
        padding: 38px 30px;
        border-radius: 16px;
        color: #FFFFFF;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(10, 37, 64, 0.25);
        border-left: 6px solid #F59E0B;
        position: relative;
    }
    .gidc-badge {
        display: inline-block;
        background: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid rgba(245, 158, 11, 0.4);
        margin-bottom: 12px;
    }
    .gidc-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 8px;
    }
    .gidc-subtitle {
        font-size: 1.05rem;
        opacity: 0.9;
        font-weight: 400;
        max-width: 850px;
    }

    /* Search & Action Bar */
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 14px 20px;
        border: 1.5px solid #CBD5E1;
        font-size: 1.1rem;
        background-color: #FFFFFF;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .stTextInput > div > div > input:focus {
        border-color: #1E3A8A;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.15);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0A2540 0%, #1E3A8A 100%);
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 700;
        border-radius: 10px;
        padding: 13px 26px;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(10, 37, 64, 0.2);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1E3A8A 0%, #D97706 100%);
        box-shadow: 0 6px 16px rgba(217, 119, 6, 0.3);
        transform: translateY(-1px);
    }

    /* Streamlit Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 22px;
        font-weight: 600;
        border: 1px solid #E2E8F0;
        border-bottom: none;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background: #0A2540 !important;
        color: #FFFFFF !important;
        border-color: #0A2540 !important;
    }

    /* Dossier Visual Containers */
    .dossier-container {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 28px 32px;
        margin-top: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
    }
    .metric-badge {
        background-color: #F1F5F9;
        border-left: 4px solid #F59E0B;
        padding: 14px 18px;
        border-radius: 6px;
        margin-bottom: 15px;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 🏛️ GIDC THEMED HERO HEADER
# ----------------------------------------------------
st.markdown("""
<div class="gidc-hero">
    <div class="gidc-badge">Autonomous Corporate Intelligence</div>
    <div class="gidc-title">Corporate Vision & Industrial Insights Engine</div>
    <div class="gidc-subtitle">
        High-speed intelligence pipeline synthesizing executive governance, core product portfolios, strategic R&D moats, and macroeconomic GDP footprint.
    </div>
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
    try:
        model_list = client.models.list()
        chat_models = [
            m.id for m in model_list.data 
            if not any(skip in m.id for skip in ["whisper", "guard", "embed", "safeguard", "vision"])
        ]
        if chat_models:
            return chat_models
    except Exception:
        pass
    return ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]

# ----------------------------------------------------
# 📥 USER SEARCH INPUT
# ----------------------------------------------------
col_search, col_btn = st.columns([4, 1.2])

with col_search:
    target_company = st.text_input(
        "Search Box",
        placeholder="Enter company name (e.g., Tata Motors, L&T, Adani Ports, Reliance, ASML, NVIDIA)...",
        label_visibility="collapsed"
    )

with col_btn:
    analyze_click = st.button("⚡ Generate Dossier")

# ----------------------------------------------------
# ⚙️ AGENT PIPELINE & STRUCTURED DOSSIER GENERATION
# ----------------------------------------------------
if analyze_click:
    if not target_company.strip():
        st.warning("⚠️ Please provide a company name to initiate analysis.")
    elif not AUTH_KEY:
        st.error("⚠️ GROQ_API_KEY is missing! Please configure `GROQ_API_KEY` in Streamlit App Settings -> Secrets.")
    else:
        with st.spinner(f"🔍 Mining web data & synthesizing executive intelligence for {target_company}..."):
            search_query = f"{target_company} CEO MD founder products revenue GDP market share"
            search_data = search_company_fast(search_query, max_results=5)

            system_instruction = """
            You are a Principal Industrial Advisor and Corporate Intelligence Analyst.
            Generate an executive-grade corporate dossier for the requested organization.
            You must provide clean, high-density factual insights without broken Markdown tables or raw HTML tags like <br>.
            Format each section strictly with the headers specified so that the user receives an elegant briefing report.
            """

            prompt = f"""
            Analyze '{target_company}' thoroughly using this web context and your factual knowledge:

            WEB SEARCH CONTEXT:
            {search_data}

            Structure the response using exactly the following Markdown section titles:

            ## 🏛️ Executive Snapshot
            * **Official Name**: [Registered Legal Name]
            * **Founded**: [Year of establishment]
            * **Founders**: [Names of Key Founders]
            * **Corporate Headquarters**: [City, State/Country]
            * **Leadership**: **Chief Executive Officer (CEO):** [Name] | **Managing Director / Chairperson:** [Name]
            * **Market Capitalization / Listing Status**: [Listing details, Ticker, Exchange, or Private Status]

            ## 🧭 Corporate Positioning & Vision
            [Provide a 2-3 paragraph deep dive on the company's identity, core mission, historical evolution, and current competitive stance in the sector.]

            ## 📦 Core Industrial & Consumer Offerings
            * **[Core Business Unit 1]**: Detailed breakdown of products, technology platform, and target market.
            * **[Core Business Unit 2]**: Detailed breakdown of products, technology platform, and target market.
            * **[Core Business Unit 3]**: Detailed breakdown of products, technology platform, and target market.
            * **[Core Business Unit 4]**: Additional revenue line or B2B infrastructure division.

            ## 🎯 Strategic Moats & Technology Horizon
            * **Competitive Moat**: Proprietary logistics, patents, high switching costs, or network effects.
            * **R&D & Technology Investments**: AI adoption, automation, clean energy/decarbonization, and next-gen tech bets.
            * **Regional & Global Expansion**: Domestic penetration targets (Tier 2/3 cities) and global footprint.

            ## 🌍 Macroeconomic Footprint & Contribution to GDP
            * **Annual Turnover & Financial Scale**: Latest annual revenue, operating profit margins, and fiscal valuation.
            * **Employment Multiplier**: Direct corporate workforce figures and the indirect job ecosystem (e.g., vendors, logistics, gig workers, supply chain).
            * **Sovereign GDP & Tax Impact**: Contribution to domestic manufacturing/services GDP, export earnings, GST, and corporate tax payments.
            * **Supply Chain & Industrial Infrastructure**: Dependency on domestic industrial estates, warehousing/dark stores, ports, and critical component vendors.
            """

            try:
                client = Groq(api_key=AUTH_KEY)
                active_models = get_available_groq_models(client)

                raw_output = ""
                for model_id in active_models:
                    try:
                        resp = client.chat.completions.create(
                            model=model_id,
                            messages=[
                                {"role": "system", "content": system_instruction},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.25
                        )
                        raw_output = resp.choices[0].message.content
                        if raw_output:
                            break
                    except Exception:
                        continue

                if not raw_output:
                    st.error("⚠️ Unable to complete intelligence generation across active model clusters. Please try again.")
                else:
                    # Parse sections cleanly for interactive tab view
                    sections = {
                        "Snapshot": "",
                        "Positioning": "",
                        "Offerings": "",
                        "Strategy": "",
                        "Macro & GDP": ""
                    }

                    # Segment the text based on headings
                    parts = raw_output.split("## ")
                    for p in parts:
                        if "Executive Snapshot" in p:
                            sections["Snapshot"] = p.replace("Executive Snapshot", "").strip()
                        elif "Corporate Positioning" in p:
                            sections["Positioning"] = p.replace("Corporate Positioning & Vision", "").strip()
                        elif "Core Industrial & Consumer Offerings" in p:
                            sections["Offerings"] = p.replace("Core Industrial & Consumer Offerings", "").strip()
                        elif "Strategic Moats & Technology Horizon" in p:
                            sections["Strategy"] = p.replace("Strategic Moats & Technology Horizon", "").strip()
                        elif "Macroeconomic Footprint" in p:
                            sections["Macro & GDP"] = p.replace("Macroeconomic Footprint & Contribution to GDP", "").strip()

                    # Render Interactive Tabs
                    st.markdown(f"### 🏢 {target_company.strip().title()} — Corporate Intelligence Briefing")
                    
                    tab1, tab2, tab3, tab4 = st.tabs([
                        "🏛️ Executive Snapshot & Vision",
                        "📦 Core Offerings & Units",
                        "🎯 Moats & Tech Strategy",
                        "🌍 Macro & GDP Contribution"
                    ])

                    with tab1:
                        st.markdown('<div class="dossier-container">', unsafe_allow_html=True)
                        st.markdown("#### 🏛️ Governance & Executive Identification")
                        st.markdown(sections["Snapshot"] if sections["Snapshot"] else "Data unavailable.")
                        st.markdown("---")
                        st.markdown("#### 🧭 Corporate Mission & Core Positioning")
                        st.markdown(sections["Positioning"] if sections["Positioning"] else "Data unavailable.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab2:
                        st.markdown('<div class="dossier-container">', unsafe_allow_html=True)
                        st.markdown("#### 📦 Product Portfolio & Commercial Divisions")
                        st.markdown(sections["Offerings"] if sections["Offerings"] else "Data unavailable.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab3:
                        st.markdown('<div class="dossier-container">', unsafe_allow_html=True)
                        st.markdown("#### 🎯 Competitive Advantage & Horizon Bets")
                        st.markdown(sections["Strategy"] if sections["Strategy"] else "Data unavailable.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    with tab4:
                        st.markdown('<div class="dossier-container">', unsafe_allow_html=True)
                        st.markdown("#### 🌍 Macroeconomic Footprint, Employment & Tax Contribution")
                        st.markdown(sections["Macro & GDP"] if sections["Macro & GDP"] else "Data unavailable.")
                        st.markdown('</div>', unsafe_allow_html=True)

                    # Export options
                    st.download_button(
                        label="📥 Export Dossier (.txt)",
                        data=raw_output,
                        file_name=f"{target_company.lower().replace(' ', '_')}_intelligence_dossier.txt",
                        mime="text/plain"
                    )

            except Exception as e:
                st.error(f"⚠️ Intelligence Engine Notice: {e}")
