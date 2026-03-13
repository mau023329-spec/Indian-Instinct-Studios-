"""
Indian Instincts Studios — Full Streamlit Website
v7: Dark/light mode · Analytics · Pin reviews · Draft mode · Released→changelog
     Reorder products · Pulse dot · Confetti · Comparison table · Share review
     Contact form · Social footer · Built with IIS watermark
Run with: streamlit run app_v7_full.py
"""

import streamlit as st
import datetime

# ─────────────────────────────────────────────
# ADMIN PASSWORD
# ─────────────────────────────────────────────
ADMIN_PASSWORD = "iis2024"

# ─────────────────────────────────────────────
# SESSION STATE BOOTSTRAP
# ─────────────────────────────────────────────
def _init():
    defaults = {
        "admin_logged_in": False,
        "dark_mode": True,
        "votes": {"Meal Nutrition Calculator": 42, "Pantry Scanner": 31,
                  "Weekly Meal Planner": 58, "Recipe Sharing Community": 19,
                  "Multi-Language Support": 27},
        "voted": set(),
        "reviews": [
            {"name": "Priya S.",  "product": "KitchenMate", "rating": 5, "pinned": True,
             "text": "This app has completely changed how I cook. I just throw in whatever's left in my fridge and boom — a real recipe!"},
            {"name": "Arjun M.", "product": "KitchenMate", "rating": 5, "pinned": False,
             "text": "Super simple to use and the recipes are genuinely delicious. Can't wait for the nutrition calculator!"},
            {"name": "Divya K.", "product": "KitchenMate", "rating": 4, "pinned": False,
             "text": "Great concept and clean UI. Would love a meal planning feature next."},
            {"name": "Rohan T.", "product": "KitchenMate", "rating": 5, "pinned": False,
             "text": "The fastest way to decide what to cook. Brilliant little tool."},
        ],
        "contact_messages": [],
        "launch_date": datetime.datetime(2026, 3, 18, 12, 0, 0),
        "launch_label": "🧠 SankalpRoom — Public Launch",
        "live_products": [
            {
                "emoji": "🍳", "name": "KitchenMate", "subtitle": "AI Kitchen Assistant",
                "version": "v1.2", "url": "https://kitchenmate.streamlit.app",
                "draft": False,
                "description": "An AI-powered cooking assistant that generates recipes based on the ingredients you have. No more food waste, no more meal-planning anxiety.",
                "features": ["AI recipe generation from your ingredients",
                             "Ingredient-based smart cooking suggestions",
                             "Simple, distraction-free UI",
                             "Quick recipe suggestions (under 5 seconds)",
                             "Dietary preference filters"],
                "stats": {"Active Users": "2,841", "Recipes Generated": "14,320", "Avg. Rating": "4.8 ⭐"},
            }
        ],
        "coming_soon_products": [
            {
                "emoji": "🧠", "name": "SankalpRoom",
                "description": "A public AI-powered team collaboration app where ideas are brainstormed in a central decision space, voted on democratically, and automatically broken down into focused subgroups for execution. AI acts as both a thinking partner and workflow coordinator — helping teams move from discussion to delivery faster.",
            }
        ],
        "roadmap": [
            {"emoji": "🧮", "title": "Meal Nutrition Calculator",
             "desc": "Automatically calculate calories, macros, and nutrients for any recipe.", "status": "In Progress"},
            {"emoji": "📸", "title": "Pantry Scanner",
             "desc": "Use your phone camera to scan ingredients in your fridge — no typing required.", "status": "Planned"},
            {"emoji": "📅", "title": "Weekly Meal Planner",
             "desc": "Generate a full 7-day meal plan based on dietary preferences and budget.", "status": "Planned"},
            {"emoji": "👥", "title": "Recipe Sharing Community",
             "desc": "Share AI-generated recipes and discover what others are cooking.", "status": "Testing"},
            {"emoji": "🌐", "title": "Multi-Language Support",
             "desc": "Use KitchenMate in Hindi, Tamil, Telugu, and other Indian languages.", "status": "Planned"},
        ],
        "updates": [
            {"version": "KitchenMate v1.2", "date": "February 2025", "tag": "Latest", "tag_badge": "badge-live",
             "items": ["Faster AI recipe generation — results in under 3 seconds",
                       "Redesigned UI with improved readability",
                       "Added clear button to reset ingredient list",
                       "Better mobile responsiveness",
                       "Improved AI prompt for Indian recipes"]},
            {"version": "KitchenMate v1.1", "date": "December 2024", "tag": "Stable", "tag_badge": "badge-prog",
             "items": ["Better ingredient detection and parsing", "Cleaner recipe card layout",
                       "Added vegetarian/non-vegetarian filter", "40% faster load time"]},
            {"version": "KitchenMate v1.0", "date": "October 2024", "tag": "Launch", "tag_badge": "badge-plan",
             "items": ["Initial launch of KitchenMate", "Core ingredient-based recipe generation",
                       "Basic UI with recipe display", "Integrated Claude AI"]},
        ],
        "social_links": {"Twitter/X": "", "LinkedIn": "", "GitHub": "", "Product Hunt": ""},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ─────────────────────────────────────────────
# THEME TOKENS
# ─────────────────────────────────────────────
DARK = {
    "bg": "#0a0a0f", "bg2": "#0f0f18", "bg3": "#13131f",
    "border": "#1e1e2e", "border2": "#2a1a3e",
    "text": "#e8e6e1", "text2": "#a09fa6", "text3": "#6e6d74",
    "heading": "#f0ede8", "accent": "#ff6b35",
    "tab_bg": "#0f0f18", "card_hover": "#ff6b35",
}
LIGHT = {
    "bg": "#f8f7f4", "bg2": "#ffffff", "bg3": "#f0ede8",
    "border": "#e0ddd8", "border2": "#d0ccc6",
    "text": "#1a1a2e", "text2": "#4a4a5a", "text3": "#8a8a9a",
    "heading": "#0a0a1a", "accent": "#e85a20",
    "tab_bg": "#ffffff", "card_hover": "#e85a20",
}
T = DARK if st.session_state.dark_mode else LIGHT

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Instincts Studios",
    page_icon="🪔", layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {T['bg']} !important;
    color: {T['text']};
}}
h1,h2,h3,h4 {{ font-family: 'Sora', sans-serif; color: {T['heading']}; }}

/* ── tabs ── */
div[data-testid="stTabs"] > div:first-child {{
    background: {T['tab_bg']};
    border-bottom: 1px solid {T['border']};
    padding: 0 8px; border-radius: 14px 14px 0 0;
}}
div[data-testid="stTabs"] button[role="tab"] {{
    font-family: 'Sora', sans-serif !important; font-size: 0.82rem !important;
    font-weight: 600 !important; letter-spacing: 0.05em !important;
    text-transform: uppercase !important; color: {T['text3']} !important;
    padding: 14px 18px !important; border: none !important;
    background: transparent !important; border-radius: 0 !important;
    transition: color 0.2s !important;
}}
div[data-testid="stTabs"] button[role="tab"]:hover {{ color: {T['heading']} !important; }}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    color: {T['accent']} !important;
    border-bottom: 2px solid {T['accent']} !important;
}}

/* ── cards ── */
.card {{
    background: {T['bg3']}; border: 1px solid {T['border']};
    border-radius: 16px; padding: 28px 24px; margin-bottom: 18px;
    transition: border-color 0.25s;
}}
.card:hover {{ border-color: {T['card_hover']}; }}

