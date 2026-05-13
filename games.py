import streamlit as st
import random
import time
import math

st.set_page_config(page_title="BrainSort Challenge", layout="centered")

# SESSION STATE SETUP
if "page" not in st.session_state:
    st.session_state.page = "home"
if "merge_level" not in st.session_state:
    st.session_state.merge_level = 1
if "merge_completed" not in st.session_state:
    st.session_state.merge_completed = []
if "merge_unlocked" not in st.session_state:
    st.session_state.merge_unlocked = [1]
if "merge_hearts" not in st.session_state:
    st.session_state.merge_hearts = 3
if "merge_numbers" not in st.session_state:
    st.session_state.merge_numbers = []
if "merge_split_levels" not in st.session_state:
    st.session_state.merge_split_levels = []
if "merge_split_idx" not in st.session_state:
    st.session_state.merge_split_idx = 0
if "merge_phase" not in st.session_state:
    st.session_state.merge_phase = "split"
if "merge_pairs" not in st.session_state:
    st.session_state.merge_pairs = []
if "merge_pair_idx" not in st.session_state:
    st.session_state.merge_pair_idx = 0
if "merge_current_left" not in st.session_state:
    st.session_state.merge_current_left = []
if "merge_current_right" not in st.session_state:
    st.session_state.merge_current_right = []
if "merge_merged_results" not in st.session_state:
    st.session_state.merge_merged_results = []
if "merge_timer_started" not in st.session_state:
    st.session_state.merge_timer_started = False
if "merge_start_time" not in st.session_state:
    st.session_state.merge_start_time = 0
if "merge_penalty" not in st.session_state:
    st.session_state.merge_penalty = 0
if "merge_code_line" not in st.session_state:
    st.session_state.merge_code_line = 0
if "merge_explain" not in st.session_state:
    st.session_state.merge_explain = "Press Split to divide the list in half!"
if "merge_available" not in st.session_state:
    st.session_state.merge_available = []
if "merge_player_order" not in st.session_state:
    st.session_state.merge_player_order = []
if "merge_personal_best" not in st.session_state:
    st.session_state.merge_personal_best = {}
if "challenge_current_groups" not in st.session_state:
    st.session_state.challenge_current_groups = []
if "challenge_split_complete" not in st.session_state:
    st.session_state.challenge_split_complete = False
if "challenge_merge_groups" not in st.session_state:
    st.session_state.challenge_merge_groups = []
if "challenge_merge_idx" not in st.session_state:
    st.session_state.challenge_merge_idx = 0
if "challenge_player_pick" not in st.session_state:
    st.session_state.challenge_player_pick = []
if "challenge_available" not in st.session_state:
    st.session_state.challenge_available = []

# Bubble sort state
if "bubble_first_move_made" not in st.session_state:
    st.session_state.bubble_first_move_made = False
if "medium_timer_start" not in st.session_state:
    st.session_state.medium_timer_start = None
if "medium_game_over" not in st.session_state:
    st.session_state.medium_game_over = None
if "medium_timer_set" not in st.session_state:
    st.session_state.medium_timer_set = False
if "medium_timer_limit" not in st.session_state:
    st.session_state.medium_timer_limit = None

# NAVIGATION
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# SHARED: Gradient background
def show_gradient_background():
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

# BUBBLE SORT: Generate numbers
def make_numbers(level):
    numbers = []
    if level == "easy":
        numbers = random.sample(range(1, 20), 6)
        numbers.sort()
        i = 0
        while i < len(numbers) - 1:
            temp = numbers[i]
            numbers[i] = numbers[i + 1]
            numbers[i + 1] = temp
            i = i + 2
    if level == "medium":
        numbers = random.sample(range(1, 30), 12)
        numbers.sort()
        for i in range(len(numbers)):
            chance = random.random()
            if chance < 0.5:
                j = random.randint(0, len(numbers) - 1)
                temp = numbers[i]
                numbers[i] = numbers[j]
                numbers[j] = temp
    if level == "hard":
        numbers = random.sample(range(1, 40), 24)
        random.shuffle(numbers)
        count = 0
        while count < len(numbers):
            i = random.randint(0, len(numbers) - 2)
            chance = random.random()
            if chance < 0.7:
                temp = numbers[i]
                numbers[i] = numbers[i + 1]
                numbers[i + 1] = temp
            count = count + 1
    return numbers

# ──────────────────────────────────────────────────────────────────
# BUBBLE SORT: EASY MODE (Educational)
# ──────────────────────────────────────────────────────────────────
def show_easy_code_and_complexity():
    active_line = st.session_state.code_line
    all_lines = [
        "def bubble_sort(arr):",
        "&nbsp;&nbsp;n = len(arr)",
        "&nbsp;&nbsp;for i in range(n):",
        "&nbsp;&nbsp;&nbsp;&nbsp;for j in range(n - i - 1):",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if arr[j] &gt; arr[j+1]:",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr[j], arr[j+1] = \\",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr[j+1], arr[j]",
        "&nbsp;&nbsp;return arr"
    ]

    code_html = ""
    for line_number, line_text in enumerate(all_lines):
        if line_number == active_line:
            style = "background:rgba(255,208,0,0.22); color:#ffd000; font-weight:bold; border-radius:6px; padding:5px 10px; display:block; border-left:3px solid #ffd000;"
        else:
            style = "color:rgba(255,255,255,0.4); padding:5px 10px; display:block;"
        code_html += f'<span style="{style}">{line_text}</span>'

    st.markdown('<p style="color:rgba(255,255,255,0.55); font-size:10px; letter-spacing:3px; text-align:center; margin-bottom:8px;">THE CODE</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:#0d0d1a; border:1px solid rgba(120,80,255,0.3); border-radius:14px; padding:18px 14px; font-family:\'Courier New\', monospace; font-size:13px; line-height:2.1; min-height:200px;">{code_html}</div>',
        unsafe_allow_html=True
    )

    # Explanation box
    st.markdown(
        f'<div style="margin-top:10px; background:rgba(255,208,0,0.9); border-left:4px solid #ff9800; border-radius:0 10px 10px 0; padding:10px 14px; color:#1a0a00; font-size:13px; line-height:1.6; font-weight:500;">💡 {st.session_state.explain}</div>',
        unsafe_allow_html=True
    )

    # Complexity section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(255,255,255,0.55); font-size:11px; letter-spacing:3px; text-align:center; margin-bottom:8px;">COMPLEXITY</p>', unsafe_allow_html=True)
    st.markdown("""
        <div style="background:#0d0d1a; border:1px solid rgba(120,80,255,0.3); border-radius:14px; padding:16px 18px; font-size:13px;">
            <p style="color:#c084ff; font-weight:700; font-size:12px; letter-spacing:2px; margin:0 0 10px;">⏱ TIME COMPLEXITY</p>
            <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:rgba(255,255,255,0.6); font-size:12px;">Best Case</span>
                    <span style="background:rgba(0,200,83,0.2); color:#00c853; font-family:monospace; font-size:12px; font-weight:700; padding:2px 10px; border-radius:6px; border:1px solid rgba(0,200,83,0.3);">O(n)</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:rgba(255,255,255,0.6); font-size:12px;">Average Case</span>
                    <span style="background:rgba(255,152,0,0.2); color:#ff9800; font-family:monospace; font-size:12px; font-weight:700; padding:2px 10px; border-radius:6px; border:1px solid rgba(255,152,0,0.3);">O(n²)</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:rgba(255,255,255,0.6); font-size:12px;">Worst Case</span>
                    <span style="background:rgba(255,32,32,0.2); color:#ff6060; font-family:monospace; font-size:12px; font-weight:700; padding:2px 10px; border-radius:6px; border:1px solid rgba(255,32,32,0.3);">O(n²)</span>
                </div>
            </div>
            <p style="color:#c084ff; font-weight:700; font-size:12px; letter-spacing:2px; margin:0 0 10px;">💾 SPACE COMPLEXITY</p>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:rgba(255,255,255,0.6); font-size:12px;">Space</span>
                <span style="background:rgba(56,189,248,0.2); color:#38bdf8; font-family:monospace; font-size:12px; font-weight:700; padding:2px 10px; border-radius:6px; border:1px solid rgba(56,189,248,0.3);">O(1)</span>
            </div>
            <p style="color:rgba(255,255,255,0.4); font-size:11px; margin:8px 0 0; font-style:italic;">Sorts in-place — no extra memory needed.</p>
        </div>
    """, unsafe_allow_html=True)


