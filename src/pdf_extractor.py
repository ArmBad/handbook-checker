import PyPDF2
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file with page tracking.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        tuple: (full_text, page_map) where page_map is dict of {page_num: text}
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            full_text = ""
            page_map = {}
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                # Store in page map (1-indexed for user display)
                page_map[page_num + 1] = page_text
                
                # Add to full text with page marker
                full_text += f"\n\n[PAGE {page_num + 1}]\n\n"
                full_text += page_text
            
            return full_text, page_map
    
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None, None

# Test function
if __name__ == "__main__":
    # Test with one of your sample handbooks
    test_pdf = "data/handbook1.pdf"
    
    if Path(test_pdf).exists():
        print(f"Testing PDF extraction on {test_pdf}...")
        text, page_map = extract_text_from_pdf(test_pdf)
        
        if text:
            print(f"\n✅ SUCCESS! Extracted {len(text)} characters from {len(page_map)} pages")
            print(f"\nFirst 500 characters:\n{text[:500]}")
            
            # Save to file so you can review
            with open("output/extracted_text.txt", "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n✅ Full text saved to output/extracted_text.txt")
        else:
            print("❌ Failed to extract text")
    else:
        print(f"❌ File not found: {test_pdf}")
        print("Please download a sample handbook PDF and save it as data/handbook1.pdf")