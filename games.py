import streamlit as st
import random
import time
import math

# HOW TO RUN: python -m streamlit run games.py
# Make sure image1.png is in the same folder!

st.set_page_config(page_title="BrainSort Challenge", layout="centered")

# ================================================================
# SESSION STATE SETUP
# ================================================================
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
if "merge_current_merged" not in st.session_state:
    st.session_state.merge_current_merged = []
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


# ================================================================
# NAVIGATION
# ================================================================
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()


# ================================================================
# SHARED: Gradient background
# ================================================================
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


# ================================================================
# BUBBLE SORT: Generate numbers
# ================================================================
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
        numbers = random.sample(range(1, 40), 20)
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


# ================================================================
# MERGE SORT: Helper functions
# ================================================================

MERGE_LEVELS = {
    1: 4,  2: 6,  3: 8,  4: 10, 5: 12,
    6: 14, 7: 16, 8: 18, 9: 20, 10: 24
}

def get_level_mode(level):
    if level <= 2:
        return "tutorial"
    elif level <= 5:
        return "semi"
    else:
        return "challenge"

def get_level_badge(level):
    mode = get_level_mode(level)
    if mode == "tutorial":
        return "🎓 TUTORIAL"
    elif mode == "semi":
        return "⚔️ SEMI-CHALLENGE"
    else:
        return "🔥 CHALLENGE"

def generate_merge_numbers(level):
    count = MERGE_LEVELS[level]
    nums = random.sample(range(1, 99), count)
    return nums

def calc_splits(arr):
    # Make sure we work with a clean list of integers
    arr = [int(x) for x in list(arr)]
    levels = [arr]
    current = [arr]

    while any(len(g) > 1 for g in current):
        next_level = []
        for g in current:
            # Make sure g is always a list
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
    # Get pairs to merge from bottom of split tree
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
    # Make sure nums is a clean list of ints
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
    st.session_state.merge_current_merged = []
    st.session_state.merge_merged_results = []
    st.session_state.merge_timer_started = False
    st.session_state.merge_start_time = 0
    st.session_state.merge_penalty = 0
    st.session_state.merge_hearts = set_hearts(level)
    st.session_state.merge_code_line = 0
    st.session_state.merge_explain = "Press Split to divide the list in half — that is the first step of Merge Sort!"
    st.session_state.merge_available = []
    st.session_state.merge_player_order = []


