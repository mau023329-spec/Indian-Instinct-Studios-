"""
Indian Instincts Studios — Full Streamlit Website
v8: Supabase persistence — all data survives restarts
Run with: streamlit run app_v8_supabase.py
Requires: pip install streamlit supabase
Secrets (Streamlit Cloud → Settings → Secrets):
    SUPABASE_URL = "https://xxx.supabase.co"
    SUPABASE_KEY = "your-anon-key"
"""

import streamlit as st
import datetime
import html as html_lib
from supabase import create_client, Client

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "iis2024")

st.set_page_config(
    page_title="Indian Instincts Studios",
    page_icon="🪔", layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# SUPABASE CLIENT
# ─────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

sb = get_supabase()

# ─────────────────────────────────────────────
# DATABASE LOAD
# ─────────────────────────────────────────────
def load_all():
    """Pull everything from Supabase into session_state."""
    try:
        # Products
        res = sb.table("products").select("*").order("sort_order").execute()
        st.session_state.live_products = [
            {
                "id": r["id"], "emoji": r["emoji"], "name": r["name"],
                "subtitle": r["subtitle"], "version": r["version"],
                "url": r["url"], "draft": r["draft"],
                "description": r["description"],
                "features": r["features"] or [],
                "stats": r["stats"] or {},
                "sort_order": r["sort_order"],
            } for r in (res.data or [])
        ]

        # Coming soon
        res = sb.table("coming_soon").select("*").execute()
        st.session_state.coming_soon_products = [
            {"id": r["id"], "emoji": r["emoji"],
             "name": r["name"], "description": r["description"]}
            for r in (res.data or [])
        ]

        # Roadmap
        res = sb.table("roadmap").select("*").order("id").execute()
        st.session_state.roadmap = [
            {"id": r["id"], "emoji": r["emoji"], "title": r["title"],
             "desc": r["description"], "status": r["status"], "votes": r["votes"]}
            for r in (res.data or [])
        ]

        # Reviews
        res = sb.table("reviews").select("*").order("created_at", desc=True).execute()
        st.session_state.reviews = [
            {"id": r["id"], "name": r["name"], "product": r["product"],
             "rating": r["rating"], "text": r["review"],
             "pinned": r["pinned"], "created_at": r.get("created_at", "")}
            for r in (res.data or [])
        ]

        # Changelog (table: changelog, date column: release_date)
        res = sb.table("changelog").select("*").order("created_at", desc=True).execute()
        st.session_state.updates = [
            {"id": r["id"], "version": r["version"],
             "date": r["release_date"],          # ← release_date not date
             "tag": r["tag"], "tag_badge": r["tag_badge"],
             "items": r["items"] or []}
            for r in (res.data or [])
        ]

        # Settings
        res = sb.table("settings").select("*").execute()
        settings = {r["key"]: r["value"] for r in (res.data or [])}

        ld = settings.get("launch_date", {})
        try:
            st.session_state.launch_date = datetime.datetime.fromisoformat(ld.get("datetime", "2026-03-18T12:00:00"))
        except Exception:
            st.session_state.launch_date = datetime.datetime(2026, 3, 18, 12, 0, 0)

        st.session_state.launch_label = settings.get("launch_label", {}).get("text", "🧠 SankalpRoom — Public Launch")
        st.session_state.social_links = settings.get("social_links", {}).get("links", {
            "Twitter/X": "", "LinkedIn": "", "GitHub": "", "Product Hunt": ""
        })

        # Contact messages
        res = sb.table("contact_messages").select("*").order("created_at", desc=True).execute()
        st.session_state.contact_messages = [
            {"id": r["id"], "name": r["name"], "email": r["email"],
             "subject": r["subject"], "message": r["message"],
             "time": r.get("created_at", "")}
            for r in (res.data or [])
        ]

        st.session_state._db_loaded = True

    except Exception as e:
        st.warning(f"⚠️ Supabase load failed: {e}. Using in-memory defaults.")
        load_defaults()

def load_defaults():
    """Fallback if Supabase is unreachable."""
    st.session_state.setdefault("live_products", [{
        "id": None, "emoji": "🍳", "name": "KitchenMate",
        "subtitle": "AI Kitchen Assistant", "version": "v1.2",
        "url": "https://kitchenmate.streamlit.app", "draft": False,
        "description": "An AI-powered cooking assistant that generates recipes based on the ingredients you have.",
        "features": ["AI recipe generation","Ingredient-based cooking","Simple UI","Quick suggestions"],
        "stats": {"Active Users": "2,841", "Recipes Generated": "14,320", "Avg. Rating": "4.8 ⭐"},
        "sort_order": 0,
    }])
    st.session_state.setdefault("coming_soon_products", [{
        "id": None, "emoji": "🧠", "name": "SankalpRoom",
        "description": "AI-powered team collaboration — from brainstorm to delivery.",
    }])
    st.session_state.setdefault("roadmap", [
        {"id": None, "emoji": "🧮", "title": "Meal Nutrition Calculator", "desc": "Calculate calories and macros.", "status": "In Progress", "votes": 42},
        {"id": None, "emoji": "📸", "title": "Pantry Scanner", "desc": "Scan ingredients with your camera.", "status": "Planned", "votes": 31},
    ])
    st.session_state.setdefault("reviews", [
        {"id": None, "name": "Priya S.", "product": "KitchenMate", "rating": 5,
         "text": "This app has completely changed how I cook!", "pinned": True, "created_at": ""},
    ])
    st.session_state.setdefault("updates", [
        {"id": None, "version": "KitchenMate v1.2", "date": "February 2025",
         "tag": "Latest", "tag_badge": "badge-live",
         "items": ["Faster recipe generation", "Improved UI"]},
    ])
    st.session_state.setdefault("launch_date", datetime.datetime(2026, 3, 18, 12, 0, 0))
    st.session_state.setdefault("launch_label", "🧠 SankalpRoom — Public Launch")
    st.session_state.setdefault("social_links", {"Twitter/X": "", "LinkedIn": "", "GitHub": "", "Product Hunt": ""})
    st.session_state.setdefault("contact_messages", [])
    st.session_state._db_loaded = True

def save_setting(key: str, value: dict):
    try:
        sb.table("settings").upsert({"key": key, "value": value}).execute()
    except Exception as e:
        st.error(f"Save failed: {e}")

def refresh():
    st.session_state._db_loaded = False
    st.rerun()

# ─────────────────────────────────────────────
# BOOTSTRAP SESSION STATE
# ─────────────────────────────────────────────
st.session_state.setdefault("admin_logged_in", False)
st.session_state.setdefault("dark_mode", True)
st.session_state.setdefault("voted", set())
st.session_state.setdefault("show_confetti", False)

if not st.session_state.get("_db_loaded"):
    load_all()

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────
DARK = {
    "bg": "#0a0a0f", "bg2": "#0f0f18", "bg3": "#13131f",
    "border": "#1e1e2e", "border2": "#2a1a3e",
    "text": "#e8e6e1", "text2": "#a09fa6", "text3": "#6e6d74",
    "heading": "#f0ede8", "accent": "#ff6b35",
    "grad_hero": "linear-gradient(135deg,#0f0f18 0%,#1a0a2e 50%,#0d1a2e 100%)",
    "grad_card": "linear-gradient(135deg,#1a0a2e,#0d1a2e)",
    "grad_cd":   "linear-gradient(135deg,#13131f,#1a0a2e)",
    "teaser_bg": "repeating-linear-gradient(45deg,#13131f,#13131f 10px,#0f0f18 10px,#0f0f18 20px)",
    "pin_grad":  "linear-gradient(135deg,#1a0a2e,#0d1a0d)",
    "about_grad":"linear-gradient(135deg,#13131f,#1a0a2e)",
}
LIGHT = {
    "bg": "#f8f7f4", "bg2": "#ffffff", "bg3": "#f0ede8",
    "border": "#e0ddd8", "border2": "#d0ccc6",
    "text": "#1a1a2e", "text2": "#4a4a5a", "text3": "#8a8a9a",
    "heading": "#0a0a1a", "accent": "#e85a20",
    "grad_hero": "linear-gradient(135deg,#fff8f4 0%,#ffe8d6 50%,#f0f4ff 100%)",
    "grad_card": "linear-gradient(135deg,#fff3ee,#f0f4ff)",
    "grad_cd":   "linear-gradient(135deg,#fff3ee,#f0f4ff)",
    "teaser_bg": "repeating-linear-gradient(45deg,#f8f7f4,#f8f7f4 10px,#f0ede8 10px,#f0ede8 20px)",
    "pin_grad":  "linear-gradient(135deg,#fff3ee,#f0fff4)",
    "about_grad":"linear-gradient(135deg,#fff3ee,#f0f4ff)",
}
T = DARK if st.session_state.dark_mode else LIGHT

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
h1,h2,h3,h4 {{ font-family:'Sora',sans-serif; color:{T['heading']}; }}

/* tabs */
div[data-testid="stTabs"] > div:first-child {{
    background:{T['bg2']}; border-bottom:1px solid {T['border']};
    padding:0 8px; border-radius:14px 14px 0 0;
}}
div[data-testid="stTabs"] button[role="tab"] {{
    font-family:'Sora',sans-serif !important; font-size:0.82rem !important;
    font-weight:600 !important; letter-spacing:0.05em !important;
    text-transform:uppercase !important; color:{T['text3']} !important;
    padding:14px 18px !important; border:none !important;
    background:transparent !important; transition:color 0.2s !important;
}}
div[data-testid="stTabs"] button[role="tab"]:hover {{ color:{T['heading']} !important; }}
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
    color:{T['accent']} !important; border-bottom:2px solid {T['accent']} !important;
}}

