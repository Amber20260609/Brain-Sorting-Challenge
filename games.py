import streamlit as st
import streamlit.components.v1 as components
import random

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
        base = random.sample(range(1, 40), 24)
        random.shuffle(base)
        for _ in range(len(base)):
            i = random.randint(0, len(base)-2)
            if random.random() < 0.7:
                base[i], base[i+1] = base[i+1], base[i]

    return base

def render_bubble_ui(level):
    if "nums" not in st.session_state or st.session_state.get("current_level") != level:
        st.session_state.nums = generate_numbers(level)
        st.session_state.index = 0
        st.session_state.current_level = level
        st.session_state.code_line = 1
        st.session_state.explain = "Press Next to start comparing neighbours."

    nums = st.session_state.nums
    i = st.session_state.index

    # --- Same gradient background ---
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

    # --- Top row: Back and Generate buttons ---
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
            st.rerun()

    # --- Title ---
    st.markdown(f"<h2 style='text-align:center; color:white;'>Bubble Sort — {level.capitalize()} Level</h2>", unsafe_allow_html=True)

    # --- Split into two columns: game left, code right ---
    left, right = st.columns(2)

    # ---- LEFT: number cards ----
    with left:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>YOUR NUMBERS</p>", unsafe_allow_html=True)

 # Build the number cards HTML
        cards_html = '<div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:16px;">'

        for idx, val in enumerate(nums):
            # Red + glow = comparing, purple = normal
            if idx == i or idx == i + 1:
                bg = "background:#ff2020; box-shadow:0 0 16px rgba(255,32,32,0.6); transform:scale(1.15);"
            else:
                bg = "background:#7850ff;"

            # Everything on one line to avoid Streamlit rendering issues
            cards_html += f'<div style="width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:white; {bg}">{val}</div>'

        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # --- Swap and Next buttons ---
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔀 SWAP"):
                if i < len(nums) - 1:
                    # Only swap if left number is bigger than right
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

    # ---- RIGHT: code panel ----
    with right:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>THE CODE</p>", unsafe_allow_html=True)

        active = st.session_state.code_line

        # Each line of bubble sort code
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
                # Yellow highlight for active line
                style = "background:rgba(255,208,0,0.2); color:#ffd000; font-weight:bold; border-radius:6px; padding:4px 8px; display:block;"
            else:
                # Dim for inactive lines
                style = "color:rgba(255,255,255,0.35); padding:4px 8px; display:block;"
            code_html += f'<span style="{style}">{line_text}</span>'

        # Dark code box
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

        # Plain English explanation — BLACK text
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

def on_difficulty_change():
    level = st.session_state.difficulty_select
    if level != "Select...":
        st.session_state.page = f"bubble_{level.lower()}"


st.markdown("""
<style>
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

# HOME PAGE
if st.session_state.page == "home":

    # Background gradient
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
    </style>
    """, unsafe_allow_html=True)

    # Title at the TOP-
    st.markdown("<h1 style='text-align:center; color:white;'>Brain Sort Challenge</h1>", unsafe_allow_html=True)

    # Image in the MIDDLE
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("image1.png", width=200)
        
    # Tagline BELOW the image
    st.markdown("<p style='text-align:center; color:white; font-size:16px;'>Sort it out. Beat the clock. Become the algorithm.<br>Pick your challenge and start sorting!</p>", unsafe_allow_html=True)

    # Small label above buttons
    st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.7); letter-spacing:3px; font-size:12px;'>CHOOSE YOUR ALGORITHM</p>", unsafe_allow_html=True)

    # Buttons 
    col1, col2 = st.columns(2)

    with col1:
        if st.button("BUBBLE SORT"):
            navigate("bubble")

    with col2:
        if st.button("MERGE SORT"):
            navigate("merge")

# BUBBLE SORT PAGE (difficulty selection)

elif st.session_state.page == "bubble":

    # --- Same gradient background ---
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

        /* Make ALL buttons normal size first */
        div.stButton > button {
            width: 100%;
            height: 50px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            border: none;
        }

        /* Back button — small and pill shaped */
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

        /* Easy button — green */
        div[data-testid="column"]:nth-child(1) div.stButton > button {
            background: #00c853;
            color: #003300;
        }

        /* Medium button — orange */
        div[data-testid="column"]:nth-child(2) div.stButton > button {
            background: #ff9800;
            color: #3d1f00;
        }

        /* Hard button — red */
        div[data-testid="column"]:nth-child(3) div.stButton > button {
            background: #ff2020;
            color: #1a0000;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Back button (small) ---
    if st.button("⬅ Back", type="secondary"):
        navigate("home")

    # --- Title ---
    st.markdown("<h1 style='text-align:center; color:white;'>Bubble Sort Game</h1>", unsafe_allow_html=True)

    # --- How to play label ---
    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>HOW TO PLAY</p>", unsafe_allow_html=True)

    # --- 3 step cards ---
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

    # --- Difficulty label ---
    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>SELECT YOUR DIFFICULTY</p>", unsafe_allow_html=True)

    # --- 3 difficulty buttons (each in its own column for color targeting) ---
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
    st.title("Bubble Sort — Easy Level")
    render_bubble_ui("easy")

elif st.session_state.page == "bubble_medium":
    st.title("Bubble Sort — Medium Level")
    render_bubble_ui("medium")

elif st.session_state.page == "bubble_hard":
    st.title("Bubble Sort — Hard Level")
    render_bubble_ui("hard")

# MERGE SORT PAGE

elif st.session_state.page == "merge":
    st.title("Merge Sort Game")
    st.info("Merge Sort coming soon!")
    if st.button("⬅ Back"):
        navigate("home")


    




