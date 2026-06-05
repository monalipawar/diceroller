import random
import streamlit as st
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dice Roller", page_icon="🎲", layout="centered")

# ── Glassmorphism dark cosmic CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

/* Animated star-field background */
.stApp {
    background: radial-gradient(ellipse at 20% 50%, #0d1b3e 0%, #020b18 60%, #000 100%);
    overflow: hidden;
}
.stApp::before {
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
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Glass card wrapper */
.glass-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 24px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 2.5rem 2rem;
    margin: 0 auto;
    max-width: 480px;
    text-align: center;
    position: relative;
    z-index: 1;
}

/* Die face SVG */
.die-face {
    width: 140px;
    height: 140px;
    margin: 0 auto 1.5rem;
    display: block;
    filter: drop-shadow(0 0 24px rgba(99, 179, 255, 0.35));
    transition: transform 0.15s ease;
}

/* Result number */
.roll-result {
    font-size: 4.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7dd3fc, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0.25rem 0;
}

.roll-label {
    color: rgba(255,255,255,0.45);
    font-size: 0.85rem;
    font-weight: 300;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* History pills */
.history-row {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1.25rem;
}
.history-pill {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    width: 36px; height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: rgba(255,255,255,0.7);
    font-size: 0.95rem;
    font-weight: 500;
    font-family: 'Outfit', sans-serif;
}
.history-pill.latest {
    background: rgba(99,179,255,0.18);
    border-color: rgba(99,179,255,0.4);
    color: #7dd3fc;
}

/* Roll button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(99,179,255,0.2), rgba(192,132,252,0.2));
    border: 1px solid rgba(99,179,255,0.4);
    border-radius: 14px;
    color: #e0f2fe;
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 0.75rem 0;
    transition: all 0.2s ease;
    cursor: pointer;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99,179,255,0.35), rgba(192,132,252,0.35));
    border-color: rgba(99,179,255,0.7);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(99,179,255,0.2);
}
div.stButton > button:active {
    transform: translateY(0px) scale(0.98);
}

/* Title */
.app-title {
    color: rgba(255,255,255,0.9);
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.app-subtitle {
    color: rgba(255,255,255,0.35);
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Spacebar hint */
.hint {
    color: rgba(255,255,255,0.25);
    font-size: 0.75rem;
    margin-top: 0.6rem;
    letter-spacing: 0.05em;
}
</style>

<!-- Spacebar listener -->
<script>
document.addEventListener('keydown', function(e) {
    if (e.code === 'Space' && !['INPUT','TEXTAREA','BUTTON'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        const btns = window.parent.document.querySelectorAll('button');
        for (const b of btns) {
            if (b.innerText.includes('Roll')) { b.click(); break; }
        }
    }
});
</script>
""", unsafe_allow_html=True)


# ── Dot positions for each face ───────────────────────────────────────────────
DOT_POSITIONS = {
    1: [(70, 70)],
    2: [(42, 42), (98, 98)],
    3: [(42, 42), (70, 70), (98, 98)],
    4: [(42, 42), (98, 42), (42, 98), (98, 98)],
    5: [(42, 42), (98, 42), (70, 70), (42, 98), (98, 98)],
    6: [(42, 35), (98, 35), (42, 70), (98, 70), (42, 105), (98, 105)],
}

def die_svg(n: int) -> str:
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
          <stop offset="0%" stop-color="#7dd3fc"/>
          <stop offset="100%" stop-color="#c084fc"/>
        </linearGradient>
      </defs>
      <rect x="6" y="6" width="128" height="128" rx="22"
            fill="url(#faceGrad)"
            stroke="rgba(255,255,255,0.18)" stroke-width="1.5"/>
      {dots}
    </svg>
    """

LABELS = {1:"Snake eyes", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Max roll!"}

# ── Session state ─────────────────────────────────────────────────────────────
if "roll" not in st.session_state:
    st.session_state.roll = None
if "history" not in st.session_state:
    st.session_state.history = []

# ── Layout ────────────────────────────────────────────────────────────────────
col = st.columns([1, 2, 1])[1]

with col:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="app-title">🎲 Dice Roller</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Six-sided · Random</div>', unsafe_allow_html=True)

    # Die face
    display_val = st.session_state.roll if st.session_state.roll else 1
    st.markdown(die_svg(display_val), unsafe_allow_html=True)

    # Result
    if st.session_state.roll:
        st.markdown(f'<div class="roll-result">{st.session_state.roll}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="roll-label">{LABELS[st.session_state.roll]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="roll-result" style="opacity:0.2">—</div>', unsafe_allow_html=True)
        st.markdown('<div class="roll-label">press roll to begin</div>', unsafe_allow_html=True)

    # Roll button
    if st.button("Roll the Die", use_container_width=True):
        with st.spinner(""):
            time.sleep(0.15)
        st.session_state.roll = random.randint(1, 6)
        st.session_state.history.insert(0, st.session_state.roll)
        if len(st.session_state.history) > 8:
            st.session_state.history.pop()
        st.rerun()

    st.markdown('<div class="hint">or press <strong>Space</strong></div>', unsafe_allow_html=True)

    # History
    if st.session_state.history:
        pills = "".join(
            f'<span class="history-pill {"latest" if i == 0 else ""}">{n}</span>'
            for i, n in enumerate(st.session_state.history)
        )
        st.markdown(f'<div class="history-row">{pills}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