/* cards */
.card {{
    background:{T['bg3']}; border:1px solid {T['border']};
    border-radius:16px; padding:28px 24px; margin-bottom:18px;
    transition:border-color 0.25s;
}}
.card:hover {{ border-color:{T['accent']}; }}

/* hero */
.hero-wrap {{
    background:{T['grad_hero']}; border-radius:24px; padding:56px 48px;
    border:1px solid {T['border']}; margin-bottom:40px;
    position:relative; overflow:hidden;
}}
.hero-wrap::before {{
    content:''; position:absolute; top:-60px; right:-60px;
    width:320px; height:320px;
    background:radial-gradient(circle,rgba(255,107,53,0.12) 0%,transparent 70%);
    border-radius:50%;
}}
.hero-title {{
    font-family:'Sora',sans-serif; font-size:clamp(1.75rem,5vw,3.2rem);
    font-weight:800; line-height:1.15;
    background:linear-gradient(135deg,{T['heading']} 30%,{T['accent']} 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin-bottom:12px;
}}
.hero-tag {{ font-family:'Sora',sans-serif; font-size:clamp(0.95rem,2.5vw,1.2rem); color:{T['accent']}; font-weight:600; margin-bottom:18px; }}
.hero-desc {{ color:{T['text2']}; font-size:clamp(0.88rem,2vw,1rem); line-height:1.7; max-width:540px; margin-bottom:28px; }}

/* badges */
.badge {{ display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.72rem; font-weight:600; letter-spacing:0.07em; text-transform:uppercase; margin-right:6px; }}
.badge-live {{ background:#0d2b1d; color:#34d399; border:1px solid #34d399; }}
.badge-plan {{ background:#1e1a0d; color:#fbbf24; border:1px solid #fbbf24; }}
.badge-prog {{ background:#0d1a2e; color:#60a5fa; border:1px solid #60a5fa; }}
.badge-test {{ background:#1e0d1a; color:#c084fc; border:1px solid #c084fc; }}
.badge-soon {{ background:#1a0a2e; color:#a78bfa; border:1px solid #a78bfa; }}

/* pulse dot */
@keyframes pulse {{ 0%,100%{{opacity:1;transform:scale(1)}} 50%{{opacity:0.5;transform:scale(1.4)}} }}
.pulse-dot {{ display:inline-block; width:8px; height:8px; background:#60a5fa; border-radius:50%; margin-right:6px; animation:pulse 1.6s ease-in-out infinite; vertical-align:middle; }}

/* pinned spotlight */
.pinned-card {{ background:{T['pin_grad']}; border:1px solid {T['accent']}; border-radius:20px; padding:28px; margin-bottom:20px; position:relative; }}
.pin-crown {{ position:absolute; top:-12px; left:24px; background:{T['accent']}; color:#0a0a0f; font-family:'Sora',sans-serif; font-size:0.65rem; font-weight:700; padding:3px 10px; border-radius:20px; letter-spacing:0.1em; text-transform:uppercase; }}

/* stat box */
.stat-box {{ background:{T['bg3']}; border:1px solid {T['border']}; border-radius:16px; padding:28px 20px; text-align:center; }}
.stat-num {{ font-family:'Sora',sans-serif; font-size:2.4rem; font-weight:800; color:{T['accent']}; }}
.stat-lbl {{ color:{T['text3']}; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; margin-top:4px; }}

/* countdown */
.cd-wrap {{ background:{T['grad_cd']}; border:1px solid {T['border2']}; border-radius:20px; padding:40px 32px; text-align:center; margin:32px 0; }}
.cd-num {{ font-family:'Sora',sans-serif; font-size:3rem; font-weight:800; color:{T['accent']}; display:block; }}
.cd-unit {{ color:{T['text3']}; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em; }}

/* review cards */
.review-card {{ background:{T['bg3']}; border:1px solid {T['border']}; border-radius:16px; padding:24px; margin-bottom:16px; }}
.review-card.love {{ border-color:{T['accent']}; }}
.stars {{ color:{T['accent']}; font-size:1.1rem; }}
.reviewer {{ font-weight:600; font-size:0.9rem; color:{T['heading']}; }}
.review-text {{ color:{T['text2']}; font-size:0.92rem; line-height:1.6; margin-top:8px; }}

/* changelog */
.update-card {{ background:{T['bg3']}; border-left:3px solid {T['accent']}; border-radius:0 14px 14px 0; padding:24px 24px 24px 28px; margin-bottom:20px; }}
.update-ver {{ font-family:'Sora',sans-serif; font-size:1rem; font-weight:700; color:{T['heading']}; }}
.update-date {{ color:{T['text3']}; font-size:0.78rem; margin-top:2px; margin-bottom:12px; }}
.update-item {{ color:{T['text2']}; font-size:0.9rem; line-height:1.7; }}
.update-item::before {{ content:"→ "; color:{T['accent']}; }}

/* section labels */
.sec-header {{ font-family:'Sora',sans-serif; font-size:0.72rem; font-weight:600; letter-spacing:0.16em; text-transform:uppercase; color:{T['accent']}; margin-bottom:6px; }}
.sec-title {{ font-family:'Sora',sans-serif; font-size:2rem; font-weight:700; color:{T['heading']}; margin-bottom:28px; }}

.feat-item {{ color:{T['text2']}; font-size:0.9rem; padding:6px 0; border-bottom:1px solid {T['border']}; }}
.feat-item::before {{ content:"✦ "; color:{T['accent']}; }}
.teaser {{ background:{T['teaser_bg']}; border:1px dashed {T['border2']}; border-radius:16px; padding:32px; text-align:center; }}
.div-line {{ border:none; border-top:1px solid {T['border']}; margin:36px 0; }}

/* comparison table */
.comp-table {{ width:100%; border-collapse:collapse; font-size:0.9rem; }}
.comp-table th {{ background:{T['bg2']}; color:{T['accent']}; font-family:'Sora',sans-serif; font-weight:700; padding:14px 16px; text-align:left; border-bottom:2px solid {T['accent']}; }}
.comp-table td {{ padding:12px 16px; border-bottom:1px solid {T['border']}; color:{T['text2']}; }}
.comp-table tr:hover td {{ background:{T['bg3']}; }}

/* admin */
.admin-banner {{ background:linear-gradient(90deg,#1a0a00,#2a1000); border:1px solid {T['accent']}; border-radius:12px; padding:14px 20px; margin-bottom:24px; font-family:'Sora',sans-serif; font-size:0.85rem; color:{T['accent']}; }}
.ana-card {{ background:{T['bg3']}; border:1px solid {T['border']}; border-radius:14px; padding:20px; text-align:center; margin-bottom:12px; }}
.ana-num {{ font-family:'Sora',sans-serif; font-size:1.8rem; font-weight:800; color:{T['accent']}; }}
.ana-lbl {{ color:{T['text3']}; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; }}

/* watermark */
.watermark {{ text-align:center; padding:32px 0 8px 0; font-family:'Sora',sans-serif; font-size:0.75rem; color:{T['text3']}; letter-spacing:0.06em; border-top:1px solid {T['border']}; margin-top:48px; }}
.watermark a {{ color:{T['accent']}; text-decoration:none; }}

/* forms */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background:{T['bg3']} !important; border-color:{T['border2']} !important;
    color:{T['text']} !important; border-radius:10px !important;
}}
.stButton > button {{
    background:{T['accent']} !important; color:#0a0a0f !important;
    font-family:'Sora',sans-serif !important; font-weight:700 !important;
    border:none !important; border-radius:10px !important;
    padding:10px 24px !important; transition:opacity 0.2s !important;
}}
.stButton > button:hover {{ opacity:0.85 !important; }}
.stButton > button:disabled {{ background:{T['border']} !important; color:{T['text3']} !important; }}

/* confetti */
@keyframes fall {{ 0%{{transform:translateY(-20px) rotate(0deg);opacity:1}} 100%{{transform:translateY(100vh) rotate(720deg);opacity:0}} }}
.confetti-piece {{ position:fixed; width:10px; height:10px; border-radius:2px; animation:fall linear forwards; z-index:9999; }}

#MainMenu, footer, header {{ visibility:hidden; }}
section[data-testid="stSidebar"] {{ display:none; }}
.block-container {{ padding-top:1.5rem; padding-bottom:4rem; max-width:1100px; }}
</style>
""", unsafe_allow_html=True)

# confetti trigger
if st.session_state.show_confetti:
    st.markdown("""<script>
    (function(){
        const c=['#ff6b35','#34d399','#60a5fa','#fbbf24','#c084fc','#f472b6'];
        for(let i=0;i<80;i++){
            const el=document.createElement('div');el.className='confetti-piece';
            el.style.left=Math.random()*100+'vw';
            el.style.background=c[Math.floor(Math.random()*c.length)];
            el.style.animationDuration=(Math.random()*2+1.5)+'s';
            el.style.animationDelay=(Math.random()*0.8)+'s';
            el.style.width=el.style.height=(Math.random()*10+6)+'px';
            document.body.appendChild(el);setTimeout(()=>el.remove(),4000);
        }
    })();
    </script>""", unsafe_allow_html=True)
    st.session_state.show_confetti = False

# ─────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────
STATUS_BADGES = {
    "Planned":"badge-plan","In Progress":"badge-prog",
    "Testing":"badge-test","Released":"badge-live",
}

def countdown_parts(target):
    delta = target - datetime.datetime.now()
    if delta.total_seconds() > 0:
        d=delta.days; h,rem=divmod(delta.seconds,3600); m,_=divmod(rem,60)
    else:
        d=h=m=0
    return d,h,m

def render_countdown(label, target):
    d,h,m = countdown_parts(target)
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
    links = {k:v for k,v in st.session_state.social_links.items() if v.strip()}
    icons = {"Twitter/X":"𝕏","LinkedIn":"in","GitHub":"GH","Product Hunt":"PH"}
    btns = "".join(
        f'<a href="{v}" target="_blank" style="display:inline-block;margin:0 6px;padding:6px 14px;'
        f'border:1px solid {T["border"]};border-radius:8px;color:{T["text2"]};font-family:Sora,sans-serif;'
        f'font-size:0.78rem;font-weight:600;text-decoration:none;">{icons.get(k,k)}</a>'
        for k,v in links.items())
    st.markdown(f"""
    <div class="watermark">
        {'<div style="margin-bottom:12px;">'+btns+'</div>' if btns else ''}
        Built with 🪔 <a href="#">Indian Instincts Studios</a> &nbsp;·&nbsp; © 2026
    </div>""", unsafe_allow_html=True)

def product_image_box(p):
    st.markdown(f"""
    <div style="background:{T['grad_card']};border-radius:16px;height:220px;
                display:flex;align-items:center;justify-content:center;
                border:1px solid {T['border2']};margin-bottom:16px;">
        <div style="text-align:center;">
            <div style="font-size:4rem;">{p['emoji']}</div>
            <div style="font-family:Sora,sans-serif;color:{T['accent']};font-weight:700;margin-top:8px;">{p['name']}</div>
            <div style="color:{T['text3']};font-size:0.8rem;">{p['version']}</div>
        </div>
    </div>""", unsafe_allow_html=True)

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
            <span style="margin-left:12px;font-size:0.7rem;color:{T['text3']};text-transform:uppercase;letter-spacing:0.1em;">KitchenMate Live</span>
        </div>
        <span class="badge badge-live" style="margin-left:16px;">● Live</span>
    </div>""", unsafe_allow_html=True)
with bar_r:
    if st.button("☀️ Light" if st.session_state.dark_mode else "🌙 Dark", key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
(tab_home, tab_products, tab_roadmap, tab_reviews,
 tab_updates, tab_about, tab_contact, tab_admin) = st.tabs([
    "🏠  Home","📦  Products","🗺️  Roadmap","⭐  Reviews",
    "📣  Updates","ℹ️  About","✉️  Contact","🔒  Admin",
])

# ═══════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════
with tab_home:
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-title">Indian Instincts Studios</div>
        <div class="hero-tag">Building smart AI tools for everyday life.</div>
        <div class="hero-desc">We are a small product studio obsessed with turning everyday friction into delightful, AI-powered tools. From the kitchen to collaboration — we build things people actually use.</div>
    </div>""", unsafe_allow_html=True)

    c1,c2,_ = st.columns([1,1,4])
    with c1:
        if st.button("🚀 Explore Products", key="hero_exp"):
            st.info("👇 Head to the **Products** tab above.")
    with c2:
        try_button("https://kitchenmate.streamlit.app","🍳 Try KitchenMate")

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # pinned review
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
                <div style="width:32px;height:32px;border-radius:50%;background:{T['accent']};display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;color:#0a0a0f;">{r['name'][0].upper()}</div>
                <div><div style="font-weight:600;color:{T['heading']};">{r['name']}</div><div style="color:{T['text3']};font-size:0.75rem;">{r['product']}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # stats
    visible_live = [p for p in st.session_state.live_products if not p.get("draft")]
    st.markdown('<div class="sec-header">Live Stats</div>', unsafe_allow_html=True)
    s1,s2,s3,s4 = st.columns(4)
    for col,(num,lbl) in zip([s1,s2,s3,s4],[
        ("2,841","KitchenMate Users"),("14,320","Recipes Generated"),
        (str(len(visible_live)),"Products Live"),
        (str(len(st.session_state.coming_soon_products)),"Coming Soon"),
    ]):
        with col:
            st.markdown(f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # featured product
    if visible_live:
        p = visible_live[0]
        st.markdown(f'<div class="sec-header">Featured Product</div><div class="sec-title">Meet {p["name"]}</div>', unsafe_allow_html=True)
        fc1,fc2 = st.columns(2)
        with fc1:
            feats = "".join(f'<div class="feat-item">{f}</div>' for f in p["features"])
            st.markdown(f"""
            <div class="card">
                <span class="badge badge-live">● Live</span>
                <h3 style="margin-top:16px;">{p['emoji']} {p['name']}</h3>
                <p style="color:{T['text2']};line-height:1.7;font-size:0.95rem;">{p['description']}</p>
                <div style="margin-top:20px;">{feats}</div>
            </div>""", unsafe_allow_html=True)
        with fc2:
            st.markdown(f"""
            <div style="background:{T['grad_card']};border-radius:16px;height:260px;display:flex;align-items:center;justify-content:center;border:1px solid {T['border2']};">
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
        cols = st.columns(min(len(st.session_state.coming_soon_products),3))
        for col,p in zip(cols,st.session_state.coming_soon_products):
            with col:
                st.markdown(f"""
                <div class="teaser">
                    <div style="font-size:2.5rem;">{p['emoji']}</div>
                    <div style="font-family:Sora,sans-serif;font-weight:700;color:{T['heading']};margin:12px 0 6px;">{p['name']}</div>
                    <div style="color:{T['text3']};font-size:0.85rem;line-height:1.5;">{p['description'][:120]}...</div>
                    <div style="margin-top:16px;"><span class="badge badge-soon">Coming Soon</span></div>
                </div>""", unsafe_allow_html=True)
    watermark()

# ═══════════════════════════════════════════════
# PRODUCTS
# ═══════════════════════════════════════════════
with tab_products:
    st.markdown('<div class="sec-header">Our Products</div><div class="sec-title">What We\'ve Built</div>', unsafe_allow_html=True)
    visible = [p for p in st.session_state.live_products if not p.get("draft")]
    if not visible:
        st.info("No live products yet — check back soon!")

    for p in visible:
        c1,c2 = st.columns([3,2])
        with c1:
            feats = "".join(f'<div class="feat-item">{f}</div>' for f in p["features"])
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
            product_image_box(p)
            try_button(p["url"],"🚀 Try Now",full_width=True)
            stat_rows = "".join(
                f'<div style="display:flex;justify-content:space-between;margin-bottom:8px;">'
                f'<span style="color:{T["text2"]};font-size:0.85rem;">{k}</span>'
                f'<span style="color:{T["accent"]};font-family:Sora,sans-serif;font-weight:700;">{v}</span></div>'
                for k,v in p["stats"].items())
            st.markdown(f"""
            <div style="background:{T['bg3']};border:1px solid {T['border']};border-radius:12px;padding:16px;margin-top:12px;">
                <div style="font-size:0.75rem;color:{T['text3']};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">Product Stats</div>
                {stat_rows}
            </div>""", unsafe_allow_html=True)

    # comparison table
    if visible and st.session_state.coming_soon_products:
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
        st.markdown('<div class="sec-header">Compare</div><div class="sec-title">Product Comparison</div>', unsafe_allow_html=True)
        p1=visible[0]; p2=st.session_state.coming_soon_products[0]
        rows=[
            ("AI-Powered","✅","✅"),("Mobile Friendly","✅","✅"),("Free to Use","✅","✅"),
            ("Team Collaboration","❌","✅"),("Live Now","✅","🔜"),
            ("Recipe Generation","✅","❌"),("Voting & Decisions","❌","✅"),
        ]
        rows_html="".join(f'<tr><td>{r}</td><td style="text-align:center;">{a}</td><td style="text-align:center;">{b}</td></tr>' for r,a,b in rows)
        st.markdown(f"""
        <table class="comp-table">
            <thead><tr><th>Feature</th><th style="text-align:center;">{p1['emoji']} {p1['name']}</th><th style="text-align:center;">{p2['emoji']} {p2['name']}</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)

    if st.session_state.coming_soon_products:
        st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
        st.markdown('<div class="sec-header">In The Pipeline</div><div class="sec-title">Coming Soon</div>', unsafe_allow_html=True)
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
    watermark()

# ═══════════════════════════════════════════════
# ROADMAP
# ═══════════════════════════════════════════════
with tab_roadmap:
    st.markdown('<div class="sec-header">Product Roadmap</div><div class="sec-title">What We\'re Building Next</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:{T["text3"]};margin-top:-16px;margin-bottom:28px;font-size:0.9rem;">Vote on features you want to see. Top-voted ideas get built first.</p>', unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.roadmap):
        key   = item["title"]
        votes = item.get("votes", 0)
        already_voted = key in st.session_state.voted
        badge_cls = STATUS_BADGES.get(item["status"], "badge-plan")

        # ── escape ALL user-supplied strings ──
        safe_emoji  = item.get("emoji", "")
        safe_title  = html_lib.escape(item.get("title", ""))
        safe_desc   = html_lib.escape(item.get("desc", ""))
        safe_status = html_lib.escape(item.get("status", ""))

        # Pulse dot for In-Progress — purely static HTML, no user data
        pulse = '<span class="pulse-dot"></span>&nbsp;' if item["status"] == "In Progress" else ""

        # ── flat card: ONLY <span> tags inside, no nested <div> or <p> ──
        # Nested block-level elements confuse Streamlit's markdown→HTML parser
        # and cause inner content to render as raw text.
        card_html = (
            f'<div class="card" style="margin-bottom:8px;">'
            f'<span style="font-size:1.8rem;vertical-align:middle;margin-right:12px;">{safe_emoji}</span>'
            f'{pulse}'
            f'<span style="font-family:Sora,sans-serif;font-size:1.05rem;font-weight:700;'
            f'color:{T["heading"]};vertical-align:middle;">{safe_title}</span>&nbsp;'
            f'<span class="badge {badge_cls}">{safe_status}</span>'
            f'<br><span style="color:{T["text2"]};font-size:0.88rem;line-height:1.8;'
            f'display:block;margin-top:6px;">{safe_desc}</span>'
            f'<br><span style="font-family:Sora,sans-serif;font-size:1.05rem;font-weight:800;'
            f'color:{T["accent"]};">▲ {votes} votes</span>'
            f'</div>'
        )

        col_card, col_vote = st.columns([5, 1])
        with col_card:
            st.markdown(card_html, unsafe_allow_html=True)
        with col_vote:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            if already_voted:
                st.button("✓ Voted", key=f"voted_btn_{i}", disabled=True)
            else:
                if st.button("Vote ▲", key=f"vote_btn_{i}"):
                    new_votes = votes + 1
                    try:
                        if item.get("id"):
                            sb.table("roadmap").update({"votes": new_votes}).eq("id", item["id"]).execute()
                    except Exception as e:
                        st.error(f"Vote save failed: {e}")
                    # ── explicitly update session_state by index so UI refreshes ──
                    st.session_state.roadmap[i]["votes"] = new_votes
                    st.session_state.voted.add(key)
                    st.rerun()

        st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)
    watermark()

# ═══════════════════════════════════════════════
# REVIEWS
# ═══════════════════════════════════════════════
with tab_reviews:
    st.markdown('<div class="sec-header">Community</div><div class="sec-title">Reviews & Feedback</div>', unsafe_allow_html=True)

    with st.expander("✍️ Write a Review", expanded=True):
        with st.form("review_form"):
            r1,r2 = st.columns(2)
            with r1:
                rname = st.text_input("Your Name")
                product_names = [p["name"] for p in st.session_state.live_products if not p.get("draft")] + \
                                [f"{p['name']} (Coming Soon)" for p in st.session_state.coming_soon_products]
                rproduct = st.selectbox("Product", product_names)
            with r2:
                rrating = st.select_slider("Rating", options=[1,2,3,4,5], value=5)
                st.markdown(f"<div style='color:{T['accent']};font-size:1.3rem;margin-top:6px;'>{'⭐'*rrating}</div>", unsafe_allow_html=True)
            rtext = st.text_area("Your Review", placeholder="Tell us what you think...", height=110)
            if st.form_submit_button("Submit Review"):
                if rname.strip() and rtext.strip():
                    try:
                        res = sb.table("reviews").insert({
                            "name":rname.strip(),"product":rproduct,
                            "rating":rrating,"review":rtext.strip(),"pinned":False
                        }).execute()
                        nr = res.data[0]
                        st.session_state.reviews.insert(0,{
                            "id":nr["id"],"name":nr["name"],"product":nr["product"],
                            "rating":nr["rating"],"text":nr["review"],
                            "pinned":False,"created_at":nr.get("created_at","")
                        })
                        if rrating==5:
                            st.session_state.show_confetti=True
                        st.success("🎉 Thank you for your review!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not save review: {e}")
                else:
                    st.error("Please fill in your name and review.")

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    love = [r for r in st.session_state.reviews if r["rating"]==5][:5]
    if love:
        st.markdown('<div class="sec-header">Highlights</div><div class="sec-title">💛 Wall of Love</div>', unsafe_allow_html=True)
        lc1,lc2 = st.columns(2)
        for i,rev in enumerate(love):
            tweet=f"Just used {rev['product']} by @IndianInstincts — {'⭐'*rev['rating']} \"{rev['text'][:80]}...\" Try it!"
            with (lc1 if i%2==0 else lc2):
                st.markdown(f"""
                <div class="review-card love">
                    <div class="stars">{'⭐'*rev['rating']}</div>
                    <div class="review-text" style="margin-top:10px;font-style:italic;">"{rev['text']}"</div>
                    <div style="margin-top:14px;display:flex;align-items:center;justify-content:space-between;">
                        <div style="display:flex;align-items:center;gap:8px;">
                            <div style="width:28px;height:28px;border-radius:50%;background:{T['accent']};display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:#0a0a0f;">{rev['name'][0].upper()}</div>
                            <div><div class="reviewer">{rev['name']}</div><div style="color:{T['text3']};font-size:0.75rem;">{rev['product']}</div></div>
                        </div>
                        <button onclick="navigator.clipboard.writeText({repr(tweet)});this.textContent='✓ Copied!';"
                            style="background:transparent;border:1px solid {T['border']};border-radius:8px;padding:4px 10px;cursor:pointer;color:{T['text3']};font-size:0.72rem;">🐦 Share</button>
                    </div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown(f'<div class="sec-header">All Reviews</div><div class="sec-title">{len(st.session_state.reviews)} Reviews</div>', unsafe_allow_html=True)
    for rev in st.session_state.reviews:
        st.markdown(f"""
        <div class="review-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div style="width:32px;height:32px;border-radius:50%;background:{T['bg3']};display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;color:{T['accent']};">{rev['name'][0].upper()}</div>
                    <div><div class="reviewer">{rev['name']}</div><div style="color:{T['text3']};font-size:0.75rem;">{rev['product']}</div></div>
                </div>
                <div class="stars">{'⭐'*rev['rating']}</div>
            </div>
            <div class="review-text">"{rev['text']}"</div>
        </div>""", unsafe_allow_html=True)
    watermark()

# ═══════════════════════════════════════════════
# UPDATES / CHANGELOG
# ═══════════════════════════════════════════════
with tab_updates:
    st.markdown('<div class="sec-header">Changelog</div><div class="sec-title">Product Updates</div>', unsafe_allow_html=True)
    st.markdown(f"<p style='color:{T['text3']};margin-top:-16px;margin-bottom:28px;font-size:0.9rem;'>Everything that's shipped, fixed, and improved.</p>", unsafe_allow_html=True)
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
    watermark()

# ═══════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════
with tab_about:
    st.markdown('<div class="sec-header">Our Story</div><div class="sec-title">About Indian Instincts Studios</div>', unsafe_allow_html=True)
    ab1,ab2 = st.columns([3,2])
    with ab1:
        st.markdown(f"""
        <div class="card" style="margin-bottom:20px;">
            <h3 style="color:{T['accent']};margin-bottom:16px;">Who We Are</h3>
            <p style="color:{T['text2']};line-height:1.8;font-size:0.95rem;">Indian Instincts Studios is a small product studio focused on building smart AI tools that solve everyday problems — starting with the kitchen, and expanding to every corner of daily life.</p>
            <p style="color:{T['text2']};line-height:1.8;font-size:0.95rem;margin-top:12px;">Currently a 4-person team based in India, we launched our first product — KitchenMate — in late 2024.</p>
        </div>
        <div class="card">
            <h3 style="color:{T['accent']};margin-bottom:16px;">🎯 Our Mission</h3>
            <p style="color:{T['text2']};line-height:1.8;font-size:0.95rem;">Build useful AI tools that make daily life easier — for everyday Indians and beyond.</p>
            <div style="margin-top:20px;">
                <div class="feat-item">AI-first from day one</div>
                <div class="feat-item">Simplicity over complexity</div>
                <div class="feat-item">Built for real everyday problems</div>
                <div class="feat-item">Proudly made in India 🇮🇳</div>
            </div>
        </div>""", unsafe_allow_html=True)
    with ab2:
        st.markdown(f"""
        <div style="background:{T['about_grad']};border-radius:20px;padding:32px;border:1px solid {T['border2']};text-align:center;margin-bottom:20px;">
            <div style="font-size:3.5rem;margin-bottom:12px;">🪔</div>
            <div style="font-family:Sora,sans-serif;font-size:1.4rem;font-weight:800;color:{T['heading']};">Indian Instincts</div>
            <div style="font-size:0.8rem;color:{T['text3']};letter-spacing:0.12em;text-transform:uppercase;margin-top:4px;">Studios</div>
        </div>""", unsafe_allow_html=True)
        for num,lbl in [("4","Team Members"),("1","Products Live"),("2024","Founded")]:
            st.markdown(f'<div class="stat-box" style="margin-bottom:16px;"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">The Team</div><div class="sec-title">4 People. 1 Big Vision.</div>', unsafe_allow_html=True)
    tm1,tm2,tm3,tm4 = st.columns(4)
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
    watermark()

# ═══════════════════════════════════════════════
# CONTACT
# ═══════════════════════════════════════════════
with tab_contact:
    st.markdown('<div class="sec-header">Get In Touch</div><div class="sec-title">Contact the Team</div>', unsafe_allow_html=True)
    cc1,cc2 = st.columns([3,2])
    with cc1:
        with st.form("contact_form"):
            cn = st.text_input("Your Name")
            ce = st.text_input("Email Address")
            cs = st.selectbox("Subject",["General Enquiry","Product Feedback","Partnership","Bug Report","Other"])
            cm = st.text_area("Message",height=150,placeholder="What's on your mind?")
            if st.form_submit_button("Send Message 📨"):
                if cn.strip() and ce.strip() and cm.strip():
                    try:
                        res = sb.table("contact_messages").insert({
                            "name":cn.strip(),"email":ce.strip(),
                            "subject":cs,"message":cm.strip()
                        }).execute()
                        nr = res.data[0]
                        st.session_state.contact_messages.insert(0,{
                            "id":nr["id"],"name":nr["name"],"email":nr["email"],
                            "subject":nr["subject"],"message":nr["message"],
                            "time":nr.get("created_at","")
                        })
                        st.success("✅ Message sent! We'll get back to you soon.")
                    except Exception as e:
                        st.error(f"Could not send message: {e}")
                else:
                    st.error("Please fill in name, email, and message.")
    with cc2:
        st.markdown(f"""
        <div class="card">
            <h3 style="color:{T['accent']};margin-bottom:16px;">📬 Other ways to reach us</h3>
            <div class="feat-item">We typically reply within 48 hours</div>
            <div class="feat-item">For bugs, use Bug Report subject</div>
            <div class="feat-item">Partnerships welcome!</div>
        </div>""", unsafe_allow_html=True)
    watermark()

# ═══════════════════════════════════════════════
# ADMIN
# ═══════════════════════════════════════════════
with tab_admin:
    if not st.session_state.admin_logged_in:
        st.markdown('<div class="sec-header">Studio Access</div><div class="sec-title">🔒 Admin Login</div>', unsafe_allow_html=True)
        _,lc,_ = st.columns([1,2,1])
        with lc:
            pw = st.text_input("Password",type="password",placeholder="Enter admin password")
            if st.button("Unlock Panel"):
                if pw==ADMIN_PASSWORD:
                    st.session_state.admin_logged_in=True
                    st.rerun()
                else:
                    st.error("Wrong password.")
    else:
        st.markdown('<div class="admin-banner">🔐 Admin Panel — all changes are saved to Supabase immediately and survive restarts.</div>', unsafe_allow_html=True)
        col_lo,col_rf = st.columns(2)
        with col_lo:
            if st.button("🔓 Log Out"):
                st.session_state.admin_logged_in=False; st.rerun()
        with col_rf:
            if st.button("🔄 Refresh from Supabase"):
                refresh()

        (atab_analytics, atab_reviews, atab_products,
         atab_roadmap, atab_changelog, atab_countdown,
         atab_social, atab_messages) = st.tabs([
            "📊 Analytics","⭐ Reviews","📦 Products",
            "🗺️ Roadmap","📣 Changelog","⏳ Countdown",
            "🔗 Social","✉️ Messages",
        ])

        # ── ANALYTICS ──
        with atab_analytics:
            st.markdown("### 📊 Analytics Dashboard")
            revs = st.session_state.reviews
            total = len(revs)
            avg = round(sum(r["rating"] for r in revs)/total,2) if total else 0
            five_star = sum(1 for r in revs if r["rating"]==5)
            total_votes = sum(i.get("votes",0) for i in st.session_state.roadmap)

            a1,a2,a3,a4 = st.columns(4)
            for col,(n,l) in zip([a1,a2,a3,a4],[
                (total,"Total Reviews"),(avg,"Avg Rating"),
                (five_star,"5-Star Reviews"),(total_votes,"Total Votes")
            ]):
                with col:
                    st.markdown(f'<div class="ana-card"><div class="ana-num">{n}</div><div class="ana-lbl">{l}</div></div>', unsafe_allow_html=True)

            st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
            st.markdown("**⭐ Rating Breakdown**")
            for star in [5,4,3,2,1]:
                count = sum(1 for r in revs if r["rating"]==star)
                pct = int(count/total*100) if total else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    <span style="color:{T['accent']};width:20px;">⭐</span>
                    <span style="color:{T['text2']};width:12px;">{star}</span>
                    <div style="flex:1;background:{T['border']};border-radius:4px;height:10px;">
                        <div style="width:{pct}%;background:{T['accent']};border-radius:4px;height:10px;"></div>
                    </div>
                    <span style="color:{T['text3']};font-size:0.8rem;width:60px;">{count} ({pct}%)</span>
                </div>""", unsafe_allow_html=True)

            st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
            st.markdown("**🗺️ Roadmap Votes**")
            sorted_items = sorted(st.session_state.roadmap, key=lambda x: x.get("votes",0), reverse=True)
            max_v = sorted_items[0].get("votes",1) if sorted_items else 1
            for item in sorted_items:
                votes=item.get("votes",0)
                pct=int(votes/max_v*100) if max_v else 0
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                    <span style="color:{T['text2']};font-size:0.85rem;width:220px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item['title']}</span>
                    <div style="flex:1;background:{T['border']};border-radius:4px;height:10px;">
                        <div style="width:{pct}%;background:#60a5fa;border-radius:4px;height:10px;"></div>
                    </div>
                    <span style="color:{T['text3']};font-size:0.8rem;width:40px;">{votes}</span>
                </div>""", unsafe_allow_html=True)

        # ── REVIEWS ADMIN ──
        with atab_reviews:
            st.markdown("### ⭐ Pin & Manage Reviews")
            st.caption("Pin a review to feature it on the homepage spotlight. Only one review can be pinned at a time.")
            for i,rev in enumerate(st.session_state.reviews):
                pinned=rev.get("pinned",False)
                col_r,col_p,col_d = st.columns([6,2,1])
                with col_r:
                    st.markdown(f"""
                    <div style="background:{T['bg3']};border:1px solid {'#ff6b35' if pinned else T['border']};border-radius:12px;padding:14px;margin-bottom:8px;">
                        <div style="display:flex;justify-content:space-between;">
                            <span style="font-weight:600;color:{T['heading']};">{rev['name']} {'📌' if pinned else ''}</span>
                            <span style="color:{T['accent']};font-size:0.9rem;">{'⭐'*rev['rating']}</span>
                        </div>
                        <div style="color:{T['text2']};font-size:0.85rem;margin-top:6px;">"{rev['text'][:100]}..."</div>
                    </div>""", unsafe_allow_html=True)
                with col_p:
                    if st.button("Unpin" if pinned else "📌 Pin",key=f"pin_{i}"):
                        try:
                            sb.table("reviews").update({"pinned":False}).neq("id",-1).execute()
                            new_pin = not pinned
                            if rev.get("id") and new_pin:
                                sb.table("reviews").update({"pinned":True}).eq("id",rev["id"]).execute()
                            for r in st.session_state.reviews: r["pinned"]=False
                            st.session_state.reviews[i]["pinned"]=new_pin
                            st.rerun()
                        except Exception as e:
                            st.error(f"Pin failed: {e}")
                with col_d:
                    if st.button("🗑️",key=f"del_rev_{i}"):
                        try:
                            if rev.get("id"):
                                sb.table("reviews").delete().eq("id",rev["id"]).execute()
                            st.session_state.reviews.pop(i); st.rerun()
                        except Exception as e:
                            st.error(f"Delete failed: {e}")

        # ── PRODUCTS ADMIN ──
        with atab_products:
            st.markdown("### 📦 Live Products")
            with st.expander("➕ Add Live Product"):
                with st.form("form_add_live"):
                    l1,l2,l3 = st.columns([1,4,2])
                    with l1: le=st.text_input("Emoji",value="🚀")
                    with l2: ln=st.text_input("Name"); ls=st.text_input("Subtitle")
                    with l3: lv=st.text_input("Version",value="v1.0"); lu=st.text_input("URL",value="https://")
                    ld_desc=st.text_area("Description",height=80)
                    lf=st.text_area("Features (one per line)",height=100)
                    if st.form_submit_button("Add Product"):
                        if ln.strip():
                            try:
                                res=sb.table("products").insert({
                                    "emoji":le.strip() or "🚀","name":ln.strip(),
                                    "subtitle":ls.strip(),"version":lv.strip(),
                                    "url":lu.strip(),"draft":False,
                                    "description":ld_desc.strip(),
                                    "features":[f.strip() for f in lf.split("\n") if f.strip()],
                                    "stats":{"Active Users":"0"},
                                    "sort_order":len(st.session_state.live_products),
                                }).execute()
                                r=res.data[0]
                                st.session_state.live_products.append({**r,"features":r["features"] or [],"stats":r["stats"] or {}})
                                st.success(f"✅ {ln} added!"); st.rerun()
                            except Exception as e:
                                st.error(f"Add failed: {e}")

            for i,p in enumerate(st.session_state.live_products):
                tag=" 🟡 DRAFT" if p.get("draft") else " 🟢 Live"
                with st.expander(f"{p['emoji']} {p['name']} {p['version']}{tag}"):
                    is_draft=p.get("draft",False)
                    tc1,tc2,tc3 = st.columns(3)
                    with tc1:
                        if st.button("📢 Go Live" if is_draft else "📝 Set Draft",key=f"draft_{i}"):
                            try:
                                nd=not is_draft
                                if p.get("id"): sb.table("products").update({"draft":nd}).eq("id",p["id"]).execute()
                                st.session_state.live_products[i]["draft"]=nd; st.rerun()
                            except Exception as e: st.error(f"Failed: {e}")
                    with tc2:
                        if i>0 and st.button("⬆️ Move Up",key=f"up_{i}"):
                            st.session_state.live_products.insert(i-1,st.session_state.live_products.pop(i)); st.rerun()
                    with tc3:
                        if i<len(st.session_state.live_products)-1 and st.button("⬇️ Move Down",key=f"dn_{i}"):
                            st.session_state.live_products.insert(i+1,st.session_state.live_products.pop(i)); st.rerun()

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
                                updated={**p,"emoji":ue,"name":un,"subtitle":us,"version":uv,"url":uu,"description":ud,
                                         "features":[f.strip() for f in uf.split("\n") if f.strip()]}
                                try:
                                    if p.get("id"):
                                        sb.table("products").update({
                                            "emoji":ue,"name":un,"subtitle":us,"version":uv,
                                            "url":uu,"description":ud,"features":updated["features"]
                                        }).eq("id",p["id"]).execute()
                                    st.session_state.live_products[i]=updated
                                    st.success("✅ Saved!"); st.rerun()
                                except Exception as e: st.error(f"Save failed: {e}")
                        with sc2:
                            if st.form_submit_button("🗑️ Delete"):
                                try:
                                    if p.get("id"): sb.table("products").delete().eq("id",p["id"]).execute()
                                    st.session_state.live_products.pop(i); st.rerun()
                                except Exception as e: st.error(f"Delete failed: {e}")

            st.markdown("---")
            st.markdown("### 🧠 Coming Soon Products")
            with st.expander("➕ Add Coming Soon"):
                with st.form("form_add_soon"):
                    a1,a2=st.columns([1,6])
                    with a1: ne=st.text_input("Emoji",value="🚀")
                    with a2: nn=st.text_input("Name")
                    nd_=st.text_area("Description",height=100)
                    if st.form_submit_button("Add"):
                        if nn.strip():
                            try:
                                res=sb.table("coming_soon").insert({"emoji":ne.strip() or "🚀","name":nn.strip(),"description":nd_.strip()}).execute()
                                r=res.data[0]
                                st.session_state.coming_soon_products.append({"id":r["id"],"emoji":r["emoji"],"name":r["name"],"description":r["description"]})
                                st.success(f"✅ {nn} added!"); st.rerun()
                            except Exception as e: st.error(f"Add failed: {e}")

            for i,p in enumerate(st.session_state.coming_soon_products):
                with st.expander(f"{p['emoji']} {p['name']}"):
                    with st.form(f"form_soon_{i}"):
                        e1,e2=st.columns([1,6])
                        with e1: se=st.text_input("Emoji",value=p["emoji"],key=f"se_{i}")
                        with e2: sn=st.text_input("Name",value=p["name"],key=f"sn_{i}")
                        sd=st.text_area("Description",value=p["description"],key=f"sd_{i}",height=100)
                        sc1,sc2=st.columns(2)
                        with sc1:
                            if st.form_submit_button("💾 Save"):
                                try:
                                    if p.get("id"): sb.table("coming_soon").update({"emoji":se,"name":sn,"description":sd}).eq("id",p["id"]).execute()
                                    st.session_state.coming_soon_products[i]={"id":p.get("id"),"emoji":se,"name":sn,"description":sd}
                                    st.success("✅ Saved!"); st.rerun()
                                except Exception as e: st.error(f"Save failed: {e}")
                        with sc2:
                            if st.form_submit_button("🗑️ Delete"):
                                try:
                                    if p.get("id"): sb.table("coming_soon").delete().eq("id",p["id"]).execute()
                                    st.session_state.coming_soon_products.pop(i); st.rerun()
                                except Exception as e: st.error(f"Delete failed: {e}")

        # ── ROADMAP ADMIN ──
        with atab_roadmap:
            st.markdown("### 🗺️ Roadmap Items")
            st.caption("Set status to **Released** → auto-adds to Changelog and removes from Roadmap.")
            with st.expander("➕ Add Roadmap Item"):
                with st.form("form_add_road"):
                    ra1,ra2=st.columns([1,6])
                    with ra1: re_=st.text_input("Emoji",value="✨")
                    with ra2: rt=st.text_input("Title")
                    rd=st.text_area("Description",height=80)
                    rs=st.selectbox("Status",["Planned","In Progress","Testing","Released"])
                    if st.form_submit_button("Add Item"):
                        if rt.strip():
                            try:
                                res=sb.table("roadmap").insert({"emoji":re_.strip(),"title":rt.strip(),"description":rd.strip(),"status":rs,"votes":0}).execute()
                                r=res.data[0]
                                st.session_state.roadmap.append({"id":r["id"],"emoji":r["emoji"],"title":r["title"],"desc":r["description"],"status":r["status"],"votes":0})
                                st.success("✅ Added!"); st.rerun()
                            except Exception as e: st.error(f"Add failed: {e}")

            for i,item in enumerate(st.session_state.roadmap):
                with st.expander(f"{item['emoji']} {item['title']} — {item['status']}"):
                    with st.form(f"form_road_{i}"):
                        rr1,rr2=st.columns([1,6])
                        with rr1: rue=st.text_input("Emoji",value=item["emoji"],key=f"re_{i}")
                        with rr2: rut=st.text_input("Title",value=item["title"],key=f"rt_{i}")
                        rud=st.text_area("Description",value=item["desc"],key=f"rd_{i}",height=80)
                        rus=st.selectbox("Status",["Planned","In Progress","Testing","Released"],
                                         index=["Planned","In Progress","Testing","Released"].index(item["status"]),key=f"rs_{i}")
                        rc1,rc2=st.columns(2)
                        with rc1:
                            if st.form_submit_button("💾 Save"):
                                try:
                                    if item.get("id"):
                                        sb.table("roadmap").update({"emoji":rue,"title":rut,"description":rud,"status":rus}).eq("id",item["id"]).execute()
                                    st.session_state.roadmap[i]={**item,"emoji":rue,"title":rut,"desc":rud,"status":rus}
                                    # auto-move to changelog if Released
                                    if rus=="Released":
                                        today=datetime.datetime.now().strftime("%B %Y")
                                        try:
                                            sb.table("changelog").insert({
                                                "version":rut,"release_date":today,
                                                "tag":"Released","tag_badge":"badge-live",
                                                "items":[f"Feature released: {rud}",f"Community votes: {item.get('votes',0)}"]
                                            }).execute()
                                        except Exception: pass
                                        if item.get("id"): sb.table("roadmap").delete().eq("id",item["id"]).execute()
                                        st.session_state.roadmap.pop(i)
                                        st.success(f"🎉 {rut} released and moved to Changelog!")
                                    else:
                                        st.success("✅ Saved!")
                                    st.rerun()
                                except Exception as e: st.error(f"Save failed: {e}")
                        with rc2:
                            if st.form_submit_button("🗑️ Delete"):
                                try:
                                    if item.get("id"): sb.table("roadmap").delete().eq("id",item["id"]).execute()
                                    st.session_state.roadmap.pop(i); st.rerun()
                                except Exception as e: st.error(f"Delete failed: {e}")

        # ── CHANGELOG ADMIN ──
        with atab_changelog:
            st.markdown("### 📣 Changelog Entries")
            with st.expander("➕ Add Entry"):
                with st.form("form_add_cl"):
                    uv1,uv2,uv3=st.columns(3)
                    with uv1: new_ver=st.text_input("Version",placeholder="KitchenMate v1.3")
                    with uv2: new_udate=st.text_input("Release Date",placeholder="March 2026")
                    with uv3:
                        new_tag=st.text_input("Tag",value="Latest")
                        new_tb=st.selectbox("Tag Color",["badge-live","badge-prog","badge-plan","badge-test"])
                    new_items=st.text_area("Changes (one per line)",height=120)
                    if st.form_submit_button("Add to Changelog"):
                        if new_ver.strip():
                            try:
                                res=sb.table("changelog").insert({
                                    "version":new_ver.strip(),"release_date":new_udate.strip(),
                                    "tag":new_tag.strip(),"tag_badge":new_tb,
                                    "items":[x.strip() for x in new_items.split("\n") if x.strip()],
                                }).execute()
                                r=res.data[0]
                                st.session_state.updates.insert(0,{
                                    "id":r["id"],"version":r["version"],"date":r["release_date"],
                                    "tag":r["tag"],"tag_badge":r["tag_badge"],"items":r["items"] or []
                                })
                                st.success("✅ Added!"); st.rerun()
                            except Exception as e: st.error(f"Add failed: {e}")

            for i,upd in enumerate(st.session_state.updates):
                with st.expander(f"{upd['version']} — {upd['date']}"):
                    with st.form(f"form_cl_{i}"):
                        up1,up2,up3=st.columns(3)
                        with up1: uuv=st.text_input("Version",value=upd["version"],key=f"uv_{i}")
                        with up2: uud=st.text_input("Release Date",value=upd["date"],key=f"ud_{i}")
                        with up3:
                            uut=st.text_input("Tag",value=upd["tag"],key=f"ut_{i}")
                            uub=st.selectbox("Tag Color",["badge-live","badge-prog","badge-plan","badge-test"],
                                             index=["badge-live","badge-prog","badge-plan","badge-test"].index(upd["tag_badge"]),key=f"ub_{i}")
                        uui=st.text_area("Changes",value="\n".join(upd["items"]),key=f"ui_{i}",height=100)
                        uc1,uc2=st.columns(2)
                        with uc1:
                            if st.form_submit_button("💾 Save"):
                                updated_items=[x.strip() for x in uui.split("\n") if x.strip()]
                                try:
                                    if upd.get("id"):
                                        sb.table("changelog").update({
                                            "version":uuv,"release_date":uud,"tag":uut,
                                            "tag_badge":uub,"items":updated_items
                                        }).eq("id",upd["id"]).execute()
                                    st.session_state.updates[i]={**upd,"version":uuv,"date":uud,"tag":uut,"tag_badge":uub,"items":updated_items}
                                    st.success("✅ Saved!"); st.rerun()
                                except Exception as e: st.error(f"Save failed: {e}")
                        with uc2:
                            if st.form_submit_button("🗑️ Delete"):
                                try:
                                    if upd.get("id"): sb.table("changelog").delete().eq("id",upd["id"]).execute()
                                    st.session_state.updates.pop(i); st.rerun()
                                except Exception as e: st.error(f"Delete failed: {e}")

        # ── COUNTDOWN ADMIN ──
        with atab_countdown:
            st.markdown("### ⏳ Launch Countdown")
            with st.form("form_countdown"):
                cl1,cl2=st.columns(2)
                with cl1: new_label=st.text_input("Label",value=st.session_state.launch_label)
                with cl2:
                    ld=st.session_state.launch_date
                    new_date=st.date_input("Date",value=ld.date())
                    new_time=st.time_input("Time",value=ld.time())
                if st.form_submit_button("💾 Save"):
                    new_dt=datetime.datetime.combine(new_date,new_time)
                    save_setting("launch_date",{"datetime":new_dt.isoformat()})
                    save_setting("launch_label",{"text":new_label})
                    st.session_state.launch_date=new_dt
                    st.session_state.launch_label=new_label
                    st.success("✅ Countdown updated!")
            st.markdown("**Preview:**")
            render_countdown(st.session_state.launch_label,st.session_state.launch_date)

        # ── SOCIAL LINKS ADMIN ──
        with atab_social:
            st.markdown("### 🔗 Social Links")
            st.caption("Links appear in the footer of every page. Leave blank to hide.")
            with st.form("form_social"):
                new_socials={}
                for platform,current in st.session_state.social_links.items():
                    new_socials[platform]=st.text_input(platform,value=current,placeholder="https://")
                if st.form_submit_button("💾 Save Links"):
                    save_setting("social_links",{"links":new_socials})
                    st.session_state.social_links=new_socials
                    st.success("✅ Social links saved!")

        # ── MESSAGES ADMIN ──
        with atab_messages:
            st.markdown("### ✉️ Contact Messages")
            msgs=st.session_state.contact_messages
            if not msgs:
                st.info("No messages yet.")
            else:
                st.markdown(f"**{len(msgs)} message(s)**")
                for i,m in enumerate(msgs):
                    with st.expander(f"📨 {m['name']} — {m['subject']} · {m['time']}"):
                        st.markdown(f"**From:** {m['name']} (`{m['email']}`)")
                        st.markdown(f"**Subject:** {m['subject']}")
                        st.markdown(f"**Message:**\n\n{m['message']}")
                        if st.button("🗑️ Delete",key=f"del_msg_{i}"):
                            try:
                                if m.get("id"): sb.table("contact_messages").delete().eq("id",m["id"]).execute()
                                st.session_state.contact_messages.pop(i); st.rerun()
                            except Exception as e: st.error(f"Delete failed: {e}")
