import streamlit as st
import requests

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Resume Branding Portal",
    page_icon="📄",
    layout="centered"
)

st.title("🚀 Resume Branding Portal")
st.markdown("Upload a resume and get a beautifully branded PDF instantly.")

# -----------------------------
# Config
# -----------------------------
N8N_WEBHOOK_URL = "https://n8n.srv1098663.hstgr.cloud/webhook/resume-portal"

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# -----------------------------
# Main Logic
# -----------------------------
if uploaded_file:
    st.success(f"📄 File ready: {uploaded_file.name}")

    if st.button("✨ Generate Branded Resume"):

        with st.spinner("Processing your resume..."):
            try:
                # Prepare file payload
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "application/pdf"
                    )
                }

                # Send to n8n
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    files=files,
                    timeout=180  # safer for AI + Docs processing
                )

                # -----------------------------
                # Success Handling
                # -----------------------------
                if response.status_code == 200 and response.content:

                    st.balloons()
                    st.success("✅ Your branded resume is ready!")

                    # Dynamic filename
                    file_name = uploaded_file.name.replace(".pdf", "_branded.pdf")

                    # Download button
                    st.download_button(
                        label="📥 Download Branded Resume (PDF)",
                        data=response.content,
                        file_name=file_name,
                        mime="application/pdf"
                    )

                # -----------------------------
                # Error Handling
                # -----------------------------
                else:
                    st.error(f"❌ Failed: {response.status_code}")
                    st.code(response.text)

            except requests.exceptions.Timeout:
                st.error("⏳ Request timed out. Try again or reduce file size.")

            except requests.exceptions.ConnectionError:
                st.error("🌐 Connection error. Check your internet or webhook URL.")

            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")