def get_compliance_prompt(handbook_text, checklist_items):
    """
    Generate the prompt for Claude to analyze handbook compliance.
    """
    
    prompt = f"""You are a California employment law expert specializing in employee handbook compliance.

Analyze the following employee handbook for compliance with California law.

IMPORTANT: The handbook text includes [PAGE X] markers showing which page each section is on. When you identify a policy, please note which page(s) it appears on.

HANDBOOK TEXT:
{handbook_text}

---

Check for the following required policies and provisions:

{checklist_items}

---

For EACH item in the checklist, provide:

1. **Status**: Present / Missing / Partially Present
2. **Pages**: List the specific page numbers where this policy appears (e.g., "Pages 12-14" or "Page 5" or "Not found")
3. **Assessment**: If present, is it compliant with current CA law? If missing or non-compliant, what's the issue?
4. **Risk Level**: High / Medium / Low
5. **Recommendation**: Specific action needed (if any)
6. **Legal Citation**: Relevant CA Labor Code section or statute

Format your response as a structured analysis with clear sections for each compliance item.

At the end, provide:
- Summary of critical issues (High risk items)
- Count of compliant vs. non-compliant items
- Overall compliance grade (A-F)
"""
    
    return prompt