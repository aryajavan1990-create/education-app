import streamlit as st
import numpy as np
import pandas as pd
from neonui import apply_theme

st.set_page_config(
    page_title="Education System",
    page_icon="🎓",
    layout="wide"
)

apply_theme("cosmic_purple")

# ۱. راه‌اندازی متغیرهای پایدار در حافظه
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "c_page" not in st.session_state:
    st.session_state.c_page = "Gradebook"

# دیتافریم فقط یک‌بار در شروع ساخته می‌شود و در حافظه می‌ماند
if "df" not in st.session_state:
    names = ["Ali", "Reza", "Hasan", "Ghasem"]
    courses = ["Math", "Physics", "Chemistry", "Religious"]
    # تا ۲۱ گذاشتیم تا نمره ۲۰ هم شامل شود
    scores = np.random.randint(10, 21, size=(len(names), len(courses)))
    st.session_state.df = pd.DataFrame(scores, index=names, columns=courses)

# ۲. صفحه لاگین
if not st.session_state.logged_in:
    _, col_center, _ = st.columns([1, 1.5, 1])

    with col_center:
        st.title("Login Page to Software")
        st.markdown("---")
        st.write("")

        username = st.text_input("Username", placeholder="e.g. admin")
        password = st.text_input("Password", placeholder="e.g. 1234", type="password")
        login_btn = st.button("Login Here", use_container_width=True)

        if login_btn:
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.success("Welcome to Evaluation System")
                st.rerun()
            else:
                st.error("Wrong password or username")

# ۳. پنل اصلی نرم‌افزار پس از لاگین
else:
    with st.sidebar:
        st.title("Scores Management System")
        st.markdown("---")

        if st.button("📝 Data", use_container_width=True):
            st.session_state.c_page = "Gradebook"

        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.c_page = "Settings"

        st.markdown("---")

        if st.button("Log out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    if st.session_state.c_page == "Gradebook":
        st.header("Data Table")
        st.info("💡 You can change data by clicking on its row in table!")

        # ویرایش زنده جدول با حفظ مقادیر
        edited_df = st.data_editor(
            st.session_state.df,
            use_container_width=True,
            num_rows="dynamic"
        )
        # ثبت تغییرات انجام‌شده در سشن
        st.session_state.df = edited_df

        st.markdown("---")

        # محاسبات آماری امن با متدهای پانداس
        max_val = edited_df.max().max()
        mean_val = edited_df.mean().mean()
        min_val = edited_df.min().min()

        col1, col2, col3 = st.columns(3)
        col1.metric("Highest Score", f"{max_val:.1f}" if pd.notna(max_val) else "-")
        col2.metric("Mean Score", f"{mean_val:.2f}" if pd.notna(mean_val) else "-")
        col3.metric("Lowest Score", f"{min_val:.1f}" if pd.notna(min_val) else "-")

        st.markdown("---")
        st.subheader("📈 نمودار وضعیت درسی دانش‌آموزان")
        # کشیدن نمودار میله‌ای زنده بر اساس جدول ویرایش‌شده
        st.bar_chart(edited_df)

    elif st.session_state.c_page == "Settings":
        st.header("Settings Page")
        st.write("Settings will be placed here.")