# ================================================================
# MERGE SORT: Code panel
# ================================================================
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
        code_html = code_html + '<span style="' + style + '">' + line + '</span>'

    st.markdown("""
        <p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>THE CODE</p>
        <div style="background:#1a1a2e; border-radius:14px; padding:16px; font-family:monospace; font-size:12px; line-height:1.9;">
    """ + code_html + """</div>""", unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top:12px; background:rgba(255,208,0,0.85); border-left:3px solid #ffd000; border-radius:0 10px 10px 0; padding:10px 14px; color:black; font-size:13px; line-height:1.6;">
        💡 """ + st.session_state.merge_explain + """</div>
    """, unsafe_allow_html=True)


# ================================================================
# MERGE SORT: Split tree display
# ================================================================
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
            # SAFETY CHECK: make sure g is always a list
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

    # Show merged results
    if merged_results:
        tree_html += '<div style="text-align:center; color:rgba(255,255,255,0.4); font-size:16px; margin:4px 0;">↓ merging...</div>'
        tree_html += '<div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">'
        for result in merged_results:
            # Safety check
            if isinstance(result, int):
                result = [result]
            else:
                result = [int(x) for x in list(result)]
            tree_html += '<div style="display:flex; gap:3px;">'
            for num in result:
                tree_html += f'<div style="width:36px; height:36px; border-radius:8px; background:#00c853; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:white;">{num}</div>'
            tree_html += '</div>'
        tree_html += '</div>'

    st.markdown("""
        <p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>SPLIT TREE</p>
        <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:16px; min-height:100px;">
    """ + tree_html + """</div>""", unsafe_allow_html=True)


# ================================================================
# MERGE SORT: Home page
# ================================================================
def render_merge_home():
    show_gradient_background()

    if st.button("⬅ Back", type="secondary"):
        go_to_page("home")

    st.markdown("<h1 style='text-align:center; color:white;'>Merge Sort Challenge</h1>", unsafe_allow_html=True)
    st.markdown("<div style='width:60px; height:3px; background:rgba(255,255,255,0.5); border-radius:2px; margin:0 auto 20px;'></div>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>HOW TO PLAY</p>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">1</p>
                <p style="color:white; font-size:14px;">Split the list into halves</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">2</p>
                <p style="color:white; font-size:14px;">Split until single elements</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">3</p>
                <p style="color:white; font-size:14px;">Compare and pick smallest</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div style="background:rgba(255,255,255,0.12); border-radius:14px; padding:16px; text-align:center;">
                <p style="color:#ffd000; font-size:22px; font-weight:bold;">4</p>
                <p style="color:white; font-size:14px;">Merge back in sorted order</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:16px; margin-bottom:24px;">
            <p style="color:#ffd000; font-size:16px; font-weight:bold; margin:0 0 10px;">📋 Level Progression</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🎓 <strong>Levels 1-2</strong> — Tutorial: Full guidance, split tree, code highlights, no pressure</p>
            <p style="color:white; font-size:14px; margin:6px 0;">⚔️ <strong>Levels 3-5</strong> — Semi-Challenge: Split tree shown, timer and hearts added</p>
            <p style="color:white; font-size:14px; margin:6px 0;">🔥 <strong>Levels 6-10</strong> — Full Challenge: No split tree, timer and hearts, you are on your own!</p>
            <p style="color:rgba(255,255,255,0.6); font-size:13px; margin:10px 0 0;">❤️ Wrong merge = lose a heart + 10 second penalty. Lose all hearts = level restart!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:white; letter-spacing:3px;'>SELECT YOUR LEVEL</p>", unsafe_allow_html=True)

    # Row 1: levels 1-5
    cols = st.columns(5)
    for level in range(1, 6):
        unlocked = level in st.session_state.merge_unlocked
        completed = level in st.session_state.merge_completed
        mode = get_level_mode(level)

        if completed:
            btn_color = "#00c853"
        elif mode == "tutorial":
            btn_color = "#7850ff"
        elif mode == "semi":
            btn_color = "#ff9800"
        else:
            btn_color = "#ff2020"

        label = f"Lv {level}"
        if completed:
            label = f"✅ {label}"

        with cols[level - 1]:
            if unlocked:
                st.markdown(f'<div style="background:{btn_color}; border-radius:10px; padding:10px 6px; text-align:center; color:white; font-size:12px; font-weight:700; margin-bottom:6px;">{label}</div>', unsafe_allow_html=True)
                if st.button(get_level_badge(level), key=f"ml_{level}", use_container_width=True):
                    st.session_state.merge_level = level
                    reset_merge_level(level)
                    go_to_page("merge_game")
            else:
                st.markdown(f'<div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:10px 6px; text-align:center; color:rgba(255,255,255,0.3); font-size:12px; font-weight:700; margin-bottom:6px;">🔒 Lv {level}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: levels 6-10
    cols2 = st.columns(5)
    for level in range(6, 11):
        unlocked = level in st.session_state.merge_unlocked
        completed = level in st.session_state.merge_completed

        label = f"Lv {level}"
        if completed:
            label = f"✅ {label}"

        with cols2[level - 6]:
            if unlocked:
                st.markdown(f'<div style="background:#ff2020; border-radius:10px; padding:10px 6px; text-align:center; color:white; font-size:12px; font-weight:700; margin-bottom:6px;">{label}</div>', unsafe_allow_html=True)
                if st.button("🔥 CHALLENGE", key=f"ml_{level}", use_container_width=True):
                    st.session_state.merge_level = level
                    reset_merge_level(level)
                    go_to_page("merge_game")
            else:
                st.markdown(f'<div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:10px 6px; text-align:center; color:rgba(255,255,255,0.3); font-size:12px; font-weight:700; margin-bottom:6px;">🔒 Lv {level}</div>', unsafe_allow_html=True)


# ================================================================
# MERGE SORT: Game page
# ================================================================
def render_merge_game():
    level = st.session_state.merge_level
    mode = get_level_mode(level)
    show_gradient_background()

    # Initialize if empty
    if not st.session_state.merge_numbers:
        reset_merge_level(level)

    # --- Top row ---
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅ Back", type="secondary"):
            go_to_page("merge")

    with col2:
        if mode in ["semi", "challenge"]:
            current_time = get_merge_time()
            st.markdown(f"""
                <div style="text-align:center; background:rgba(0,0,0,0.3); border-radius:12px; padding:8px; border:2px solid #ffd000;">
                    <span style="color:#ffd000; font-size:22px; font-weight:800;">⏱ {format_time(current_time)}</span>
                    <br><span style="color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px;">TIME</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align:center; background:rgba(120,80,255,0.2); border-radius:12px; padding:8px; border:2px solid #7850ff;">
                    <span style="color:#c084ff; font-size:14px; font-weight:800;">{get_level_badge(level)}</span>
                </div>
            """, unsafe_allow_html=True)

    with col3:
        if mode in ["semi", "challenge"]:
            hearts = "❤️" * st.session_state.merge_hearts
            st.markdown(f"<div style='text-align:center; font-size:20px; padding-top:8px;'>{hearts}</div>", unsafe_allow_html=True)

    # Title
    st.markdown(f"<h2 style='text-align:center; color:white;'>Merge Sort — Level {level}</h2>", unsafe_allow_html=True)

    # --- Game over ---
    if mode in ["semi", "challenge"] and st.session_state.merge_hearts <= 0:
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

    # ---- SPLIT PHASE ----
    if st.session_state.merge_phase == "split":

        split_levels = st.session_state.merge_split_levels
        split_idx = st.session_state.merge_split_idx

        # Show split tree for tutorial and semi
        if mode in ["tutorial", "semi"]:
            show_split_tree()
            st.markdown("<br>", unsafe_allow_html=True)

        if split_idx < len(split_levels) - 1:

            # Show numbers for challenge mode
            if mode == "challenge":
                st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>YOUR NUMBERS</p>", unsafe_allow_html=True)
                nums = st.session_state.merge_numbers
                cards_html = '<div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:16px;">'
                for num in nums:
                    cards_html += f'<div style="width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:white; background:#7850ff;">{num}</div>'
                cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)

            left_col, right_col = st.columns(2)

            with left_col:
                if mode == "tutorial":
                    st.markdown("""
                        <div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:12px; margin-bottom:12px;">
                            <p style="color:white; font-size:13px; margin:0;">👆 Press <strong>Split</strong> to divide the list in half. Keep splitting until every number is alone!</p>
                        </div>
                    """, unsafe_allow_html=True)

                if st.button("🔀 SPLIT", use_container_width=True):
                    if mode in ["semi", "challenge"]:
                        start_merge_timer()

                    st.session_state.merge_split_idx += 1
                    new_idx = st.session_state.merge_split_idx
                    groups = split_levels[new_idx]
                    all_single = all(len(list(g)) == 1 for g in groups)

                    if all_single:
                        st.session_state.merge_code_line = 1
                        st.session_state.merge_explain = "Every number is now alone — a single number is already sorted! Now we merge them back together in order."
                    else:
                        st.session_state.merge_code_line = 3
                        st.session_state.merge_explain = "Split! The list is divided in half. We keep splitting until every piece has just one number."
                    st.rerun()

            with right_col:
                if mode == "tutorial":
                    show_merge_code_panel()

        else:
            # All split — ready to merge
            st.session_state.merge_code_line = 8
            st.session_state.merge_explain = "All numbers are alone! Now we start merging. Pick the smallest number from each pair to build the sorted list."

            left_col, right_col = st.columns(2)

            with left_col:
                if mode == "tutorial":
                    st.markdown("""
                        <div style="background:rgba(0,200,83,0.15); border:1px solid #00c853; border-radius:10px; padding:12px; margin-bottom:12px;">
                            <p style="color:#00c853; font-size:13px; margin:0;">✅ All split! Now press <strong>Start Merging</strong> to put them back together in sorted order.</p>
                        </div>
                    """, unsafe_allow_html=True)

                if st.button("✅ Start Merging!", use_container_width=True):
                    st.session_state.merge_phase = "merge"
                    pairs = st.session_state.merge_pairs
                    if pairs:
                        first_pair = pairs[0]
                        left_list = sorted([int(x) for x in list(first_pair[0])])
                        right_list = sorted([int(x) for x in list(first_pair[1])])
                        st.session_state.merge_current_left = left_list
                        st.session_state.merge_current_right = right_list
                        st.session_state.merge_current_merged = []
                        st.session_state.merge_available = sorted(left_list + right_list)
                        st.session_state.merge_player_order = []
                        st.session_state.merge_code_line = 10
                        st.session_state.merge_explain = "Pick the smallest number from the left or right list to add to your merged result!"
                    st.rerun()

            with right_col:
                if mode == "tutorial":
                    show_merge_code_panel()

    # ---- MERGE PHASE ----
    elif st.session_state.merge_phase == "merge":

        pair_idx = st.session_state.merge_pair_idx
        pairs = st.session_state.merge_pairs
        merged_results = st.session_state.merge_merged_results

        if mode in ["tutorial", "semi"]:
            show_split_tree()
            st.markdown("<br>", unsafe_allow_html=True)

        # Check if all pairs merged = level complete
        if pair_idx >= len(pairs):
            total_time = format_time(get_merge_time())

            if level not in st.session_state.merge_completed:
                st.session_state.merge_completed.append(level)
            next_level = level + 1
            if next_level <= 10 and next_level not in st.session_state.merge_unlocked:
                st.session_state.merge_unlocked.append(next_level)

            if level == 10:
                st.markdown(f"""
                    <div style="background:rgba(255,208,0,0.2); border:2px solid #ffd000; border-radius:14px; padding:30px; text-align:center; margin:20px 0;">
                        <p style="color:#ffd000; font-size:36px; font-weight:800; margin:0;">🏆 MERGE SORT MASTER!</p>
                        <p style="color:white; font-size:16px; margin:8px 0 0;">You completed all 10 levels in {total_time}!</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background:rgba(0,200,83,0.2); border:2px solid #00c853; border-radius:14px; padding:24px; text-align:center; margin:20px 0;">
                        <p style="color:#00c853; font-size:28px; font-weight:800; margin:0;">🎉 Level {level} Complete!</p>
                        <p style="color:white; font-size:14px; margin:8px 0 0;">Time: {total_time} — Level {level + 1} unlocked!</p>
                    </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if level < 10:
                    if st.button(f"➡ Level {level + 1}", use_container_width=True):
                        st.session_state.merge_level = level + 1
                        reset_merge_level(level + 1)
                        st.rerun()
            with col2:
                if st.button("🏠 Back to Levels", use_container_width=True):
                    go_to_page("merge")
            return

        # Show current merge pair
        left = [int(x) for x in list(st.session_state.merge_current_left)]
        right = [int(x) for x in list(st.session_state.merge_current_right)]
        player_order = st.session_state.merge_player_order
        available = [int(x) for x in list(st.session_state.merge_available)]

        st.markdown(f"<p style='text-align:center; color:white; letter-spacing:3px; font-size:11px;'>MERGING PAIR {pair_idx + 1} OF {len(pairs)}</p>", unsafe_allow_html=True)

        left_col, right_col = st.columns(2)

        with left_col:
            # Left and right lists display
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
                st.markdown("""
                    <div style="background:rgba(255,255,255,0.08); border-radius:10px; padding:10px; margin-bottom:10px;">
                        <p style="color:white; font-size:12px; margin:0;">👆 Click <strong>Pick</strong> under the smallest number to add it to your sorted result!</p>
                    </div>
                """, unsafe_allow_html=True)

            # Available numbers
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
                                # Correct!
                                player_order.append(num)
                                available.remove(num)
                                st.session_state.merge_player_order = player_order
                                st.session_state.merge_available = available
                                st.session_state.merge_code_line = 11
                                st.session_state.merge_explain = str(num) + " is the smallest — added to the merged list! Keep going."

                                # Check if pair done
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
                                        st.session_state.merge_current_merged = []
                                        st.session_state.merge_available = sorted(next_left + next_right)
                                        st.session_state.merge_player_order = []
                                        st.session_state.merge_code_line = 10
                                        st.session_state.merge_explain = "Great! Now merge the next pair. Pick the smallest number again!"
                            else:
                                # Wrong pick
                                st.session_state.merge_code_line = 11
                                st.session_state.merge_explain = str(num) + " is not the smallest! Look carefully — pick the smallest number from both lists."
                                if mode in ["semi", "challenge"]:
                                    st.session_state.merge_hearts -= 1
                                    st.session_state.merge_penalty += 10
                                    st.session_state.merge_explain += " — ❌ -1 heart, +10 seconds!"
                            st.rerun()

            # Show merged result so far
            if player_order:
                st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:2px; margin-top:10px;'>YOUR MERGED RESULT:</p>", unsafe_allow_html=True)
                merged_html = '<div style="display:flex; flex-wrap:wrap; gap:4px;">'
                for num in player_order:
                    merged_html += f'<div style="width:40px; height:40px; border-radius:8px; background:#00c853; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; color:white;">{num}</div>'
                merged_html += '</div>'
                st.markdown(merged_html, unsafe_allow_html=True)

                if st.button("↩ Undo", use_container_width=True):
                    last = player_order.pop()
                    available.append(last)
                    available.sort()
                    st.session_state.merge_player_order = player_order
                    st.session_state.merge_available = available
                    st.rerun()

        with right_col:
            if mode in ["tutorial", "semi"]:
                show_merge_code_panel()
            else:
                st.markdown("""
                    <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:16px;">
                        <p style="color:#ffd000; font-size:13px; font-weight:bold; margin:0 0 8px;">🔥 Challenge Mode</p>
                        <p style="color:white; font-size:12px; margin:4px 0;">No hints — you know the algorithm!</p>
                        <p style="color:white; font-size:12px; margin:4px 0;">Pick the smallest number each time.</p>
                        <p style="color:rgba(255,255,255,0.5); font-size:11px; margin:10px 0 0;">Wrong pick = ❤️ lost + ⏱ +10s</p>
                    </div>
                """, unsafe_allow_html=True)


# ================================================================
# BUBBLE SORT: Main game
# ================================================================
def show_bubble_game(level):

    if "nums" not in st.session_state:
        st.session_state.nums = make_numbers(level)
        st.session_state.index = 0
        st.session_state.current_level = level
        st.session_state.code_line = 1
        st.session_state.explain = "Press Next to start comparing neighbours."

    if st.session_state.current_level != level:
        st.session_state.nums = make_numbers(level)
        st.session_state.index = 0
        st.session_state.current_level = level
        st.session_state.code_line = 1
        st.session_state.explain = "Press Next to start comparing neighbours."

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

    if level == "hard":
        if st.session_state.timer_set == False:
            st.markdown("""
            <div style="text-align:center; padding:30px 0 10px;">
                <p style="font-size:48px; margin:0;">⏱</p>
                <h2 style="color:#ffd000; font-size:32px; font-weight:800; margin:8px 0 4px;">Set Your Timer</h2>
                <p style="color:rgba(255,255,255,0.7); font-size:16px; margin:0 0 24px;">How many seconds do you want to sort in?</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                user_seconds = st.number_input(
                    "Seconds", min_value=10, max_value=600,
                    value=60, step=5, label_visibility="collapsed"
                )
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 Start Timer", use_container_width=True):
                    st.session_state.timer_limit = user_seconds
                    st.session_state.timer_start = time.time()
                    st.session_state.timer_set = True
                    st.session_state.game_over = None
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅ Back", type="secondary"):
                go_to_page("bubble")
            return

        time_limit = st.session_state.timer_limit
        time_passed = time.time() - st.session_state.timer_start
        time_left = time_limit - time_passed
        if time_left < 0:
            time_left = 0

        if st.session_state.game_over == None:
            if st.session_state.nums == sorted(st.session_state.nums):
                st.session_state.game_over = "win"

        if st.session_state.game_over == None:
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
                    st.session_state.code_line = 1
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
                <p style="color:white; font-size:22px; margin:0 0 8px;">
                    Completed in <span style="color:#ffd000; font-weight:700;">{time_taken} seconds</span>
                    out of <span style="color:#ffd000; font-weight:700;">{time_limit}</span>!
                </p>
                <p style="color:rgba(255,255,255,0.6); font-size:16px;">Hard mode conquered — well done!</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.nums = make_numbers(level)
                    st.session_state.index = 0
                    st.session_state.code_line = 1
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

    nums = st.session_state.nums
    i = st.session_state.index

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back", type="secondary"):
            go_to_page("bubble")
    with col2:
        if st.button("🔄 Generate Numbers"):
            st.session_state.nums = make_numbers(level)
            st.session_state.index = 0
            st.session_state.code_line = 1
            st.session_state.explain = "New numbers generated! Press Next to start."
            if level == "hard":
                st.session_state.timer_set = False
                st.session_state.timer_start = None
                st.session_state.timer_limit = None
                st.session_state.game_over = None
            st.rerun()

    st.markdown(f"<h2 style='text-align:center; color:white;'>Bubble Sort — {level.capitalize()} Level</h2>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>YOUR NUMBERS</p>", unsafe_allow_html=True)

        cards_html = '<div style="display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-bottom:16px;">'
        card_number = 0
        while card_number < len(nums):
            value = nums[card_number]
            if card_number == i or card_number == i + 1:
                card_style = "background:#ff2020; box-shadow:0 0 16px rgba(255,32,32,0.6); transform:scale(1.15);"
            else:
                card_style = "background:#7850ff;"
            cards_html = cards_html + '<div style="width:44px; height:44px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:white; ' + card_style + '">' + str(value) + '</div>'
            card_number = card_number + 1
        cards_html = cards_html + '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

        swap_col, next_col = st.columns(2)

        with swap_col:
            if st.button("🔀 SWAP"):
                if i < len(nums) - 1:
                    left_num = nums[i]
                    right_num = nums[i + 1]
                    if left_num > right_num:
                        nums[i] = right_num
                        nums[i + 1] = left_num
                        st.session_state.nums = nums
                        st.session_state.code_line = 5
                        st.session_state.explain = "Swapped " + str(nums[i + 1]) + " and " + str(nums[i]) + " because " + str(nums[i + 1]) + " was bigger!"
                    else:
                        st.session_state.code_line = 3
                        st.session_state.explain = "No swap needed — " + str(nums[i]) + " is already smaller than " + str(nums[i + 1]) + "."
                st.rerun()

        with next_col:
            if st.button("➡ Next"):
                if i < len(nums) - 2:
                    st.session_state.index = st.session_state.index + 1
                    next_left = nums[i + 1]
                    next_right = nums[i + 2]
                    st.session_state.code_line = 3
                    st.session_state.explain = "Comparing " + str(next_left) + " and " + str(next_right) + " — is the left number bigger than the right?"
                else:
                    st.session_state.index = 0
                    st.session_state.code_line = 1
                    st.session_state.explain = "Starting a new pass from the beginning!"
                st.rerun()

    with right_col:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:10px; letter-spacing:3px; text-align:center;'>THE CODE</p>", unsafe_allow_html=True)

        active_line = st.session_state.code_line

        all_lines = [
            "def bubble_sort(arr):",
            "&nbsp;&nbsp;for i in range(len(arr)):",
            "&nbsp;&nbsp;&nbsp;&nbsp;for j in range(len(arr)-i-1):",
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if arr[j] &gt; arr[j+1]:",
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# swap them",
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;arr[j], arr[j+1] = arr[j+1], arr[j]",
            "&nbsp;&nbsp;return arr"
        ]

        code_html = ""
        line_number = 0
        while line_number < len(all_lines):
            line_text = all_lines[line_number]
            if line_number == active_line:
                style = "background:rgba(255,208,0,0.2); color:#ffd000; font-weight:bold; border-radius:6px; padding:4px 8px; display:block;"
            else:
                style = "color:rgba(255,255,255,0.35); padding:4px 8px; display:block;"
            code_html = code_html + '<span style="' + style + '">' + line_text + '</span>'
            line_number = line_number + 1

        st.markdown('<div style="background:#1a1a2e; border-radius:14px; padding:16px; font-family:monospace; font-size:13px; line-height:2;">' + code_html + '</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:12px; background:rgba(255,208,0,0.85); border-left:3px solid #ffd000; border-radius:0 10px 10px 0; padding:10px 14px; color:black; font-size:13px; line-height:1.6;">💡 ' + st.session_state.explain + '</div>', unsafe_allow_html=True)

    if level == "hard":
        if st.session_state.game_over == None:
            time.sleep(1)
            st.rerun()


# ================================================================
# HOME PAGE
# ================================================================
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
            go_to_page("bubble")
    with col2:
        if st.button("MERGE SORT"):
            go_to_page("merge")


# ================================================================
# BUBBLE SORT PAGE (difficulty selection)
# ================================================================
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
        go_to_page("home")

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
            go_to_page("bubble_easy")
    with col2:
        if st.button("MEDIUM"):
            go_to_page("bubble_medium")
    with col3:
        if st.button("HARD"):
            go_to_page("bubble_hard")


# ================================================================
# BUBBLE SORT LEVELS
# ================================================================
elif st.session_state.page == "bubble_easy":
    show_bubble_game("easy")

elif st.session_state.page == "bubble_medium":
    show_bubble_game("medium")

elif st.session_state.page == "bubble_hard":
    show_bubble_game("hard")


# ================================================================
# MERGE SORT PAGES
# ================================================================
elif st.session_state.page == "merge":
    render_merge_home()

elif st.session_state.page == "merge_game":
    render_merge_game()

    




