"""
Indian Instincts Studios — Full Streamlit Website
v3: Tab-based navigation + responsive hero title fix
Run with: streamlit run app_v3_tabs.py
"""

import streamlit as st
import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Instincts Studios",
    page_icon="🪔",
    layout="wide",
    initial_sidebar_state="collapsed",   # sidebar hidden — we use tabs now
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- fonts ---------- */
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ---------- base ---------- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e6e1;
}

/* ---------- headings ---------- */
h1, h2, h3, h4 {
    font-family: 'Sora', sans-serif;
    color: #f0ede8;
}

/* ---------- TAB NAV — styled to look like a proper top nav bar ---------- */
div[data-testid="stTabs"] > div:first-child {
    background: #0f0f18;
    border-bottom: 1px solid #1e1e2e;
    padding: 0 8px;
    border-radius: 14px 14px 0 0;
    gap: 4px;
}
/* individual tab buttons */
div[data-testid="stTabs"] button[role="tab"] {
    font-family: 'Sora', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #6e6d74 !important;
    padding: 14px 18px !important;
    border: none !important;
    background: transparent !important;
    border-radius: 0 !important;
    transition: color 0.2s !important;
}
div[data-testid="stTabs"] button[role="tab"]:hover {
    color: #f0ede8 !important;
}
/* active tab */
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #ff6b35 !important;
    border-bottom: 2px solid #ff6b35 !important;
}
/* hide the default tab underline Streamlit adds */
div[data-testid="stTabs"] > div:first-child > div {
    gap: 0 !important;
}

