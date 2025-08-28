import streamlit as st
import random

# =====================
# 🧠 Brain Battle – Full Quiz App
# Features:
# - 70-question bank, randomly plays 50 per game
# - Stars: +1 for correct, -1 for wrong
# - Ranks depend on stars (10 stars per rank): BEGINNER, AMATEUR, PRO, ADVANCED, PROFESSIONAL
# - Auto-advance to next question when you select an option
# - Shows Rank Room whenever your rank changes
# - Simple Sign Up / Login / Logout using session state
# - Colorful UI: red page, blue account box, yellow stars box, emojis everywhere 😄
# =====================

st.set_page_config(page_title="Brain Battle", page_icon="🧠", layout="centered")

# ---------- Constants ----------
TOTAL_PER_GAME = 50  # how many questions to play per game
RANKS = ["BEGINNER 🐣", "AMATEUR 🎯", "PRO 💪", "ADVANCED 🚀", "PROFESSIONAL 👑"]

# ---------- Styling ----------
st.markdown(
    """
    <style>
    /* Overall page background */
    .stApp { background: #b30000; } /* deep red */

    /* Pretty cards */
    .bb-card { background: rgba(255,255,255,0.9); padding: 1rem 1.25rem; border-radius: 16px; }

    /* Account box (blue) */
    .account-box { background: #0d47a1; color: white; padding: 10px 14px; border-radius: 14px; font-weight: 600; }

    /* Stars box (yellow) */
    .stars-box { background: #ffeb3b; color: #333; padding: 10px 14px; border-radius: 14px; font-weight: 700; }

    /* Buttons */
    div.stButton > button { border-radius: 12px; font-weight: 700; }

    /* Question text */
    .bb-question { font-size: 1.1rem; font-weight: 700; }

    /* Rank Room banner */
    .rank-room { background: linear-gradient(135deg, #fff, #ffe082); padding: 16px; border-radius: 16px; border: 3px dashed #f57f17; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Utilities ----------
def score_to_rank(stars: int):
    """Return (rank_index 0..4, rank_name, stars_within_this_rank 0..10)."""
    if stars < 10:
        return 0, RANKS[0], stars
    elif stars < 20:
        return 1, RANKS[1], stars - 10
    elif stars < 30:
        return 2, RANKS[2], stars - 20
    elif stars < 40:
        return 3, RANKS[3], stars - 30
    else:
        return 4, RANKS[4], min(stars - 40, 10)


def stars_bar(filled: int, total: int = 10):
    return "⭐" * max(0, filled) + "☆" * max(0, total - filled)


# ---------- Question Bank (70) ----------
def load_bank():
    raw = """
Capital of France?|Berlin|Madrid|Paris|Rome|London|C
Which planet is known as the Red Planet?|Earth|Mars|Venus|Jupiter|Saturn|B
5 + 7 = ?|10|11|12|13|14|C
Who wrote 'Hamlet'?|Charles Dickens|J.K. Rowling|William Shakespeare|Mark Twain|Jane Austen|C
Which gas do humans need to breathe?|Nitrogen|Carbon Dioxide|Oxygen|Hydrogen|Helium|C
What is the largest mammal?|Elephant|Blue Whale|Giraffe|Shark|Hippopotamus|B
Which continent is Egypt located in?|Asia|Africa|Europe|South America|Australia|B
How many continents are there on Earth?|5|6|7|8|9|C
What is the boiling point of water at sea level?|50°C|75°C|90°C|100°C|120°C|D
Which is the fastest land animal?|Lion|Horse|Cheetah|Tiger|Leopard|C
Which country is called the Land of the Rising Sun?|China|Japan|Korea|Thailand|India|B
Who painted the Mona Lisa?|Michelangelo|Leonardo da Vinci|Picasso|Van Gogh|Rembrandt|B
What is H2O commonly known as?|Salt|Water|Sugar|Oxygen|Hydrogen|B
Which is the smallest prime number?|0|1|2|3|5|C
Which organ pumps blood in the human body?|Brain|Lungs|Heart|Kidney|Stomach|C
How many players are on a football (soccer) team on the field?|9|10|11|12|13|C
Which country currently has the largest population?|USA|India|China|Russia|Brazil|B
Which is the longest river in the world?|Nile|Amazon|Yangtze|Mississippi|Congo|A
Which is the hottest planet in the solar system?|Mercury|Venus|Mars|Jupiter|Saturn|B
Which blood type is known as the universal donor?|A|B|AB|O negative|O positive|D
Which ocean is the largest?|Atlantic|Indian|Pacific|Arctic|Southern|C
What is the freezing point of water (°C)?|−10°C|0°C|10°C|32°C|50°C|B
What is the currency of Japan?|Dollar|Yen|Peso|Yuan|Rupee|B
What is the tallest mountain above sea level?|K2|Mount Everest|Kilimanjaro|Mont Blanc|Denali|B
Which metal is liquid at room temperature?|Iron|Mercury|Silver|Copper|Gold|B
Which planet has the most moons (as of recent counts)?|Earth|Jupiter|Saturn|Mars|Uranus|C
What is the largest desert in the world?|Sahara|Gobi|Arctic|Kalahari|Antarctic|E
How many bones are in the adult human body?|200|206|210|215|220|B
Which language is spoken in Brazil?|Spanish|English|French|Portuguese|Italian|D
What is the hardest natural substance?|Iron|Diamond|Gold|Silver|Quartz|B
What is the national sport of Japan?|Judo|Karate|Sumo Wrestling|Baseball|Kendo|C
Which is the smallest country in the world?|Monaco|Vatican City|Malta|Liechtenstein|San Marino|B
Who is credited with discovering gravity (apple legend)?|Newton|Einstein|Galileo|Archimedes|Tesla|A
Which instrument has keys, pedals and strings?|Guitar|Piano|Violin|Flute|Harp|B
Which animal is known as the King of the Jungle?|Tiger|Elephant|Lion|Leopard|Gorilla|C
What is the capital of Nigeria?|Lagos|Abuja|Port Harcourt|Kano|Ibadan|B
Which gas is used in party balloons?|Hydrogen|Helium|Oxygen|Carbon Dioxide|Nitrogen|B
Which is the largest planet in the solar system?|Earth|Mars|Jupiter|Saturn|Uranus|C
Which animal lays the largest eggs?|Hen|Ostrich|Eagle|Penguin|Crocodile|B
Who invented the telephone?|Alexander Graham Bell|Thomas Edison|Nikola Tesla|Isaac Newton|James Watt|A
What is the chemical symbol for gold?|Ag|Au|Gd|Go|Pt|B
What is 9 × 9?|72|81|88|91|99|B
What are the primary colors of light?|Red, Green, Blue|Red, Yellow, Blue|Cyan, Magenta, Yellow|Red, Green, Yellow|Blue, Yellow, Black|A
Which is the largest continent?|Africa|Asia|North America|Europe|Antarctica|B
How many days are in a leap year?|364|365|366|367|368|C
Who was the first human in space?|Neil Armstrong|Buzz Aldrin|Yuri Gagarin|Alan Shepard|John Glenn|C
What is the longest bone in the human body?|Tibia|Femur|Humerus|Fibula|Radius|B
Who developed the theory of relativity?|Isaac Newton|Albert Einstein|Galileo Galilei|Niels Bohr|James Clerk Maxwell|B
What is the square root of 144?|10|11|12|13|14|C
What is the capital of Italy?|Milan|Venice|Rome|Naples|Turin|C
Which is the tallest living animal?|Elephant|Giraffe|Rhino|Horse|Polar bear|B
Which is the fastest bird in a dive?|Golden eagle|Bald eagle|Peregrine falcon|Albatross|Sparrow|C
What is the largest organ of the human body?|Liver|Skin|Lungs|Brain|Intestines|B
Which gas do plants absorb for photosynthesis?|Oxygen|Nitrogen|Carbon Dioxide|Hydrogen|Methane|C
Which instrument measures temperature?|Barometer|Thermometer|Hygrometer|Anemometer|Altimeter|B
What is the largest island in the world?|Borneo|New Guinea|Greenland|Madagascar|Honshu|C
What is the currency of the United Kingdom?|Euro|Dollar|Pound Sterling|Yen|Franc|C
Which planet is famous for its prominent rings?|Mercury|Earth|Mars|Jupiter|Saturn|E
Who painted 'The Starry Night'?|Pablo Picasso|Michelangelo|Leonardo da Vinci|Vincent van Gogh|Claude Monet|D
Photosynthesis is the process by which plants…?|breathe in oxygen|make food using sunlight|grow roots|sleep at night|absorb minerals only|B
1 kilometer equals how many meters?|10|100|500|1000|1500|D
Which vitamin is produced by the body in sunlight?|Vitamin A|Vitamin B12|Vitamin C|Vitamin D|Vitamin E|D
What is the deepest ocean trench?|Puerto Rico Trench|Java Trench|Mariana Trench|Tonga Trench|Kermadec Trench|C
Change of water from liquid to gas is called?|Condensation|Evaporation|Sublimation|Precipitation|Transpiration|B
What is the binary representation of decimal 2?|00|01|10|11|100|C
What is the currency of Nigeria?|Dollar|Cedi|Rand|Naira|Shilling|D
What is the capital of Kenya?|Mombasa|Nairobi|Kisumu|Nakuru|Eldoret|B
Largest freshwater lake by surface area?|Lake Baikal|Lake Victoria|Lake Superior|Lake Michigan|Lake Tanganyika|C
Which planet is closest to the Sun?|Mercury|Venus|Earth|Mars|Neptune|A
The Great Pyramid of Giza is located in?|Mexico|Peru|Egypt|Iraq|Greece|C
    """
    bank = []
    for line in raw.strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 7:
            continue
        q, A, B, Cc, D, E, ans = parts
        bank.append({
            "question": q,
            "options": {"A": A, "B": B, "C": Cc, "D": D, "E": E},
            "answer": ans.upper(),
        })
    return bank

BANK = load_bank()  # 70 questions

# ---------- Session State ----------
if "users" not in st.session_state:
    st.session_state.users = {}  # {username: password} – demo only (not persistent)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "stars" not in st.session_state:
    st.session_state.stars = 0
if "mode" not in st.session_state:
    st.session_state.mode = "quiz"  # or "rank_room" or "finished"
if "current_rank_idx" not in st.session_state:
    st.session_state.current_rank_idx = 0
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None  # (is_correct: bool, text: str)


def start_game():
    st.session_state.quiz = random.sample(BANK, k=min(TOTAL_PER_GAME, len(BANK)))
    st.session_state.q_index = 0
    st.session_state.stars = 0
    st.session_state.mode = "quiz"
    st.session_state.current_rank_idx = 0
    st.session_state.last_feedback = None


# ---------- Auth ----------
def signup_view():
    st.subheader("🔵 Create Account")
    u = st.text_input("Username", key="su_u")
    p = st.text_input("Password", type="password", key="su_p")
    if st.button("Sign Up ✨"):
        if not u or not p:
            st.error("Please fill both fields.")
        elif u in st.session_state.users:
            st.error("❌ Username already exists!")
        else:
            st.session_state.users[u] = p
            st.success("✅ Account created! Please log in.")


def login_view():
    st.subheader("🔵 Login")
    u = st.text_input("Username", key="li_u")
    p = st.text_input("Password", type="password", key="li_p")
    if st.button("Login 🚪"):
        if u in st.session_state.users and st.session_state.users[u] == p:
            st.session_state.logged_in = True
            st.session_state.username = u
            start_game()
            st.success(f"✅ Welcome {u}! Let’s battle brains! 🧠🔥")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")


def logout_button():
    if st.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("✅ Logged out successfully!")
        st.rerun()


# ---------- Answer handling ----------
def handle_answer(chosen_letter: str):
    # compute rank before scoring
    before_idx, _, _ = score_to_rank(st.session_state.stars)

    q = st.session_state.quiz[st.session_state.q_index]
    correct_letter = q["answer"]
    correct_text = q["options"][correct_letter]

    if chosen_letter == correct_letter:
        st.session_state.stars += 1
        st.toast("✅ Correct! +1 ⭐", icon="✅")
        feedback = (True, f"Correct! +1 ⭐")
    else:
        st.session_state.stars = max(0, st.session_state.stars - 1)
        st.toast(f"❌ Wrong! Correct: {correct_letter}. {correct_text}  (-1 ⭐)", icon="❌")
        feedback = (False, f"Wrong. Correct was {correct_letter}. {correct_text}")

    # rank change detection
    after_idx, _, _ = score_to_rank(st.session_state.stars)

    st.session_state.last_feedback = feedback

    if after_idx != before_idx:
        st.session_state.current_rank_idx = after_idx
        st.session_state.mode = "rank_room"
    else:
        # move to next question immediately
        st.session_state.q_index += 1
        if st.session_state.q_index >= len(st.session_state.quiz):
            st.session_state.mode = "finished"

    st.rerun()


# ---------- Unauthenticated views ----------
if not st.session_state.logged_in:
    st.title("🧠 Brain Battle")
    st.markdown(
        "<div class='bb-card'>🎉 Welcome to <b>Brain Battle</b>!\n<br>Answer questions, earn ⭐, and climb ranks: BEGINNER → AMATEUR → PRO → ADVANCED → PROFESSIONAL.</div>",
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
    with tab_login:
        login_view()
    with tab_signup:
        signup_view()
    st.stop()

# ---------- Authenticated UI ----------
st.title("🧠 Brain Battle")

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown(f"<div class='account-box'>👤 Logged in as <b>{st.session_state.username}</b></div>", unsafe_allow_html=True)
with col2:
    logout_button()

# Stars + Rank panel (yellow)
rank_idx, rank_name, stars_in_rank = score_to_rank(st.session_state.stars)
st.markdown(
    f"<div class='stars-box'>⭐ Stars: <b>{st.session_state.stars}</b> &nbsp; | &nbsp; 🏆 Rank: <b>{rank_name}</b><br>{stars_bar(stars_in_rank)} </div>",
    unsafe_allow_html=True,
)

st.caption(f"Progress: {st.session_state.q_index}/{TOTAL_PER_GAME} questions")
st.progress(st.session_state.q_index / TOTAL_PER_GAME if TOTAL_PER_GAME else 0)

st.markdown("---")

# ---------- Mode router ----------
if st.session_state.mode == "rank_room":
    # Show a celebratory rank room
    st.markdown(
        f"<div class='rank-room'>🎊 <b>Rank Up!</b><br>You are now: <b>{RANKS[st.session_state.current_rank_idx]}</b><br>Keep going to earn more stars!</div>",
        unsafe_allow_html=True,
    )
    st.balloons()
    if st.button("Continue ➡️"):
        # After rank room, continue quiz without skipping a question
        st.session_state.mode = "quiz"
        st.rerun()

elif st.session_state.mode == "finished":
    st.subheader("🎉 Quiz Completed!")
    st.write(f"Final Stars: {st.session_state.stars} ⭐")
    st.write(f"Final Rank: {rank_name}")
    st.balloons()
    colA, colB = st.columns(2)
    with colA:
        if st.button("🔁 Play Again"):
            start_game()
            st.rerun()
    with colB:
        if st.button("🏠 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

else:
    # Quiz Mode
    # Initialize game if needed
    if not st.session_state.quiz:
        start_game()

    if st.session_state.q_index < len(st.session_state.quiz):
        q = st.session_state.quiz[st.session_state.q_index]
        st.markdown(f"<div class='bb-card bb-question'>❓ Q{st.session_state.q_index + 1}: {q['question']}</div>", unsafe_allow_html=True)

        # Render options as buttons A–E for instant submit
        letters = ["A", "B", "C", "D", "E"]
        opts = [f"{lt}. {q['options'][lt]}" for lt in letters]

        # Show as 5 buttons in two rows
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button(opts[0]):
                handle_answer("A")
        with c2:
            if st.button(opts[1]):
                handle_answer("B")
        with c3:
            if st.button(opts[2]):
                handle_answer("C")
        c4, c5, _ = st.columns(3)
        with c4:
            if st.button(opts[3]):
                handle_answer("D")
        with c5:
            if st.button(opts[4]):
                handle_answer("E")

        # Show last feedback if any (from previous question)
        if st.session_state.last_feedback is not None:
            ok, msg = st.session_state.last_feedback
            if ok:
                st.success(f"{msg}")
            else:
                st.error(f"{msg}")
            # Clear so it doesn't repeat forever
            st.session_state.last_feedback = None
    else:
        # safety: if index passes limit
        st.session_state.mode = "finished"
        st.rerun()