/* ── hero ── */
.hero-wrap {{
    background: {'linear-gradient(135deg, #0f0f18 0%, #1a0a2e 50%, #0d1a2e 100%)' if st.session_state.dark_mode else 'linear-gradient(135deg, #fff8f4 0%, #ffe8d6 50%, #f0f4ff 100%)'};
    border-radius: 24px; padding: 56px 48px;
    border: 1px solid {T['border']}; margin-bottom: 40px;
    position: relative; overflow: hidden;
}}
.hero-wrap::before {{
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(255,107,53,0.12) 0%, transparent 70%);
    border-radius: 50%;
}}
.hero-title {{
    font-family: 'Sora', sans-serif;
    font-size: clamp(1.75rem, 5vw, 3.2rem);
    font-weight: 800; line-height: 1.15;
    background: linear-gradient(135deg, {T['heading']} 30%, {T['accent']} 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 12px;
}}
.hero-tag {{
    font-family: 'Sora', sans-serif;
    font-size: clamp(0.95rem, 2.5vw, 1.2rem);
    color: {T['accent']}; font-weight: 600; margin-bottom: 18px;
}}
.hero-desc {{
    color: {T['text2']}; font-size: clamp(0.88rem, 2vw, 1rem);
    line-height: 1.7; max-width: 540px; margin-bottom: 28px;
}}

/* ── badges ── */
.badge {{
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.07em;
    text-transform: uppercase; margin-right: 6px;
}}
.badge-live {{ background: #0d2b1d; color: #34d399; border: 1px solid #34d399; }}
.badge-plan {{ background: #1e1a0d; color: #fbbf24; border: 1px solid #fbbf24; }}
.badge-prog {{ background: #0d1a2e; color: #60a5fa; border: 1px solid #60a5fa; }}
.badge-test {{ background: #1e0d1a; color: #c084fc; border: 1px solid #c084fc; }}
.badge-soon {{ background: #1a0a2e; color: #a78bfa; border: 1px solid #a78bfa; }}
.badge-draft {{ background: #1a1a0d; color: #facc15; border: 1px solid #facc15; }}

/* ── pulse dot (In Progress) ── */
@keyframes pulse {{
    0%,100% {{ opacity:1; transform:scale(1); }}
    50% {{ opacity:0.5; transform:scale(1.4); }}
}}
.pulse-dot {{
    display: inline-block; width: 8px; height: 8px;
    background: #60a5fa; border-radius: 50%; margin-right: 6px;
    animation: pulse 1.6s ease-in-out infinite;
    vertical-align: middle;
}}

/* ── pinned review spotlight ── */
.pinned-card {{
    background: {'linear-gradient(135deg,#1a0a2e,#0d1a0d)' if st.session_state.dark_mode else 'linear-gradient(135deg,#fff3ee,#f0fff4)'};
    border: 1px solid {T['accent']}; border-radius: 20px;
    padding: 28px; margin-bottom: 20px; position: relative;
}}
.pin-crown {{
    position: absolute; top: -12px; left: 24px;
    background: {T['accent']}; color: #0a0a0f;
    font-family: 'Sora', sans-serif; font-size: 0.65rem; font-weight: 700;
    padding: 3px 10px; border-radius: 20px; letter-spacing: 0.1em;
    text-transform: uppercase;
}}

/* ── stat box ── */
.stat-box {{
    background: {T['bg3']}; border: 1px solid {T['border']};
    border-radius: 16px; padding: 28px 20px; text-align: center;
}}
.stat-num {{ font-family: 'Sora', sans-serif; font-size: 2.4rem; font-weight: 800; color: {T['accent']}; }}
.stat-lbl {{ color: {T['text3']}; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }}

/* ── countdown ── */
.cd-wrap {{
    background: {'linear-gradient(135deg,#13131f,#1a0a2e)' if st.session_state.dark_mode else 'linear-gradient(135deg,#fff3ee,#f0f4ff)'};
    border: 1px solid {T['border2']}; border-radius: 20px;
    padding: 40px 32px; text-align: center; margin: 32px 0;
}}
.cd-num {{ font-family: 'Sora', sans-serif; font-size: 3rem; font-weight: 800; color: {T['accent']}; display: block; }}
.cd-unit {{ color: {T['text3']}; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; }}

/* ── review card ── */
.review-card {{
    background: {T['bg3']}; border: 1px solid {T['border']};
    border-radius: 16px; padding: 24px; margin-bottom: 16px;
}}
.review-card.love {{ border-color: {T['accent']}; }}
.stars {{ color: {T['accent']}; font-size: 1.1rem; }}
.reviewer {{ font-weight: 600; font-size: 0.9rem; color: {T['heading']}; }}
.review-text {{ color: {T['text2']}; font-size: 0.92rem; line-height: 1.6; margin-top: 8px; }}

/* ── update card ── */
.update-card {{
    background: {T['bg3']}; border-left: 3px solid {T['accent']};
    border-radius: 0 14px 14px 0; padding: 24px 24px 24px 28px; margin-bottom: 20px;
}}
.update-ver {{ font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 700; color: {T['heading']}; }}
.update-date {{ color: {T['text3']}; font-size: 0.78rem; margin-top: 2px; margin-bottom: 12px; }}
.update-item {{ color: {T['text2']}; font-size: 0.9rem; line-height: 1.7; }}
.update-item::before {{ content: "→ "; color: {T['accent']}; }}

/* ── section labels ── */
.sec-header {{
    font-family: 'Sora', sans-serif; font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.16em; text-transform: uppercase; color: {T['accent']}; margin-bottom: 6px;
}}
.sec-title {{
    font-family: 'Sora', sans-serif; font-size: 2rem; font-weight: 700;
    color: {T['heading']}; margin-bottom: 28px;
}}

.feat-item {{ color: {T['text2']}; font-size: 0.9rem; padding: 6px 0; border-bottom: 1px solid {T['border']}; }}
.feat-item::before {{ content: "✦ "; color: {T['accent']}; }}

.teaser {{
    background: {'repeating-linear-gradient(45deg,#13131f,#13131f 10px,#0f0f18 10px,#0f0f18 20px)' if st.session_state.dark_mode else 'repeating-linear-gradient(45deg,#f8f7f4,#f8f7f4 10px,#f0ede8 10px,#f0ede8 20px)'};
    border: 1px dashed {T['border2']}; border-radius: 16px; padding: 32px; text-align: center;
}}

.div-line {{ border: none; border-top: 1px solid {T['border']}; margin: 36px 0; }}

/* ── comparison table ── */
.comp-table {{ width:100%; border-collapse:collapse; font-size:0.9rem; }}
.comp-table th {{
    background: {T['bg2']}; color: {T['accent']};
    font-family:'Sora',sans-serif; font-weight:700;
    padding: 14px 16px; text-align:left; border-bottom: 2px solid {T['accent']};
}}
.comp-table td {{
    padding: 12px 16px; border-bottom: 1px solid {T['border']};
    color: {T['text2']}; vertical-align:middle;
}}
.comp-table tr:hover td {{ background: {T['bg3']}; }}
.comp-tick {{ color: #34d399; font-size:1.1rem; }}
.comp-cross {{ color: #f87171; font-size:1.1rem; }}

/* ── admin banner ── */
.admin-banner {{
    background: linear-gradient(90deg, #1a0a00, #2a1000);
    border: 1px solid {T['accent']}; border-radius: 12px;
    padding: 14px 20px; margin-bottom: 24px;
    font-family: 'Sora', sans-serif; font-size: 0.85rem; color: {T['accent']};
}}

/* ── analytics card ── */
.ana-card {{
    background: {T['bg3']}; border: 1px solid {T['border']};
    border-radius: 14px; padding: 20px; text-align:center; margin-bottom:12px;
}}
.ana-num {{ font-family:'Sora',sans-serif; font-size:1.8rem; font-weight:800; color:{T['accent']}; }}
.ana-lbl {{ color:{T['text3']}; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; }}

/* ── watermark ── */
.watermark {{
    text-align:center; padding: 32px 0 8px 0;
    font-family:'Sora',sans-serif; font-size:0.75rem;
    color: {T['text3']}; letter-spacing:0.06em;
    border-top: 1px solid {T['border']}; margin-top: 48px;
}}
.watermark a {{ color: {T['accent']}; text-decoration:none; }}

/* ── forms ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: {T['bg3']} !important; border-color: {T['border2']} !important;
    color: {T['text']} !important; border-radius: 10px !important;
}}
.stButton > button {{
    background: {T['accent']} !important; color: #0a0a0f !important;
    font-family: 'Sora', sans-serif !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
    padding: 10px 24px !important; transition: opacity 0.2s !important;
}}
.stButton > button:hover {{ opacity: 0.85 !important; }}
.stButton > button:disabled {{ background: {T['border']} !important; color: {T['text3']} !important; }}

/* ── confetti ── */
@keyframes fall {{
    0%   {{ transform: translateY(-20px) rotate(0deg); opacity:1; }}
    100% {{ transform: translateY(100vh) rotate(720deg); opacity:0; }}
}}
.confetti-piece {{
    position:fixed; width:10px; height:10px; border-radius:2px;
    animation: fall linear forwards;
    z-index: 9999;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
section[data-testid="stSidebar"] {{ display: none; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1100px; }}
</style>
""", unsafe_allow_html=True)

# Confetti JS (fires when show_confetti is set)
if st.session_state.get("show_confetti"):
    st.markdown("""
    <script>
    (function(){
        const colors = ['#ff6b35','#34d399','#60a5fa','#fbbf24','#c084fc','#f472b6'];
        for(let i=0;i<80;i++){
            const el = document.createElement('div');
            el.className = 'confetti-piece';
            el.style.left = Math.random()*100+'vw';
            el.style.background = colors[Math.floor(Math.random()*colors.length)];
            el.style.animationDuration = (Math.random()*2+1.5)+'s';
            el.style.animationDelay = (Math.random()*0.8)+'s';
            el.style.width = el.style.height = (Math.random()*10+6)+'px';
            document.body.appendChild(el);
            setTimeout(()=>el.remove(), 4000);
        }
    })();
    </script>
    """, unsafe_allow_html=True)
    st.session_state.show_confetti = False

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
STATUS_BADGES = {
    "Planned": "badge-plan", "In Progress": "badge-prog",
    "Testing": "badge-test", "Released": "badge-live",
}

def countdown_parts(target):
    delta = target - datetime.datetime.now()
    if delta.total_seconds() > 0:
        d = delta.days; h, rem = divmod(delta.seconds, 3600); m, _ = divmod(rem, 60)
    else:
        d = h = m = 0
    return d, h, m

def render_countdown(label, target):
    d, h, m = countdown_parts(target)
    st.markdown(f"""
    <div class="cd-wrap">
        <div style="font-family:Sora,sans-serif;font-size:1.05rem;color:{T['heading']};margin-bottom:24px;font-weight:600;">⏳ {label}</div>
        <div style="display:flex;justify-content:center;gap:48px;">
            <div style="text-align:center;"><span class="cd-num">{d:02d}</span><span class="cd-unit">Days</span></div>
            <div style="text-align:center;"><span class="cd-num">{h:02d}</span><span class="cd-unit">Hours</span></div>
            <div style="text-align:center;"><span class="cd-num">{m:02d}</span><span class="cd-unit">Minutes</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

def try_button(url, label="🚀 Try Now", full_width=False):
    w = "width:100%;" if full_width else ""
    st.markdown(
        f'<a href="{url}" target="_blank"><button style="background:{T["accent"]};color:#0a0a0f;'
        f'font-family:Sora,sans-serif;font-weight:700;border:none;border-radius:10px;'
        f'padding:10px 24px;cursor:pointer;font-size:0.9rem;{w}">{label}</button></a>',
        unsafe_allow_html=True)

def watermark():
    st.markdown(f"""
    <div class="watermark">
        Built with 🪔 <a href="https://indianinstincts.studio">Indian Instincts Studios</a>
        &nbsp;·&nbsp; © 2026
    </div>""", unsafe_allow_html=True)

def social_footer():
    links = {k: v for k, v in st.session_state.social_links.items() if v.strip()}
    if not links:
        return
    icons = {"Twitter/X": "𝕏", "LinkedIn": "in", "GitHub": "GH", "Product Hunt": "PH"}
    btns = "".join(
        f'<a href="{v}" target="_blank" style="display:inline-block;margin:0 6px;'
        f'padding:6px 14px;border:1px solid {T["border"]};border-radius:8px;'
        f'color:{T["text2"]};font-family:Sora,sans-serif;font-size:0.78rem;font-weight:600;'
        f'text-decoration:none;">{icons.get(k,k)}</a>'
        for k, v in links.items()
    )
    st.markdown(f'<div style="text-align:center;margin-top:16px;">{btns}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────
bar_l, bar_r = st.columns([6, 1])
with bar_l:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:8px 4px 18px 4px;">
        <span style="font-size:1.5rem;">🪔</span>
        <div>
            <span style="font-family:Sora,sans-serif;font-size:1.05rem;font-weight:800;color:{T['heading']};">Indian Instincts Studios</span>
            <span style="margin-left:12px;font-size:0.7rem;color:{T['text3']};text-transform:uppercase;letter-spacing:0.1em;">v1.2 · KitchenMate Live</span>
        </div>
        <span class="badge badge-live" style="margin-left:16px;">● Live</span>
    </div>""", unsafe_allow_html=True)
with bar_r:
    mode_label = "☀️ Light" if st.session_state.dark_mode else "🌙 Dark"
    if st.button(mode_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab_home, tab_products, tab_roadmap, tab_reviews, tab_updates, tab_about, tab_contact, tab_admin = st.tabs([
    "🏠  Home", "📦  Products", "🗺️  Roadmap", "⭐  Reviews",
    "📣  Updates", "ℹ️  About", "✉️  Contact", "🔒  Admin",
])

# ═══════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════
with tab_home:
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-title">Indian Instincts Studios</div>
        <div class="hero-tag">Building smart AI tools for everyday life.</div>
        <div class="hero-desc">
            We are a small product studio obsessed with turning everyday friction into delightful,
            AI-powered tools. From the kitchen to collaboration — we build things people actually use.
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        if st.button("🚀 Explore Products", key="hero_exp"):
            st.info("👇 Head to the **Products** tab above.")
    with c2:
        try_button("https://kitchenmate.streamlit.app", "🍳 Try KitchenMate")

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # ── Pinned review spotlight ──
    pinned = [r for r in st.session_state.reviews if r.get("pinned")]
    if pinned:
        r = pinned[0]
        st.markdown('<div class="sec-header">Featured Review</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="pinned-card">
            <div class="pin-crown">⭐ Featured Review</div>
            <div style="color:{T['accent']};font-size:1.3rem;margin-bottom:8px;">{'⭐'*r['rating']}</div>
            <div style="font-style:italic;color:{T['text2']};font-size:1rem;line-height:1.7;">"{r['text']}"</div>
            <div style="margin-top:14px;display:flex;align-items:center;gap:10px;">
                <div style="width:32px;height:32px;border-radius:50%;background:{T['accent']};
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.8rem;font-weight:700;color:#0a0a0f;">{r['name'][0].upper()}</div>
                <div><div style="font-weight:600;color:{T['heading']};">{r['name']}</div>
                     <div style="color:{T['text3']};font-size:0.75rem;">{r['product']}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # ── Stats ──
    st.markdown('<div class="sec-header">Live Stats</div>', unsafe_allow_html=True)
    visible_live = [p for p in st.session_state.live_products if not p.get("draft")]
    s1,s2,s3,s4 = st.columns(4)
    for col,(num,lbl) in zip([s1,s2,s3,s4],[
        ("2,841","KitchenMate Users"),("14,320","Recipes Generated"),
        (str(len(visible_live)),"Products Live"),
        (str(len(st.session_state.coming_soon_products)),"Coming Soon"),
    ]):
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>',unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # ── Featured product ──
    if visible_live:
        p = visible_live[0]
        st.markdown('<div class="sec-header">Featured Product</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-title">Meet {p["name"]}</div>', unsafe_allow_html=True)
        fc1,fc2 = st.columns(2)
        with fc1:
            feats="".join(f'<div class="feat-item">{f}</div>' for f in p["features"])
            st.markdown(f"""
            <div class="card">
                <span class="badge badge-live">● Live</span>
                <h3 style="margin-top:16px;">{p['emoji']} {p['name']}</h3>
                <p style="color:{T['text2']};line-height:1.7;font-size:0.95rem;">{p['description']}</p>
                <div style="margin-top:20px;">{feats}</div>
            </div>""", unsafe_allow_html=True)
        with fc2:
            st.markdown(f"""
            <div style="background:{'linear-gradient(135deg,#1a0a2e,#0d1a2e)' if st.session_state.dark_mode else 'linear-gradient(135deg,#fff3ee,#f0f4ff)'};
                        border-radius:16px;height:260px;display:flex;align-items:center;
                        justify-content:center;border:1px solid {T['border2']};">
                <div style="text-align:center;">
                    <div style="font-size:4rem;">{p['emoji']}</div>
                    <div style="font-family:Sora,sans-serif;color:{T['accent']};font-weight:700;margin-top:8px;">{p['name']}</div>
                    <div style="color:{T['text3']};font-size:0.8rem;margin-top:4px;">{p['subtitle']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">Next Launch</div>', unsafe_allow_html=True)
    render_countdown(st.session_state.launch_label, st.session_state.launch_date)

    if st.session_state.coming_soon_products:
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
        st.markdown("<div class='sec-header'>What's Next</div>", unsafe_allow_html=True)
        cols = st.columns(min(len(st.session_state.coming_soon_products), 3))
        for col,p in zip(cols,st.session_state.coming_soon_products):
            with col:
                st.markdown(f"""
                <div class="teaser">
                    <div style="font-size:2.5rem;">{p['emoji']}</div>
                    <div style="font-family:Sora,sans-serif;font-weight:700;color:{T['heading']};margin:12px 0 6px;">{p['name']}</div>
                    <div style="color:{T['text3']};font-size:0.85rem;line-height:1.5;">{p['description'][:120]}...</div>
                    <div style="margin-top:16px;"><span class="badge badge-soon">Coming Soon</span></div>
                </div>""", unsafe_allow_html=True)

    social_footer()
    watermark()


# ═══════════════════════════════════════════════════════
# PRODUCTS
# ═══════════════════════════════════════════════════════
with tab_products:
    st.markdown('<div class="sec-header">Our Products</div>', unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>What We've Built</div>", unsafe_allow_html=True)

    visible = [p for p in st.session_state.live_products if not p.get("draft")]
    if not visible:
        st.info("No live products yet.")
    for p in visible:
        c1,c2 = st.columns([3,2])
        with c1:
            feats="".join(f'<div class="feat-item">{f}</div>' for f in p["features"])
            st.markdown(f"""
            <div class="card">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                    <div style="font-size:2.5rem;">{p['emoji']}</div>
                    <div>
                        <div style="font-family:Sora,sans-serif;font-size:1.4rem;font-weight:700;color:{T['heading']};">{p['name']}</div>
                        <div style="color:{T['text3']};font-size:0.82rem;">{p['subtitle']}</div>
                    </div>
                    <span class="badge badge-live" style="margin-left:auto;">● Live</span>
                </div>
                <p style="color:{T['text2']};line-height:1.75;font-size:0.95rem;">{p['description']}</p>
                <div style="margin-top:20px;margin-bottom:4px;font-size:0.75rem;color:{T['text3']};text-transform:uppercase;letter-spacing:0.1em;">Features</div>
                {feats}
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:{'linear-gradient(135deg,#1a0a2e,#0d1a2e)' if st.session_state.dark_mode else 'linear-gradient(135deg,#fff3ee,#f0f4ff)'};
                        border-radius:16px;height:220px;display:flex;align-items:center;
                        justify-content:center;border:1px solid {T['border2']};margin-bottom:16px;">
                <div style="text-align:center;">
                    <div style="font-size:4rem;">{p['emoji']}</div>
                    <div style="font-family:Sora,sans-serif;color:{T['accent']};font-weight:700;margin-top:8px;">{p['name']}</div>
                    <div style="color:{T['text3']};font-size:0.8rem;">{p['version']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            try_button(p["url"], "🚀 Try Now", full_width=True)
            stat_rows="".join(
                f'<div style="display:flex;justify-content:space-between;margin-bottom:8px;">'
                f'<span style="color:{T["text2"]};font-size:0.85rem;">{k}</span>'
                f'<span style="color:{T["accent"]};font-family:Sora,sans-serif;font-weight:700;">{v}</span></div>'
                for k,v in p["stats"].items())
            st.markdown(f"""
            <div style="background:{T['bg3']};border:1px solid {T['border']};border-radius:12px;padding:16px;margin-top:12px;">
                <div style="font-size:0.75rem;color:{T['text3']};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">Product Stats</div>
                {stat_rows}
            </div>""", unsafe_allow_html=True)

    # ── Comparison table ──
    if len(visible) >= 1 and st.session_state.coming_soon_products:
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
        st.markdown('<div class="sec-header">Compare</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Product Comparison</div>', unsafe_allow_html=True)
        p1 = visible[0]
        p2 = st.session_state.coming_soon_products[0]
        rows = [
            ("AI-Powered",        "✅","✅"),
            ("Mobile Friendly",   "✅","✅"),
            ("Free to Use",       "✅","✅"),
            ("Team Collaboration","❌","✅"),
            ("Live Now",          "✅","🔜"),
            ("Recipe Generation", "✅","❌"),
            ("Voting & Decisions","❌","✅"),
        ]
        rows_html="".join(
            f'<tr><td>{r}</td>'
            f'<td style="text-align:center;" class="comp-tick">{a}</td>'
            f'<td style="text-align:center;" class="comp-tick">{b}</td></tr>'
            for r,a,b in rows)
        st.markdown(f"""
        <table class="comp-table">
            <thead><tr>
                <th>Feature</th>
                <th style="text-align:center;">{p1['emoji']} {p1['name']}</th>
                <th style="text-align:center;">{p2['emoji']} {p2['name']}</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)

    if st.session_state.coming_soon_products:
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
        st.markdown('<div class="sec-header">In The Pipeline</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Coming Soon</div>', unsafe_allow_html=True)
        cols=st.columns(min(len(st.session_state.coming_soon_products),3))
        for col,p in zip(cols,st.session_state.coming_soon_products):
            with col:
                st.markdown(f"""
                <div class="card" style="opacity:0.85;">
                    <div style="font-size:2.2rem;margin-bottom:12px;">{p['emoji']}</div>
                    <div style="font-family:Sora,sans-serif;font-size:1.1rem;font-weight:700;color:{T['heading']};margin-bottom:8px;">{p['name']}</div>
                    <p style="color:{T['text2']};font-size:0.88rem;line-height:1.65;">{p['description']}</p>
                    <span class="badge badge-soon" style="margin-top:16px;display:inline-block;">Coming Soon</span>
                </div>""", unsafe_allow_html=True)

    social_footer(); watermark()


# ═══════════════════════════════════════════════════════
# ROADMAP
# ═══════════════════════════════════════════════════════
with tab_roadmap:
    st.markdown('<div class="sec-header">Product Roadmap</div>', unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>What We're Building Next</div>", unsafe_allow_html=True)
    st.markdown(f'<p style="color:{T["text3"]};margin-top:-16px;margin-bottom:28px;font-size:0.9rem;">Vote on features you want to see. Top-voted ideas get built first.</p>',unsafe_allow_html=True)

    for item in st.session_state.roadmap:
        key = item["title"]
        vote_count = st.session_state.votes.get(key, 0)
        already_voted = key in st.session_state.voted
        badge_cls = STATUS_BADGES.get(item["status"], "badge-plan")
        pulse = '<span class="pulse-dot"></span>' if item["status"] == "In Progress" else ""

        col_card, col_vote = st.columns([5,1])
        with col_card:
            st.markdown(f"""
            <div class="card" style="margin-bottom:4px;">
                <div style="display:flex;align-items:flex-start;gap:14px;">
                    <div style="font-size:1.8rem;">{item['emoji']}</div>
                    <div style="flex:1;">
                        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                            {pulse}
                            <span style="font-family:Sora,sans-serif;font-size:1.05rem;font-weight:700;color:{T['heading']};">{item['title']}</span>
                            <span class="badge {badge_cls}">{item['status']}</span>
                        </div>
                        <p style="color:{T['text2']};font-size:0.88rem;line-height:1.6;margin:0;">{item['desc']}</p>
                        <div style="margin-top:10px;font-family:Sora,sans-serif;font-size:1.1rem;font-weight:800;color:{T['accent']};">▲ {vote_count} votes</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col_vote:
            st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
            if already_voted:
                st.button("✓ Voted", key=f"vote_{key}", disabled=True)
            else:
                if st.button("Vote ▲", key=f"vote_{key}"):
                    st.session_state.votes[key] = st.session_state.votes.get(key,0)+1
                    st.session_state.voted.add(key)
                    st.rerun()
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

    social_footer(); watermark()


# ═══════════════════════════════════════════════════════
# REVIEWS
# ═══════════════════════════════════════════════════════
with tab_reviews:
    st.markdown('<div class="sec-header">Community</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Reviews & Feedback</div>', unsafe_allow_html=True)

    with st.expander("✍️ Write a Review", expanded=True):
        with st.form("review_form"):
            r1,r2=st.columns(2)
            with r1:
                name=st.text_input("Your Name")
                product_names=[p["name"] for p in st.session_state.live_products if not p.get("draft")] + \
                              [f"{p['name']} (Coming Soon)" for p in st.session_state.coming_soon_products]
                product=st.selectbox("Product", product_names)
            with r2:
                rating=st.select_slider("Rating",options=[1,2,3,4,5],value=5)
                st.markdown(f"<div style='color:{T['accent']};font-size:1.3rem;margin-top:6px;'>{'⭐'*rating}</div>",unsafe_allow_html=True)
            review_text=st.text_area("Your Review",placeholder="Tell us what you think...",height=110)
            if st.form_submit_button("Submit Review"):
                if name.strip() and review_text.strip():
                    st.session_state.reviews.insert(0,{
                        "name":name.strip(),"product":product,
                        "rating":rating,"text":review_text.strip(),"pinned":False
                    })
                    if rating==5:
                        st.session_state.show_confetti=True
                    st.success("🎉 Thank you for your review!")
                    st.rerun()
                else:
                    st.error("Please fill in your name and review.")

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    love=[r for r in st.session_state.reviews if r["rating"]==5][:5]
    if love:
        st.markdown('<div class="sec-header">Highlights</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">💛 Wall of Love</div>', unsafe_allow_html=True)
        lc1,lc2=st.columns(2)
        for i,rev in enumerate(love):
            with (lc1 if i%2==0 else lc2):
                # Share tweet button
                tweet=f"Just used {rev['product']} by @IndianInstincts — {'⭐'*rev['rating']} \"{rev['text'][:80]}...\" Check it out!"
                st.markdown(f"""
                <div class="review-card love">
                    <div class="stars">{'⭐'*rev['rating']}</div>
                    <div class="review-text" style="margin-top:10px;font-style:italic;">"{rev['text']}"</div>
                    <div style="margin-top:14px;display:flex;align-items:center;justify-content:space-between;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <div style="width:28px;height:28px;border-radius:50%;background:{T['accent']};
                                        display:flex;align-items:center;justify-content:center;
                                        font-size:0.75rem;font-weight:700;color:#0a0a0f;">{rev['name'][0].upper()}</div>
                            <div><div class="reviewer">{rev['name']}</div>
                                 <div style="color:{T['text3']};font-size:0.75rem;">{rev['product']}</div></div>
                        </div>
                        <button onclick="navigator.clipboard.writeText({repr(tweet)});this.textContent='✓ Copied!';"
                            style="background:transparent;border:1px solid {T['border']};border-radius:8px;
                                   padding:4px 10px;cursor:pointer;color:{T['text3']};font-size:0.72rem;">
                            🐦 Share
                        </button>
                    </div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown(f'<div class="sec-header">All Reviews</div><div class="sec-title">{len(st.session_state.reviews)} Reviews</div>',unsafe_allow_html=True)
    for rev in st.session_state.reviews:
        st.markdown(f"""
        <div class="review-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:32px;height:32px;border-radius:50%;background:{T['bg3']};
                                display:flex;align-items:center;justify-content:center;
                                font-size:0.8rem;font-weight:700;color:{T['accent']};">{rev['name'][0].upper()}</div>
                    <div><div class="reviewer">{rev['name']}</div>
                         <div style="color:{T['text3']};font-size:0.75rem;">{rev['product']}</div></div>
                </div>
                <div class="stars">{'⭐'*rev['rating']}</div>
            </div>
            <div class="review-text">"{rev['text']}"</div>
        </div>""", unsafe_allow_html=True)

    social_footer(); watermark()


# ═══════════════════════════════════════════════════════
# UPDATES
# ═══════════════════════════════════════════════════════
with tab_updates:
    st.markdown('<div class="sec-header">Changelog</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Product Updates</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='color:{T['text3']};margin-top:-16px;margin-bottom:28px;font-size:0.9rem;'>Everything that's shipped, fixed, and improved.</p>",unsafe_allow_html=True)

    for upd in st.session_state.updates:
        items_html="".join(f'<div class="update-item">{i}</div>' for i in upd["items"])
        st.markdown(f"""
        <div class="update-card">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
                <span class="update-ver">{upd['version']}</span>
                <span class="badge {upd['tag_badge']}">{upd['tag']}</span>
            </div>
            <div class="update-date">Released {upd['date']}</div>
            {items_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">Next Release</div>', unsafe_allow_html=True)
    render_countdown(st.session_state.launch_label, st.session_state.launch_date)
    social_footer(); watermark()


# ═══════════════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════════════
with tab_about:
    st.markdown('<div class="sec-header">Our Story</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">About Indian Instincts Studios</div>', unsafe_allow_html=True)
    ab1,ab2=st.columns([3,2])
    with ab1:
        st.markdown(f"""
        <div class="card" style="margin-bottom:20px;">
            <h3 style="color:{T['accent']};margin-bottom:16px;">Who We Are</h3>
            <p style="color:{T['text2']};line-height:1.8;font-size:0.95rem;">
                Indian Instincts Studios is a small product studio focused on building smart AI tools
                that solve everyday problems — starting with the kitchen, and expanding to every corner of daily life.
            </p>
            <p style="color:{T['text2']};line-height:1.8;font-size:0.95rem;margin-top:12px;">
                Currently a 4-person team based in India, we launched our first product —
                KitchenMate — in late 2024.
            </p>
        </div>
        <div class="card">
            <h3 style="color:{T['accent']};margin-bottom:16px;">🎯 Our Mission</h3>
            <p style="color:{T['text2']};line-height:1.8;font-size:0.95rem;">
                Build useful AI tools that make daily life easier — for everyday Indians and beyond.
            </p>
            <div style="margin-top:20px;">
                <div class="feat-item">AI-first from day one</div>
                <div class="feat-item">Simplicity over complexity</div>
                <div class="feat-item">Built for real everyday problems</div>
                <div class="feat-item">Proudly made in India 🇮🇳</div>
            </div>
        </div>""", unsafe_allow_html=True)
    with ab2:
        st.markdown(f"""
        <div style="background:{'linear-gradient(135deg,#13131f,#1a0a2e)' if st.session_state.dark_mode else 'linear-gradient(135deg,#fff3ee,#f0f4ff)'};
                    border-radius:20px;padding:32px;border:1px solid {T['border2']};text-align:center;margin-bottom:20px;">
            <div style="font-size:3.5rem;margin-bottom:12px;">🪔</div>
            <div style="font-family:Sora,sans-serif;font-size:1.4rem;font-weight:800;color:{T['heading']};">Indian Instincts</div>
            <div style="font-size:0.8rem;color:{T['text3']};letter-spacing:0.12em;text-transform:uppercase;margin-top:4px;">Studios</div>
        </div>""", unsafe_allow_html=True)
        for num,lbl in [("4","Team Members"),("1","Products Live"),("2024","Founded")]:
            st.markdown(f'<div class="stat-box" style="margin-bottom:16px;"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>',unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">The Team</div><div class="sec-title">4 People. 1 Big Vision.</div>',unsafe_allow_html=True)
    tm1,tm2,tm3,tm4=st.columns(4)
    for col,(emoji,role,desc) in zip([tm1,tm2,tm3,tm4],[
        ("🧑‍💻","Founder & CEO","Product vision & strategy"),
        ("👩‍🎨","Lead Designer","UI/UX & brand design"),
        ("🧑‍🔬","AI Engineer","Model integration & APIs"),
        ("👨‍💼","Growth Lead","Marketing & community"),
    ]):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:2.2rem;margin-bottom:10px;">{emoji}</div>
                <div style="font-family:Sora,sans-serif;font-size:0.9rem;font-weight:700;color:{T['heading']};">{role}</div>
                <div style="color:{T['text3']};font-size:0.78rem;margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    social_footer(); watermark()


# ═══════════════════════════════════════════════════════
# CONTACT
# ═══════════════════════════════════════════════════════
with tab_contact:
    st.markdown('<div class="sec-header">Get In Touch</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Contact the Team</div>', unsafe_allow_html=True)

    cc1, cc2 = st.columns([3,2])
    with cc1:
        with st.form("contact_form"):
            cn = st.text_input("Your Name")
            ce = st.text_input("Email Address")
            cs = st.selectbox("Subject", ["General Enquiry", "Product Feedback", "Partnership", "Bug Report", "Other"])
            cm = st.text_area("Message", height=150, placeholder="What's on your mind?")
            if st.form_submit_button("Send Message 📨"):
                if cn.strip() and ce.strip() and cm.strip():
                    st.session_state.contact_messages.append({
                        "name": cn.strip(), "email": ce.strip(),
                        "subject": cs, "message": cm.strip(),
                        "time": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
                    })
                    st.success("✅ Message sent! We'll get back to you soon.")
                else:
                    st.error("Please fill in name, email, and message.")

    with cc2:
        st.markdown(f"""
        <div class="card">
            <h3 style="color:{T['accent']};margin-bottom:16px;">📬 Other ways to reach us</h3>
            <div class="feat-item">We typically reply within 48 hours</div>
            <div class="feat-item">For product bugs use Bug Report</div>
            <div class="feat-item">Partnerships welcome!</div>
        </div>""", unsafe_allow_html=True)

    social_footer(); watermark()


# ═══════════════════════════════════════════════════════
# 🔒 ADMIN
# ═══════════════════════════════════════════════════════
with tab_admin:

    if not st.session_state.admin_logged_in:
        st.markdown('<div class="sec-header">Studio Access</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">🔒 Admin Login</div>', unsafe_allow_html=True)
        _,lc,_ = st.columns([1,2,1])
        with lc:
            pw = st.text_input("Password", type="password", placeholder="Enter admin password")
            if st.button("Unlock Panel"):
                if pw == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Wrong password.")
    else:
        st.markdown('<div class="admin-banner">🔐 Admin Panel — changes reflect instantly across all tabs.</div>', unsafe_allow_html=True)
        if st.button("🔓 Log Out"):
            st.session_state.admin_logged_in = False
            st.rerun()

        # ─── ADMIN SUB-TABS ───
        (atab_analytics, atab_reviews, atab_products,
         atab_roadmap, atab_updates, atab_countdown,
         atab_social, atab_contact) = st.tabs([
            "📊 Analytics", "⭐ Reviews", "📦 Products",
            "🗺️ Roadmap", "📣 Changelog", "⏳ Countdown",
            "🔗 Social Links", "✉️ Messages",
        ])

        # ── ANALYTICS ──
        with atab_analytics:
            st.markdown("### 📊 Analytics Dashboard")
            all_reviews = st.session_state.reviews
            total = len(all_reviews)
            avg = round(sum(r["rating"] for r in all_reviews)/total, 2) if total else 0
            five_star = sum(1 for r in all_reviews if r["rating"]==5)
            total_votes = sum(st.session_state.votes.values())

            a1,a2,a3,a4 = st.columns(4)
            for col,(n,l) in zip([a1,a2,a3,a4],[
                (total,"Total Reviews"),(avg,"Avg Rating"),
                (five_star,"5-Star Reviews"),(total_votes,"Total Votes")
            ]):
                with col:
                    st.markdown(f'<div class="ana-card"><div class="ana-num">{n}</div><div class="ana-lbl">{l}</div></div>',unsafe_allow_html=True)

            st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
            st.markdown("**⭐ Rating Breakdown**")
            for star in [5,4,3,2,1]:
                count = sum(1 for r in all_reviews if r["rating"]==star)
                pct = int(count/total*100) if total else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    <span style="color:{T['accent']};width:20px;">{'⭐'}</span>
                    <span style="color:{T['text2']};width:12px;">{star}</span>
                    <div style="flex:1;background:{T['border']};border-radius:4px;height:10px;">
                        <div style="width:{pct}%;background:{T['accent']};border-radius:4px;height:10px;"></div>
                    </div>
                    <span style="color:{T['text3']};font-size:0.8rem;width:50px;">{count} ({pct}%)</span>
                </div>""", unsafe_allow_html=True)

            st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
            st.markdown("**🗺️ Roadmap Votes**")
            sorted_votes = sorted(st.session_state.votes.items(), key=lambda x: x[1], reverse=True)
            max_v = sorted_votes[0][1] if sorted_votes else 1
            for title, votes in sorted_votes:
                pct = int(votes/max_v*100) if max_v else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    <span style="color:{T['text2']};font-size:0.85rem;width:200px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{title}</span>
                    <div style="flex:1;background:{T['border']};border-radius:4px;height:10px;">
                        <div style="width:{pct}%;background:#60a5fa;border-radius:4px;height:10px;"></div>
                    </div>
                    <span style="color:{T['text3']};font-size:0.8rem;width:40px;">{votes}</span>
                </div>""", unsafe_allow_html=True)

        # ── REVIEWS ADMIN ──
        with atab_reviews:
            st.markdown("### ⭐ Pin & Manage Reviews")
            st.caption("Pin a review to feature it on the homepage spotlight.")
            for i, rev in enumerate(st.session_state.reviews):
                pinned = rev.get("pinned", False)
                pin_label = "📌 Unpin" if pinned else "📌 Pin to Homepage"
                col_r, col_p, col_d = st.columns([6,2,1])
                with col_r:
                    st.markdown(f"""
                    <div style="background:{T['bg3']};border:1px solid {'#ff6b35' if pinned else T['border']};
                                border-radius:12px;padding:14px;margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;">
                            <span style="font-weight:600;color:{T['heading']};">{rev['name']}</span>
                            <span style="color:{T['accent']};font-size:0.9rem;">{'⭐'*rev['rating']}</span>
                        </div>
                        <div style="color:{T['text2']};font-size:0.85rem;margin-top:6px;">"{rev['text'][:100]}..."</div>
                    </div>""", unsafe_allow_html=True)
                with col_p:
                    if st.button(pin_label, key=f"pin_{i}"):
                        # Unpin all others if pinning
                        if not pinned:
                            for r in st.session_state.reviews: r["pinned"] = False
                        st.session_state.reviews[i]["pinned"] = not pinned
                        st.rerun()
                with col_d:
                    if st.button("🗑️", key=f"del_rev_{i}"):
                        st.session_state.reviews.pop(i)
                        st.rerun()

        # ── PRODUCTS ADMIN ──
        with atab_products:
            st.markdown("### 📦 Live Products")
            st.caption("Toggle Draft to hide a product from visitors without deleting it.")

            with st.expander("➕ Add Live Product"):
                with st.form("form_add_live"):
                    l1,l2,l3=st.columns([1,4,2])
                    with l1: le=st.text_input("Emoji",value="🚀")
                    with l2: ln=st.text_input("Name"); ls=st.text_input("Subtitle")
                    with l3: lv=st.text_input("Version",value="v1.0"); lu=st.text_input("URL",value="https://")
                    ld_desc=st.text_area("Description",height=80)
                    lf=st.text_area("Features (one per line)",height=100)
                    if st.form_submit_button("Add"):
                        if ln.strip():
                            st.session_state.live_products.append({
                                "emoji":le.strip()or"🚀","name":ln.strip(),"subtitle":ls.strip(),
                                "version":lv.strip(),"url":lu.strip(),"draft":False,
                                "description":ld_desc.strip(),
                                "features":[f.strip() for f in lf.split("\n") if f.strip()],
                                "stats":{"Active Users":"0","Launched":lv.strip()},
                            })
                            st.success(f"✅ {ln} added!"); st.rerun()

            for i,p in enumerate(st.session_state.live_products):
                draft_tag = " 🟡 DRAFT" if p.get("draft") else ""
                with st.expander(f"{p['emoji']} {p['name']} {p['version']}{draft_tag}"):
                    # Draft toggle
                    is_draft = p.get("draft", False)
                    tc1, tc2 = st.columns([3,1])
                    with tc1:
                        st.markdown(f"**Status:** {'🟡 Draft — hidden from visitors' if is_draft else '🟢 Live — visible to visitors'}")
                    with tc2:
                        toggle_label = "📢 Go Live" if is_draft else "📝 Set to Draft"
                        if st.button(toggle_label, key=f"draft_{i}"):
                            st.session_state.live_products[i]["draft"] = not is_draft
                            st.rerun()

                    # Reorder
                    rc1, rc2 = st.columns(2)
                    with rc1:
                        if i > 0 and st.button("⬆️ Move Up", key=f"up_{i}"):
                            st.session_state.live_products.insert(i-1, st.session_state.live_products.pop(i))
                            st.rerun()
                    with rc2:
                        if i < len(st.session_state.live_products)-1 and st.button("⬇️ Move Down", key=f"dn_{i}"):
                            st.session_state.live_products.insert(i+1, st.session_state.live_products.pop(i))
                            st.rerun()

                    with st.form(f"form_live_{i}"):
                        lp1,lp2,lp3=st.columns([1,4,2])
                        with lp1: ue=st.text_input("Emoji",value=p["emoji"],key=f"le_{i}")
                        with lp2: un=st.text_input("Name",value=p["name"],key=f"ln_{i}"); us=st.text_input("Subtitle",value=p["subtitle"],key=f"ls_{i}")
                        with lp3: uv=st.text_input("Version",value=p["version"],key=f"lv_{i}"); uu=st.text_input("URL",value=p["url"],key=f"lu_{i}")
                        ud=st.text_area("Description",value=p["description"],key=f"ld_{i}",height=80)
                        uf=st.text_area("Features (one per line)",value="\n".join(p["features"]),key=f"lf_{i}",height=100)
                        sc1,sc2=st.columns(2)
                        with sc1:
                            if st.form_submit_button("💾 Save"):
                                st.session_state.live_products[i]={**p,"emoji":ue,"name":un,"subtitle":us,"version":uv,"url":uu,"description":ud,"features":[f.strip() for f in uf.split("\n") if f.strip()]}
                                st.success("✅ Saved!"); st.rerun()
                        with sc2:
                            if st.form_submit_button("🗑️ Delete"):
                                st.session_state.live_products.pop(i); st.rerun()

            st.markdown("---")
            st.markdown("### 🧠 Coming Soon Products")
            with st.expander("➕ Add Coming Soon"):
                with st.form("form_add_soon"):
                    a1,a2=st.columns([1,6])
                    with a1: ne=st.text_input("Emoji",value="🚀")
                    with a2: nn=st.text_input("Name")
                    nd=st.text_area("Description",height=100)
                    if st.form_submit_button("Add"):
                        if nn.strip():
                            st.session_state.coming_soon_products.append({"emoji":ne.strip()or"🚀","name":nn.strip(),"description":nd.strip()})
                            st.success(f"✅ {nn} added!"); st.rerun()

            for i,p in enumerate(st.session_state.coming_soon_products):
                with st.expander(f"{p['emoji']} {p['name']}"):
                    with st.form(f"form_soon_{i}"):
                        e1,e2=st.columns([1,6])
                        with e1: ue=st.text_input("Emoji",value=p["emoji"],key=f"se_{i}")
                        with e2: un=st.text_input("Name",value=p["name"],key=f"sn_{i}")
                        ud=st.text_area("Description",value=p["description"],key=f"sd_{i}",height=100)
                        sc1,sc2=st.columns(2)
                        with sc1:
                            if st.form_submit_button("💾 Save"):
                                st.session_state.coming_soon_products[i]={"emoji":ue,"name":un,"description":ud}
                                st.success("✅ Saved!"); st.rerun()
                        with sc2:
                            if st.form_submit_button("🗑️ Delete"):
                                st.session_state.coming_soon_products.pop(i); st.rerun()

        # ── ROADMAP ADMIN ──
        with atab_roadmap:
            st.markdown("### 🗺️ Roadmap Items")
            st.caption("Set status to **Released** to auto-move the item to the Changelog.")

            with st.expander("➕ Add Roadmap Item"):
                with st.form("form_add_road"):
                    ra1,ra2=st.columns([1,6])
                    with ra1: re_=st.text_input("Emoji",value="✨")
                    with ra2: rt=st.text_input("Title")
                    rd=st.text_area("Description",height=80)
                    rs=st.selectbox("Status",["Planned","In Progress","Testing","Released"])
                    if st.form_submit_button("Add Item"):
                        if rt.strip():
                            st.session_state.roadmap.append({"emoji":re_.strip(),"title":rt.strip(),"desc":rd.strip(),"status":rs})
                            st.session_state.votes[rt.strip()]=0
                            st.success("✅ Added!"); st.rerun()

            for i,item in enumerate(st.session_state.roadmap):
                with st.expander(f"{item['emoji']} {item['title']} — {item['status']}"):
                    with st.form(f"form_road_{i}"):
                        rr1,rr2=st.columns([1,6])
                        with rr1: rue=st.text_input("Emoji",value=item["emoji"],key=f"re_{i}")
                        with rr2: rut=st.text_input("Title",value=item["title"],key=f"rt_{i}")
                        rud=st.text_area("Description",value=item["desc"],key=f"rd_{i}",height=80)
                        rus=st.selectbox("Status",["Planned","In Progress","Testing","Released"],
                                         index=["Planned","In Progress","Testing","Released"].index(item["status"]),
                                         key=f"rs_{i}")
                        rc1,rc2=st.columns(2)
                        with rc1:
                            if st.form_submit_button("💾 Save"):
                                old_title=st.session_state.roadmap[i]["title"]
                                st.session_state.roadmap[i]={"emoji":rue,"title":rut,"desc":rud,"status":rus}
                                if old_title!=rut:
                                    st.session_state.votes[rut]=st.session_state.votes.pop(old_title,0)
                                # Auto-move to changelog if Released
                                if rus=="Released":
                                    today=datetime.datetime.now().strftime("%B %Y")
                                    st.session_state.updates.insert(0,{
                                        "version":rut,"date":today,"tag":"Released","tag_badge":"badge-live",
                                        "items":[f"Feature released: {rud}",f"Votes received: {st.session_state.votes.get(rut,0)}"]
                                    })
                                    st.session_state.roadmap.pop(i)
                                    st.success(f"🎉 {rut} marked Released and moved to Changelog!")
                                else:
                                    st.success("✅ Saved!")
                                st.rerun()
                        with rc2:
                            if st.form_submit_button("🗑️ Delete"):
                                st.session_state.roadmap.pop(i); st.rerun()

        # ── CHANGELOG ADMIN ──
        with atab_updates:
            st.markdown("### 📣 Changelog Entries")
            with st.expander("➕ Add Update"):
                with st.form("form_add_update"):
                    uv1,uv2,uv3=st.columns(3)
                    with uv1: new_ver=st.text_input("Version",placeholder="KitchenMate v1.3")
                    with uv2: new_udate=st.text_input("Date",placeholder="March 2026")
                    with uv3: new_tag=st.text_input("Tag",value="Latest"); new_tb=st.selectbox("Tag Color",["badge-live","badge-prog","badge-plan","badge-test"])
                    new_items=st.text_area("Changes (one per line)",height=120)
                    if st.form_submit_button("Add to Changelog"):
                        if new_ver.strip():
                            st.session_state.updates.insert(0,{
                                "version":new_ver.strip(),"date":new_udate.strip(),
                                "tag":new_tag.strip(),"tag_badge":new_tb,
                                "items":[x.strip() for x in new_items.split("\n") if x.strip()],
                            })
                            st.success("✅ Added!"); st.rerun()

            for i,upd in enumerate(st.session_state.updates):
                with st.expander(f"{upd['version']} — {upd['date']}"):
                    with st.form(f"form_upd_{i}"):
                        up1,up2,up3=st.columns(3)
                        with up1: uuv=st.text_input("Version",value=upd["version"],key=f"uv_{i}")
                        with up2: uud=st.text_input("Date",value=upd["date"],key=f"ud_{i}")
                        with up3:
                            uut=st.text_input("Tag",value=upd["tag"],key=f"ut_{i}")
                            uub=st.selectbox("Tag Color",["badge-live","badge-prog","badge-plan","badge-test"],
                                             index=["badge-live","badge-prog","badge-plan","badge-test"].index(upd["tag_badge"]),key=f"ub_{i}")
                        uui=st.text_area("Changes",value="\n".join(upd["items"]),key=f"ui_{i}",height=100)
                        uc1,uc2=st.columns(2)
                        with uc1:
                            if st.form_submit_button("💾 Save"):
                                st.session_state.updates[i]={"version":uuv,"date":uud,"tag":uut,"tag_badge":uub,"items":[x.strip() for x in uui.split("\n") if x.strip()]}
                                st.success("✅ Saved!"); st.rerun()
                        with uc2:
                            if st.form_submit_button("🗑️ Delete"):
                                st.session_state.updates.pop(i); st.rerun()

        # ── COUNTDOWN ADMIN ──
        with atab_countdown:
            st.markdown("### ⏳ Launch Countdown")
            with st.form("form_countdown"):
                cl1,cl2=st.columns(2)
                with cl1: new_label=st.text_input("Countdown Label",value=st.session_state.launch_label)
                with cl2:
                    ld=st.session_state.launch_date
                    new_date=st.date_input("Launch Date",value=ld.date())
                    new_time=st.time_input("Launch Time",value=ld.time())
                if st.form_submit_button("💾 Save Countdown"):
                    st.session_state.launch_label=new_label
                    st.session_state.launch_date=datetime.datetime.combine(new_date,new_time)
                    st.success("✅ Countdown updated!")

            st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
            st.markdown("**Preview:**")
            render_countdown(st.session_state.launch_label, st.session_state.launch_date)

        # ── SOCIAL LINKS ADMIN ──
        with atab_social:
            st.markdown("### 🔗 Social Links")
            st.caption("Links appear in the footer of every page. Leave blank to hide.")
            with st.form("form_social"):
                new_socials = {}
                for platform, current in st.session_state.social_links.items():
                    new_socials[platform] = st.text_input(platform, value=current, placeholder=f"https://")
                if st.form_submit_button("💾 Save Links"):
                    st.session_state.social_links = new_socials
                    st.success("✅ Social links updated!")

        # ── CONTACT MESSAGES ADMIN ──
        with atab_contact:
            st.markdown("### ✉️ Contact Messages")
            msgs = st.session_state.contact_messages
            if not msgs:
                st.info("No messages yet.")
            else:
                st.markdown(f"**{len(msgs)} message(s) received**")
                for i, m in enumerate(reversed(msgs)):
                    with st.expander(f"📨 {m['name']} — {m['subject']} · {m['time']}"):
                        st.markdown(f"**From:** {m['name']} (`{m['email']}`)")
                        st.markdown(f"**Subject:** {m['subject']}")
                        st.markdown(f"**Message:**\n\n{m['message']}")
                        if st.button("🗑️ Delete", key=f"del_msg_{i}"):
                            st.session_state.contact_messages.pop(len(msgs)-1-i)
                            st.rerun()
