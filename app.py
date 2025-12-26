import streamlit as st
import time
from data import PEOPLE

st.set_page_config(
    page_title="A New Year Surprise",
    page_icon="🎆",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    /* GLOBAL THEME */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); /* Deep midnight blue */
        color: #e3d5ca; /* Muted Gold / Cream */
        font-family: 'Georgia', serif;
    }
    
    /* TYPOGRAPHY */
    h1 {
        color: #d4af37 !important; /* Muted Gold */
        text-shadow: 1px 1px 2px #000;
        text-align: center;
        font-weight: normal;
        letter-spacing: 1px;
    }
    p, div {
        color: #e3d5ca;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* INPUTS */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #d4af37;
        border: 1px solid #d4af37;
        text-align: center;
        border-radius: 5px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #fff;
        box-shadow: none;
    }

    /* BUTTONS */
    .stButton>button {
        background-color: transparent;
        color: #d4af37;
        border: 1px solid #d4af37;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 2px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #d4af37;
        color: #1a1a2e;
        border-color: #d4af37;
    }
    
    /* MOVIE REEL CSS */
    .reel-container {
        overflow: hidden;
        white-space: nowrap;
        position: relative;
        width: 100%;
        padding: 40px 0;
        /* Faded edges mask */
        mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
        -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
    }
    .reel-track {
        display: inline-block;
        animation: scroll 40s linear infinite; /* Slower speed */
    }
    .reel-img {
        height: 280px; /* Reducing height slightly */
        border-radius: 4px;
        margin-right: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        vertical-align: middle;
        opacity: 0.9;
        transition: opacity 0.3s;
    }
    .reel-img:hover {
        opacity: 1;
    }
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    </style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE & FLOW CONTROL ----------
# Strict order: login -> movie -> transition -> puzzle -> letter -> end
STEP_ORDER = ["login", "movie", "transition", "puzzle", "letter", "end"]

if "stage" not in st.session_state:
    st.session_state.stage = "login"

def advance_stage():
    current_idx = STEP_ORDER.index(st.session_state.stage)
    if current_idx < len(STEP_ORDER) - 1:
        st.session_state.stage = STEP_ORDER[current_idx + 1]
        st.rerun()

# ---------- LOGIN ----------
def login_screen():
    st.title("🔐 A Private Moment")
    
    # Countdown (Simplified elegant text)
    st.markdown(f"<p style='text-align: center; opacity: 0.7; font-size: 0.9rem;'>Counting down to a new beginning...</p>", unsafe_allow_html=True)
    
    code = st.text_input("Enter your secret code", type="password")

    if st.button("Unlock"):
        if code in PEOPLE:
            st.session_state.code = code
            st.session_state.person = PEOPLE[code]
            advance_stage()
        else:
            st.error("That code doesn’t feel right.")

# ---------- MOVIE ----------
def movie_screen():
    person = st.session_state.person
    st.title(person["display_name"])
    st.markdown("<p style='text-align: center; font-style: italic; opacity: 0.8;'>Some memories play on a loop...</p>", unsafe_allow_html=True)
    # 1. AUDIO (attempt to start early)
    import os
    import base64
    audio_html = ""
    if person["images"]:
        folder = os.path.dirname(person["images"][0])
        for file in os.listdir(folder):
            if file.lower().endswith(".mp3"):
                audio_path = os.path.join(folder, file)
                try:
                    with open(audio_path, "rb") as f:
                        audio_b64 = base64.b64encode(f.read()).decode()
                        # Use JS to set volume after element is available
                        audio_html = f'''<audio id="bg-audio" autoplay loop playsinline>
                                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                            </audio>
                            <script>
                                (function(){{
                                    const a = document.getElementById('bg-audio');
                                    if(a){{
                                        try{{ a.volume = 0.3; a.play(); }}catch(e){{}}
                                    }}
                                }})();
                            </script>'''
                        break
                except Exception:
                    pass

    # 2. MOVIE REEL
    images_html = ""
    for img_path in person["images"]:
        try:
            with open(img_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                ext = img_path.split(".")[-1]
                images_html += f'<img src="data:image/{ext};base64,{encoded}" class="reel-img" />'
        except Exception:
            pass

    # render audio first (if available) to encourage earlier playback
    if audio_html:
        st.markdown(audio_html, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="reel-container">
            <div class="reel-track">
                {images_html} {images_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. PACING - Delay button appearance
    time.sleep(2.0)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue"):
        advance_stage()

# ---------- TRANSITION ----------
def transition_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #d4af37;'>Some things aren’t meant to be read immediately.</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.6;'>(Take a breathe...)</p>", unsafe_allow_html=True)
    
    # Auto advance after pause
    time.sleep(4)
    advance_stage()

# ---------- PUZZLE ----------
def puzzle_screen():
    person = st.session_state.person
    st.title("🧩 One Small Thing")

    st.write(person["puzzle_question"])
    
    # Disable input if already solved? No, we just move on.
    answer = st.text_input("Your answer")

    if st.button("Submit"):
        if answer.strip().upper() == person["puzzle_answer"]:
            # No balloons, just proceed
            advance_stage()
        else:
            st.warning("Take your time. No rush.")

# ---------- LETTER ----------
def letter_screen():
    person = st.session_state.person
    st.title("💌")
    # Slower Typewriter effect, but only animate once per code
    key = f"letter_rendered_{st.session_state.get('code','') }"
    if not st.session_state.get(key, False):
        placeholder = st.empty()
        full_text = ""
        for char in person["letter"]:
            full_text += char
            placeholder.markdown(f"<div style='white-space: pre-wrap;'>{full_text}</div>", unsafe_allow_html=True)
            time.sleep(0.04)
        st.session_state[key] = True
    else:
        st.markdown(f"<div style='white-space: pre-wrap;'>{person['letter']}</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: right; font-weight: bold;'>— Disha</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Close this moment"):
        advance_stage()

# ---------- END ----------
def end_screen():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>You can come back to this anytime.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>❤️</p>", unsafe_allow_html=True)

# ---------- ROUTER ----------
if st.session_state.stage == "login":
    login_screen()
elif st.session_state.stage == "movie":
    movie_screen()
elif st.session_state.stage == "transition":
    transition_screen()
elif st.session_state.stage == "puzzle":
    puzzle_screen()
elif st.session_state.stage == "letter":
    letter_screen()
elif st.session_state.stage == "end":
    end_screen()