/* ---------- cards ---------- */
.card {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 28px 24px;
    margin-bottom: 18px;
    transition: border-color 0.25s;
}
.card:hover { border-color: #ff6b35; }

/* ---------- HERO — RESPONSIVE TITLE FIX ---------- */
.hero-wrap {
    background: linear-gradient(135deg, #0f0f18 0%, #1a0a2e 50%, #0d1a2e 100%);
    border-radius: 24px;
    padding: 56px 48px;
    border: 1px solid #1e1e2e;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(255,107,53,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
/* 
  KEY FIX: Use clamp() so the title scales gracefully between small and large screens.
  On a ~375px mobile viewport this renders at ~1.8rem — one clean line.
  On desktop it grows to 3.2rem as before.
  white-space: nowrap is intentionally NOT set so it can wrap, but the smaller
  base size means it wraps far less aggressively.
*/
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: clamp(1.75rem, 5vw, 3.2rem);
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(135deg, #f0ede8 30%, #ff6b35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
}
.hero-tag {
    font-family: 'Sora', sans-serif;
    font-size: clamp(0.95rem, 2.5vw, 1.2rem);
    color: #ff6b35;
    font-weight: 600;
    letter-spacing: 0.01em;
    margin-bottom: 18px;
}
.hero-desc {
    color: #a09fa6;
    font-size: clamp(0.88rem, 2vw, 1rem);
    line-height: 1.7;
    max-width: 540px;
    margin-bottom: 28px;
}

/* ---------- badges ---------- */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-right: 6px;
}
.badge-live { background: #0d2b1d; color: #34d399; border: 1px solid #34d399; }
.badge-plan { background: #1e1a0d; color: #fbbf24; border: 1px solid #fbbf24; }
.badge-prog { background: #0d1a2e; color: #60a5fa; border: 1px solid #60a5fa; }
.badge-test { background: #1e0d1a; color: #c084fc; border: 1px solid #c084fc; }
.badge-soon { background: #1a0a2e; color: #a78bfa; border: 1px solid #a78bfa; }

/* ---------- stat box ---------- */
.stat-box {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
}
.stat-num {
    font-family: 'Sora', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #ff6b35;
}
.stat-lbl { color: #6e6d74; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

/* ---------- countdown ---------- */
.cd-wrap {
    background: linear-gradient(135deg, #13131f, #1a0a2e);
    border: 1px solid #2a1a3e;
    border-radius: 20px;
    padding: 40px 32px;
    text-align: center;
    margin: 32px 0;
}
.cd-num {
    font-family: 'Sora', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: #ff6b35;
    display: block;
}
.cd-unit { color: #6e6d74; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; }

/* ---------- review card ---------- */
.review-card {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}
.review-card.love { border-color: #ff6b35; }
.stars { color: #ff6b35; font-size: 1.1rem; }
.reviewer { font-weight: 600; font-size: 0.9rem; color: #f0ede8; }
.review-text { color: #a09fa6; font-size: 0.92rem; line-height: 1.6; margin-top: 8px; }

/* ---------- update card ---------- */
.update-card {
    background: #13131f;
    border-left: 3px solid #ff6b35;
    border-radius: 0 14px 14px 0;
    padding: 24px 24px 24px 28px;
    margin-bottom: 20px;
}
.update-ver { font-family: 'Sora', sans-serif; font-size: 1rem; font-weight: 700; color: #f0ede8; }
.update-date { color: #6e6d74; font-size: 0.78rem; margin-top: 2px; margin-bottom: 12px; }
.update-item { color: #a09fa6; font-size: 0.9rem; line-height: 1.7; }
.update-item::before { content: "→ "; color: #ff6b35; }

/* ---------- section header ---------- */
.sec-header {
    font-family: 'Sora', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #ff6b35;
    margin-bottom: 6px;
}
.sec-title {
    font-family: 'Sora', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f0ede8;
    margin-bottom: 28px;
}

/* ---------- product feature list ---------- */
.feat-item { color: #a09fa6; font-size: 0.9rem; padding: 6px 0; border-bottom: 1px solid #1e1e2e; }
.feat-item::before { content: "✦ "; color: #ff6b35; }

/* ---------- teaser card ---------- */
.teaser {
    background: repeating-linear-gradient(
        45deg,
        #13131f,
        #13131f 10px,
        #0f0f18 10px,
        #0f0f18 20px
    );
    border: 1px dashed #2a2a3e;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
}

/* ---------- divider ---------- */
.div-line { border: none; border-top: 1px solid #1e1e2e; margin: 36px 0; }

/* ---------- form overrides ---------- */
input, textarea, select {
    background: #13131f !important;
    color: #e8e6e1 !important;
    border-color: #1e1e2e !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #13131f !important;
    border-color: #2a2a3e !important;
    color: #e8e6e1 !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: #ff6b35 !important;
    color: #0a0a0f !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
.stButton > button:disabled { background: #1e1e2e !important; color: #6e6d74 !important; }

/* ---------- hide streamlit chrome & sidebar toggle ---------- */
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }
.block-container { padding-top: 1.5rem; padding-bottom: 4rem; max-width: 1100px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "votes" not in st.session_state:
    st.session_state.votes = {
        "Meal Nutrition Calculator": 42,
        "Pantry Scanner": 31,
        "Weekly Meal Planner": 58,
        "Recipe Sharing Community": 19,
        "Multi-Language Support": 27,
    }
if "reviews" not in st.session_state:
    st.session_state.reviews = [
        {"name": "Priya S.",  "product": "KitchenMate", "rating": 5, "text": "This app has completely changed how I cook. I just throw in whatever's left in my fridge and boom — a real recipe!"},
        {"name": "Arjun M.", "product": "KitchenMate", "rating": 5, "text": "Super simple to use and the recipes are genuinely delicious. Can't wait for the nutrition calculator!"},
        {"name": "Divya K.", "product": "KitchenMate", "rating": 4, "text": "Great concept and clean UI. Would love a meal planning feature next."},
        {"name": "Rohan T.", "product": "KitchenMate", "rating": 5, "text": "The fastest way to decide what to cook. Brilliant little tool."},
    ]
if "voted" not in st.session_state:
    st.session_state.voted = set()

# ─────────────────────────────────────────────
# TOP NAV BRANDING STRIP
# ─────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; padding: 8px 4px 18px 4px;">
    <span style="font-size:1.5rem;">🪔</span>
    <div>
        <span style="font-family:Sora,sans-serif; font-size:1.05rem; font-weight:800; color:#f0ede8;">Indian Instincts Studios</span>
        <span style="margin-left:12px; font-size:0.7rem; color:#6e6d74; text-transform:uppercase; letter-spacing:0.1em;">v1.2 · KitchenMate Live</span>
    </div>
    <span class="badge badge-live" style="margin-left:auto;">● Live</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB NAVIGATION
# ─────────────────────────────────────────────
tab_home, tab_products, tab_roadmap, tab_reviews, tab_updates, tab_about = st.tabs([
    "🏠  Home",
    "📦  Products",
    "🗺️  Roadmap",
    "⭐  Reviews",
    "📣  Updates",
    "ℹ️  About",
])

# ═══════════════════════════════════════════════════════
# HOME TAB
# ═══════════════════════════════════════════════════════
with tab_home:

    # HERO — title now uses clamp() via .hero-title class (see CSS above)
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">Indian Instincts Studios</div>
        <div class="hero-tag">Building smart AI tools for everyday life.</div>
        <div class="hero-desc">
            We are a small product studio obsessed with turning everyday friction into delightful,
            AI-powered tools. From the kitchen to the calendar — we build things people actually use.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("🚀 Explore Products", key="hero_exp"):
            st.info("👇 Head to the **Products** tab above to see what we've built.")
    with col2:
        if st.button("🍳 Try KitchenMate", key="hero_try"):
            st.info("🍳 KitchenMate is live! Visit **kitchenmate.app** to get started.")

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # LIVE STATS
    st.markdown('<div class="sec-header">Live Stats</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [("2,841", "KitchenMate Users"), ("14,320", "Recipes Generated"), ("1", "Products Live"), ("3", "Coming Soon")]
    for col, (num, lbl) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-num">{num}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # FEATURED PRODUCT CARD
    st.markdown('<div class="sec-header">Featured Product</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Meet KitchenMate</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns([1, 1])
    with fc1:
        st.markdown("""
        <div class="card">
            <span class="badge badge-live">● Live</span>
            <h3 style="margin-top:16px; font-family:Sora,sans-serif;">🍳 KitchenMate</h3>
            <p style="color:#a09fa6; line-height:1.7; font-size:0.95rem;">
                Tell KitchenMate what ingredients you have — it instantly generates delicious,
                step-by-step recipes powered by AI. No more staring at the fridge wondering what to cook.
            </p>
            <div style="margin-top:20px;">
                <div class="feat-item">AI recipe generation</div>
                <div class="feat-item">Ingredient-based cooking</div>
                <div class="feat-item">Simple, clean UI</div>
                <div class="feat-item">Instant suggestions</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with fc2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a0a2e,#0d1a2e); border-radius:16px;
                    height:260px; display:flex; align-items:center; justify-content:center;
                    border:1px solid #2a1a3e;">
            <div style="text-align:center;">
                <div style="font-size:4rem;">🍳</div>
                <div style="font-family:Sora,sans-serif; color:#ff6b35; font-weight:700; margin-top:8px;">KitchenMate</div>
                <div style="color:#6e6d74; font-size:0.8rem; margin-top:4px;">AI Kitchen Assistant</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    # COUNTDOWN
    launch_date = datetime.datetime(2025, 9, 1, 0, 0, 0)
    now = datetime.datetime.now()
    delta = launch_date - now
    if delta.total_seconds() > 0:
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, _ = divmod(rem, 60)
    else:
        days = hours = minutes = 0

    st.markdown('<div class="sec-header">Coming Soon</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="cd-wrap">
        <div style="font-family:Sora,sans-serif; font-size:1.1rem; color:#f0ede8; margin-bottom:24px; font-weight:600;">
            ⏳ Next Product Launch
        </div>
    """, unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    for col, val, unit in zip([t1, t2, t3], [days, hours, minutes], ["Days", "Hours", "Minutes"]):
        with col:
            st.markdown(f"""
            <div style="text-align:center;">
                <span class="cd-num">{val:02d}</span>
                <span class="cd-unit">{unit}</span>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # FUTURE TEASERS
    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-header'>What's Next</div>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    teasers = [
        ("🧮", "NutriScan",  "Track nutrition instantly using your camera."),
        ("📅", "MealWeek",   "AI-powered weekly meal planning made effortless."),
        ("🛒", "PantryBot",  "Smart pantry management with auto shopping lists."),
    ]
    for col, (icon, name, desc) in zip([t1, t2, t3], teasers):
        with col:
            st.markdown(f"""
            <div class="teaser">
                <div style="font-size:2.5rem;">{icon}</div>
                <div style="font-family:Sora,sans-serif; font-weight:700; color:#f0ede8; margin:12px 0 6px;">{name}</div>
                <div style="color:#6e6d74; font-size:0.85rem; line-height:1.5;">{desc}</div>
                <div style="margin-top:16px;"><span class="badge badge-soon">Coming Soon</span></div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# PRODUCTS TAB
# ═══════════════════════════════════════════════════════
with tab_products:
    st.markdown('<div class="sec-header">Our Products</div>', unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>What We've Built</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("""
        <div class="card">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                <div style="font-size:2.5rem;">🍳</div>
                <div>
                    <div style="font-family:Sora,sans-serif; font-size:1.4rem; font-weight:700; color:#f0ede8;">KitchenMate</div>
                    <div style="color:#6e6d74; font-size:0.82rem;">AI Kitchen Assistant</div>
                </div>
                <span class="badge badge-live" style="margin-left:auto;">● Live</span>
            </div>
            <p style="color:#a09fa6; line-height:1.75; font-size:0.95rem;">
                An AI-powered cooking assistant that generates recipes based on the ingredients you have.
                No more food waste, no more meal-planning anxiety.
            </p>
            <div style="margin-top:20px; margin-bottom:4px; font-size:0.75rem; color:#6e6d74; text-transform:uppercase; letter-spacing:0.1em;">Features</div>
            <div class="feat-item">AI recipe generation from your ingredients</div>
            <div class="feat-item">Ingredient-based smart cooking suggestions</div>
            <div class="feat-item">Simple, distraction-free UI</div>
            <div class="feat-item">Quick recipe suggestions (under 5 seconds)</div>
            <div class="feat-item">Dietary preference filters</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a0a2e,#0d1a2e); border-radius:16px;
                    height:220px; display:flex; align-items:center; justify-content:center;
                    border:1px solid #2a1a3e; margin-bottom:16px;">
            <div style="text-align:center;">
                <div style="font-size:4rem;">🍳</div>
                <div style="font-family:Sora,sans-serif; color:#ff6b35; font-weight:700; margin-top:8px;">KitchenMate</div>
                <div style="color:#6e6d74; font-size:0.8rem;">v1.2</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🚀 Try KitchenMate Now", key="try_km")
        st.markdown("""
        <div style="background:#13131f; border:1px solid #1e1e2e; border-radius:12px; padding:16px; margin-top:12px;">
            <div style="font-size:0.75rem; color:#6e6d74; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:12px;">Product Stats</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#a09fa6; font-size:0.85rem;">Active Users</span>
                <span style="color:#ff6b35; font-family:Sora,sans-serif; font-weight:700;">2,841</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#a09fa6; font-size:0.85rem;">Recipes Generated</span>
                <span style="color:#ff6b35; font-family:Sora,sans-serif; font-weight:700;">14,320</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="color:#a09fa6; font-size:0.85rem;">Avg. Rating</span>
                <span style="color:#ff6b35; font-family:Sora,sans-serif; font-weight:700;">4.8 ⭐</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">In The Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Coming Soon Products</div>', unsafe_allow_html=True)

    cs1, cs2, cs3 = st.columns(3)
    coming_soon = [
        ("🧮", "NutriScan",  "Point your camera at any meal and get instant, accurate nutritional information powered by computer vision."),
        ("📅", "MealWeek",   "AI-curated weekly meal plans tailored to your dietary goals, budget, and flavor preferences."),
        ("🛒", "PantryBot",  "Intelligently track your pantry, predict what you'll run out of, and auto-generate shopping lists."),
    ]
    for col, (icon, name, desc) in zip([cs1, cs2, cs3], coming_soon):
        with col:
            st.markdown(f"""
            <div class="card" style="opacity:0.7;">
                <div style="font-size:2.2rem; margin-bottom:12px;">{icon}</div>
                <div style="font-family:Sora,sans-serif; font-size:1.1rem; font-weight:700; color:#f0ede8; margin-bottom:8px;">{name}</div>
                <p style="color:#a09fa6; font-size:0.88rem; line-height:1.65;">{desc}</p>
                <span class="badge badge-soon" style="margin-top:16px; display:inline-block;">Coming Soon</span>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# ROADMAP TAB
# ═══════════════════════════════════════════════════════
with tab_roadmap:
    st.markdown('<div class="sec-header">Product Roadmap</div>', unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>What We're Building Next</div>", unsafe_allow_html=True)
    st.markdown('<p style="color:#6e6d74; margin-top:-16px; margin-bottom:28px; font-size:0.9rem;">Vote on features you want to see. Top-voted ideas get built first.</p>', unsafe_allow_html=True)

    roadmap = [
        {"title": "Meal Nutrition Calculator", "desc": "Automatically calculate calories, macros, and nutrients for any recipe generated by KitchenMate.", "status": "In Progress", "badge": "badge-prog", "emoji": "🧮"},
        {"title": "Pantry Scanner",            "desc": "Use your phone camera to scan ingredients in your fridge or pantry — no typing required.",               "status": "Planned",     "badge": "badge-plan", "emoji": "📸"},
        {"title": "Weekly Meal Planner",        "desc": "Generate a full 7-day meal plan based on your dietary preferences, budget, and available time.",          "status": "Planned",     "badge": "badge-plan", "emoji": "📅"},
        {"title": "Recipe Sharing Community",   "desc": "Share your AI-generated recipes with the community and discover what others are cooking.",                "status": "Testing",     "badge": "badge-test", "emoji": "👥"},
        {"title": "Multi-Language Support",     "desc": "Use KitchenMate in Hindi, Tamil, Telugu, and other Indian languages.",                                    "status": "Planned",     "badge": "badge-plan", "emoji": "🌐"},
    ]

    for item in roadmap:
        key = item["title"]
        vote_count = st.session_state.votes.get(key, 0)
        already_voted = key in st.session_state.voted

        col_card, col_vote = st.columns([5, 1])
        with col_card:
            st.markdown(f"""
            <div class="card" style="margin-bottom:4px;">
                <div style="display:flex; align-items:flex-start; gap:14px;">
                    <div style="font-size:1.8rem;">{item['emoji']}</div>
                    <div style="flex:1;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                            <span style="font-family:Sora,sans-serif; font-size:1.05rem; font-weight:700; color:#f0ede8;">{item['title']}</span>
                            <span class="badge {item['badge']}">{item['status']}</span>
                        </div>
                        <p style="color:#a09fa6; font-size:0.88rem; line-height:1.6; margin:0;">{item['desc']}</p>
                        <div style="margin-top:10px; font-family:Sora,sans-serif; font-size:1.1rem; font-weight:800; color:#ff6b35;">
                            ▲ {vote_count} votes
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_vote:
            st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)
            if already_voted:
                st.button("✓ Voted", key=f"vote_{key}", disabled=True)
            else:
                if st.button("Vote ▲", key=f"vote_{key}"):
                    st.session_state.votes[key] = st.session_state.votes.get(key, 0) + 1
                    st.session_state.voted.add(key)
                    st.rerun()
        st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#13131f; border:1px solid #1e1e2e; border-radius:14px; padding:20px 24px; margin-top:20px; text-align:center;">
        <span style="color:#6e6d74; font-size:0.88rem;">Have a feature idea? Drop it in the </span>
        <span style="color:#ff6b35; font-weight:600;">Reviews & Feedback</span>
        <span style="color:#6e6d74; font-size:0.88rem;"> tab.</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# REVIEWS TAB
# ═══════════════════════════════════════════════════════
with tab_reviews:
    st.markdown('<div class="sec-header">Community</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Reviews & Feedback</div>', unsafe_allow_html=True)

    with st.expander("✍️ Write a Review", expanded=True):
        with st.form("review_form"):
            r1, r2 = st.columns(2)
            with r1:
                name = st.text_input("Your Name")
                product = st.selectbox("Product", ["KitchenMate", "NutriScan (Coming Soon)", "MealWeek (Coming Soon)"])
            with r2:
                rating = st.select_slider("Rating", options=[1, 2, 3, 4, 5], value=5)
                st.markdown(f"<div style='color:#ff6b35; font-size:1.3rem; margin-top:6px;'>{'⭐' * rating}</div>", unsafe_allow_html=True)
            review_text = st.text_area("Your Review", placeholder="Tell us what you think...", height=110)
            submitted = st.form_submit_button("Submit Review")
            if submitted:
                if name.strip() and review_text.strip():
                    st.session_state.reviews.insert(0, {
                        "name": name.strip(),
                        "product": product,
                        "rating": rating,
                        "text": review_text.strip(),
                    })
                    st.success("🎉 Thank you for your review!")
                else:
                    st.error("Please fill in your name and review.")

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)

    love_reviews = [r for r in st.session_state.reviews if r["rating"] == 5][:5]
    if love_reviews:
        st.markdown('<div class="sec-header">Highlights</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">💛 Wall of Love</div>', unsafe_allow_html=True)
        lc1, lc2 = st.columns(2)
        for i, rev in enumerate(love_reviews):
            col = lc1 if i % 2 == 0 else lc2
            with col:
                st.markdown(f"""
                <div class="review-card love">
                    <div class="stars">{'⭐' * rev['rating']}</div>
                    <div class="review-text" style="margin-top:10px; font-style:italic;">"{rev['text']}"</div>
                    <div style="margin-top:14px; display:flex; align-items:center; gap:8px;">
                        <div style="width:28px; height:28px; border-radius:50%; background:#ff6b35;
                                    display:flex; align-items:center; justify-content:center;
                                    font-size:0.75rem; font-weight:700; color:#0a0a0f;">
                            {rev['name'][0].upper()}
                        </div>
                        <div>
                            <div class="reviewer">{rev['name']}</div>
                            <div style="color:#6e6d74; font-size:0.75rem;">{rev['product']}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">All Reviews</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-title">{len(st.session_state.reviews)} Reviews</div>', unsafe_allow_html=True)

    for rev in st.session_state.reviews:
        st.markdown(f"""
        <div class="review-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:32px; height:32px; border-radius:50%; background:#1e1e2e;
                                display:flex; align-items:center; justify-content:center;
                                font-size:0.8rem; font-weight:700; color:#ff6b35;">
                        {rev['name'][0].upper()}
                    </div>
                    <div>
                        <div class="reviewer">{rev['name']}</div>
                        <div style="color:#6e6d74; font-size:0.75rem;">{rev['product']}</div>
                    </div>
                </div>
                <div class="stars">{'⭐' * rev['rating']}</div>
            </div>
            <div class="review-text">"{rev['text']}"</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# UPDATES TAB
# ═══════════════════════════════════════════════════════
with tab_updates:
    st.markdown('<div class="sec-header">Changelog</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Product Updates</div>', unsafe_allow_html=True)
    st.markdown("<p style=\"color:#6e6d74; margin-top:-16px; margin-bottom:28px; font-size:0.9rem;\">Everything that's shipped, fixed, and improved.</p>", unsafe_allow_html=True)

    updates = [
        {
            "version": "KitchenMate v1.2", "date": "February 2025", "tag": "Latest", "tag_badge": "badge-live",
            "items": [
                "Faster AI recipe generation — results in under 3 seconds",
                "Redesigned UI with improved readability and spacing",
                "Added clear button to reset ingredient list instantly",
                "Better mobile responsiveness across all screen sizes",
                "Improved AI prompt for more culturally relevant Indian recipes",
            ]
        },
        {
            "version": "KitchenMate v1.1", "date": "December 2024", "tag": "Stable", "tag_badge": "badge-prog",
            "items": [
                "Better ingredient detection and parsing",
                "UI improvements: cleaner recipe card layout",
                "Added vegetarian/non-vegetarian filter",
                "Performance improvements — 40% faster load time",
            ]
        },
        {
            "version": "KitchenMate v1.0", "date": "October 2024", "tag": "Launch", "tag_badge": "badge-plan",
            "items": [
                "Initial launch of KitchenMate AI Kitchen Assistant",
                "Core feature: ingredient-based recipe generation",
                "Basic UI with recipe display and ingredient input",
                "Integrated Claude AI for recipe generation",
            ]
        },
    ]

    for upd in updates:
        st.markdown(f"""
        <div class="update-card">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
                <span class="update-ver">{upd['version']}</span>
                <span class="badge {upd['tag_badge']}">{upd['tag']}</span>
            </div>
            <div class="update-date">Released {upd['date']}</div>
            {"".join(f'<div class="update-item">{item}</div>' for item in upd['items'])}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">Next Release</div>', unsafe_allow_html=True)

    # Countdown — guarded against past dates (Fix 1 from v2)
    launch_date = datetime.datetime(2025, 9, 1, 0, 0, 0)
    now = datetime.datetime.now()
    delta = launch_date - now
    if delta.total_seconds() > 0:
        days = delta.days
        hours, rem = divmod(delta.seconds, 3600)
        minutes, _ = divmod(rem, 60)
    else:
        days = hours = minutes = 0

    st.markdown(f"""
    <div class="cd-wrap">
        <div style="font-family:Sora,sans-serif; font-size:1rem; color:#f0ede8; margin-bottom:20px;">
            ⏳ KitchenMate v1.3 — dropping soon
        </div>
        <div style="display:flex; justify-content:center; gap:48px;">
            <div style="text-align:center;">
                <span class="cd-num">{days:02d}</span>
                <span class="cd-unit">Days</span>
            </div>
            <div style="text-align:center;">
                <span class="cd-num">{hours:02d}</span>
                <span class="cd-unit">Hours</span>
            </div>
            <div style="text-align:center;">
                <span class="cd-num">{minutes:02d}</span>
                <span class="cd-unit">Minutes</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════
# ABOUT TAB
# ═══════════════════════════════════════════════════════
with tab_about:
    st.markdown('<div class="sec-header">Our Story</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">About Indian Instincts Studios</div>', unsafe_allow_html=True)

    ab1, ab2 = st.columns([3, 2])
    with ab1:
        st.markdown("""
        <div class="card" style="margin-bottom:20px;">
            <h3 style="font-family:Sora,sans-serif; color:#ff6b35; margin-bottom:16px;">Who We Are</h3>
            <p style="color:#a09fa6; line-height:1.8; font-size:0.95rem;">
                Indian Instincts Studios is a small product studio focused on building smart AI tools
                that solve everyday problems — starting with the kitchen, and expanding to every corner
                of daily life.
            </p>
            <p style="color:#a09fa6; line-height:1.8; font-size:0.95rem; margin-top:12px;">
                Currently a 4-person team based in India, we launched our first product —
                KitchenMate — in late 2024. We believe great tools should feel effortless,
                not overwhelming.
            </p>
        </div>
        <div class="card">
            <h3 style="font-family:Sora,sans-serif; color:#ff6b35; margin-bottom:16px;">🎯 Our Mission</h3>
            <p style="color:#a09fa6; line-height:1.8; font-size:0.95rem;">
                Build useful AI tools that make daily life easier — for everyday Indians and beyond.
            </p>
            <div style="margin-top:20px;">
                <div class="feat-item">AI-first from day one</div>
                <div class="feat-item">Simplicity over complexity</div>
                <div class="feat-item">Built for real everyday problems</div>
                <div class="feat-item">Proudly made in India 🇮🇳</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with ab2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#13131f,#1a0a2e); border-radius:20px;
                    padding:32px; border:1px solid #2a1a3e; text-align:center; margin-bottom:20px;">
            <div style="font-size:3.5rem; margin-bottom:12px;">🪔</div>
            <div style="font-family:Sora,sans-serif; font-size:1.4rem; font-weight:800; color:#f0ede8;">Indian Instincts</div>
            <div style="font-size:0.8rem; color:#6e6d74; letter-spacing:0.12em; text-transform:uppercase; margin-top:4px;">Studios</div>
        </div>
        <div class="stat-box" style="margin-bottom:16px;">
            <div class="stat-num">4</div>
            <div class="stat-lbl">Team Members</div>
        </div>
        <div class="stat-box" style="margin-bottom:16px;">
            <div class="stat-num">1</div>
            <div class="stat-lbl">Products Live</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">2024</div>
            <div class="stat-lbl">Founded</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-header">The Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">4 People. 1 Big Vision.</div>', unsafe_allow_html=True)

    tm1, tm2, tm3, tm4 = st.columns(4)
    team = [
        ("🧑‍💻", "Founder & CEO",  "Product vision & strategy"),
        ("👩‍🎨", "Lead Designer",   "UI/UX & brand design"),
        ("🧑‍🔬", "AI Engineer",     "Model integration & APIs"),
        ("👨‍💼", "Growth Lead",     "Marketing & community"),
    ]
    for col, (emoji, role, desc) in zip([tm1, tm2, tm3, tm4], team):
        with col:
            st.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:2.2rem; margin-bottom:10px;">{emoji}</div>
                <div style="font-family:Sora,sans-serif; font-size:0.9rem; font-weight:700; color:#f0ede8;">{role}</div>
                <div style="color:#6e6d74; font-size:0.78rem; margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='div-line'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; padding:24px 0;">
        <div style="font-family:Sora,sans-serif; font-size:0.8rem; color:#3a3a4e; letter-spacing:0.06em;">
            © 2025 Indian Instincts Studios · Made with 🪔 in India
        </div>
    </div>
    """, unsafe_allow_html=True)
