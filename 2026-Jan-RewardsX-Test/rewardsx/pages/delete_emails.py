import streamlit as st
import os

EMAIL_FOLDER = "data/emails"

st.set_page_config(page_title="Manage Emails", layout="wide")

st.title("Manage Emails")


# ✅ 2. Hide default Streamlit navigation
st.markdown("""
<style>

/* Hide default nav (you already have this) */
[data-testid="stSidebarNav"] {
    display: none;
}

/* 🔥 Make sidebar radio label bigger */
section[data-testid="stSidebar"] .stRadio label {
    font-size: 20px !important;
    font-weight: 600;
}

/* 🔥 Make "Navigation" title bigger */
section[data-testid="stSidebar"] h2 {
    font-size: 26px !important;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ✅ 3. Navigation (THIS WAS MISSING LOGIC)
page = st.sidebar.radio(
    "Navigation",
    ["📧 Email Parser", "📂 Manage Emails"],
    index=1
)

# 🔥 THIS PART IS CRITICAL
if page == "📧 Email Parser":
    st.switch_page("app.py")   # ✅ use page name, NOT file path


# Load emails
emails = sorted(os.listdir(EMAIL_FOLDER))

if not emails:
    st.warning("No emails found.")
else:
    selected_email = st.selectbox("Select Email to Delete", emails)

    st.write(f"Selected: **{selected_email}**")

    st.divider()

    confirm = st.checkbox("Confirm deletion")

    if confirm:
        if st.button("Delete Email"):

            file_path = os.path.join(EMAIL_FOLDER, selected_email)

            try:
                os.remove(file_path)

                st.success(f"{selected_email} deleted successfully")

                # Refresh list
                st.rerun()

            except Exception as e:
                st.error(f"Error deleting file: {e}")

# Back button
st.divider()

if st.button("Back to Main Page"):
    st.switch_page("app.py")