def show_easy_placeholder():
    st.markdown("""
        <div style="background:rgba(120,80,255,0.08); border:1px dashed rgba(120,80,255,0.35); border-radius:14px; padding:30px 18px; text-align:center; min-height:200px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <p style="font-size:28px; margin:0 0 8px;">🧠</p>
            <p style="color:rgba(255,255,255,0.5); font-size:13px; line-height:1.6; margin:0;">Make your first move to reveal<br>the code and complexity info!</p>
        </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# BUBBLE SORT: MEDIUM MODE timer bar (countdown)
# ──────────────────────────────────────────────────────────────────
def show_medium_timer_bar():
    if st.session_state.medium_timer_start is None or st.session_state.medium_timer_limit is None:
        return
    elapsed = time.time() - st.session_state.medium_timer_start
    time_left = max(0, st.session_state.medium_timer_limit - elapsed)
    mins = int(time_left) // 60
    secs = int(time_left) % 60
    percent = (time_left / st.session_state.medium_timer_limit) * 100
    bar_color = "#00c853"
    if time_left < (st.session_state.medium_timer_limit * 0.33):
        bar_color = "#ff9800"
    if time_left < 10:
        bar_color = "#ff2020"

    st.markdown(f"""
        <div style="margin-bottom:16px;">
            <div style="display:inline-flex; align-items:center; gap:10px; background:rgba(0,0,0,0.35); border-radius:999px; padding:8px 22px; border:1px solid rgba(255,208,0,0.4);">
                <span style="font-size:20px;">⏱</span>
                <span style="font-size:26px; font-weight:800; font-family:monospace; color:#ffd000; letter-spacing:2px;">{mins:02d}:{secs:02d}</span>
                <span style="font-size:10px; color:rgba(255,255,255,0.5); letter-spacing:3px;">REMAINING</span>
            </div>
            <div style="height:10px; background:rgba(255,255,255,0.15); border-radius:999px; overflow:hidden; margin-top:8px;">
                <div style="height:100%; width:{percent:.1f}%; background:{bar_color}; border-radius:999px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# BUBBLE SORT: Main game entry
# ──────────────────────────────────────────────────────────────────
def show_bubble_game(level):
    if "nums" not in st.session_state:
        st.session_state.nums = make_numbers(level)
        st.session_state.index = 0
        st.session_state.current_level = level
        st.session_state.code_line = 0
        st.session_state.explain = "Press Next to start comparing neighbours."
        st.session_state.bubble_first_move_made = False

    if st.session_state.get("current_level") != level:
        st.session_state.nums = make_numbers(level)
        st.session_state.index = 0
        st.session_state.current_level = level
        st.session_state.code_line = 0
        st.session_state.explain = "Press Next to start comparing neighbours."
        st.session_state.bubble_first_move_made = False

    # ── HARD MODE: timer setup screen ──
    if level == "hard":
        if "timer_start" not in st.session_state:
            st.session_state.timer_start = None
        if "timer_limit" not in st.session_state:
            st.session_state.timer_limit = None
        if "game_over" not in st.session_state:
            st.session_state.game_over = None
        if "timer_set" not in st.session_state:
            st.session_state.timer_set = False

    show_gradient_background()

    # ── HARD: Timer set screen ──
    if level == "hard" and not st.session_state.timer_set:
        st.markdown("""
        <div style="text-align:center; padding:30px 0 10px;">
            <p style="font-size:48px; margin:0;">⏱</p>
            <h2 style="color:#ffd000; font-size:32px; font-weight:800; margin:8px 0 4px;">Set Your Timer</h2>
            <p style="color:rgba(255,255,255,0.7); font-size:16px; margin:0 0 8px;">How many seconds do you want to sort in?</p>
            <p style="color:rgba(255,100,100,0.9); font-size:13px; margin:0 0 24px;">⚠️ Maximum: 120 seconds (under 2 minutes)</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_seconds = st.number_input(
                "Seconds",
                min_value=10,
                max_value=120,
                value=60,
                step=5,
                label_visibility="collapsed"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("COUNT DOWN", use_container_width=True):
                st.session_state.timer_limit = user_seconds
                st.session_state.timer_start = time.time()
                st.session_state.timer_set = True
                st.session_state.game_over = None
                st.session_state.nums = make_numbers(level)
                st.session_state.index = 0
                st.session_state.code_line = 0
                st.session_state.explain = "Press Next to start comparing neighbours."
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ Back", type="secondary"):
            go_to_page("bubble")
        return

    # ── HARD: Timeout / Win screens ──
    if level == "hard" and st.session_state.timer_set:
        time_limit = st.session_state.timer_limit
        time_passed = time.time() - st.session_state.timer_start
        time_left = max(0, time_limit - time_passed)

        if st.session_state.game_over is None:
            if st.session_state.nums == sorted(st.session_state.nums):
                st.session_state.game_over = "win"
        if st.session_state.game_over is None:
            if time_left <= 0:
                st.session_state.game_over = "timeout"

        if st.session_state.game_over == "timeout":
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:420px; text-align:center;">
                <div style="background:#ff2020; border-radius:28px; padding:60px 70px;">
                    <p style="font-size:90px; margin:0 0 8px;">⏰</p>
                    <h1 style="font-size:72px; font-weight:900; color:white; letter-spacing:6px; margin:0 0 16px;">TIME OUT!</h1>
                    <p style="color:rgba(255,255,255,0.85); font-size:20px; margin:0;">You ran out of time. Give it another shot!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.nums = make_numbers(level)
                    st.session_state.index = 0
                    st.session_state.code_line = 0
                    st.session_state.explain = "New game! Press Next to start comparing."
                    st.session_state.timer_set = False
                    st.session_state.timer_start = None
                    st.session_state.timer_limit = None
                    st.session_state.game_over = None
                    st.rerun()
            with col2:
                if st.button("⬅ Back to Levels", use_container_width=True):
                    go_to_page("bubble")
            return

        if st.session_state.game_over == "win":
            time_taken = int(time.time() - st.session_state.timer_start)
            st.markdown(f"""
            <div style="text-align:center; padding:40px 20px;">
                <h1 style="color:#ffd000; font-size:52px; font-weight:900; margin:0 0 16px;">You sorted it! 🎉</h1>
                <p style="color:white; font-size:22px; margin:0 0 8px;">Completed in <span style="color:#ffd000; font-weight:700;">{time_taken}s</span> out of <span style="color:#ffd000; font-weight:700;">{time_limit}s</span>!</p>
                <p style="color:rgba(255,255,255,0.6); font-size:16px;">Hard mode conquered!</p>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.nums = make_numbers(level)
                    st.session_state.index = 0
                    st.session_state.code_line = 0
                    st.session_state.explain = "New game! Press Next to start comparing."
                    st.session_state.timer_set = False
                    st.session_state.timer_start = None
                    st.session_state.timer_limit = None
                    st.session_state.game_over = None
                    st.rerun()
            with col2:
                if st.button("⬅ Back to Levels", use_container_width=True):
                    go_to_page("bubble")
            return

        # Hard timer bar
        minutes = int(time_left) // 60
        seconds = int(time_left) % 60
        percent = (time_left / time_limit) * 100
        bar_color = "#00c853"
        if time_left < (time_limit * 0.33):
            bar_color = "#ff9800"
        if time_left < 10:
            bar_color = "#ff2020"

        st.markdown(f"""
        <div style="margin-bottom:18px;">
            <div style="display:inline-flex; align-items:center; gap:10px; background:#1a1a2e; border-radius:999px; padding:10px 24px;">
                <span style="font-size:24px;">⏱</span>
                <span style="font-size:30px; font-weight:700; font-family:monospace; color:#ffd000; letter-spacing:2px;">{minutes:02d}:{seconds:02d}</span>
                <span style="font-size:11px; color:rgba(255,255,255,0.5); letter-spacing:3px;">REMAINING</span>
            </div>
            <div style="height:10px; background:rgba(255,255,255,0.15); border-radius:999px; overflow:hidden; margin-top:8px;">
                <div style="height:100%; width:{percent:.1f}%; background:{bar_color}; border-radius:999px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── MEDIUM: Timer setup screen ──
    if level == "medium" and not st.session_state.medium_timer_set:
        st.markdown("""
        <div style="text-align:center; padding:30px 0 10px;">
            <p style="font-size:48px; margin:0;">⏱</p>
            <h2 style="color:#ffd000; font-size:32px; font-weight:800; margin:8px 0 4px;">Set Your Timer</h2>
            <p style="color:rgba(255,255,255,0.7); font-size:16px; margin:0 0 8px;">How many seconds do you want to sort in?</p>
            <p style="color:rgba(255,200,100,0.9); font-size:13px; margin:0 0 24px;">⚠️ Maximum: 120 seconds (under 2 minutes)</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_seconds = st.number_input(
                "Seconds",
                min_value=10,
                max_value=120,
                value=60,
                step=5,
                label_visibility="collapsed"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Start Timer", use_container_width=True):
                st.session_state.medium_timer_limit = user_seconds
                st.session_state.medium_timer_start = time.time()
                st.session_state.medium_timer_set = True
                st.session_state.medium_game_over = None
                st.session_state.nums = make_numbers(level)
                st.session_state.index = 0
                st.session_state.code_line = 0
                st.session_state.explain = "Press Next to start comparing neighbours."
                st.session_state.bubble_first_move_made = False
                st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ Back", type="secondary"):
            go_to_page("bubble")
        return

    # ── MEDIUM: Check timeout and win ──
    if level == "medium" and st.session_state.medium_timer_set:
        time_left = max(0, st.session_state.medium_timer_limit - (time.time() - st.session_state.medium_timer_start))

        # Check win — only after first move
        if st.session_state.medium_game_over is None and st.session_state.bubble_first_move_made:
            if st.session_state.nums == sorted(st.session_state.nums):
                st.session_state.medium_game_over = "win"

        # Check timeout
        if st.session_state.medium_game_over is None and time_left <= 0:
            st.session_state.medium_game_over = "timeout"

        # ── Timeout screen ──
        if st.session_state.medium_game_over == "timeout":
            st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:420px; text-align:center;">
                <div style="background:#ff2020; border-radius:28px; padding:60px 70px;">
                    <p style="font-size:90px; margin:0 0 8px;">⏰</p>
                    <h1 style="font-size:64px; font-weight:900; color:white; letter-spacing:6px; margin:0 0 16px;">TIME OUT!</h1>
                    <p style="color:rgba(255,255,255,0.85); font-size:20px; margin:0;">You ran out of time. Give it another shot!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Try Again", use_container_width=True):
                    st.session_state.medium_timer_set = False
                    st.session_state.medium_timer_start = None
                    st.session_state.medium_timer_limit = None
                    st.session_state.medium_game_over = None
                    st.session_state.bubble_first_move_made = False
                    st.session_state.pop("nums", None)
                    st.rerun()
            with col2:
                if st.button("⬅ Back to Levels", use_container_width=True):
                    go_to_page("bubble")
            return

        # ── Win screen ──
        if st.session_state.medium_game_over == "win":
            elapsed = int(st.session_state.medium_timer_limit - time_left)
            m = elapsed // 60
            s = elapsed % 60
            time_limit = st.session_state.medium_timer_limit
            st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:420px; text-align:center;">
                <div style="background:rgba(0,200,83,0.2); border:3px solid #00c853; border-radius:28px; padding:50px 60px;">
                    <p style="font-size:80px; margin:0 0 8px;">🎉</p>
                    <h1 style="font-size:52px; font-weight:900; color:#00c853; letter-spacing:2px; margin:0 0 12px;">Sorted!</h1>
                    <p style="color:white; font-size:20px; margin:0 0 6px;">Finished in <span style="color:#ffd000; font-weight:700;">{m:02d}:{s:02d}</span> out of <span style="color:#ffd000; font-weight:700;">{time_limit}s</span>!</p>
                    <p style="color:rgba(255,255,255,0.6); font-size:14px; margin:0;">Medium mode cleared!</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.medium_timer_set = False
                    st.session_state.medium_timer_start = None
                    st.session_state.medium_timer_limit = None
                    st.session_state.medium_game_over = None
                    st.session_state.bubble_first_move_made = False
                    st.session_state.pop("nums", None)
                    st.rerun()
            with col2:
                if st.button("⬅ Back to Levels", use_container_width=True):
                    go_to_page("bubble")
            return

    nums = st.session_state.nums
    i = st.session_state.index

    # Top buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back", type="secondary"):
            go_to_page("bubble")
    with col2:
        if level == "medium":
            if st.button("🔄 New Numbers"):
                st.session_state.medium_timer_set = False
                st.session_state.medium_timer_start = None
                st.session_state.medium_timer_limit = None
                st.session_state.medium_game_over = None
                st.session_state.bubble_first_move_made = False
                st.session_state.pop("nums", None)
                st.rerun()
        else:
            if st.button("🔄 New Numbers"):
                st.session_state.nums = make_numbers(level)
                st.session_state.index = 0
                st.session_state.code_line = 0
                st.session_state.explain = "New numbers! Press Next to start comparing."
                st.session_state.bubble_first_move_made = False
                if level == "hard":
                    st.session_state.timer_set = False
                    st.session_state.timer_start = None
                    st.session_state.timer_limit = None
                    st.session_state.game_over = None
                st.rerun()

    # Medium elapsed timer
    if level == "medium":
        show_medium_timer_bar()

    st.markdown(f"<h2 style='text-align:center; color:white;'>Bubble Sort — {level.capitalize()} Level</h2>", unsafe_allow_html=True)

    # ── LAYOUT ──
    # Easy: two columns (game | code+complexity)
    # Medium/Hard: wide single column for gameplay, no code panel
    if level == "easy":
        left_col, right_col = st.columns([1, 1])
    else:
        left_col = st.container()
        right_col = None  # not used for medium/hard

    # ── GAME AREA ──
    with left_col:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>YOUR NUMBERS</p>", unsafe_allow_html=True)

        cards_html = '<div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:16px;">'
        for card_number, value in enumerate(nums):
            if card_number == i or card_number == i + 1:
                card_style = "background:#ff2020; box-shadow:0 0 16px rgba(255,32,32,0.6); transform:scale(1.15);"
            else:
                card_style = "background:#7850ff;"
            cards_html += f'<div style="width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:white; {card_style}">{value}</div>'
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        # Sorted check for easy
        if level == "easy" and nums == sorted(nums) and st.session_state.bubble_first_move_made:
            st.markdown("""
                <div style="background:rgba(0,200,83,0.2); border:2px solid #00c853; border-radius:12px; padding:18px; text-align:center; margin-bottom:12px;">
                    <p style="color:#00c853; font-size:22px; font-weight:800; margin:0;">🎉 Sorted! Well done!</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Try Again", use_container_width=True):
                st.session_state.nums = make_numbers(level)
                st.session_state.index = 0
                st.session_state.code_line = 0
                st.session_state.explain = "Press Next to start comparing neighbours."
                st.session_state.bubble_first_move_made = False
                st.rerun()
        else:
            swap_col, next_col = st.columns(2)
            with swap_col:
                if st.button("🔀 SWAP", use_container_width=True):
                    st.session_state.bubble_first_move_made = True

                    if i < len(nums) - 1:
                        left_num = nums[i]
                        right_num = nums[i + 1]
                        if left_num > right_num:
                            nums[i] = right_num
                            nums[i + 1] = left_num
                            st.session_state.nums = nums
                            st.session_state.code_line = 5
                            st.session_state.explain = f"Swapped {nums[i+1]} and {nums[i]} because {nums[i+1]} &gt; {nums[i]}. Bigger values bubble right! ↑"
                        else:
                            st.session_state.code_line = 4
                            st.session_state.explain = f"No swap needed — {left_num} ≤ {right_num}. They're already in order. ✓"
                    st.rerun()

            with next_col:
                if st.button("➡ NEXT", use_container_width=True):
                    st.session_state.bubble_first_move_made = True

                    if i < len(nums) - 2:
                        st.session_state.index = i + 1
                        next_left = nums[i + 1]
                        next_right = nums[i + 2]
                        st.session_state.code_line = 4
                        st.session_state.explain = f"Comparing {next_left} and {next_right} — is {next_left} &gt; {next_right}? {('Yes, swap!' if next_left > next_right else 'No, move on.')}"
                    else:
                        st.session_state.index = 0
                        st.session_state.code_line = 2
                        st.session_state.explain = "Starting a new pass from the beginning! Each pass guarantees the largest unsorted value reaches its final position."
                    st.rerun()

        # Easy: show current comparison info
        if level == "easy" and st.session_state.bubble_first_move_made and i < len(nums) - 1:
            left_val = nums[i]
            right_val = nums[i + 1]
            cmp_color = "#ff2020" if left_val > right_val else "#00c853"
            cmp_text = f"{left_val} &gt; {right_val} → SWAP!" if left_val > right_val else f"{left_val} ≤ {right_val} → No swap"
            st.markdown(f"""
                <div style="margin-top:10px; background:rgba(255,255,255,0.07); border-radius:10px; padding:10px; text-align:center;">
                    <span style="color:{cmp_color}; font-size:15px; font-weight:700; font-family:monospace;">{cmp_text}</span>
                </div>
            """, unsafe_allow_html=True)

    # ── RIGHT PANEL (Easy only) ──
    if level == "easy":
        with right_col:
            if st.session_state.bubble_first_move_made:
                show_easy_code_and_complexity()
            else:
                show_easy_placeholder()

    # Hard: countdown keeps ticking
    if level == "hard" and st.session_state.timer_set and st.session_state.game_over is None:
        time.sleep(1)
        st.rerun()

    # Medium: countdown keeps ticking
    if level == "medium" and st.session_state.medium_timer_set and st.session_state.medium_game_over is None:
        time.sleep(1)
        st.rerun()


# ══════════════════════════════════════════════════════════════════
# MERGE SORT HELPERS (unchanged from original)
# ══════════════════════════════════════════════════════════════════
MERGE_LEVELS = {
    1: 4,  2: 6,  3: 8,  4: 10,
    5: 12, 6: 14, 7: 16, 8: 18, 9: 20, 10: 24
}

def get_level_mode(level):
    if level <= 2:
        return "tutorial"
    elif level <= 4:
        return "guided"
    else:
        return "challenge"

def get_level_badge(level):
    mode = get_level_mode(level)
    if mode == "tutorial":
        return "🎓 TUTORIAL"
    elif mode == "guided":
        return "📖 GUIDED"
    else:
        return "🔥 CHALLENGE"

def generate_merge_numbers(level):
    count = MERGE_LEVELS[level]
    nums = random.sample(range(1, 99), count)
    return nums

def calc_splits(arr):
    arr = [int(x) for x in list(arr)]
    levels = [arr]
    current = [arr]
    while any(len(g) > 1 for g in current):
        next_level = []
        for g in current:
            g = [int(x) for x in list(g)]
            if len(g) > 1:
                mid = math.ceil(len(g) / 2)
                next_level.append([int(x) for x in g[:mid]])
                next_level.append([int(x) for x in g[mid:]])
            else:
                next_level.append([int(x) for x in g])
        levels.append(next_level)
        current = next_level
    return levels

def calc_merge_pairs(split_levels):
    singles = split_levels[-1]
    pairs = []
    i = 0
    while i < len(singles) - 1:
        left = [int(x) for x in list(singles[i])]
        right = [int(x) for x in list(singles[i + 1])]
        pairs.append([left, right])
        i = i + 2
    return pairs

def get_merge_time():
    if not st.session_state.merge_timer_started:
        return 0
    elapsed = time.time() - st.session_state.merge_start_time
    elapsed = elapsed + st.session_state.merge_penalty
    return int(elapsed)

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def set_hearts(level):
    if level in [5, 10]:
        return 2
    return 3

def is_sorted(nums):
    return list(nums) == sorted(list(nums))

def start_merge_timer():
    if not st.session_state.merge_timer_started:
        st.session_state.merge_start_time = time.time()
        st.session_state.merge_timer_started = True

def reset_merge_level(level):
    nums = generate_merge_numbers(level)
    nums = [int(x) for x in nums]
    split_levels = calc_splits(nums)
    pairs = calc_merge_pairs(split_levels)

    st.session_state.merge_numbers = nums
    st.session_state.merge_split_levels = split_levels
    st.session_state.merge_split_idx = 0
    st.session_state.merge_pairs = pairs
    st.session_state.merge_pair_idx = 0
    st.session_state.merge_phase = "split"
    st.session_state.merge_current_left = []
    st.session_state.merge_current_right = []
    st.session_state.merge_merged_results = []
    st.session_state.merge_timer_started = False
    st.session_state.merge_start_time = 0
    st.session_state.merge_penalty = 0
    st.session_state.merge_hearts = set_hearts(level)
    st.session_state.merge_code_line = 0
    st.session_state.merge_explain = "Press Split to divide the list in half — that is the first step of Merge Sort!"
    st.session_state.merge_available = []
    st.session_state.merge_player_order = []
    st.session_state.challenge_current_groups = [nums[:]]
    st.session_state.challenge_split_complete = False
    st.session_state.challenge_merge_groups = []
    st.session_state.challenge_merge_idx = 0
    st.session_state.challenge_player_pick = []
    st.session_state.challenge_available = []

def show_merge_code_panel():
    active = st.session_state.merge_code_line
    all_lines = [
        "def merge_sort(arr):",
        "&nbsp;&nbsp;if len(arr) &lt;= 1:",
        "&nbsp;&nbsp;&nbsp;&nbsp;return arr",
        "&nbsp;&nbsp;mid = len(arr) // 2",
        "&nbsp;&nbsp;left = merge_sort(arr[:mid])",
        "&nbsp;&nbsp;right = merge_sort(arr[mid:])",
        "&nbsp;&nbsp;return merge(left, right)",
        "&nbsp;",
        "def merge(left, right):",
        "&nbsp;&nbsp;result = []",
        "&nbsp;&nbsp;while left and right:",
        "&nbsp;&nbsp;&nbsp;&nbsp;if left[0] &lt; right[0]:",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;result.append(left.pop(0))",
        "&nbsp;&nbsp;&nbsp;&nbsp;else:",
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;result.append(right.pop(0))",
        "&nbsp;&nbsp;return result + left + right",
    ]
    code_html = ""
    for idx, line in enumerate(all_lines):
        if idx == active:
            style = "background:rgba(255,208,0,0.2); color:#ffd000; font-weight:bold; border-radius:6px; padding:4px 8px; display:block;"
        else:
            style = "color:rgba(255,255,255,0.35); padding:4px 8px; display:block;"
        code_html += f'<span style="{style}">{line}</span>'

    st.markdown('<p style="color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;">THE CODE</p>', unsafe_allow_html=True)
    st.markdown('<div style="background:#1a1a2e; border-radius:14px; padding:16px; font-family:monospace; font-size:12px; line-height:1.9;">' + code_html + '</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:12px; background:rgba(255,208,0,0.85); border-left:3px solid #ffd000; border-radius:0 10px 10px 0; padding:10px 14px; color:black; font-size:13px; line-height:1.6;">💡 ' + st.session_state.merge_explain + '</div>', unsafe_allow_html=True)

def show_split_tree():
    split_levels = st.session_state.merge_split_levels
    split_idx = st.session_state.merge_split_idx
    merged_results = st.session_state.merge_merged_results
    show_up_to = min(split_idx + 1, len(split_levels))
    tree_html = ""

    for lvl in range(show_up_to):
        groups = split_levels[lvl]
        tree_html += '<div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:6px;">'
        for g in groups:
            if isinstance(g, int):
                g = [g]
            else:
                g = [int(x) for x in list(g)]
            tree_html += '<div style="display:flex; gap:3px;">'
            for num in g:
                if lvl == 0:
                    bg = "#7850ff"
                elif len(g) == 1:
                    bg = "#ff9800"
                elif lvl % 2 == 1:
                    bg = "#ef4444"
                else:
                    bg = "#3b82f6"
                tree_html += f'<div style="width:36px; height:36px; border-radius:8px; background:{bg}; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:white;">{num}</div>'
            tree_html += '</div>'
        tree_html += '</div>'
        if lvl < show_up_to - 1:
            tree_html += '<div style="text-align:center; color:rgba(255,255,255,0.4); font-size:16px; margin:2px 0;">↓</div>'

    if merged_results:
        tree_html += '<div style="text-align:center; color:rgba(255,255,255,0.4); font-size:16px; margin:4px 0;">↓ merging...</div>'
        tree_html += '<div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">'
        for result in merged_results:
            if isinstance(result, int):
                result = [result]
            else:
                result = [int(x) for x in list(result)]
            tree_html += '<div style="display:flex; gap:3px;">'
            for num in result:
                tree_html += f'<div style="width:36px; height:36px; border-radius:8px; background:#00c853; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:white;">{num}</div>'
            tree_html += '</div>'
        tree_html += '</div>'

    st.markdown('<p style="color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;">SPLIT TREE</p>', unsafe_allow_html=True)
    st.markdown('<div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:16px; min-height:80px;">' + tree_html + '</div>', unsafe_allow_html=True)

def render_challenge_split():
    groups = st.session_state.challenge_current_groups
    all_single = all(len(g) == 1 for g in groups)

    if all_single:
        st.markdown("""
            <div style="background:rgba(0,200,83,0.15); border:1px solid #00c853; border-radius:10px; padding:12px; text-align:center; margin-bottom:12px;">
                <p style="color:#00c853; font-weight:bold; margin:0;">✅ All split into single numbers! Now merge them back in sorted order.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Start Merging!", use_container_width=True):
            singles = [[g[0]] for g in groups]
            pairs = []
            i = 0
            while i < len(singles) - 1:
                pairs.append([singles[i], singles[i + 1]])
                i = i + 2
            st.session_state.merge_pairs = pairs
            st.session_state.merge_pair_idx = 0
            st.session_state.merge_phase = "merge"
            if pairs:
                first_pair = pairs[0]
                left_list = [int(x) for x in first_pair[0]]
                right_list = [int(x) for x in first_pair[1]]
                st.session_state.merge_current_left = left_list
                st.session_state.merge_current_right = right_list
                st.session_state.merge_available = left_list + right_list
                random.shuffle(st.session_state.merge_available)
                st.session_state.merge_player_order = []
            st.rerun()
        return

    st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>CURRENT GROUPS — Click a number to split its group at that position</p>", unsafe_allow_html=True)

    for group_idx, group in enumerate(groups):
        if len(group) <= 1:
            card_html = '<div style="display:flex; gap:6px; justify-content:center; margin-bottom:8px;">'
            for num in group:
                card_html += f'<div style="width:44px; height:44px; border-radius:10px; background:#ff9800; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:white;">{num}</div>'
            card_html += '</div>'
            st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color:rgba(255,255,255,0.5); font-size:11px; text-align:center;'>Group {group_idx + 1} — click where to split:</p>", unsafe_allow_html=True)
            display_group = group[:]
            cols = st.columns(len(display_group))
            for num_idx, num in enumerate(display_group):
                with cols[num_idx]:
                    st.markdown(f'<div style="background:#7850ff; border-radius:8px; padding:8px; text-align:center; color:white; font-weight:700; font-size:14px; margin-bottom:4px;">{num}</div>', unsafe_allow_html=True)
                    if st.button(f"Split here", key=f"split_g{group_idx}_n{num_idx}_{num}", use_container_width=True):
                        mid = num_idx + 1
                        left_part = display_group[:mid]
                        right_part = display_group[mid:]
                        correct_mid = math.ceil(len(display_group) / 2)
                        is_correct = (mid == correct_mid)
                        if is_correct:
                            new_groups = []
                            for idx2, g in enumerate(groups):
                                if idx2 == group_idx:
                                    new_groups.append(left_part)
                                    new_groups.append(right_part)
                                else:
                                    new_groups.append(g)
                            st.session_state.challenge_current_groups = new_groups
                            st.session_state.merge_explain = "Correct split! Keep splitting until every number is alone."
                        else:
                            st.session_state.merge_hearts -= 1
                            st.session_state.merge_penalty += 10
                            st.session_state.merge_explain = "Wrong split point! Split as close to the middle as possible. -1 heart, +10 seconds!"
                        st.rerun()

    st.markdown('<div style="margin-top:12px; background:rgba(255,208,0,0.85); border-left:3px solid #ffd000; border-radius:0 10px 10px 0; padding:10px 14px; color:black; font-size:13px; line-height:1.6;">💡 ' + st.session_state.merge_explain + '</div>', unsafe_allow_html=True)

def render_merge_home():
    show_gradient_background()
    if st.button("⬅ Back", type="secondary"):
        go_to_page("home")

    st.markdown("<h1 style='text-align:center; color:white;'>Merge Sort Challenge</h1>", unsafe_allow_html=True)
    st.markdown("<div style='width:60px; height:3px; background:rgba(255,255,255,0.5); border-radius:2px; margin:0 auto 20px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>HOW TO PLAY</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">1</p><p style="color:white; font-size:14px;">Split the list into halves</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">2</p><p style="color:white; font-size:14px;">Split until single elements</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">3</p><p style="color:white; font-size:14px;">Compare and pick smallest</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">4</p><p style="color:white; font-size:14px;">Merge back in sorted order</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:16px; margin-bottom:24px;">
            <p style="color:#ffd000; font-size:16px; font-weight:bold; margin:0 0 10px;">📋 Level Progression</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🎓 <strong>Levels 1-2</strong> — Tutorial: SPLIT button works, code shown, hints, no timer, no hearts</p>
            <p style="color:white; font-size:14px; margin:6px 0;">📖 <strong>Levels 3-4</strong> — Guided: SPLIT button works, code shown, stopwatch starts, hearts added</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🔥 <strong>Levels 5-10</strong> — Challenge: YOU split manually by choosing the midpoint, no hints, stopwatch, hearts, no undo!</p>
            <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:10px 0 0;">❤️ Wrong split or wrong merge = lose a heart + 10 second penalty added to your time!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>SELECT YOUR LEVEL</p>", unsafe_allow_html=True)

    cols = st.columns(5)
    for level in range(1, 6):
        unlocked = level in st.session_state.merge_unlocked
        completed = level in st.session_state.merge_completed
        mode = get_level_mode(level)
        if completed:
            btn_color = "#00c853"
        elif mode == "tutorial":
            btn_color = "#7850ff"
        elif mode == "guided":
            btn_color = "#ff9800"
        else:
            btn_color = "#ff2020"
        label = f"Lv {level}"
        if completed:
            label = f"✅ {label}"
        pb = st.session_state.merge_personal_best.get(level)
        pb_text = f"Best: {format_time(pb)}" if pb else ""
        with cols[level - 1]:
            if unlocked:
                st.markdown(f'<div style="background:{btn_color}; border-radius:10px; padding:8px 6px; text-align:center; color:white; font-size:12px; font-weight:700; margin-bottom:4px;">{label}<br><span style="font-size:10px; opacity:0.8;">{pb_text}</span></div>', unsafe_allow_html=True)
                if st.button(get_level_badge(level), key=f"ml_{level}", use_container_width=True):
                    st.session_state.merge_level = level
                    reset_merge_level(level)
                    go_to_page("merge_game")
            else:
                st.markdown(f'<div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:10px 6px; text-align:center; color:rgba(255,255,255,0.3); font-size:12px; font-weight:700; margin-bottom:6px;">🔒 Lv {level}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cols2 = st.columns(5)
    for level in range(6, 11):
        unlocked = level in st.session_state.merge_unlocked
        completed = level in st.session_state.merge_completed
        label = f"Lv {level}"
        if completed:
            label = f"✅ {label}"
        pb = st.session_state.merge_personal_best.get(level)
        pb_text = f"Best: {format_time(pb)}" if pb else ""
        with cols2[level - 6]:
            if unlocked:
                st.markdown(f'<div style="background:#ff2020; border-radius:10px; padding:8px 6px; text-align:center; color:white; font-size:12px; font-weight:700; margin-bottom:4px;">{label}<br><span style="font-size:10px; opacity:0.8;">{pb_text}</span></div>', unsafe_allow_html=True)
                if st.button("🔥 CHALLENGE", key=f"ml_{level}", use_container_width=True):
                    st.session_state.merge_level = level
                    reset_merge_level(level)
                    go_to_page("merge_game")
            else:
                st.markdown(f'<div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:10px 6px; text-align:center; color:rgba(255,255,255,0.3); font-size:12px; font-weight:700; margin-bottom:6px;">🔒 Lv {level}</div>', unsafe_allow_html=True)

def render_merge_game():
    level = st.session_state.merge_level
    mode = get_level_mode(level)
    show_gradient_background()

    if not st.session_state.merge_numbers:
        reset_merge_level(level)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ Back", type="secondary"):
            go_to_page("merge")
    with col2:
        if mode in ["guided", "challenge"]:
            current_time = get_merge_time()
            st.markdown(f"""
                <div style="text-align:center; background:rgba(0,0,0,0.3); border-radius:12px; padding:8px; border:2px solid #ffd000;">
                    <span style="color:#ffd000; font-size:22px; font-weight:800;">⏱ {format_time(current_time)}</span>
                    <br><span style="color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px;">YOUR TIME</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align:center; background:rgba(120,80,255,0.2); border-radius:12px; padding:8px; border:2px solid #7850ff;">
                    <span style="color:#c084ff; font-size:14px; font-weight:800;">{get_level_badge(level)}</span>
                </div>
            """, unsafe_allow_html=True)
    with col3:
        if mode in ["guided", "challenge"]:
            hearts = "❤️" * st.session_state.merge_hearts
            st.markdown(f"<div style='text-align:center; font-size:20px; padding-top:8px;'>{hearts}</div>", unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align:center; color:white;'>Merge Sort — Level {level}</h2>", unsafe_allow_html=True)

    if mode in ["guided", "challenge"] and st.session_state.merge_hearts <= 0:
        st.markdown("""
            <div style="background:rgba(255,32,32,0.3); border:2px solid #ff2020; border-radius:14px; padding:30px; text-align:center; margin:20px 0;">
                <p style="color:white; font-size:32px; font-weight:800; margin:0;">💀 GAME OVER</p>
                <p style="color:rgba(255,255,255,0.8); font-size:14px; margin:8px 0 0;">You lost all your hearts! Try again.</p>
            </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Restart Level", use_container_width=True):
                reset_merge_level(level)
                st.rerun()
        with col2:
            if st.button("🏠 Back to Levels", use_container_width=True):
                go_to_page("merge")
        return

    if mode == "challenge":
        start_merge_timer()
        if st.session_state.merge_phase == "split":
            st.markdown("""
                <div style="background:rgba(255,32,32,0.15); border:1px solid #ff2020; border-radius:10px; padding:12px; text-align:center; margin-bottom:16px;">
                    <p style="color:#ff2020; font-weight:bold; font-size:13px; margin:0;">🔥 CHALLENGE MODE — Split the numbers yourself! Click where to divide each group.</p>
                </div>
            """, unsafe_allow_html=True)
            render_challenge_split()
        elif st.session_state.merge_phase == "merge":
            render_challenge_merge(level)
    else:
        split_levels = st.session_state.merge_split_levels
        split_idx = st.session_state.merge_split_idx

        if st.session_state.merge_phase == "split":
            show_split_tree()
            st.markdown("<br>", unsafe_allow_html=True)
            if split_idx < len(split_levels) - 1:
                left_col, right_col = st.columns(2)
                with left_col:
                    if mode == "tutorial":
                        st.markdown('<div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:12px; margin-bottom:12px;"><p style="color:white; font-size:13px; margin:0;">👆 Press <strong>Split</strong> to divide the list in half. Keep splitting until every number is alone!</p></div>', unsafe_allow_html=True)
                    if st.button("🔀 SPLIT", use_container_width=True):
                        if mode == "guided":
                            start_merge_timer()
                        st.session_state.merge_split_idx += 1
                        new_idx = st.session_state.merge_split_idx
                        groups = split_levels[new_idx]
                        all_single = all(len(list(g)) == 1 for g in groups)
                        if all_single:
                            st.session_state.merge_code_line = 1
                            st.session_state.merge_explain = "Every number is now alone — a single number is already sorted! Now we merge them back together."
                        else:
                            st.session_state.merge_code_line = 3
                            st.session_state.merge_explain = "Split! Each group is divided in half. Keep splitting until every piece has just one number."
                        st.rerun()
                with right_col:
                    show_merge_code_panel()
            else:
                left_col, right_col = st.columns(2)
                with left_col:
                    if mode == "tutorial":
                        st.markdown('<div style="background:rgba(0,200,83,0.15); border:1px solid #00c853; border-radius:10px; padding:12px; margin-bottom:12px;"><p style="color:#00c853; font-size:13px; margin:0;">✅ All split! Press <strong>Start Merging</strong> to put them back in sorted order.</p></div>', unsafe_allow_html=True)
                    if st.button("✅ Start Merging!", use_container_width=True):
                        st.session_state.merge_phase = "merge"
                        pairs = st.session_state.merge_pairs
                        if pairs:
                            first_pair = pairs[0]
                            left_list = sorted([int(x) for x in list(first_pair[0])])
                            right_list = sorted([int(x) for x in list(first_pair[1])])
                            st.session_state.merge_current_left = left_list
                            st.session_state.merge_current_right = right_list
                            combined = left_list + right_list
                            random.shuffle(combined)
                            st.session_state.merge_available = combined
                            st.session_state.merge_player_order = []
                            st.session_state.merge_code_line = 10
                            st.session_state.merge_explain = "Pick the smallest number from either list to build the sorted result!"
                        st.rerun()
                with right_col:
                    show_merge_code_panel()

        elif st.session_state.merge_phase == "merge":
            render_tutorial_merge(level, mode)

def render_tutorial_merge(level, mode):
    pair_idx = st.session_state.merge_pair_idx
    pairs = st.session_state.merge_pairs
    merged_results = st.session_state.merge_merged_results

    show_split_tree()
    st.markdown("<br>", unsafe_allow_html=True)

    if pair_idx >= len(pairs):
        show_level_complete(level)
        return

    left = [int(x) for x in list(st.session_state.merge_current_left)]
    right = [int(x) for x in list(st.session_state.merge_current_right)]
    player_order = st.session_state.merge_player_order
    available = [int(x) for x in list(st.session_state.merge_available)]

    st.markdown(f"<p style='text-align:center; color:white; letter-spacing:3px; font-size:11px;'>MERGING PAIR {pair_idx + 1} OF {len(pairs)}</p>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)
    with left_col:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<p style='color:#ef4444; font-size:11px; font-weight:bold; text-align:center;'>🔴 LEFT</p>", unsafe_allow_html=True)
            left_html = '<div style="display:flex; flex-wrap:wrap; gap:4px; justify-content:center;">'
            for num in left:
                left_html += f'<div style="width:40px; height:40px; border-radius:8px; background:#ef4444; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:white;">{num}</div>'
            left_html += '</div>'
            st.markdown(left_html, unsafe_allow_html=True)
        with c2:
            st.markdown("<p style='color:#3b82f6; font-size:11px; font-weight:bold; text-align:center;'>🔵 RIGHT</p>", unsafe_allow_html=True)
            right_html = '<div style="display:flex; flex-wrap:wrap; gap:4px; justify-content:center;">'
            for num in right:
                right_html += f'<div style="width:40px; height:40px; border-radius:8px; background:#3b82f6; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:white;">{num}</div>'
            right_html += '</div>'
            st.markdown(right_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if mode == "tutorial":
            st.markdown('<div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:10px; margin-bottom:10px;"><p style="color:white; font-size:12px; margin:0;">👆 Click <strong>Pick</strong> under the smallest number!</p></div>', unsafe_allow_html=True)

        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px;'>PICK THE SMALLEST:</p>", unsafe_allow_html=True)

        num_cols = min(len(available), 6) if available else 1
        if available:
            avail_cols = st.columns(num_cols)
            for idx, num in enumerate(available):
                bg = "#ef4444" if num in left else "#3b82f6"
                with avail_cols[idx % num_cols]:
                    st.markdown(f'<div style="background:{bg}; border-radius:8px; padding:8px; text-align:center; color:white; font-weight:700; font-size:14px; margin-bottom:4px;">{num}</div>', unsafe_allow_html=True)
                    if st.button(f"Pick", key=f"pick_{num}_{idx}_{pair_idx}", use_container_width=True):
                        smallest = min(available)
                        if num == smallest:
                            player_order.append(num)
                            available.remove(num)
                            st.session_state.merge_player_order = player_order
                            st.session_state.merge_available = available
                            st.session_state.merge_code_line = 11
                            st.session_state.merge_explain = str(num) + " is the smallest — added to the merged list! Keep going."
                            if not available:
                                st.session_state.merge_merged_results.append(player_order[:])
                                st.session_state.merge_pairs[pair_idx] = [player_order[:], []]
                                st.session_state.merge_pair_idx += 1
                                next_idx = st.session_state.merge_pair_idx
                                if next_idx < len(pairs):
                                    next_pair = pairs[next_idx]
                                    next_left = sorted([int(x) for x in list(next_pair[0])])
                                    next_right = sorted([int(x) for x in list(next_pair[1])])
                                    st.session_state.merge_current_left = next_left
                                    st.session_state.merge_current_right = next_right
                                    combined = next_left + next_right
                                    random.shuffle(combined)
                                    st.session_state.merge_available = combined
                                    st.session_state.merge_player_order = []
                                    st.session_state.merge_code_line = 10
                                    st.session_state.merge_explain = "Great! Now merge the next pair!"
                        else:
                            st.session_state.merge_code_line = 11
                            st.session_state.merge_explain = str(num) + " is not the smallest! Pick the smallest from both lists."
                            if mode == "guided":
                                st.session_state.merge_hearts -= 1
                                st.session_state.merge_penalty += 10
                                st.session_state.merge_explain += " ❌ -1 heart, +10s!"
                        st.rerun()

        if player_order:
            st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px; margin-top:10px;'>YOUR MERGED RESULT:</p>", unsafe_allow_html=True)
            merged_html = '<div style="display:flex; flex-wrap:wrap; gap:4px;">'
            for num in player_order:
                merged_html += f'<div style="width:40px; height:40px; border-radius:8px; background:#00c853; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:white;">{num}</div>'
            merged_html += '</div>'
            st.markdown(merged_html, unsafe_allow_html=True)
            if mode == "tutorial":
                if st.button("↩ Undo", use_container_width=True):
                    last = player_order.pop()
                    available.append(last)
                    available.sort()
                    st.session_state.merge_player_order = player_order
                    st.session_state.merge_available = available
                    st.rerun()

    with right_col:
        show_merge_code_panel()

def render_challenge_merge(level):
    pair_idx = st.session_state.merge_pair_idx
    pairs = st.session_state.merge_pairs

    if pair_idx >= len(pairs):
        show_level_complete(level)
        return

    left = [int(x) for x in list(st.session_state.merge_current_left)]
    right = [int(x) for x in list(st.session_state.merge_current_right)]
    player_order = st.session_state.merge_player_order
    available = [int(x) for x in list(st.session_state.merge_available)]

    st.markdown(f"<p style='text-align:center; color:white; letter-spacing:3px; font-size:11px;'>MERGING PAIR {pair_idx + 1} OF {len(pairs)}</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px; text-align:center;'>PICK THE SMALLEST NUMBER TO MERGE:</p>", unsafe_allow_html=True)

    num_cols = min(len(available), 8) if available else 1
    if available:
        avail_cols = st.columns(num_cols)
        for idx, num in enumerate(available):
            with avail_cols[idx % num_cols]:
                st.markdown(f'<div style="background:#7850ff; border-radius:8px; padding:8px; text-align:center; color:white; font-weight:700; font-size:14px; margin-bottom:4px;">{num}</div>', unsafe_allow_html=True)
                if st.button(f"Pick", key=f"cpick_{num}_{idx}_{pair_idx}", use_container_width=True):
                    smallest = min(available)
                    if num == smallest:
                        player_order.append(num)
                        available.remove(num)
                        st.session_state.merge_player_order = player_order
                        st.session_state.merge_available = available
                        if not available:
                            st.session_state.merge_merged_results.append(player_order[:])
                            st.session_state.merge_pairs[pair_idx] = [player_order[:], []]
                            st.session_state.merge_pair_idx += 1
                            next_idx = st.session_state.merge_pair_idx
                            if next_idx < len(pairs):
                                next_pair = pairs[next_idx]
                                next_left = [int(x) for x in list(next_pair[0])]
                                next_right = [int(x) for x in list(next_pair[1])]
                                st.session_state.merge_current_left = next_left
                                st.session_state.merge_current_right = next_right
                                combined = next_left + next_right
                                random.shuffle(combined)
                                st.session_state.merge_available = combined
                                st.session_state.merge_player_order = []
                    else:
                        st.session_state.merge_hearts -= 1
                        st.session_state.merge_penalty += 10
                    st.rerun()

    if player_order:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px; margin-top:10px; text-align:center;'>YOUR MERGED RESULT:</p>", unsafe_allow_html=True)
        merged_html = '<div style="display:flex; flex-wrap:wrap; gap:4px; justify-content:center;">'
        for num in player_order:
            merged_html += f'<div style="width:40px; height:40px; border-radius:8px; background:#00c853; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:white;">{num}</div>'
        merged_html += '</div>'
        st.markdown(merged_html, unsafe_allow_html=True)

def show_level_complete(level):
    total_seconds = get_merge_time()
    total_time = format_time(total_seconds)
    existing_best = st.session_state.merge_personal_best.get(level)
    is_new_best = False
    if existing_best is None or total_seconds < existing_best:
        st.session_state.merge_personal_best[level] = total_seconds
        is_new_best = True

    if level not in st.session_state.merge_completed:
        st.session_state.merge_completed.append(level)
    next_level = level + 1
    if next_level <= 10 and next_level not in st.session_state.merge_unlocked:
        st.session_state.merge_unlocked.append(next_level)

    if level == 10:
        st.markdown(f"""
            <div style="background:rgba(255,208,0,0.2); border:2px solid #ffd000; border-radius:14px; padding:30px; text-align:center; margin:20px 0;">
                <p style="color:#ffd000; font-size:36px; font-weight:800; margin:0;">🏆 MERGE SORT MASTER!</p>
                <p style="color:white; font-size:16px; margin:8px 0 0;">You completed all 10 levels!</p>
                <p style="color:#ffd000; font-size:20px; font-weight:700; margin:8px 0 0;">Time: {total_time}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        new_best_text = "🌟 New Personal Best!" if is_new_best else ""
        st.markdown(f"""
            <div style="background:rgba(0,200,83,0.2); border:2px solid #00c853; border-radius:14px; padding:24px; text-align:center; margin:20px 0;">
                <p style="color:#00c853; font-size:28px; font-weight:800; margin:0;">🎉 Level {level} Complete!</p>
                <p style="color:#ffd000; font-size:22px; font-weight:700; margin:8px 0;">⏱ {total_time}</p>
                <p style="color:white; font-size:13px; margin:4px 0;">{new_best_text}</p>
                <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:4px 0;">Level {level + 1} unlocked!</p>
            </div>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Try Again", use_container_width=True):
            reset_merge_level(level)
            st.rerun()
    with col2:
        if level < 10:
            if st.button(f"➡ Level {level + 1}", use_container_width=True):
                st.session_state.merge_level = level + 1
                reset_merge_level(level + 1)
                st.rerun()
    with col3:
        if st.button("🏠 Levels", use_container_width=True):
            go_to_page("merge")


# ══════════════════════════════════════════════════════════════════
# PAGE ROUTING
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0d0010 0%, #5a0080 25%, #c0003c 50%, #ff6600 75%, #ffd000 100%);
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
        div.stButton > button:hover { background-color: #ff3a3a; }
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
            go_to_page("bubble")
    with col2:
        if st.button("MERGE SORT"):
            go_to_page("merge")

elif st.session_state.page == "bubble":
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0d0010 0%, #5a0080 25%, #c0003c 50%, #ff6600 75%, #ffd000 100%); }
        div.stButton > button { width: 100%; height: 50px; font-size: 16px; font-weight: bold; border-radius: 10px; border: none; }
        div.stButton:has(button[kind="secondary"]) > button { width: auto; height: 36px; font-size: 13px; background: rgba(255,255,255,0.15); color: white; border: 1px solid rgba(255,255,255,0.3); border-radius: 20px; padding: 0 16px; }
        div[data-testid="column"]:nth-child(1) div.stButton > button { background: #00c853; color: #003300; }
        div[data-testid="column"]:nth-child(2) div.stButton > button { background: #ff9800; color: #3d1f00; }
        div[data-testid="column"]:nth-child(3) div.stButton > button { background: #ff2020; color: #1a0000; }
    </style>
    """, unsafe_allow_html=True)

    if st.button("⬅ Back", type="secondary"):
        go_to_page("home")

    st.markdown("<h1 style='text-align:center; color:white;'>Bubble Sort Game</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>HOW TO PLAY</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">1</p><p style="color:white; font-size:12px;">Choose a difficulty level</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">2</p><p style="color:white; font-size:12px;">Click Generate Numbers to start</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;"><p style="color:#ffd000; font-size:22px; font-weight:bold;">3</p><p style="color:white; font-size:12px;">Use Swap and Next to sort!</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mode descriptions
    st.markdown("""
        <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:16px; margin-bottom:20px;">
            <p style="color:#ffd000; font-size:15px; font-weight:bold; margin:0 0 10px;">📋 Mode Guide</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🟢 <strong>Easy</strong> — Educational mode. See the code, learn the algorithm, understand complexity. Best for beginners!</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🟠 <strong>Medium</strong> — Gameplay. How fast can you sort? set your own countdown(max 120s)</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🔴 <strong>Hard</strong> — Pure challenge. Set your own countdown (max 120s). Race against time!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>SELECT YOUR DIFFICULTY</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("EASY"):
            st.session_state.bubble_first_move_made = False
            st.session_state.pop("nums", None)
            go_to_page("bubble_easy")
    with col2:
        if st.button("MEDIUM"):
            st.session_state.medium_timer_set = False
            st.session_state.medium_timer_start = None
            st.session_state.medium_timer_limit = None
            st.session_state.medium_game_over = None
            st.session_state.bubble_first_move_made = False
            st.session_state.pop("nums", None)
            go_to_page("bubble_medium")
    with col3:
        if st.button("HARD"):
            st.session_state.pop("nums", None)
            go_to_page("bubble_hard")

elif st.session_state.page == "bubble_easy":
    show_bubble_game("easy")

elif st.session_state.page == "bubble_medium":
    show_bubble_game("medium")

elif st.session_state.page == "bubble_hard":
    show_bubble_game("hard")

elif st.session_state.page == "merge":
    render_merge_home()

elif st.session_state.page == "merge_game":
    render_merge_game()
        

    




