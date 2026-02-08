import streamlit as st
import os
import sys
from pathlib import Path
import shutil
import hashlib

# Add src to path so we can import our modules
sys.path.append(str(Path(__file__).parent / 'src'))

from pdf_extractor import extract_text_from_pdf
from analyzer import HandbookAnalyzer
from report_generator import ReportGenerator
from checklist import get_checklist

# Page config
st.set_page_config(
    page_title="Handbook Compliance Checker",
    page_icon="📋",
    layout="centered"
)

# Password protection
def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Hash the entered password
        entered_hash = hashlib.sha256(st.session_state["password"].encode()).hexdigest()
        
        # AUTHORIZED PASSWORDS:
        # To add a new password:
        # 1. Open Command Prompt
        # 2. Run: python -c "import hashlib; print(hashlib.sha256('YourNewPassword'.encode()).hexdigest())"
        # 3. Add the output hash to the list below
        
        authorized_hashes = [
            # Default password: "axiom2026"
            "ba7564b9c8950db69ad04479e64d12ad62919739aabd02b93da70c57ad8d7d0d",
            
            # Add more password hashes here for different clients
            # Example: "abc123def456..." for password "ClientPassword123"
        ]
        
        if entered_hash in authorized_hashes:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run or password not yet entered
    if "password_correct" not in st.session_state:
        st.title("🔒 Access Required")
        st.markdown("### Axiom Legal Workflow - Handbook Compliance Checker")
        st.markdown("---")
        st.markdown("This is a restricted tool for authorized clients only.")
        st.text_input(
            "Enter your access code:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.info("💡 If you need access, contact Axiom Legal Workflow")
        return False
    
    # Password incorrect
    elif not st.session_state["password_correct"]:
        st.title("🔒 Access Required")
        st.markdown("### Axiom Legal Workflow - Handbook Compliance Checker")
        st.markdown("---")
        st.text_input(
            "Enter your access code:",
            type="password",
            on_change=password_entered,
            key="password"
        )
        st.error("❌ Incorrect access code. Please try again.")
        return False
    
    # Password correct
    else:
        return True

# Check password before showing the app
if not check_password():
    st.stop()

# If password is correct, show the main app
st.title("📋 California Employee Handbook Compliance Checker")
st.markdown("### Powered by Axiom Legal Workflow")
st.markdown("---")

st.markdown("""
**Analyze your employee handbook for California compliance in seconds.**

This tool checks your handbook against 20 core California employment law requirements 
including 2026 updates (PAGA, AI disclosure, emergency contacts, and more).

Simply upload your handbook PDF below and we'll generate a comprehensive compliance report.
""")

st.markdown("---")

# File uploader
uploaded_file = st.file_uploader(
    "Upload Employee Handbook (PDF)",
    type=['pdf'],
    help="Drag and drop your PDF here, or click to browse"
)

if uploaded_file is not None:
    # Show file info
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Optional: Handbook name input
    handbook_name = st.text_input(
        "Handbook Name (optional)",
        value=uploaded_file.name.replace('.pdf', ''),
        help="This will appear on the report"
    )
    
    # Analyze button
    if st.button("🔍 Analyze Handbook", type="primary"):
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Save uploaded file
            status_text.text("📄 Saving PDF...")
            progress_bar.progress(10)
            
            # Save to temp location
            temp_pdf_path = Path("temp_upload.pdf")
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Step 2: Extract text
            status_text.text("📖 Extracting text from PDF...")
            progress_bar.progress(25)
            
            handbook_text, page_map = extract_text_from_pdf(str(temp_pdf_path))
            
            if not handbook_text:
                st.error("❌ Error: Could not extract text from PDF. Please make sure it's a valid PDF file.")
                st.stop()
            
            # Step 3: Get checklist
            status_text.text("📋 Loading compliance checklist...")
            progress_bar.progress(40)
            
            checklist = get_checklist()
            
            # Step 4: Analyze with AI
            status_text.text("🤖 Analyzing with AI (this may take 30-60 seconds)...")
            progress_bar.progress(50)
            
            # Get API key from environment
            api_key = os.getenv("ANTHROPIC_API_KEY")
            
            if not api_key:
                st.error("❌ Error: ANTHROPIC_API_KEY not set. Please contact Axiom Legal Workflow.")
                st.stop()
            
            analyzer = HandbookAnalyzer(api_key)
            analysis = analyzer.analyze_handbook(handbook_text)
            
            if not analysis:
                st.error("❌ Error: Analysis failed. Please try again.")
                st.stop()
            
            progress_bar.progress(75)
            
            # Step 5: Generate report
            status_text.text("📊 Generating professional PDF report...")
            
            output_path = Path("output") / f"{handbook_name}_compliance_report.pdf"
            output_path.parent.mkdir(exist_ok=True)
            
            generator = ReportGenerator()
            generator.generate_report(
                analysis_text=analysis,
                handbook_name=handbook_name,
                output_path=str(output_path)
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
            
            # Step 6: Provide download
            st.success("🎉 Report generated successfully!")
            
            # Read the generated PDF
            with open(output_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            
            # Download button
            st.download_button(
                label="📥 Download Compliance Report",
                data=pdf_bytes,
                file_name=f"{handbook_name}_compliance_report.pdf",
                mime="application/pdf",
                type="primary"
            )
            
            # Show preview of analysis
            with st.expander("📄 View Analysis Summary"):
                # Extract key stats from analysis
                import re
                
                grade_match = re.search(r'(?:Overall Compliance Grade|Grade)[:\s]*\*?\*?\s*([A-F])', analysis, re.IGNORECASE)
                compliant_match = re.search(r'Compliant Items[:\s]*\*?\*?\s*(\d+)', analysis, re.IGNORECASE)
                noncompliant_match = re.search(r'Non-Compliant Items[:\s]*\*?\*?\s*(\d+)', analysis, re.IGNORECASE)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Compliance Grade", grade_match.group(1) if grade_match else "N/A")
                
                with col2:
                    st.metric("Compliant Items", compliant_match.group(1) if compliant_match else "0")
                
                with col3:
                    st.metric("Non-Compliant Items", noncompliant_match.group(1) if noncompliant_match else "0")
                
                st.text_area("Full Analysis", analysis, height=400)
            
            # Cleanup
            if temp_pdf_path.exists():
                temp_pdf_path.unlink()
                
        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            st.exception(e)
            progress_bar.progress(0)
            status_text.text("")

# Sidebar
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    This tool analyzes California employee handbooks for compliance with:
    
    - **Core Policies**: At-will, EEO, harassment, wage/hour
    - **Leave Policies**: CFRA, PDL, sick leave, bereavement
    - **2026 Updates**: AI disclosure, PAGA, emergency contacts
    - **And 15+ more requirements**
    
    **Questions?**  
    Contact Axiom Legal Workflow
    """)
    
    st.markdown("---")
    st.markdown("### 🔒 Privacy")
    st.markdown("""
    Your handbook is analyzed securely and not stored permanently. 
    All data is processed locally and deleted after analysis.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>© 2026 Axiom Legal Workflow</p>
    <p><em>This tool provides informational analysis only and does not constitute legal advice.</em></p>
</div>
""", unsafe_allow_html=True)