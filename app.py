import streamlit as st
from supabase import create_client
from datetime import date

# ==========================================
# 1. ตั้งค่าหน้าเว็บ
# ==========================================

st.set_page_config(
    page_title="Kawaii Life Planner",
    page_icon="🌷",
    layout="centered"
)


# ==========================================
# KAWAII PASTEL POP THEME 🍓
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Mali:wght@400;500;600;700&display=swap');

:root {
    --raspberry: #F26190;
    --lilac: #E7BEF8;
    --blueberry: #93ABD9;
    --lemon: #EDE986;
    --background: #FFF8FB;
    --text: #665264;
}

/* ฟอนต์ */
html, body, [class*="css"] {
    font-family: 'Mali', sans-serif;
}

/* พื้นหลัง */
.stApp {
    background: linear-gradient(
        135deg,
        #FFF8FB 0%,
        #FBF3FF 55%,
        #F1F6FF 100%
    );
}

/* หัวข้อ */
h1, h2, h3 {
    color: var(--raspberry) !important;
    font-weight: 700 !important;
}

/* ข้อความ */
p, label, .stMarkdown {
    color: var(--text);
}


/* KAWAII PASTEL BUTTONS 🍓 */

.stButton > button {
    background: linear-gradient(
        135deg,
        #F26190,
        #E7BEF8
    );
    color: white;
    border: 2px solid #F26190;
    border-radius: 20px;
    padding: 10px 22px;
    font-family: 'Mali', sans-serif;
    font-weight: 700;
    transition: all 0.25s ease;
    box-shadow: 0 4px 10px rgba(242, 97, 144, 0.18);
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #E7BEF8,
        #93ABD9
    );
    color: white;
    border: 2px solid #93ABD9;
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(147, 171, 217, 0.25);
}

.stButton > button:active {
    transform: scale(0.97);
}


/* ช่องกรอกข้อมูล */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: white;
    border: 1px solid var(--lilac);
    border-radius: 12px;
    color: var(--text);
}


/* KAWAII PASTEL CARDS 🍓 */

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #FFFFFF, #FFF0F5);
    border: 2px solid #F26190;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(242, 97, 144, 0.12);
}

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 2px solid #E7BEF8;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 4px 12px rgba(180, 140, 210, 0.12);
}

div[data-testid="stAlert"] {
    border-radius: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #80658F;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #F26190;
    font-weight: 700;
}


/* แถบเมนู */
.stTabs [data-baseweb="tab"] {
    color: #80658F;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: var(--raspberry) !important;
}

/* ช่องเลือกข้อมูล */
div[data-baseweb="select"] > div {
    border-radius: 12px;
    border-color: var(--lilac);
}

/* เส้นแบ่ง */
hr {
    border-color: #E7BEF8;
}


/* KAWAII SIDEBAR 🌷 */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #F8ECFF 0%,
        #F0F4FF 100%
    );
    border-right: 2px solid #E7BEF8;
}

/* เมนู Sidebar */
section[data-testid="stSidebar"] label {
    color: #80658F;
    font-weight: 600;
}

/* เมนูที่เลือก */
section[data-testid="stSidebar"] [aria-checked="true"] {
    background-color: #E7BEF8;
    border-radius: 12px;
}

/* เส้นแบ่ง Sidebar */
section[data-testid="stSidebar"] hr {
    border-color: #93ABD9;
}
/* ตัวเลขสถิติ */
div[data-testid="stMetricValue"] {
    color: var(--raspberry);
}

/* Checkbox */
.stCheckbox label {
    color: var(--text);
}

