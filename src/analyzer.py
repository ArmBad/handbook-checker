import anthropic
import os
import time
from prompts import get_compliance_prompt
from checklist import get_checklist

class HandbookAnalyzer:
    def __init__(self, api_key):
        """Initialize the analyzer with Anthropic API key."""
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def analyze_handbook(self, handbook_text):
        """
        Analyze handbook for CA employment law compliance.
        
        Args:
            handbook_text: Extracted text from handbook PDF
            
        Returns:
            str: Analysis results from Claude
        """
        
        # Get the checklist
        checklist = get_checklist()
        
        # Create the prompt
        prompt = get_compliance_prompt(handbook_text, checklist)
        
        print("🤖 Sending to Claude for analysis...")
        print(f"📄 Analyzing {len(handbook_text)} characters of handbook text...")
        
        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the response
            analysis = message.content[0].text
            
            print("✅ Analysis complete!")
            return analysis
            
        except Exception as e:
            # Check if it's a rate limit error
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print("⏳ Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                print("🔄 Retrying...")
                
                # Retry the API call
                try:
                    message = self.client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=4000,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    analysis = message.content[0].text
                    print("✅ Analysis complete!")
                    return analysis
                    
                except Exception as retry_error:
                    print(f"❌ Error on retry: {retry_error}")
                    return None
            else:
                # If it's a different error, just report it
                print(f"❌ Error calling Claude API: {e}")
                return None

# Test function
if __name__ == "__main__":
    # Get API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not set!")
        print("\nTo set it:")
        print("Command Prompt: set ANTHROPIC_API_KEY=your-key-here")
        print("PowerShell: $env:ANTHROPIC_API_KEY='your-key-here'")
        exit(1)
    
    # Load sample extracted text
    try:
        with open("output/extracted_text.txt", "r", encoding="utf-8") as f:
            handbook_text = f.read()
    except FileNotFoundError:
        print("❌ File not found: output/extracted_text.txt")
        print("Run pdf_extractor.py first to extract text from a handbook PDF")
        exit(1)
    
    # Create analyzer
    analyzer = HandbookAnalyzer(api_key)
    
    # Run analysis
    analysis = analyzer.analyze_handbook(handbook_text)
    
    if analysis:
        # Save results
        with open("output/analysis_results.txt", "w", encoding="utf-8") as f:
            f.write(analysis)
        
        print(f"\n✅ Analysis saved to output/analysis_results.txt")
        print(f"\nFirst 1000 characters:\n{analysis[:1000]}")