import streamlit as st
import random
import time

st.set_page_config(page_title="Sorting Hub", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "home"

def navigate(page_name):
    st.session_state.page = page_name
    st.rerun()

def generate_numbers(level):
    if level == "easy":
        base = random.sample(range(1, 20), 6)
        base.sort()
        for i in range(0, len(base), 2):
            if i + 1 < len(base):
                base[i], base[i+1] = base[i+1], base[i]

    elif level == "medium":
        base = random.sample(range(1, 30), 12)
        base.sort()
        for i in range(len(base)):
            if random.random() < 0.5:
                j = random.randint(0, len(base)-1)
                base[i], base[j] = base[j], base[i]

    elif level == "hard":
        base = random.sample(range(1, 40), 20)
        random.shuffle(base)
        for _ in range(len(base)):
            i = random.randint(0, len(base)-2)
            if random.random() < 0.7:
                base[i], base[i+1] = base[i+1], base[i]

    return base

def render_bubble_ui(level):

    # Initialise session state
    if "nums" not in st.session_state or st.session_state.get("current_level") != level:
        st.session_state.nums = generate_numbers(level)
        st.session_state.index = 0
        st.session_state.current_level = level
        st.session_state.code_line = 1
        st.session_state.explain = "Press Next to start comparing neighbours."
        if level == "hard":
            st.session_state.timer_start = None
            st.session_state.timer_limit = None
            st.session_state.game_over = None
            st.session_state.timer_set = False

    #  Gradient background 
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg,
                #0d0010 0%,
                #5a0080 25%,
                #c0003c 50%,
                #ff6600 75%,
                #ffd000 100%
            );
        }
    </style>
    """, unsafe_allow_html=True)
    # HARD MODE
    if level == "hard":

        # STEP 1: Player hasn't set a time yet — show the input screen 
        if not st.session_state.get("timer_set", False):
            st.markdown("""
            <div style="text-align:center; padding:30px 0 10px;">
                <p style="font-size:48px; margin:0;">⏱</p>
                <h2 style="color:#ffd000; font-size:32px; font-weight:800; margin:8px 0 4px;">
                    Set Your Timer
                </h2>
                <p style="color:rgba(255,255,255,0.7); font-size:16px; margin:0 0 24px;">
                    How many seconds do you want to sort in?
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                secs_input = st.number_input(
                    "Seconds", min_value=10, max_value=600,
                    value=60, step=5, label_visibility="collapsed"
                )
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 Start Timer", use_container_width=True):
                    st.session_state.timer_limit = secs_input
                    st.session_state.timer_start = time.time()
                    st.session_state.timer_set = True
                    st.session_state.game_over = None
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅ Back", type="secondary"):
                navigate("bubble")
            return

        #  STEP 2: Timer is running — check win/timeout 
        time_limit = st.session_state.timer_limit
        elapsed = time.time() - st.session_state.timer_start
        remaining = max(0.0, time_limit - elapsed)

        if st.session_state.game_over is None:
            if st.session_state.nums == sorted(st.session_state.nums):
                st.session_state.game_over = "win"

        if st.session_state.game_over is None and remaining <= 0:
            st.session_state.game_over = "timeout"

        # ---- TIMEOUT SCREEN ----
        if st.session_state.game_over == "timeout":
            st.markdown("""
            <style>
                @keyframes shake {
                    0%,100% { transform: translateX(0); }
                    20%      { transform: translateX(-12px); }
                    40%      { transform: translateX(12px); }
                    60%      { transform: translateX(-8px); }
                    80%      { transform: translateX(8px); }
                }
            </style>
            <div style="
                display:flex; flex-direction:column;
                align-items:center; justify-content:center;
                min-height:420px; text-align:center;
            ">
                <div style="
                    background:#ff2020;
                    border-radius:28px;
                    padding:60px 70px;
                    animation: shake 0.6s ease;
                ">
                    <p style="font-size:90px; margin:0 0 8px;">⏰</p>
                    <h1 style="
                        font-size:72px; font-weight:900; color:white;
                        letter-spacing:6px; margin:0 0 16px; text-transform:uppercase;
                    ">TIME OUT!</h1>
                    <p style="color:rgba(255,255,255,0.85); font-size:20px; margin:0;">
                        You ran out of time. Give it another shot!
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.nums = generate_numbers(level)
                    st.session_state.index = 0
                    st.session_state.code_line = 1
                    st.session_state.explain = "New game! Press Next to start comparing."
                    st.session_state.timer_set = False
                    st.session_state.timer_start = None
                    st.session_state.timer_limit = None
                    st.session_state.game_over = None
                    st.rerun()
            with c2:
                if st.button("⬅ Back to Levels", use_container_width=True):
                    navigate("bubble")
            return

        # WIN SCREEN
        if st.session_state.game_over == "win":
            time_taken = int(time.time() - st.session_state.timer_start)
            st.markdown(f"""
            <style>
                @keyframes floatUp {{
                    0%   {{ transform: translateY(0px)   rotate(-6deg); opacity:1; }}
                    100% {{ transform: translateY(-40px) rotate(6deg);  opacity:0.8; }}
                }}
                .balloon {{
                    display: inline-block;
                    font-size: 64px;
                    animation: floatUp 1.8s ease-in-out infinite alternate;
                }}
            </style>
            <div style="text-align:center; padding:40px 20px;">
                <div style="margin-bottom:24px; line-height:1.2;">
                    <span class="balloon" style="animation-delay:0.0s;">🎈</span>
                    <span class="balloon" style="animation-delay:0.2s;">🎈</span>
                    <span class="balloon" style="animation-delay:0.4s;">🎈</span>
                    <span class="balloon" style="animation-delay:0.6s;">🎈</span>
                    <span class="balloon" style="animation-delay:0.8s;">🎈</span>
                    <span class="balloon" style="animation-delay:1.0s;">🎈</span>
                    <span class="balloon" style="animation-delay:1.2s;">🎈</span>
                </div>
                <h1 style="color:#ffd000; font-size:52px; font-weight:900; margin:0 0 16px;">
                    You sorted it! 🎉
                </h1>
                <p style="color:white; font-size:22px; margin:0 0 8px;">
                    Completed in <span style="color:#ffd000; font-weight:700;">{time_taken} seconds</span>
                    out of <span style="color:#ffd000; font-weight:700;">{time_limit}</span>!
                </p>
                <p style="color:rgba(255,255,255,0.6); font-size:16px;">
                    Hard mode conquered — well done!
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.nums = generate_numbers(level)
                    st.session_state.index = 0
                    st.session_state.code_line = 1
                    st.session_state.explain = "New game! Press Next to start comparing."
                    st.session_state.timer_set = False
                    st.session_state.timer_start = None
                    st.session_state.timer_limit = None
                    st.session_state.game_over = None
                    st.rerun()
            with c2:
                if st.button("⬅ Back to Levels", use_container_width=True):
                    navigate("bubble")
            return

        # LIVE TIMER DISPLAY 
        mins = int(remaining) // 60
        secs_left = int(remaining) % 60
        pct = (remaining / time_limit) * 100
        bar_color = "#ff2020" if remaining < 10 else "#ff9800" if remaining < (time_limit * 0.33) else "#00c853"

        st.markdown(f"""
        <div style="margin-bottom:18px;">
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:8px;">
                <div style="
                    display:inline-flex; align-items:center; gap:10px;
                    background:#1a1a2e; border-radius:999px;
                    padding:10px 24px;
                ">
                    <span style="font-size:24px;">⏱</span>
                    <span style="
                        font-size:30px; font-weight:700;
                        font-family:monospace; color:#ffd000;
                        letter-spacing:2px;
                    ">{mins:02d}:{secs_left:02d}</span>
                    <span style="
                        font-size:11px; color:rgba(255,255,255,0.5);
                        letter-spacing:3px;
                    ">REMAINING</span>
                </div>
            </div>
            <div style="
                height:10px; background:rgba(255,255,255,0.15);
                border-radius:999px; overflow:hidden;
            ">
                <div style="
                    height:100%; width:{pct:.1f}%;
                    background:{bar_color};
                    border-radius:999px;
                    transition: width 0.9s linear, background 0.4s;
                "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # MAIN GAME UI
    nums = st.session_state.nums
    i = st.session_state.index

    # Top row: Back and Generate buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back", type="secondary"):
            navigate("bubble")
    with col2:
        if st.button("🔄 Generate Numbers"):
            st.session_state.nums = generate_numbers(level)
            st.session_state.index = 0
            st.session_state.code_line = 1
            st.session_state.explain = "New numbers generated! Press Next to start."
            if level == "hard":
                st.session_state.timer_set = False
                st.session_state.timer_start = None
                st.session_state.timer_limit = None
                st.session_state.game_over = None
            st.rerun()

    # Title 
    st.markdown(f"<h2 style='text-align:center; color:white;'>Bubble Sort — {level.capitalize()} Level</h2>", unsafe_allow_html=True)

    # Split into two columns: game left, code right 
    left, right = st.columns(2)

    #  LEFT: number cards 
    with left:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>YOUR NUMBERS</p>", unsafe_allow_html=True)

        cards_html = '<div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:16px;">'
        for idx, val in enumerate(nums):
            if idx == i or idx == i + 1:
                bg = "background:#ff2020; box-shadow:0 0 16px rgba(255,32,32,0.6); transform:scale(1.15);"
            else:
                bg = "background:#7850ff;"
            cards_html += f'<div style="width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:white; {bg}">{val}</div>'
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔀 SWAP"):
                if i < len(nums) - 1:
                    if nums[i] > nums[i + 1]:
                        nums[i], nums[i + 1] = nums[i + 1], nums[i]
                        st.session_state.nums = nums
                        st.session_state.code_line = 5
                        st.session_state.explain = f"Swapped {nums[i+1]} and {nums[i]} because {nums[i+1]} was bigger!"
                    else:
                        st.session_state.code_line = 3
                        st.session_state.explain = f"No swap needed — {nums[i]} is already smaller than {nums[i+1]}."
                st.rerun()

        with c2:
            if st.button("➡ Next"):
                if i < len(nums) - 2:
                    st.session_state.index += 1
                    st.session_state.code_line = 3
                    st.session_state.explain = f"Comparing {nums[i+1]} and {nums[i+2]} — is the left number bigger than the right?"
                else:
                    st.session_state.index = 0
                    st.session_state.code_line = 1
                    st.session_state.explain = "Starting a new pass from the beginning!"
                st.rerun()

    #  RIGHT: code panel
    with right:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>THE CODE</p>", unsafe_allow_html=True)

        active = st.session_state.code_line
        code_lines = [
            (0, "def bubble_sort(arr):"),
            (1, "&nbsp;&nbsp;for i in range(len(arr)):"),
            (2, "&nbsp;&nbsp;&nbsp;&nbsp;for j in range(len(arr)-i-1):"),
            (3, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if arr[j] &gt; arr[j+1]:"),
            (4, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# swap them"),
            (5, "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr[j], arr[j+1] = arr[j+1], arr[j]"),
            (6, "&nbsp;&nbsp;return arr"),
        ]

        code_html = ""
        for line_num, line_text in code_lines:
            if line_num == active:
                style = "background:rgba(255,208,0,0.2); color:#ffd000; font-weight:bold; border-radius:6px; padding:4px 8px; display:block;"
            else:
                style = "color:rgba(255,255,255,0.35); padding:4px 8px; display:block;"
            code_html += f'<span style="{style}">{line_text}</span>'

        st.markdown(f"""
            <div style="
                background:#1a1a2e;
                border-radius:14px;
                padding:16px;
                font-family:monospace;
                font-size:13px;
                line-height:2;
            ">{code_html}</div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="
                margin-top:12px;
                background:rgba(255,208,0,0.85);
                border-left:3px solid #ffd000;
                border-radius:0 10px 10px 0;
                padding:10px 14px;
                color:black;
                font-size:13px;
                line-height:1.6;
            ">💡 {st.session_state.explain}</div>
        """, unsafe_allow_html=True)

    # Keep refreshing every second so the timer counts down live
    if level == "hard" and st.session_state.get("game_over") is None:
        time.sleep(1)
        st.rerun()


def on_difficulty_change():
    level = st.session_state.difficulty_select
    if level != "Select...":
        st.session_state.page = f"bubble_{level.lower()}"
        
# HOME PAGE
if st.session_state.page == "home":

    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg,
                #0d0010 0%,
                #5a0080 25%,
                #c0003c 50%,
                #ff6600 75%,
                #ffd000 100%
            );
        }
        img {
            background-color: black;
            border-radius: 50%;
            padding: 10px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        div.stButton > button {
            width: 200px;
            height: 60px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            background-color: #ff2020;
            color: #1a0000;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #ff3a3a;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center; color:white;'>Brain Sort Challenge</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("image1.png", width=200)

    st.markdown("<p style='text-align:center; color:white; font-size:16px;'>Sort it out. Beat the clock. Become the algorithm.<br>Pick your challenge and start sorting!</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.7); letter-spacing:3px; font-size:12px;'>CHOOSE YOUR ALGORITHM</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("BUBBLE SORT"):
            navigate("bubble")
    with col2:
        if st.button("MERGE SORT"):
            navigate("merge")
            
# BUBBLE SORT PAGE (difficulty selection)
elif st.session_state.page == "bubble":

    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(
                135deg,
                #0d0010 0%,
                #5a0080 25%,
                #c0003c 50%,
                #ff6600 75%,
                #ffd000 100%
            );
        }
        div.stButton > button {
            width: 100%;
            height: 50px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
        }
        div.stButton:has(button[kind="secondary"]) > button {
            width: auto;
            height: 36px;
            font-size: 13px;
            background: rgba(255,255,255,0.15);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 20px;
            padding: 0 16px;
        }
        div[data-testid="column"]:nth-child(1) div.stButton > button {
            background: #00c853;
            color: #003300;
        }
        div[data-testid="column"]:nth-child(2) div.stButton > button {
            background: #ff9800;
            color: #3d1f00;
        }
        div[data-testid="column"]:nth-child(3) div.stButton > button {
            background: #ff2020;
            color: #1a0000;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("⬅ Back", type="secondary"):
        navigate("home")

    st.markdown("<h1 style='text-align:center; color:white;'>Bubble Sort Game</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>HOW TO PLAY</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">1</p>
                <p style="color:white; font-size:12px;">Choose a difficulty level</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">2</p>
                <p style="color:white; font-size:12px;">Click Generate Numbers to start</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">3</p>
                <p style="color:white; font-size:12px;">Use Swap and Next to sort!</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>SELECT YOUR DIFFICULTY</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("EASY"):
            navigate("bubble_easy")
    with col2:
        if st.button("MEDIUM"):
            navigate("bubble_medium")
    with col3:
        if st.button("HARD"):
            navigate("bubble_hard")
            
# BUBBLE SORT LEVELS
elif st.session_state.page == "bubble_easy":
    render_bubble_ui("easy")

elif st.session_state.page == "bubble_medium":
    render_bubble_ui("medium")

elif st.session_state.page == "bubble_hard":
    render_bubble_ui("hard")

# MERGE SORT PAGE
elif st.session_state.page == "merge":
    st.title("Merge Sort Game")
    st.info("Merge Sort coming soon!")
    if st.button("⬅ Back"):
        navigate("home")

    




