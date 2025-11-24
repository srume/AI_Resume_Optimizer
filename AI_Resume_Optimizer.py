from dotenv import load_dotenv
import os
import streamlit as st

system_prompt = """
You are an expert Resume Optimization AI.
Your task:
1. Improve grammar, clarity, and impact of the resume.
2. Match keywords from the provided job description.
3. Add missing skills relevant to the role.
4. Rewrite bullet points using strong action verbs.
5. Provide an improved professional summary.
6. Maintain truthful content — do not fabricate experience.

Output in this structure:

### Optimized Summary
...
### Optimized Skills
...
### Optimized Experience
...
### Missing but Relevant Keywords
...
### Suggestions to Improve ATS Score
...
"""



# Load the file manually
load_dotenv(r"C:\Users\Hp\Personal AI\Master_Summarizer\new.env", override=True)


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("⚠️ GROQ_API_KEY not found in new.env")

print("API key loaded successfully!")

from groq import Groq

# Initialize Groq client
client = Groq(api_key=api_key)

def optimize_resume(resume_text, job_description):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""
Resume:
{resume_text}

Job Description:
{job_description}
"""}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    
    return response.choices[0].message.content



st.title("📄 AI Resume Optimizer (Groq Powered)")

uploaded_pdf = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_pdf is not None:
    st.success("PDF uploaded successfully!")
    st.write("Uploaded file:", uploaded_pdf.name)

from pypdf import PdfReader

if uploaded_pdf is not None:
    st.success("PDF uploaded successfully!")
    st.write("Uploaded file:", uploaded_pdf.name)
    
    # Extract text
    reader = PdfReader(uploaded_pdf)
    extracted_text = ""

    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"

    # Show extracted text
    st.subheader("📄 Extracted Resume Text")
    st.write(extracted_text)

# Job description input
job_desc = st.text_area("Paste Job Description Here", height=200)

# Button to optimize resume
if st.button("Optimize Resume"):
    if uploaded_pdf is None:
        st.warning("Please upload a resume first.")
    elif job_desc.strip() == "":
        st.warning("Please paste the job description.")
    else:
        with st.spinner("Optimizing resume..."):
            optimized_text = optimize_resume(extracted_text, job_desc)
        
        st.subheader("✨ Optimized Resume")
        st.write(optimized_text)


