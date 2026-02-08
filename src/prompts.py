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

CRITICAL: You MUST format your response EXACTLY as shown below. Use this format for EACH item:

### 1. At-Will Employment Disclaimer (Labor Code §2922)
- **Status**: Present
- **Pages**: Pages 5, 9
- **Assessment**: Compliant. Clear statement that employment can be terminated by either party...
- **Risk Level**: Low
- **Recommendation**: No action needed
- **Legal Citation**: Labor Code §2922

### 2. Equal Employment Opportunity Policy (Gov. Code §12940)
- **Status**: Present
- **Pages**: Page 12
- **Assessment**: Compliant. Comprehensive policy covering all protected classes...
- **Risk Level**: Low
- **Recommendation**: No action needed
- **Legal Citation**: Gov. Code §12940

IMPORTANT FORMATTING RULES:
1. Start each item with "### [NUMBER]. [TITLE] ([CODE])"
2. Use bullet points with "- **FieldName**: value" format
3. ALL field names must be bolded with **
4. Include all 6 fields in order: Status, Pages, Assessment, Risk Level, Recommendation, Legal Citation
5. Use exactly these field names (case-sensitive)

At the end, provide a summary section:

## SUMMARY OF CRITICAL ISSUES

1. **Missing PAGA Notice** - Description of the issue
2. **Another Issue** - Description

---

## COMPLIANCE SCORECARD

- **Compliant Items**: 15
- **Partially Compliant Items**: 2
- **Non-Compliant Items**: 3
- **Total Items Reviewed**: 20
- **Overall Compliance Grade**: B

DO NOT deviate from this format. The output will be parsed by software that expects this exact structure.
"""
    
    return prompt