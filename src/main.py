import os
import sys
from pathlib import Path
from pdf_extractor import extract_text_from_pdf
from analyzer import HandbookAnalyzer
from report_generator import ReportGenerator
def main(pdf_path):
    """
    Complete pipeline: Analyze a handbook and generate compliance report.
    
    Args:
        pdf_path: Path to the handbook PDF
    """
    
    print("="*60)
    print("📋 AXIOM LEGAL WORKFLOW - Handbook Compliance Checker")
    print("="*60)
    print()
    
    # Step 1: Extract text from PDF
    print("Step 1/3: Extracting text from PDF...")
    handbook_text = extract_text_from_pdf(pdf_path)
    
    if not handbook_text:
        print("❌ Failed to extract text from PDF")
        return
    
    print(f"✅ Extracted {len(handbook_text)} characters")
    print()
    
    # Step 2: Analyze with Claude
    print("Step 2/3: Analyzing compliance with Claude AI...")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set!")
        print("\nSet it with:")
        print("  Mac/Linux: export ANTHROPIC_API_KEY='your-key'")
        print("  Windows: set ANTHROPIC_API_KEY=your-key")
        return
    
    analyzer = HandbookAnalyzer(api_key)
    analysis = analyzer.analyze_handbook(handbook_text)
    
    if not analysis:
        print("❌ Failed to analyze handbook")
        return
    
    print("✅ Analysis complete")
    print()
    
    # Step 3: Generate PDF report
    print("Step 3/3: Generating compliance report...")
    
    handbook_name = Path(pdf_path).stem
    output_path = f"output/{handbook_name}_compliance_report.pdf"
    
    generator = ReportGenerator()
    generator.generate_report(
        analysis_text=analysis,
        handbook_name=handbook_name,
        output_path=output_path
    )
    
    print()
    print("="*60)
    print("✅ COMPLETE!")
    print(f"📄 Report saved to: {output_path}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <path-to-handbook.pdf>")
        print("\nExample:")
        print("  python src/main.py data/handbook1.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)
    
    main(pdf_path)