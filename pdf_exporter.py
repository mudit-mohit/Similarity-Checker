from fpdf import FPDF
import os
import unicodedata

def export_to_pdf(path1, path2, score, text1, text2):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        def safe_text(text):
            if not text:
                return ""
            text = str(text)
            text = unicodedata.normalize('NFKD', text)
            # Replace any remaining problematic characters
            text = text.encode('latin-1', 'replace').decode('latin-1')
            return text

        # Title
        pdf.cell(200, 10, txt="Plagiarism Detection Report", ln=True, align='C')
        pdf.ln(10)
        
        # Document info
        pdf.cell(200, 10, txt=f"Document 1: {safe_text(os.path.basename(path1))}", ln=True)
        pdf.cell(200, 10, txt=f"Document 2: {safe_text(os.path.basename(path2))}", ln=True)
        pdf.cell(200, 10, txt=f"Similarity Score: {score}%", ln=True)
        pdf.ln(10)
        
        # Document contents
        pdf.multi_cell(0, 10, txt="--- Document 1 Content ---")
        safe_text1 = safe_text(text1[:1000] + "..." if len(text1) > 1000 else text1)
        pdf.multi_cell(0, 10, txt=safe_text1)
        
        pdf.ln(5)
        pdf.multi_cell(0, 10, txt="--- Document 2 Content ---")
        safe_text2 = safe_text(text2[:1000] + "..." if len(text2) > 1000 else text2)
        pdf.multi_cell(0, 10, txt=safe_text2)

        # Get the current working directory
        current_dir = os.getcwd()
        output_path = os.path.join(current_dir, "plagiarism_report.pdf")
        
        pdf.output(output_path)
        
        # Verify the file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            return f"Success: File created at {output_path} (Size: {file_size} bytes)"
        else:
            return "Error: File was not created"
            
    except Exception as e:
        return f"Error during PDF creation: {str(e)}"