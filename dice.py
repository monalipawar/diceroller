import random
import streamlit as st
import time

st.set_page_config(page_title="Dice Roller", page_icon="🎲", layout="centered")

# ═══════════════════════════════════════════════════════════════════════════════
# THEMES
# ═══════════════════════════════════════════════════════════════════════════════
THEMES = {
    "Cosmic":   {
        "bg": "radial-gradient(ellipse at 20% 50%, #0d1b3e 0%, #020b18 60%, #000 100%)",
        "accent1": "#7dd3fc", "accent2": "#c084fc",
        "border": "rgba(99,179,255,0.4)", "glow": "rgba(99,179,255,0.35)",
        "btn_border": "rgba(99,179,255,0.4)", "btn_text": "#e0f2fe",
    },
    "Ember":    {
        "bg": "radial-gradient(ellipse at 20% 50%, #3b0a00 0%, #1a0500 60%, #000 100%)",
        "accent1": "#fb923c", "accent2": "#f87171",
        "border": "rgba(251,146,60,0.4)", "glow": "rgba(251,146,60,0.35)",
        "btn_border": "rgba(251,146,60,0.4)", "btn_text": "#fed7aa",
    },
    "Forest":   {
        "bg": "radial-gradient(ellipse at 20% 50%, #052e16 0%, #011808 60%, #000 100%)",
        "accent1": "#4ade80", "accent2": "#86efac",
        "border": "rgba(74,222,128,0.4)", "glow": "rgba(74,222,128,0.35)",
        "btn_border": "rgba(74,222,128,0.4)", "btn_text": "#bbf7d0",
    },
    "Neon":     {
        "bg": "radial-gradient(ellipse at 20% 50%, #1a003b 0%, #0a0018 60%, #000 100%)",
        "accent1": "#f0abfc", "accent2": "#a78bfa",
        "border": "rgba(240,171,252,0.4)", "glow": "rgba(240,171,252,0.35)",
        "btn_border": "rgba(240,171,252,0.4)", "btn_text": "#fae8ff",
    },
    "Gold":     {
        "bg": "radial-gradient(ellipse at 20% 50%, #292400 0%, #141200 60%, #000 100%)",
        "accent1": "#fde047", "accent2": "#fb923c",
        "border": "rgba(253,224,71,0.4)", "glow": "rgba(253,224,71,0.35)",
        "btn_border": "rgba(253,224,71,0.4)", "btn_text": "#fef9c3",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
for k, v in [
    ("roll", None),
    ("history", []),
    ("multiplayer", None),   # None = not asked, True/False
    ("num_players", 2),
    ("current_player", 0),
    ("theme", "Cosmic"),
    ("player_rolls", {}),
]:
    if k not in st.session_state:
        st.session_state[k] = v

theme = st.session_state.theme
T = THEMES[theme]

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {{ font-family: 'Outfit', sans-serif; }}

.stApp {{
    background: {T['bg']};
    overflow: hidden;
}}
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 70%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 50% 10%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 35%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 55%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 65% 45%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 85%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 15%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 5%  90%, rgba(255,255,255,0.6) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.glass-card {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 2.5rem 2rem;
    margin: 0 auto;
    max-width: 480px;
    text-align: center;
    position: relative;
    z-index: 1;
}}

.die-face {{
    width: 140px; height: 140px;
    margin: 0 auto 1.5rem;
    display: block;
    filter: drop-shadow(0 0 24px {T['glow']});
    transition: transform 0.15s ease;
}}

.roll-result {{
    font-size: 4.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, {T['accent1']}, {T['accent2']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0.25rem 0;
}}
.roll-label {{
    color: rgba(255,255,255,0.45);
    font-size: 0.85rem;
    font-weight: 300;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}}

.player-badge {{
    display: inline-block;
    background: linear-gradient(135deg, {T['accent1']}33, {T['accent2']}33);
    border: 1px solid {T['border']};
    border-radius: 30px;
    padding: 6px 20px;
    font-size: 0.95rem;
    font-weight: 600;
    color: {T['accent1']};
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
}}

.scoreboard {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    text-align: left;
}}
.scoreboard-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 0;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.65);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}}
.scoreboard-row:last-child {{ border-bottom: none; }}
.scoreboard-row.active {{
    color: {T['accent1']};
    font-weight: 600;
}}
.score-val {{
    background: linear-gradient(135deg, {T['accent1']}, {T['accent2']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}}

.history-row {{
    display: flex; gap: 8px;
    justify-content: center; flex-wrap: wrap;
    margin-top: 1.25rem;
}}
.history-pill {{
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    width: 36px; height: 36px;
    display: inline-flex;
    align-items: center; justify-content: center;
    color: rgba(255,255,255,0.7);
    font-size: 0.95rem; font-weight: 500;
    font-family: 'Outfit', sans-serif;
}}
.history-pill.latest {{
    background: {T['accent1']}2e;
    border-color: {T['border']};
    color: {T['accent1']};
}}

div.stButton > button {{
    width: 100%;
    background: linear-gradient(135deg, {T['accent1']}33, {T['accent2']}33);
    border: 1px solid {T['btn_border']};
    border-radius: 14px;
    color: {T['btn_text']};
    font-family: 'Outfit', sans-serif;
    font-size: 1rem; font-weight: 600;
    letter-spacing: 0.06em;
    padding: 0.75rem 0;
    transition: all 0.2s ease;
    cursor: pointer;
}}
div.stButton > button:hover {{
    background: linear-gradient(135deg, {T['accent1']}55, {T['accent2']}55);
    border-color: {T['accent1']};
    transform: translateY(-1px);
    box-shadow: 0 8px 24px {T['glow']};
}}
div.stButton > button:active {{
    transform: translateY(0px) scale(0.98);
}}

.app-title {{
    color: rgba(255,255,255,0.9);
    font-size: 1.5rem; font-weight: 600;
    letter-spacing: 0.05em; margin-bottom: 0.25rem;
}}
.app-subtitle {{
    color: rgba(255,255,255,0.35);
    font-size: 0.8rem; letter-spacing: 0.15em;
    text-transform: uppercase; margin-bottom: 1.5rem;
}}
.hint {{
    color: rgba(255,255,255,0.25);
    font-size: 0.75rem; margin-top: 0.6rem;
    letter-spacing: 0.05em;
}}
.section-label {{
    color: rgba(255,255,255,0.5);
    font-size: 0.8rem; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.5rem;
}}

/* selectbox + radio overrides */
[data-testid="stSelectbox"] > div > div {{
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important; color: white !important;
    font-family: 'Outfit', sans-serif !important;
}}
label, .stRadio label, .stNumberInput label {{ color: rgba(255,255,255,0.6) !important; font-family: 'Outfit', sans-serif !important; }}
.stRadio > div {{ gap: 8px; }}
[data-testid="stNumberInput"] input {{
    background: rgba(15,23,42,0.85) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    caret-color: white !important;
}}
[data-testid="stNumberInput"] input::selection {{
    background: rgba(99,179,255,0.4) !important;
    color: white !important;
}}
</style>

<script>
document.addEventListener('keydown', function(e) {{
    if (e.code === 'Space' && !['INPUT','TEXTAREA','BUTTON'].includes(document.activeElement.tagName)) {{
        e.preventDefault();
        const btns = window.parent.document.querySelectorAll('button');
        for (const b of btns) {{
            if (b.innerText.includes('Roll')) {{ b.click(); break; }}
        }}
    }}
}});
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DOT POSITIONS & SVG
# ═══════════════════════════════════════════════════════════════════════════════
DOT_POSITIONS = {
    1: [(70, 70)],
    2: [(42, 42), (98, 98)],
    3: [(42, 42), (70, 70), (98, 98)],
    4: [(42, 42), (98, 42), (42, 98), (98, 98)],
    5: [(42, 42), (98, 42), (70, 70), (42, 98), (98, 98)],
    6: [(42, 35), (98, 35), (42, 70), (98, 70), (42, 105), (98, 105)],
}

def die_svg(n, a1, a2):
    dots = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="8" fill="url(#dotGrad)"/>'
        for cx, cy in DOT_POSITIONS.get(n, [])
    )
    return f"""
    <svg class="die-face" viewBox="0 0 140 140" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="faceGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="rgba(255,255,255,0.12)"/>
          <stop offset="100%" stop-color="rgba(255,255,255,0.04)"/>
        </linearGradient>
        <linearGradient id="dotGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{a1}"/>
          <stop offset="100%" stop-color="{a2}"/>
        </linearGradient>
      </defs>
      <rect x="6" y="6" width="128" height="128" rx="22"
            fill="url(#faceGrad)"
            stroke="rgba(255,255,255,0.18)" stroke-width="1.5"/>
      {dots}
    </svg>
    """

LABELS = {1:"Snake eyes", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Max roll!"}

# ═══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════
col = st.columns([1, 2, 1])[1]

with col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="app-title">🎲 Dice Roller</div>', unsafe_allow_html=True)

    # ── Theme picker ──────────────────────────────────────────────────────────
    chosen_theme = st.selectbox("🎨 Theme", list(THEMES.keys()),
                                index=list(THEMES.keys()).index(st.session_state.theme),
                                key="theme_sel")
    if chosen_theme != st.session_state.theme:
        st.session_state.theme = chosen_theme
        st.rerun()

    st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)

    # ── Multiplayer setup ─────────────────────────────────────────────────────
    if st.session_state.multiplayer is None:
        st.markdown('<div class="app-subtitle">Are you playing with others?</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("👥 Yes, multiplayer", use_container_width=True):
                st.session_state.multiplayer = True
                st.rerun()
        with c2:
            if st.button("🎲 Solo play", use_container_width=True):
                st.session_state.multiplayer = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    # ── Player count setup (multiplayer only) ─────────────────────────────────
    if st.session_state.multiplayer and st.session_state.num_players == 2 and not st.session_state.player_rolls:
        st.markdown('<div class="app-subtitle">How many players?</div>', unsafe_allow_html=True)
        num = st.number_input("", min_value=2, max_value=8, value=2,
                              label_visibility="collapsed", key="player_count_input")
        if st.button("✅ Start Game", use_container_width=True):
            st.session_state.num_players = int(num)
            st.session_state.current_player = 0
            st.session_state.player_rolls = {i: [] for i in range(int(num))}
            st.rerun()
        if st.button("← Back", use_container_width=True):
            st.session_state.multiplayer = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    # ── Main roller ───────────────────────────────────────────────────────────
    mp = st.session_state.multiplayer
    cp = st.session_state.current_player
    np = st.session_state.num_players

    # Subtitle
    if mp:
        st.markdown(f'<div class="player-badge">🎮 Player {cp + 1}\'s Turn</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="app-subtitle">Six-sided · Random</div>', unsafe_allow_html=True)

    # Scoreboard (multiplayer only)
    if mp and st.session_state.player_rolls:
        rows = ""
        for i in range(np):
            rolls = st.session_state.player_rolls.get(i, [])
            total = sum(rolls)
            last  = rolls[-1] if rolls else "—"
            active_class = "active" if i == cp else ""
            rows += (f'<div class="scoreboard-row {active_class}">'
                     f'<span>{"▶ " if i == cp else ""}Player {i+1}</span>'
                     f'<span>Rolls: {len(rolls)} &nbsp;|&nbsp; Last: {last} &nbsp;|&nbsp; '
                     f'<span class="score-val">Total: {total}</span></span>'
                     f'</div>')
        st.markdown(f'<div class="scoreboard">{rows}</div>', unsafe_allow_html=True)

    # Die face
    display_val = st.session_state.roll if st.session_state.roll else 1
    st.markdown(die_svg(display_val, T["accent1"], T["accent2"]), unsafe_allow_html=True)

    # Result
    if st.session_state.roll:
        st.markdown(f'<div class="roll-result">{st.session_state.roll}</div>', unsafe_allow_html=True)
        if mp:
            st.markdown(f'<div class="roll-label">Player {cp + 1} rolled {LABELS[st.session_state.roll].lower()}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="roll-label">{LABELS[st.session_state.roll]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="roll-result" style="opacity:0.2">—</div>', unsafe_allow_html=True)
        st.markdown('<div class="roll-label">press roll to begin</div>', unsafe_allow_html=True)

    # Roll button label
    roll_label = f"🎲 Roll for Player {cp + 1}" if mp else "Roll the Die"

    if st.button(roll_label, use_container_width=True):
        with st.spinner(""):
            time.sleep(0.15)
        result = random.randint(1, 6)
        st.session_state.roll = result
        st.session_state.history.insert(0, result)
        if len(st.session_state.history) > 8:
            st.session_state.history.pop()

        # Record in multiplayer scoreboard & advance player
        if mp:
            st.session_state.player_rolls[cp].append(result)
            st.session_state.current_player = (cp + 1) % np

        st.rerun()

    st.markdown('<div class="hint">or press <strong>Space</strong></div>', unsafe_allow_html=True)

    # History
    if st.session_state.history:
        pills = "".join(
            f'<span class="history-pill {"latest" if i == 0 else ""}">{n}</span>'
            for i, n in enumerate(st.session_state.history)
        )
        st.markdown(f'<div class="history-row">{pills}</div>', unsafe_allow_html=True)

    # Reset / change mode buttons
    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
    if mp:
        rc1, rc2 = st.columns(2)
        with rc1:
            if st.button("🔄 Reset Scores", use_container_width=True):
                st.session_state.player_rolls = {i: [] for i in range(np)}
                st.session_state.current_player = 0
                st.session_state.roll = None
                st.session_state.history = []
                st.rerun()
        with rc2:
            if st.button("← Change Mode", use_container_width=True):
                st.session_state.multiplayer = None
                st.session_state.player_rolls = {}
                st.session_state.num_players = 2
                st.session_state.current_player = 0
                st.session_state.roll = None
                st.session_state.history = []
                st.rerun()
    else:
        if st.button("← Change Mode", use_container_width=True):
            st.session_state.multiplayer = None
            st.session_state.roll = None
            st.session_state.history = []
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
