from fpdf import FPDF

def export_to_pdf(path1, path2, score, text1, text2):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="📄 Plagiarism Detection Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Document 1: {path1}", ln=True)
    pdf.cell(200, 10, txt=f"Document 2: {path2}", ln=True)
    pdf.cell(200, 10, txt=f"Similarity Score: {score}%", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="--- Document 1 Content ---")
    pdf.multi_cell(0, 10, txt=text1[:1000] + "..." if len(text1) > 1000 else text1)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt="--- Document 2 Content ---")
    pdf.multi_cell(0, 10, txt=text2[:1000] + "..." if len(text2) > 1000 else text2)

    pdf.output("plagiarism_report.pdf")