</style>
""", unsafe_allow_html=True)


st.title("🌷 Kawaii Life Planner")
st.write("Your little steps to a happier life!")

# ==========================================
# 2. เชื่อมต่อ Supabase
# ==========================================

if "supabase_client" not in st.session_state:
    st.session_state.supabase_client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = st.session_state.supabase_client

# ==========================================
# 3. ค่าเริ่มต้น
# ==========================================

if "user" not in st.session_state:
    st.session_state.user = None

if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "refresh_token" not in st.session_state:
    st.session_state.refresh_token = None

CATEGORIES = [
    "การเรียน",
    "การทำงาน",
    "สุขภาพ",
    "งานอดิเรก",
    "การพักผ่อน",
    "การเงิน",
    "อื่น ๆ"
]

HABIT_CATEGORIES = [
    "สุขภาพ",
    "การเรียนรู้",
    "การทำงาน",
    "การดูแลตัวเอง",
    "งานอดิเรก",
    "อื่น ๆ"
]


def parse_due_date(value):
    if not value:
        return None

    if isinstance(value, date):
        return value

    try:
        return date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None

def calculate_streaks(log_dates, today):
    """
    คำนวณจำนวนวันที่ทำต่อเนื่องในปัจจุบัน
    และจำนวนวันที่ทำต่อเนื่องสูงสุด
    """

    dates = {
        date.fromisoformat(str(d)[:10])
        for d in log_dates
        if date.fromisoformat(str(d)[:10]) <= today
    }

    if not dates:
        return 0, 0

    # Current Streak
    if today in dates:
        current_day = today
    elif date.fromordinal(today.toordinal() - 1) in dates:
        current_day = date.fromordinal(today.toordinal() - 1)
    else:
        current_day = None

    current_streak = 0

    if current_day:
        while current_day in dates:
            current_streak += 1
            current_day = date.fromordinal(
                current_day.toordinal() - 1
            )

    # Best Streak
    sorted_dates = sorted(dates)

    best_streak = 0
    running_streak = 0
    previous_day = None

    for log_day in sorted_dates:
        if (
            previous_day is not None
            and (log_day - previous_day).days == 1
        ):
            running_streak += 1
        else:
            running_streak = 1

        best_streak = max(best_streak, running_streak)
        previous_day = log_day

    return current_streak, best_streak


# ==========================================
# 4. เมื่อเข้าสู่ระบบแล้ว
# ==========================================

if st.session_state.user:

    try:
        verified_user = supabase.auth.get_user(
            st.session_state.access_token
        )

        if verified_user.user is None:
            st.session_state.user = None
            st.session_state.access_token = None
            st.session_state.refresh_token = None
            st.warning("Session หมดอายุ กรุณาเข้าสู่ระบบใหม่")
            st.stop()

        user_id = verified_user.user.id
        user_email = verified_user.user.email

    except Exception as e:
        st.error("ตรวจสอบ Session ไม่สำเร็จ")
        st.code(f"{type(e).__name__}: {e}")
        st.stop()

    st.success(f"ยินดีต้อนรับ 💖 {user_email}")

    # ======================================
    # 5. เมนูหลัก
    # ======================================

    page = st.radio(
    "เมนูหลัก",
    [
	"🏠 Dashboard",
	"📋 Daily Planner",
        "🌱 Habit Tracker",
        "🎯 My Goals",
        "📊 My Progress",
	"📖 My Journal"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

    st.divider()
    # ======================================
    # 5. DASHBOARD
    # ======================================

    if page == "🏠 Dashboard":

        st.header("🏠 My Dashboard")
        st.write("ภาพรวมความก้าวหน้าเล็ก ๆ ของคุณในวันนี้ 💗")

        st.divider()

        # งานทั้งหมด
        try:
            activities_result = (
                supabase.table("activities")
                .select("id,is_completed")
                .eq("user_id", user_id)
                .execute()
            )

            activities = activities_result.data or []

            total_tasks = len(activities)
            completed_tasks = sum(
                1 for task in activities
                if task["is_completed"]
            )
            pending_tasks = total_tasks - completed_tasks

        except Exception as e:
            st.error("โหลดข้อมูลงานไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")
            total_tasks = 0
            completed_tasks = 0
            pending_tasks = 0

        # นิสัย
        try:
            habits_result = (
                supabase.table("habits")
                .select("id")
                .eq("user_id", user_id)
                .eq("is_active", True)
                .execute()
            )

            habits = habits_result.data or []
            total_habits = len(habits)

            logs_result = (
                supabase.table("habit_logs")
                .select("id")
                .eq("user_id", user_id)
                .eq("log_date", date.today().isoformat())
                .execute()
            )

            completed_habits = len(logs_result.data or [])

        except Exception as e:
            st.error("โหลดข้อมูลนิสัยไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")
            total_habits = 0
            completed_habits = 0

        # แสดงสรุป
        col1, col2 = st.columns(2)

        with col1:
            st.metric("📋 งานทั้งหมด", total_tasks)
            st.metric("⏳ งานที่ยังไม่เสร็จ", pending_tasks)

        with col2:
            st.metric("✅ งานที่เสร็จแล้ว", completed_tasks)
            st.metric("🌱 นิสัยทั้งหมด", total_habits)

        st.divider()

        st.subheader("🌱 ความสำเร็จของวันนี้")

        habit_progress = (
            completed_habits / total_habits
            if total_habits > 0 else 0
        )

        st.write(
            f"ทำสำเร็จ {completed_habits} / {total_habits} นิสัย"
        )

        st.progress(habit_progress)

        st.divider()

        st.subheader("🎯 ภาพรวมเป้าหมาย")

        try:
            goals_result = (
                supabase.table("goals")
                .select("id,status,target_value,current_value")
                .eq("user_id", user_id)
                .execute()
            )

            dashboard_goals = goals_result.data or []

            total_goals = len(dashboard_goals)

            completed_goals = sum(
                1 for goal in dashboard_goals
                if goal["status"] == "completed"
            )

            active_goals = sum(
                1 for goal in dashboard_goals
                if goal["status"] == "active"
            )

            total_target = sum(
                float(goal["target_value"])
                for goal in dashboard_goals
            )

            total_current = sum(
                float(goal["current_value"])
                for goal in dashboard_goals
            )

            goal_progress = (
                min(total_current / total_target, 1.0)
                if total_target > 0 else 0
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🎯 เป้าหมายทั้งหมด", total_goals)

            with col2:
                st.metric("🌱 กำลังทำ", active_goals)

            with col3:
                st.metric("🏆 สำเร็จแล้ว", completed_goals)

            st.write(
                f"ความคืบหน้ารวม {goal_progress * 100:.1f}%"
            )

            st.progress(goal_progress)

        except Exception as e:
            st.error("โหลดข้อมูลเป้าหมายไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")

        st.divider()

        st.subheader("📖 บันทึกและอารมณ์ล่าสุด")

        try:
            latest_journal_result = (
                supabase.table("journals")
                .select("entry_date,mood,title")
                .eq("user_id", user_id)
                .order("entry_date", desc=True)
                .limit(1)
                .execute()
            )

            latest_journals = latest_journal_result.data or []

            if latest_journals:
                latest_journal = latest_journals[0]

                parsed_journal_date = parse_due_date(
                    latest_journal["entry_date"]
                )

                st.success(
                    f"อารมณ์ล่าสุด: {latest_journal['mood']}"
                )

                st.write(
                    f"📝 {latest_journal['title']}"
                )

                st.caption(
                    f"บันทึกล่าสุดวันที่ "
                    f"{parsed_journal_date.strftime('%d/%m/%Y')}"
                )

            else:
                st.info("ยังไม่มีบันทึกประจำวัน 🌷")

        except Exception as e:
            st.error("โหลดบันทึกล่าสุดไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")


        if total_habits > 0 and completed_habits == total_habits:
            st.success("เก่งมาก! วันนี้ทำครบทุกนิสัยแล้ว 🎉")
        elif total_habits > 0:
            st.info("ค่อย ๆ ทำไปทีละนิดนะ คุณทำได้ 💗")
        else:
            st.caption("ยังไม่มีนิสัยที่กำลังติดตาม")

    # ======================================
    # 6. DAILY PLANNER
    # ======================================

    if page == "📋 Daily Planner":

        st.header("📝 เพิ่มงานใหม่")

        with st.form("add_task_form"):

            new_title = st.text_input(
                "ชื่องาน",
                placeholder="เช่น อ่านหนังสือ 30 นาที"
            )

            new_category = st.selectbox(
                "หมวดหมู่",
                CATEGORIES
            )

            new_weight = st.slider(
                "ระดับความสำคัญ",
                1, 10, 5
            )

            has_due_date = st.checkbox(
                "กำหนดวันครบกำหนด"
            )

            new_due_date = st.date_input(
                "วันครบกำหนด",
                value=date.today()
            )

            add_submitted = st.form_submit_button(
                "เพิ่มงาน 💗"
            )

        if add_submitted:

            if not new_title.strip():
                st.warning("กรุณากรอกชื่องานก่อนบันทึก")

            else:
                try:
                    supabase.table("activities").insert({
                        "user_id": user_id,
                        "category": new_category,
                        "title": new_title.strip(),
                        "weight": new_weight,
                        "due_date": (
                            new_due_date.isoformat()
                            if has_due_date else None
                        ),
                        "is_completed": False
                    }).execute()

                    st.success("เพิ่มงานสำเร็จแล้ว! 🌷")
                    st.rerun()

                except Exception as e:
                    st.error("เพิ่มงานไม่สำเร็จ")
                    st.code(f"{type(e).__name__}: {e}")

        st.divider()
        st.header("📋 งานของฉัน")

        try:
            result = (
                supabase.table("activities")
                .select(
                    "id, category, title, weight, due_date, "
                    "is_completed, created_at"
                )
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )

            tasks = result.data or []

        except Exception as e:
            st.error("ไม่สามารถโหลดรายการงานได้")
            st.code(f"{type(e).__name__}: {e}")
            tasks = []

        completed_tasks = [
            task for task in tasks
            if task["is_completed"]
        ]

        pending_tasks = [
            task for task in tasks
            if not task["is_completed"]
        ]

        total = len(tasks)
        completed_count = len(completed_tasks)

        progress = (
            completed_count / total
            if total > 0 else 0
        )

        col1, col2 = st.columns(2)

        col1.metric("งานทั้งหมด", total)
        col2.metric("ทำสำเร็จแล้ว", completed_count)

        st.progress(progress)
        st.caption(f"ความสำเร็จ {progress * 100:.0f}%")

        tab_pending, tab_completed = st.tabs([
            f"🌱 ยังไม่เสร็จ ({len(pending_tasks)})",
            f"✅ เสร็จแล้ว ({len(completed_tasks)})"
        ])

        # งานที่ยังไม่เสร็จ
        with tab_pending:

            if not pending_tasks:
                st.info("ไม่มีงานค้างแล้ว เก่งมาก! 🎉")

            for task in pending_tasks:

                task_id = task["id"]
                task_due_date = parse_due_date(
                    task.get("due_date")
                )

                with st.expander(f"🌷 {task['title']}"):

                    st.caption(
                        f"หมวดหมู่: {task['category']} "
                        f"| ความสำคัญ: {task['weight']}/10"
                    )

                    if task_due_date:
                        st.caption(
                            "📅 ครบกำหนด: "
                            f"{task_due_date.strftime('%d/%m/%Y')}"
                        )
                    else:
                        st.caption("📅 ยังไม่ได้กำหนดวันครบกำหนด")

                    with st.form(f"edit_task_{task_id}"):

                        edit_title = st.text_input(
                            "แก้ไขชื่องาน",
                            value=task["title"],
                            key=f"title_{task_id}"
                        )

                        edit_categories = list(CATEGORIES)

                        if task["category"] not in edit_categories:
                            edit_categories.append(task["category"])

                        edit_category = st.selectbox(
                            "หมวดหมู่",
                            edit_categories,
                            index=edit_categories.index(task["category"]),
                            key=f"category_{task_id}"
                        )

                        edit_weight = st.slider(
                            "ระดับความสำคัญ",
                            1, 10,
                            int(task["weight"]),
                            key=f"weight_{task_id}"
                        )

                        edit_has_due_date = st.checkbox(
                            "กำหนดวันครบกำหนด",
                            value=task_due_date is not None,
                            key=f"has_date_{task_id}"
                        )

                        edit_due_date = st.date_input(
                            "วันครบกำหนด",
                            value=task_due_date or date.today(),
                            key=f"date_{task_id}"
                        )

                        mark_completed = st.checkbox(
                            "ทำงานนี้เสร็จแล้ว ✅",
                            value=False,
                            key=f"complete_{task_id}"
                        )

                        save_submitted = st.form_submit_button(
                            "บันทึกการแก้ไข 💗"
                        )

                    if save_submitted:

                        if not edit_title.strip():
                            st.warning("กรุณากรอกชื่องาน")

                        else:
                            try:
                                supabase.table("activities").update({
                                    "title": edit_title.strip(),
                                    "category": edit_category,
                                    "weight": edit_weight,
                                    "due_date": (
                                        edit_due_date.isoformat()
                                        if edit_has_due_date else None
                                    ),
                                    "is_completed": mark_completed
                                }).eq(
                                    "id", task_id
                                ).eq(
                                    "user_id", user_id
                                ).execute()

                                st.success("บันทึกการแก้ไขสำเร็จ! 🌸")
                                st.rerun()

                            except Exception as e:
                                st.error("แก้ไขงานไม่สำเร็จ")
                                st.code(f"{type(e).__name__}: {e}")

                    if st.button(
                        "🗑️ ลบงานนี้",
                        key=f"delete_{task_id}"
                    ):

                        try:
                            supabase.table("activities").delete().eq(
                                "id", task_id
                            ).eq(
                                "user_id", user_id
                            ).execute()

                            st.success("ลบงานเรียบร้อยแล้ว")
                            st.rerun()

                        except Exception as e:
                            st.error("ลบงานไม่สำเร็จ")
                            st.code(f"{type(e).__name__}: {e}")

        # งานที่เสร็จแล้ว
        with tab_completed:

            if not completed_tasks:
                st.info(
                    "ยังไม่มีงานที่ทำเสร็จ "
                    "ลองเริ่มจากงานเล็ก ๆ กันนะ 💗"
                )

            for task in completed_tasks:

                task_id = task["id"]

                st.write(f"✅ ~~{task['title']}~~")

                st.caption(
                    f"หมวดหมู่: {task['category']} "
                    f"| ความสำคัญ: {task['weight']}/10"
                )

                if st.button(
                    "↩️ นำกลับไปเป็นงานที่ยังไม่เสร็จ",
                    key=f"undo_{task_id}"
                ):

                    try:
                        supabase.table("activities").update({
                            "is_completed": False
                        }).eq(
                            "id", task_id
                        ).eq(
                            "user_id", user_id
                        ).execute()

                        st.rerun()

                    except Exception as e:
                        st.error("เปลี่ยนสถานะไม่สำเร็จ")
                        st.code(f"{type(e).__name__}: {e}")

                st.divider()

    # ======================================
    # 7. HABIT TRACKER
    # ======================================

    elif page == "🌱 Habit Tracker":

        st.header("🌱 Habit Tracker")
        st.write("สร้างนิสัยเล็ก ๆ เพื่อชีวิตที่ดีขึ้น 💗")

        today = date.today()
        today_text = today.isoformat()

        # ----------------------------------
        # เพิ่มนิสัยใหม่
        # ----------------------------------

        st.subheader("✨ เพิ่มนิสัยใหม่")

        with st.form("add_habit_form"):

            habit_title = st.text_input(
                "ฉันอยากสร้างนิสัย...",
                placeholder="เช่น ดื่มน้ำ 8 แก้วต่อวัน"
            )

            habit_category = st.selectbox(
                "หมวดหมู่",
                HABIT_CATEGORIES
            )

            habit_submitted = st.form_submit_button(
                "เพิ่มนิสัย 🌷"
            )

        if habit_submitted:

            if not habit_title.strip():
                st.warning("กรุณากรอกชื่อนิสัยก่อนนะ")

            else:
                try:
                    supabase.table("habits").insert({
                        "user_id": user_id,
                        "title": habit_title.strip(),
                        "category": habit_category
                    }).execute()

                    st.success("เพิ่มนิสัยสำเร็จแล้ว! 💖")
                    st.rerun()

                except Exception as e:
                    st.error("เพิ่มนิสัยไม่สำเร็จ")
                    st.code(f"{type(e).__name__}: {e}")

        st.divider()

        # ----------------------------------
        # โหลดรายการนิสัย
        # ----------------------------------

        st.subheader("🌸 นิสัยของฉัน")

        try:
            habit_result = (
                supabase.table("habits")
                .select("id, title, category, is_active, created_at")
                .eq("user_id", user_id)
                .eq("is_active", True)
                .order("created_at", desc=True)
                .execute()
            )

            habits = habit_result.data or []

        except Exception as e:
            st.error("โหลดรายการนิสัยไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")
            habits = []

        if not habits:
            st.info(
                "ยังไม่มีนิสัยที่บันทึกไว้ "
                "ลองเพิ่มนิสัยแรกของคุณกันนะ 🌱"
            )

        else:

            # โหลดประวัติการทำทั้งหมดของผู้ใช้
            try:
                log_result = (
                    supabase.table("habit_logs")
                    .select("habit_id, log_date")
                    .eq("user_id", user_id)
                    .execute()
                )

                logs = log_result.data or []

            except Exception as e:
                st.error("โหลดประวัติ Habit ไม่สำเร็จ")
                st.code(f"{type(e).__name__}: {e}")
                logs = []

            logs_by_habit = {}

            for log in logs:
                habit_id = log["habit_id"]

                if habit_id not in logs_by_habit:
                    logs_by_habit[habit_id] = set()

                logs_by_habit[habit_id].add(
                    str(log["log_date"])[:10]
                )

            # สรุปภาพรวม
            total_habits = len(habits)

            completed_today = sum(
                1 for habit in habits
                if today_text in logs_by_habit.get(
                    habit["id"], set()
                )
            )

            col1, col2 = st.columns(2)

            col1.metric("นิสัยทั้งหมด", total_habits)
            col2.metric("ทำสำเร็จวันนี้", completed_today)

            daily_progress = (
                completed_today / total_habits
                if total_habits > 0 else 0
            )

            st.progress(daily_progress)

            st.caption(
                f"ความสำเร็จวันนี้ {daily_progress * 100:.0f}%"
            )

            st.divider()

            # แสดงนิสัยแต่ละรายการ
            for habit in habits:

                habit_id = habit["id"]
                habit_logs = logs_by_habit.get(
                    habit_id, set()
                )

                done_today = today_text in habit_logs
                
                total_days = len(habit_logs)

                current_streak, best_streak = calculate_streaks(
                    habit_logs,
                    today
                )

                with st.container(border=True):

                    st.subheader(f"🌷 {habit['title']}")

                    st.caption(
                        f"หมวดหมู่: {habit['category']}"
                    )

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "วันที่ทำสำเร็จ",
                        f"{total_days} วัน"
                    )

                    col2.metric(
                        "สถานะวันนี้",
                        "สำเร็จแล้ว 💚" if done_today else "ยังไม่ได้ทำ"
                    )

                    col3, col4 = st.columns(2)

                    col3.metric(
                        "🔥 Current Streak",
                        f"{current_streak} วัน"
                    )

                    col4.metric(
                        "🏆 Best Streak",
                        f"{best_streak} วัน"
                    )


                    if done_today:

                        st.success(
                            "วันนี้คุณทำสำเร็จแล้ว เก่งมาก! 🎉"
                        )

                        if st.button(
                            "↩️ ยกเลิกการบันทึกวันนี้",
                            key=f"undo_habit_{habit_id}"
                        ):

                            try:
                                supabase.table("habit_logs").delete().eq(
                                    "habit_id", habit_id
                                ).eq(
                                    "user_id", user_id
                                ).eq(
                                    "log_date", today_text
                                ).execute()

                                st.success("ยกเลิกการบันทึกแล้ว")
                                st.rerun()

                            except Exception as e:
                                st.error("ยกเลิกไม่สำเร็จ")
                                st.code(
                                    f"{type(e).__name__}: {e}"
                                )

                    else:

                        if st.button(
                            "✅ วันนี้ทำสำเร็จแล้ว!",
                            key=f"complete_habit_{habit_id}",
                            type="primary"
                        ):

                            try:
                                supabase.table("habit_logs").insert({
                                    "habit_id": habit_id,
                                    "user_id": user_id,
                                    "log_date": today_text
                                }).execute()

                                st.success("บันทึกความสำเร็จแล้ว! 🌸")
                                st.rerun()

                            except Exception as e:
                                st.error("บันทึกไม่สำเร็จ")
                                st.code(
                                    f"{type(e).__name__}: {e}"
                                )

                    # ประวัติย้อนหลัง
                    with st.expander("📅 ดูประวัติการทำ"):

                        sorted_dates = sorted(
                            habit_logs,
                            reverse=True
                        )

                        if sorted_dates:
                            for log_date in sorted_dates[:10]:
                                parsed_date = date.fromisoformat(log_date)

                                st.write(
                                    f"✅ {parsed_date.strftime('%d/%m/%Y')}"
                                )
                        else:
                            st.info("ยังไม่มีประวัติการทำ")

                    # ลบนิสัย
                    with st.expander("⚙️ จัดการนิสัย"):

                        st.warning(
                            "การลบนิสัยจะลบประวัติการทำของนิสัยนี้ด้วย"
                        )

                        if st.button(
                            "🗑️ ลบนิสัยนี้",
                            key=f"delete_habit_{habit_id}"
                        ):

                            try:
                                supabase.table("habits").delete().eq(
                                    "id", habit_id
                                ).eq(
                                    "user_id", user_id
                                ).execute()

                                st.success("ลบนิสัยเรียบร้อยแล้ว")
                                st.rerun()

                            except Exception as e:
                                st.error("ลบนิสัยไม่สำเร็จ")
                                st.code(
                                    f"{type(e).__name__}: {e}"
                                )

    # ======================================
    # 8. MY GOALS
    # ======================================

    if page == "🎯 My Goals":

        st.header("🎯 เป้าหมายของฉัน")
        st.write("Small steps, big dreams! 🌷")

        # เพิ่มเป้าหมายใหม่
        st.subheader("✨ สร้างเป้าหมายใหม่")

        with st.form("add_goal_form"):

            goal_title = st.text_input(
                "ชื่อเป้าหมาย",
                placeholder="เช่น อ่านหนังสือให้ครบ 5 เล่ม"
            )

            goal_description = st.text_area(
                "รายละเอียดเพิ่มเติม (ไม่บังคับ)",
                placeholder="เขียนรายละเอียดเป้าหมายของคุณ"
            )

            goal_category = st.selectbox(
                "หมวดหมู่",
                CATEGORIES
            )

            goal_target = st.number_input(
                "จำนวนเป้าหมายที่ต้องการ",
                min_value=1.0,
                value=5.0,
                step=1.0
            )

            goal_unit = st.text_input(
                "หน่วย",
                value="ครั้ง",
                placeholder="เช่น เล่ม, บาท, ครั้ง"
            )
            goal_deadline = st.date_input(
                "📅 วันครบกำหนด",
                value=None,
                min_value=date.today()
            )
            goal_submitted = st.form_submit_button(
                "💗 เพิ่มเป้าหมาย"
            )

        if goal_submitted:

            if not goal_title.strip():
                st.warning("กรุณากรอกชื่อเป้าหมายก่อนค่ะ")

            elif not goal_unit.strip():
                st.warning("กรุณากรอกหน่วยของเป้าหมาย")

            else:
                try:
                    supabase.table("goals").insert({
                        "user_id": user_id,
                        "title": goal_title.strip(),
                        "description": goal_description.strip(),
                        "category": goal_category,
                        "target_value": goal_target,
                        "current_value": 0,
                        "unit": goal_unit.strip(),
                        "target_date": (
                            goal_deadline.isoformat()
                            if goal_deadline else None
                        ),
                        "status": "active"
                    }).execute()

                    st.success("เพิ่มเป้าหมายสำเร็จแล้ว! 🎉")
                    st.rerun()

                except Exception as e:
                    st.error("เพิ่มเป้าหมายไม่สำเร็จ")
                    st.code(
                        f"{type(e).__name__}: {e}"
                    )

        st.divider()

        # แสดงเป้าหมาย
        st.subheader("🌸 เป้าหมายของฉัน")

        try:
            goal_result = (
                supabase.table("goals")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )

            goals = goal_result.data or []

        except Exception as e:
            st.error("โหลดเป้าหมายไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")
            goals = []

        if not goals:

            st.info(
                "ยังไม่มีเป้าหมาย มาเริ่มสร้างความฝันแรกกันนะคะ 💗"
            )

        else:

            active_goals = [
                goal for goal in goals
                if goal["status"] == "active"
            ]

            completed_goals = [
                goal for goal in goals
                if goal["status"] == "completed"
            ]

            col1, col2 = st.columns(2)

            col1.metric(
                "เป้าหมายทั้งหมด",
                len(goals)
            )

            col2.metric(
                "สำเร็จแล้ว 🎉",
                len(completed_goals)
            )

            for goal in goals:

                target = float(goal["target_value"])
                current = float(goal["current_value"])

                progress = min(current / target, 1.0)

                with st.container(border=True):

                    st.subheader(
                        f"🎯 {goal['title']}"
                    )

                    st.caption(
                        f"หมวดหมู่: {goal['category']}"
                    )

                    if goal.get("description"):
                        st.write(goal["description"])

                    st.write(
                        f"ความคืบหน้า: {current:g} / {target:g} "
                        f"{goal['unit']}"
                    )

                    st.progress(progress)

                    st.caption(
                        f"สำเร็จแล้ว {progress * 100:.0f}%"
                    )

                    # แสดงวันครบกำหนด
                    deadline = parse_due_date(
                        goal.get("target_date")
                    )

                    if deadline:

                        remaining_days = (
                            deadline - date.today()
                        ).days

                        if goal["status"] == "completed":
                            st.success("🏆 เป้าหมายสำเร็จแล้ว!")

                        elif remaining_days > 0:
                            st.info(
                                f"📅 เหลืออีก {remaining_days} วัน "
                                f"(ครบกำหนด {deadline.strftime('%d/%m/%Y')})"
                            )

                        elif remaining_days == 0:
                            st.warning("⏰ ครบกำหนดวันนี้!")

                        else:
                            st.error(
                                f"⚠️ เลยกำหนดมาแล้ว "
                                f"{abs(remaining_days)} วัน"
                            )

                    else:
                        st.caption("📅 ยังไม่ได้กำหนดวันครบกำหนด")

                    with st.expander("⚙️ จัดการเป้าหมาย"):

                        st.markdown("### ✏️ แก้ไขเป้าหมาย")

                        with st.form(
                            f"edit_goal_form_{goal['id']}"
                        ):

                            edit_title = st.text_input(
                                "ชื่อเป้าหมาย",
                                value=goal["title"]
                            )

                            edit_description = st.text_area(
                                "รายละเอียด",
                                value=goal.get("description") or ""
                            )

                            edit_category = st.selectbox(
                                "หมวดหมู่",
                                CATEGORIES,
                                index=(
                                    CATEGORIES.index(goal["category"])
                                    if goal["category"] in CATEGORIES
                                    else 0
                                )
                            )

                            edit_target = st.number_input(
                                "จำนวนเป้าหมาย",
                                min_value=1.0,
                                value=target,
                                step=1.0
                            )

                            edit_unit = st.text_input(
                                "หน่วย",
                                value=goal["unit"]
                            )

                            edit_submitted = st.form_submit_button(
                                "💾 บันทึกการแก้ไข"
                            )

                        if edit_submitted:

                            if not edit_title.strip():
                                st.warning("กรุณากรอกชื่อเป้าหมาย")

                            elif not edit_unit.strip():
                                st.warning("กรุณากรอกหน่วย")

                            else:
                                try:
                                    updated_target = edit_target

                                    updated_current = min(
                                        current,
                                        updated_target
                                    )

                                    updated_status = (
                                        "completed"
                                        if updated_current >= updated_target
                                        else "active"
                                    )

                                    supabase.table("goals").update({
                                        "title": edit_title.strip(),
                                        "description": edit_description.strip(),
                                        "category": edit_category,
                                        "target_value": updated_target,
                                        "current_value": updated_current,
                                        "unit": edit_unit.strip(),
                                        "status": updated_status
                                    }).eq(
                                        "id", goal["id"]
                                    ).eq(
                                        "user_id", user_id
                                    ).execute()

                                    st.success("แก้ไขเป้าหมายสำเร็จ! 💗")
                                    st.rerun()

                                except Exception as e:
                                    st.error("แก้ไขไม่สำเร็จ")
                                    st.code(
                                        f"{type(e).__name__}: {e}"
                                    )


                        st.warning(
                            "การลบเป้าหมายไม่สามารถกู้คืนได้"
                        )

                        if st.button(
                            "🗑️ ลบเป้าหมายนี้",
                            key=f"delete_goal_{goal['id']}"
                        ):

                            try:
                                supabase.table("goals").delete().eq(
                                    "id", goal["id"]
                                ).eq(
                                    "user_id", user_id
                                ).execute()

                                st.success("ลบเป้าหมายเรียบร้อยแล้ว")
                                st.rerun()

                            except Exception as e:
                                st.error("ลบเป้าหมายไม่สำเร็จ")
                                st.code(
                                    f"{type(e).__name__}: {e}"
                                )

                    if goal["status"] == "completed":
                        st.success("เป้าหมายนี้สำเร็จแล้ว! 🏆")

                    elif goal["status"] == "paused":
                        st.warning("เป้าหมายนี้หยุดพักอยู่")

                    else:
                        st.info("กำลังทำเป้าหมายนี้อยู่ 🌱")

                        with st.form(
                            f"update_goal_form_{goal['id']}"
                        ):

                            new_progress = st.number_input(
                                "เพิ่มความคืบหน้า",
                                min_value=0.0,
                                max_value=target,
                                value=0.0,
                                step=1.0,
                                key=f"progress_{goal['id']}"
                            )

                            update_submitted = st.form_submit_button(
                                "🌷 บันทึกความคืบหน้า"
                            )

                        if update_submitted:

                            updated_value = min(
                                current + new_progress,
                                target
                            )

                            new_status = (
                                "completed"
                                if updated_value >= target
                                else "active"
                            )

                            try:
                                supabase.table("goals").update({
                                    "current_value": updated_value,
                                    "status": new_status
                                }).eq(
                                    "id", goal["id"]
                                ).eq(
                                    "user_id", user_id
                                ).execute()

                                st.success("อัปเดตความคืบหน้าสำเร็จ! 💗")
                                st.rerun()

                            except Exception as e:
                                st.error("อัปเดตไม่สำเร็จ")
                                st.code(
                                    f"{type(e).__name__}: {e}"
                                )

    elif page == "📊 My Progress":

        st.header("📊 My Progress")
        st.write("ทุกก้าวเล็ก ๆ คือความสำเร็จของคุณ 💗")

        try:
            # โหลดข้อมูล Daily Planner
            task_result = (
                supabase.table("activities")
                .select("id, is_completed")
                .eq("user_id", user_id)
                .execute()
            )
            tasks = task_result.data or []

            # โหลดข้อมูล Habit Tracker
            habit_result = (
                supabase.table("habits")
                .select("id, is_active")
                .eq("user_id", user_id)
                .eq("is_active", True)
                .execute()
            )
            habits = habit_result.data or []

            # โหลดประวัติ Habit วันนี้
            log_result = (
                supabase.table("habit_logs")
                .select("habit_id")
                .eq("user_id", user_id)
                .eq("log_date", date.today().isoformat())
                .execute()
            )
            today_logs = log_result.data or []

            # โหลดข้อมูล My Goals
            goal_result = (
                supabase.table("goals")
                .select("status, target_value, current_value")
                .eq("user_id", user_id)
                .execute()
            )
            goals = goal_result.data or []

            # คำนวณสถิติ
            total_tasks = len(tasks)
            completed_tasks = sum(
                1 for task in tasks
                if task["is_completed"]
            )

            task_progress = (
                completed_tasks / total_tasks
                if total_tasks else 0
            )

            total_habits = len(habits)

            completed_habits = len({
                log["habit_id"]
                for log in today_logs
            } & {
                habit["id"]
                for habit in habits
            })

            total_goals = len(goals)

            completed_goals = sum(
                1 for goal in goals
                if goal["status"] == "completed"
            )

            target_sum = sum(
                float(goal["target_value"])
                for goal in goals
            )

            current_sum = sum(
                float(goal["current_value"])
                for goal in goals
            )

            goal_progress = (
                min(current_sum / target_sum, 1.0)
                if target_sum > 0 else 0
            )

            # แสดงภาพรวม
            st.subheader("🌸 ภาพรวมของฉัน")

            col1, col2 = st.columns(2)

            col1.metric(
                "📋 งานที่ทำสำเร็จ",
                f"{completed_tasks}/{total_tasks}"
            )

            col2.metric(
                "🌱 นิสัยที่ทำวันนี้",
                f"{completed_habits}/{total_habits}"
            )

            col3, col4 = st.columns(2)

            col3.metric(
                "🎯 เป้าหมายทั้งหมด",
                total_goals
            )

            col4.metric(
                "🏆 เป้าหมายที่สำเร็จ",
                completed_goals
            )

            st.divider()

            # ความคืบหน้า Daily Planner
            st.subheader("📋 Daily Planner")
            st.progress(task_progress)
            st.caption(
                f"ทำงานสำเร็จ {task_progress * 100:.0f}%"
            )

            # ความคืบหน้า Habit Tracker
            habit_progress = (
                completed_habits / total_habits
                if total_habits else 0
            )

            st.subheader("🌱 Habit Tracker")
            st.progress(habit_progress)
            st.caption(
                f"ทำสำเร็จวันนี้ {habit_progress * 100:.0f}%"
            )

            # ความคืบหน้า My Goals
            st.subheader("🎯 My Goals")
            st.progress(goal_progress)
            st.caption(
                f"ความคืบหน้ารวม {goal_progress * 100:.0f}%"
            )

            st.success(
                "คุณกำลังพัฒนาตัวเองไปทีละก้าว เก่งมาก! 💖"
            )

        except Exception as e:
            st.error("โหลดข้อมูลความสำเร็จไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")

    elif page == "📖 My Journal":

        st.header("📖 My Journal")
        st.write("เก็บเรื่องราวเล็ก ๆ ในแต่ละวันของคุณ 💗")

        st.subheader("✨ เขียนบันทึกวันนี้")

        with st.form("add_journal_form"):

            journal_date = st.date_input(
                "วันที่บันทึก",
                value=date.today()
            )

            journal_mood = st.selectbox(
                "วันนี้คุณรู้สึกอย่างไร?",
                [
                    "😊 มีความสุข",
                    "🥰 สดใส",
                    "😌 สงบ",
                    "😐 เฉย ๆ",
                    "😔 เศร้า",
                    "😫 เหนื่อย",
                    "😤 เครียด"
                ]
            )

            journal_title = st.text_input(
                "หัวข้อบันทึก",
                placeholder="วันนี้มีอะไรเกิดขึ้นบ้าง?"
            )

            journal_content = st.text_area(
                "เรื่องราวของวันนี้",
                placeholder="เขียนทุกอย่างที่อยากบันทึกได้เลย...",
                height=200
            )

            journal_submitted = st.form_submit_button(
                "💗 บันทึกเรื่องราว"
            )

        if journal_submitted:

            if not journal_title.strip():
                st.warning("กรุณากรอกหัวข้อบันทึก")

            elif not journal_content.strip():
                st.warning("กรุณาเขียนเรื่องราวก่อนบันทึก")

            else:
                try:
                    supabase.table("journals").insert({
                        "user_id": user_id,
                        "entry_date": journal_date.isoformat(),
                        "mood": journal_mood,
                        "title": journal_title.strip(),
                        "content": journal_content.strip()
                    }).execute()

                    st.success("บันทึกเรื่องราวสำเร็จแล้ว! 🌸")
                    st.rerun()

                except Exception as e:
                    st.error(
                        "บันทึกไม่สำเร็จ "
                        "อาจมีบันทึกของวันนี้อยู่แล้ว"
                    )
                    st.code(f"{type(e).__name__}: {e}")
			
        st.divider()

        st.subheader("📚 บันทึกย้อนหลัง")

        try:
            journal_result = (
                supabase.table("journals")
                .select("*")
                .eq("user_id", user_id)
                .order("entry_date", desc=True)
                .execute()
            )

            journals = journal_result.data or []

        except Exception as e:
            st.error("โหลดบันทึกย้อนหลังไม่สำเร็จ")
            st.code(f"{type(e).__name__}: {e}")
            journals = []

        if not journals:
            st.info("ยังไม่มีบันทึกย้อนหลัง 🌷")

        else:
            for journal in journals:

                with st.container(border=True):

                    parsed_date = parse_due_date(
                        journal["entry_date"]
                    )

                    st.subheader(journal["title"])

                    st.caption(
                        f"📅 {parsed_date.strftime('%d/%m/%Y')} "
                        f"| {journal['mood']}"
                    )

                    st.write(journal["content"])
                    with st.expander("✏️ แก้ไขบันทึก"):

                        with st.form(
                            f"edit_journal_{journal['id']}"
                        ):

                            edit_date = st.date_input(
                                "วันที่บันทึก",
                                value=parse_due_date(
                                    journal["entry_date"]
                                ),
                                key=f"edit_date_{journal['id']}"
                            )

                            mood_options = [
                                "😊 มีความสุข",
                                "🥰 สดใส",
                                "😌 สงบ",
                                "😐 เฉย ๆ",
                                "😔 เศร้า",
                                "😫 เหนื่อย",
                                "😤 เครียด"
                            ]

                            edit_mood = st.selectbox(
                                "อารมณ์",
                                mood_options,
                                index=(
                                    mood_options.index(journal["mood"])
                                    if journal["mood"] in mood_options
                                    else 0
                                ),
                                key=f"edit_mood_{journal['id']}"
                            )

                            edit_title = st.text_input(
                                "หัวข้อ",
                                value=journal["title"],
                                key=f"edit_title_{journal['id']}"
                            )

                            edit_content = st.text_area(
                                "เนื้อหาบันทึก",
                                value=journal["content"],
                                height=180,
                                key=f"edit_content_{journal['id']}"
                            )

                            edit_submitted = st.form_submit_button(
                                "💾 บันทึกการแก้ไข"
                            )

                        if edit_submitted:

                            if not edit_title.strip():
                                st.warning("กรุณากรอกหัวข้อ")

                            elif not edit_content.strip():
                                st.warning("กรุณากรอกเนื้อหาบันทึก")

                            else:
                                try:
                                    supabase.table("journals").update({
                                        "entry_date": edit_date.isoformat(),
                                        "mood": edit_mood,
                                        "title": edit_title.strip(),
                                        "content": edit_content.strip(),
                                        "updated_at": date.today().isoformat()
                                    }).eq(
                                        "id", journal["id"]
                                    ).eq(
                                        "user_id", user_id
                                    ).execute()

                                    st.success("แก้ไขบันทึกสำเร็จ! 💗")
                                    st.rerun()

                                except Exception as e:
                                    st.error(
                                        "แก้ไขไม่สำเร็จ "
                                        "อาจมีบันทึกของวันดังกล่าวอยู่แล้ว"
                                    )
                                    st.code(
                                        f"{type(e).__name__}: {e}"
                                    )
                    with st.form(
                        f"delete_journal_{journal['id']}"
                    ):
                        delete_confirm = st.checkbox(
                            "ยืนยันว่าต้องการลบบันทึกนี้"
                        )

                        delete_submitted = st.form_submit_button(
                            "🗑️ ลบบันทึก"
                        )

                    if delete_submitted:

                        if not delete_confirm:
                            st.warning("กรุณายืนยันก่อนลบบันทึก")

                        else:
                            try:
                                supabase.table("journals").delete().eq(
                                    "id", journal["id"]
                                ).eq(
                                    "user_id", user_id
                                ).execute()

                                st.success("ลบบันทึกเรียบร้อยแล้ว 🌷")
                                st.rerun()

                            except Exception as e:
                                st.error("ลบบันทึกไม่สำเร็จ")
                                st.code(
                                    f"{type(e).__name__}: {e}"
                                )

    # ======================================
    # 8. ออกจากระบบ
    # ======================================

    st.divider()

    if st.button("ออกจากระบบ 🚪"):

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        st.session_state.user = None
        st.session_state.access_token = None
        st.session_state.refresh_token = None

        st.rerun()


# ==========================================
# 9. ยังไม่ได้เข้าสู่ระบบ
# ==========================================

else:

    tab_login, tab_signup = st.tabs([
        "เข้าสู่ระบบ 🔑",
        "สมัครสมาชิก 🌸"
    ])

    # เข้าสู่ระบบ
    with tab_login:

        st.subheader("ยินดีต้อนรับกลับมา!")

        email_login = st.text_input(
            "อีเมล",
            key="email_login"
        )

        password_login = st.text_input(
            "รหัสผ่าน",
            type="password",
            key="password_login"
        )

        if st.button("เข้าสู่ระบบ", key="login_button"):

            if not email_login or not password_login:
                st.warning("กรุณากรอกอีเมลและรหัสผ่าน")

            else:
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email_login,
                        "password": password_login
                    })

                    if response.session is None:
                        st.error("ไม่พบ Session กรุณาลองใหม่")

                    else:
                        st.session_state.user = response.user

                        st.session_state.access_token = (
                            response.session.access_token
                        )

                        st.session_state.refresh_token = (
                            response.session.refresh_token
                        )

                        st.success("เข้าสู่ระบบสำเร็จ! 💖")
                        st.rerun()

                except Exception as e:
                    st.error("เข้าสู่ระบบไม่สำเร็จ")
                    st.code(f"{type(e).__name__}: {e}")

    # สมัครสมาชิก
    with tab_signup:

        st.subheader("สร้างบัญชีใหม่ 🌷")

        email_signup = st.text_input(
            "อีเมลสำหรับสมัคร",
            key="email_signup"
        )

        password_signup = st.text_input(
            "ตั้งรหัสผ่าน",
            type="password",
            key="password_signup"
        )

        confirm_password = st.text_input(
            "ยืนยันรหัสผ่าน",
            type="password",
            key="confirm_password"
        )

        if st.button("สมัครสมาชิก", key="signup_button"):

            if not email_signup or not password_signup:
                st.warning("กรุณากรอกข้อมูลให้ครบ")

            elif len(password_signup) < 8:
                st.warning("รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร")

            elif password_signup != confirm_password:
                st.warning("รหัสผ่านทั้งสองช่องไม่ตรงกัน")

            else:
                try:
                    response = supabase.auth.sign_up({
                        "email": email_signup,
                        "password": password_signup
                    })

                    if response.session:
                        st.success("สมัครสมาชิกสำเร็จ! 💖")
                    else:
                        st.success(
                            "สมัครสมาชิกสำเร็จ! "
                            "กรุณาตรวจสอบอีเมลเพื่อยืนยันบัญชี 🌸"
                        )

                except Exception as e:
                    st.error("สมัครสมาชิกไม่สำเร็จ")
                    st.code(f"{type(e).__name__}: {e}")
