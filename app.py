import streamlit as st
import time

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-dark:  #0a0f1e;
    --bg-card:  #111827;
    --accent:   #6c63ff;
    --accent2:  #a78bfa;
    --accent3:  #38bdf8;
    --green:    #10b981;
    --red:      #f43f5e;
    --muted:    #94a3b8;
    --border:   rgba(108,99,255,0.2);
    --glow:     0 0 40px rgba(108,99,255,0.15);
}
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-dark) !important;
    font-family: 'Inter', sans-serif !important;
    color: #f1f5f9 !important;
}
[data-testid="stSidebar"] {
    background: #0d1424 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* Hero */
.hero-banner {
    background: linear-gradient(135deg, #1a0533 0%, #0f172a 40%, #0c1a3d 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 44px 40px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
}
.hero-banner::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:300px; height:300px;
    background:radial-gradient(circle,rgba(108,99,255,.18) 0%,transparent 70%);
}
.hero-banner::after {
    content:''; position:absolute; bottom:-40px; left:-40px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(56,189,248,.12) 0%,transparent 70%);
}
.hero-badge {
    display:inline-block;
    background:rgba(108,99,255,.15);
    border:1px solid rgba(108,99,255,.4);
    color:var(--accent2);
    font-size:.72rem; font-weight:600;
    letter-spacing:.1em; text-transform:uppercase;
    padding:4px 12px; border-radius:999px; margin-bottom:14px;
}
.hero-title {
    font-size:2.6rem; font-weight:800;
    background:linear-gradient(135deg,#a78bfa,#6c63ff,#38bdf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin:0 0 8px; line-height:1.2;
}
.hero-sub { font-size:1rem; color:var(--muted); margin:0; }

/* Step cards */
.step-card {
    border-radius:14px; padding:18px 20px; margin-bottom:10px;
    border:1px solid transparent; position:relative; overflow:hidden;
}
.step-idle    { background:var(--bg-card); border-color:rgba(148,163,184,.12); }
.step-running {
    background:linear-gradient(135deg,#1a1040 0%,#111827 100%);
    border-color:var(--accent);
    box-shadow:0 0 24px rgba(108,99,255,.25);
    animation: pulseB 1.8s ease-in-out infinite;
}
.step-done  { background:linear-gradient(135deg,#0a2218 0%,#111827 100%); border-color:rgba(16,185,129,.5); }
.step-error { background:linear-gradient(135deg,#200a14 0%,#111827 100%); border-color:rgba(244,63,94,.5); }
@keyframes pulseB {
    0%,100%{box-shadow:0 0 20px rgba(108,99,255,.2);}
    50%    {box-shadow:0 0 40px rgba(108,99,255,.55);}
}
.step-header { display:flex; align-items:center; gap:12px; }
.step-icon {
    font-size:1.3rem; width:40px; height:40px;
    display:flex; align-items:center; justify-content:center;
    border-radius:10px; flex-shrink:0;
}
.icon-idle    { background:rgba(148,163,184,.08); }
.icon-running { background:rgba(108,99,255,.18); }
.icon-done    { background:rgba(16,185,129,.15); }
.icon-error   { background:rgba(244,63,94,.15); }
.step-label { font-size:.95rem; font-weight:600; }
.label-idle    { color:#f1f5f9; }
.label-running { color:var(--accent2); }
.label-done    { color:var(--green); }
.label-error   { color:var(--red); }
.step-badge {
    margin-left:auto; font-size:.68rem; font-weight:700;
    letter-spacing:.08em; text-transform:uppercase;
    padding:3px 10px; border-radius:999px;
}
.badge-idle    { background:rgba(148,163,184,.1);  color:var(--muted); }
.badge-running { background:rgba(108,99,255,.2);   color:var(--accent2); }
.badge-done    { background:rgba(16,185,129,.15);  color:var(--green); }
.badge-error   { background:rgba(244,63,94,.15);   color:var(--red); }
.step-desc { font-size:.8rem; color:var(--muted); margin:6px 0 0 52px; line-height:1.5; }

/* Results */
.result-wrap {
    background:var(--bg-card); border:1px solid var(--border);
    border-radius:16px; padding:22px; box-shadow:var(--glow);
}
.result-title { font-size:1.05rem; font-weight:700; margin-bottom:12px; }
.box-blue   { background:#0d1424; border:1px solid rgba(56,189,248,.15); border-radius:10px; padding:20px; font-size:.88rem; line-height:1.8; color:#e2e8f0; max-height:560px; overflow-y:auto; white-space:pre-wrap; }
.box-purple { background:#0d1424; border:1px solid rgba(108,99,255,.12); border-radius:10px; padding:16px; font-size:.86rem; line-height:1.75; color:#cbd5e1; max-height:340px; overflow-y:auto; white-space:pre-wrap; }
.box-amber  { background:#0d1424; border:1px solid rgba(245,158,11,.12); border-radius:10px; padding:16px; font-size:.86rem; line-height:1.75; color:#fde68a; max-height:340px; overflow-y:auto; white-space:pre-wrap; }
.box-green  { background:linear-gradient(135deg,#0a1f14,#0d1424); border:1px solid rgba(16,185,129,.2); border-radius:10px; padding:16px; font-size:.86rem; line-height:1.75; color:#a7f3d0; max-height:340px; overflow-y:auto; white-space:pre-wrap; }
.box-blue::-webkit-scrollbar,.box-purple::-webkit-scrollbar,
.box-amber::-webkit-scrollbar,.box-green::-webkit-scrollbar { width:5px; }
.box-blue::-webkit-scrollbar-thumb,.box-purple::-webkit-scrollbar-thumb,
.box-amber::-webkit-scrollbar-thumb,.box-green::-webkit-scrollbar-thumb
{ background:rgba(108,99,255,.3); border-radius:3px; }

/* stat chips */
.stat-row { display:flex; gap:10px; flex-wrap:wrap; margin-top:14px; }
.stat-chip { background:rgba(108,99,255,.1); border:1px solid rgba(108,99,255,.25); border-radius:8px; padding:7px 13px; font-size:.78rem; color:var(--accent2); }
.stat-chip b { color:#f1f5f9; }

/* Streamlit overrides */
div[data-testid="stTextInput"] input {
    background:#111827!important; border:1px solid rgba(108,99,255,.35)!important;
    border-radius:10px!important; color:#f1f5f9!important;
    font-family:'Inter',sans-serif!important; font-size:1rem!important;
    padding:12px 16px!important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:var(--accent)!important;
    box-shadow:0 0 0 3px rgba(108,99,255,.15)!important;
}
div[data-testid="stButton"]>button {
    background:linear-gradient(135deg,#6c63ff,#4f46e5)!important;
    color:#fff!important; border:none!important; border-radius:10px!important;
    font-size:1rem!important; font-weight:600!important; width:100%!important;
    padding:12px 28px!important; font-family:'Inter',sans-serif!important;
    box-shadow:0 4px 24px rgba(108,99,255,.35)!important;
    transition:all .25s!important;
}
div[data-testid="stButton"]>button:hover { box-shadow:0 6px 32px rgba(108,99,255,.55)!important; }
div[data-testid="stButton"]>button:disabled {
    background:rgba(108,99,255,.25)!important; box-shadow:none!important;
}
.stTabs [data-baseweb="tab-list"] { background:transparent!important; }
.stTabs [data-baseweb="tab"] { background:rgba(108,99,255,.08)!important; border-radius:8px!important; color:var(--muted)!important; }
.stTabs [aria-selected="true"] { background:rgba(108,99,255,.25)!important; color:#f1f5f9!important; }
</style>
""", unsafe_allow_html=True)


# ─── Session state ────────────────────────────────────────────────────────────
for k, v in {
    "results": {}, "history": [], "topic": "",
    "elapsed": 0.0, "done": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Helpers ──────────────────────────────────────────────────────────────────
STEPS = {
    1: ("🔍", "Search Agent",  "Querying the web for recent, reliable information."),
    2: ("📖", "Reader Agent",  "Scraping the most relevant URL for deep content."),
    3: ("✍️", "Writer Agent",  "Drafting a comprehensive research report."),
    4: ("🧐", "Critic Agent",  "Reviewing report quality and giving feedback."),
}

def card(icon, label, desc, status):
    badge = {"idle":"badge-idle","running":"badge-running","done":"badge-done","error":"badge-error"}[status]
    btxt  = {"idle":"Waiting","running":"Running…","done":"Done ✓","error":"Error ✗"}[status]
    return f"""
    <div class="step-card step-{status}">
        <div class="step-header">
            <div class="step-icon icon-{status}">{icon}</div>
            <div class="step-label label-{status}">{label}</div>
            <span class="step-badge {badge}">{btxt}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>"""


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:18px 0 22px'>
        <div style='font-size:2.2rem'>🔬</div>
        <div style='font-size:1.05rem;font-weight:700;color:#a78bfa;margin-top:6px'>ResearchMind</div>
        <div style='font-size:.7rem;color:#475569;letter-spacing:.08em;text-transform:uppercase'>Multi-Agent AI</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#64748b;border-bottom:1px solid rgba(108,99,255,.2);padding-bottom:8px;margin-bottom:12px">Pipeline Overview</div>', unsafe_allow_html=True)
    for icon, label, desc in STEPS.values():
        st.markdown(f"""
        <div style='display:flex;gap:10px;align-items:flex-start;margin-bottom:9px;
             background:rgba(108,99,255,.05);border:1px solid rgba(108,99,255,.12);
             border-radius:8px;padding:9px 11px'>
            <span style='font-size:1rem'>{icon}</span>
            <div>
                <div style='font-size:.82rem;font-weight:600;color:#e2e8f0'>{label}</div>
                <div style='font-size:.72rem;color:#64748b'>{desc[:44]}…</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#64748b;border-bottom:1px solid rgba(108,99,255,.2);padding-bottom:8px;margin-bottom:12px;margin-top:18px">Recent Searches</div>', unsafe_allow_html=True)
    if not st.session_state["history"]:
        st.markdown('<div style="font-size:.78rem;color:#475569;text-align:center;padding:14px 0">No searches yet.</div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(st.session_state["history"]):
            lbl = f"🕐 {item['topic'][:24]}…" if len(item['topic']) > 24 else f"🕐 {item['topic']}"
            if st.button(lbl, key=f"h{i}", use_container_width=True):
                st.session_state["results"] = item["results"]
                st.session_state["topic"]   = item["topic"]
                st.session_state["done"]    = True
                st.rerun()


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">✨ Powered by LangGraph + Google Gemini</div>
    <div class="hero-title">ResearchMind AI</div>
    <div class="hero-sub">A four-agent pipeline that searches, reads, writes and critiques — so you don't have to.</div>
</div>""", unsafe_allow_html=True)


# ─── Layout ───────────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.35], gap="large")

with left:
    st.markdown("#### 🎯 Research Topic")
    topic_input = st.text_input("topic", label_visibility="collapsed",
                                placeholder="e.g. Quantum computing breakthroughs")

    run_clicked = st.button("🚀  Launch Research Pipeline",
                            disabled=not topic_input.strip())

    st.markdown("#### 🤖 Agent Pipeline")
    placeholders = {i: st.empty() for i in range(1, 5)}

    for i, (icon, label, desc) in STEPS.items():
        placeholders[i].markdown(card(icon, label, desc, "idle"), unsafe_allow_html=True)

    stats_ph = st.empty()

with right:
    result_ph = st.empty()

    def show_results(results, topic):
        with result_ph.container():
            tab_r, tab_s, tab_sc, tab_f = st.tabs(
                ["📄 Report", "🔍 Search Results", "📖 Scraped Content", "🧐 Critic Feedback"])
            with tab_r:
                st.markdown('<div class="result-wrap"><div class="result-title" style="color:#38bdf8">📄 Research Report</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="box-blue">{results.get("report","—")}</div></div>', unsafe_allow_html=True)
                st.download_button("⬇️ Download Report", data=results.get("report",""),
                                   file_name=f"report_{topic[:28].replace(' ','_')}.txt",
                                   mime="text/plain", use_container_width=True)
            with tab_s:
                st.markdown('<div class="result-wrap"><div class="result-title" style="color:#a78bfa">🔍 Raw Search Results</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="box-purple">{results.get("search_results","—")}</div></div>', unsafe_allow_html=True)
            with tab_sc:
                st.markdown('<div class="result-wrap"><div class="result-title" style="color:#f59e0b">📖 Scraped Web Content</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="box-amber">{results.get("scraped_content","—")}</div></div>', unsafe_allow_html=True)
            with tab_f:
                st.markdown('<div class="result-wrap"><div class="result-title" style="color:#10b981">🧐 Critic Feedback</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="box-green">{results.get("feedback","—")}</div></div>', unsafe_allow_html=True)

    if st.session_state["done"] and st.session_state["results"]:
        show_results(st.session_state["results"], st.session_state["topic"])
    else:
        result_ph.markdown("""
        <div style='text-align:center;padding:80px 20px;
             background:rgba(15,23,42,.5);border:1px dashed rgba(108,99,255,.2);
             border-radius:16px;color:#475569'>
            <div style='font-size:3rem;margin-bottom:14px'>🧠</div>
            <div style='font-size:1.1rem;font-weight:600;color:#64748b'>Ready to Research</div>
            <div style='font-size:.84rem;margin-top:8px'>
                Enter a topic on the left and click <strong style="color:#a78bfa">Launch Research Pipeline</strong>.
            </div>
        </div>""", unsafe_allow_html=True)


# ─── Run pipeline (synchronous) ───────────────────────────────────────────────
if run_clicked and topic_input.strip():
    topic = topic_input.strip()
    st.session_state["done"] = False
    st.session_state["results"] = {}
    st.session_state["topic"] = topic

    results = {}
    start = time.time()
    error_msg = None
    current_step = None

    result_ph.markdown("""
    <div style='text-align:center;padding:80px 20px;color:#475569'>
        <div style='font-size:3rem;margin-bottom:14px'>⚙️</div>
        <div style='font-size:1.1rem;font-weight:600;color:#94a3b8'>Pipeline is running…</div>
        <div style='font-size:.84rem;margin-top:8px'>Results will appear here once all agents finish.</div>
    </div>""", unsafe_allow_html=True)

    def set_step(step_id, status):
        icon, label, desc = STEPS[step_id]
        placeholders[step_id].markdown(card(icon, label, desc, status), unsafe_allow_html=True)

    try:
        from agents import build_research_agent, build_reader_agent, writer_chain, critic_chain

        # ── Step 1: Search ──────────────────────────────
        current_step = 1
        set_step(1, "running")
        search_agent = build_research_agent()
        sr = search_agent.invoke({"messages": [
            ("user", f"Find recent, reliable and detailed information about: {topic}")
        ]})
        results["search_results"] = sr["messages"][-1].content
        set_step(1, "done")

        # ── Step 2: Reader ──────────────────────────────
        current_step = 2
        set_step(2, "running")
        reader_agent = build_reader_agent()
        
        search_summary = results['search_results'][:2000]
        
        rr = reader_agent.invoke({"messages": [(
            "user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{search_summary}"
        )]})
        results["scraped_content"] = rr["messages"][-1].content
        set_step(2, "done")

        # ── Step 3: Writer ──────────────────────────────
        current_step = 3
        set_step(3, "running")
        
        trimmed_search = results['search_results'][:4000]
        trimmed_scraped = results['scraped_content'][:4000]
        combined = (f"SEARCH RESULT:\n{trimmed_search}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{trimmed_scraped}")

        results["report"] = writer_chain.invoke({"topic": topic, "research": combined})
        set_step(3, "done")

        # ── Step 4: Critic ──────────────────────────────
        current_step = 4
        set_step(4, "running")
        results["feedback"] = critic_chain.invoke({"report": results["report"][:4000]})
        set_step(4, "done")
        current_step = None

    except ImportError as e:
        error_msg = (f"**Import Error:** Could not import from `agents.py`.\n\n"
                     f"Make sure `app.py` is in the **same folder** as `agents.py`.\n\n"
                     f"Details: `{e}`")
        if current_step:
            set_step(current_step, "error")

    except Exception as e:
        error_msg = f"**Pipeline Error:** `{type(e).__name__}: {e}`"
        if current_step:
            set_step(current_step, "error")

    elapsed = round(time.time() - start, 1)

    if error_msg:
        result_ph.error(error_msg, icon="🚨")
    else:
        st.session_state["results"] = results
        st.session_state["elapsed"] = elapsed
        st.session_state["done"] = True
        st.session_state["history"].insert(0, {
            "topic": topic, "time": time.strftime("%H:%M"), "results": dict(results)
        })
        st.session_state["history"] = st.session_state["history"][:10]

        stats_ph.markdown(f"""
        <div class="stat-row">
            <div class="stat-chip">⏱ Time <b>{elapsed}s</b></div>
            <div class="stat-chip">🤖 Agents <b>4</b></div>
            <div class="stat-chip">✅ Status <b>Complete</b></div>
        </div>""", unsafe_allow_html=True)

        show_results(results, topic)
