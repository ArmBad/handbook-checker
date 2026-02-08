"""
California Employment Law Compliance Checklist
20 core requirements for employee handbooks
"""

def get_checklist():
    """
    Returns the CA employment law compliance checklist.
    """
    
    checklist = """
# CALIFORNIA EMPLOYMENT LAW COMPLIANCE CHECKLIST (20 Core Items)

1. **At-Will Employment Disclaimer** (Labor Code §2922)
   - Clear statement that employment is at-will
   - Can be terminated by either party at any time
   - Only authorized person can modify in writing

2. **Equal Employment Opportunity Policy** (Gov. Code §12940)
   - Prohibits discrimination based on all protected classes
   - Includes: race, color, religion, sex, gender identity, sexual orientation, age, disability, medical condition, genetic information, marital status, military status, reproductive health decisions

3. **Anti-Harassment Policy** (Gov. Code §12940)
   - Definitions of harassment (sexual and all protected classes)
   - Examples of prohibited conduct
   - Clear statement it will not be tolerated

4. **Harassment Complaint Procedure** (Gov. Code §12950)
   - Multiple reporting channels
   - Investigation process
   - Confidentiality provisions
   - Anti-retaliation statement

5. **Meal Break Policy** (Labor Code §512)
   - 30-minute unpaid meal break before end of 5th hour
   - Second meal break before end of 10th hour
   - Waiver provisions
   - Premium pay for violations

6. **Rest Break Policy** (Labor Code §226.7)
   - 10-minute paid rest break per 4 hours worked
   - Timing requirements
   - Premium pay for violations

7. **Overtime Policy** (Labor Code §510)
   - Time-and-a-half after 8 hours/day or 40 hours/week
   - Double-time after 12 hours/day
   - 7th day overtime rules

8. **Paid Sick Leave** (Labor Code §246)
   - Accrual requirements (1 hour per 30 hours worked)
   - Usage rights (employee, family member, designated person)
   - Covered reasons including safe time

9. **California Family Rights Act (CFRA)** (Gov. Code §12945.2)
   - 12 weeks protected leave for eligible employees
   - Covered reasons: bonding, serious health condition, military exigency
   - Job restoration rights

10. **Pregnancy Disability Leave (PDL)** (Gov. Code §12945)
    - Up to 4 months leave for pregnancy-related disability
    - Reasonable accommodation requirements
    - No minimum service requirement

11. **Wage Statement Requirements** (Labor Code §226)
    - Required information on pay stubs
    - Sick leave balance disclosure
    - Employee access to records

12. **Personnel Records Access** (Labor Code §1198.5)
    - Employee right to inspect personnel files
    - Timing requirements (within 30 days)
    - Representative designation rights

13. **Expense Reimbursement** (Labor Code §2802)
    - Reimbursement for necessary business expenses
    - Covers mileage, cell phone, tools, supplies

14. **PAGA Notice** (Labor Code §2699)
    - Notice of Private Attorneys General Act rights
    - Employee right to file representative claims

15. **Lactation Accommodation** (Labor Code §1031)
    - Break time for expressing milk
    - Private space requirements
    - Anti-retaliation protections

16. **Whistleblower Protection** (Labor Code §1102.5)
    - Protection for reporting legal violations
    - Covers internal and external reporting
    - Anti-retaliation provisions

17. **Anti-Retaliation Policy** (Labor Code §98.6)
    - Prohibition on retaliation for exercising rights
    - Covers wage complaints, leave requests, complaints

18. **AI/Automated Decision Systems Policy** (SB 1001 - effective 2026)
    - Disclosure of AI use in employment decisions
    - Transparency requirements
    - Employee rights regarding automated systems

19. **Emergency Contact Designation** (SB 294 - effective 2026)
    - Allow employees to designate emergency contacts
    - Notification procedures during emergencies
    - Confidentiality protections

20. **Workers' Rights Notice** (SB 294 - effective 2026)
    - Comprehensive notice of employee rights
    - Wage/hour protections
    - Safety and anti-discrimination rights
"""
    
    return checklist

# Test function
if __name__ == "__main__":
    checklist = get_checklist()
    print(checklist)
    print(f"\n✅ Checklist loaded: {len(checklist)} characters")