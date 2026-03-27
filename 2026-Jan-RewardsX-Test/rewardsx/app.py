# RewardsX AI Parser App
import streamlit as st
import os
# this pandas is just for displaying AI output in a nice table format
import pandas as pd

# importing the functions from the other modules
from ingestion.parser import parse_eml
from ai.interpreter import extract_rewards_info

# saving folder path for easy access, this is where the .eml files are stored for testing and parsing in the app
EMAIL_FOLDER = "data/emails"

# this is setting up the Streamlit page with a title and icon, and defining the layout as wide
st.set_page_config(
    page_title="RewardsX AI Parser",
    layout="wide"
)
# ✅ 2. Hide default nav
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

# ✅ 3. CUSTOM NAVIGATION (PUT IT HERE)
page = st.sidebar.radio(
    "Navigation",
    ["📧 Email Parser", "📂 Manage Emails"]
)

if page == "📧 Email Parser":
    pass  # stay here
else:
    st.switch_page("pages/delete_emails.py")

# title
st.title("RewardsX Email Rewards Extractor")

# intro text
st.write("Select an email to parse and extract rewards points using AI.")

# Get email files
emails = sorted(os.listdir(EMAIL_FOLDER))

# Layout
left, right = st.columns([1,2])

# EMAIL LIST
with left:
    st.subheader("Email Inbox")

    selected_email = st.radio(
        "Available Emails",
        emails
    )

# EMAIL PREVIEW
with right:

    if selected_email:
    #  this constructs the full file path to the selected email, which is needed to read and parse the .eml file
        file_path = os.path.join(EMAIL_FOLDER, selected_email)

        st.subheader("Email Preview")

        email_data = parse_eml(file_path)

# this displays the email's subject and sender, followed by a divider and then the cleaned body of the email. The "Extract Rewards Points" button triggers the AI extraction process when clicked.
        st.markdown(f"**Subject:** {email_data.get('subject')}")
        st.markdown(f"**From:** {email_data.get('sender')}")

        st.markdown("---")

        st.write(email_data.get("body"))

        st.divider()

        # if this buttons clicked, it will send the email data to the AI for extraction and display the results

        if st.button("Extract Rewards Points"):

            with st.spinner("Parsing email and getting required information..."):

                email_data = parse_eml(file_path)

                ai_result = extract_rewards_info(email_data)

            st.subheader("Extraction Result")

            # ERROR HANDLING
            if "error" in ai_result:

                st.error("Extraction Failed")

                st.json(ai_result)

#  if extraction from ai is successful, it will show the program, points, email in a clean format. If there are null valies, it will show none or null and default 0 for points.
            else:

                program = ai_result.get("program")
                points = ai_result.get("points")
                email = ai_result.get("email")
                #awarded date and expiry date  
                awarded_date = ai_result.get("awarded_date")
                expiry_date = ai_result.get("expiry_date")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Rewards Program",
                    program if program else "None"
                )

                col2.metric(
                    "Points Earned",
                    points if points else 0
                )

                col3.metric(
                    "Customer Email",
                    email if email else "Unknown"
                )

                st.divider()


                col4, col5 = st.columns(2)

                col4.metric(
                 "Awarded Date",
                awarded_date if awarded_date else "Unknown"
                        )

                col5.metric(
                     "Expiry Date",
                     expiry_date if expiry_date else "None"
                              )
