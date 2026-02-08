from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from datetime import datetime
import re

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles."""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#2c5aa0'),
            spaceBefore=24,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Item header
        self.styles.add(ParagraphStyle(
            name='ItemHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#1a1a1a'),
            spaceBefore=16,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Executive summary style
        self.styles.add(ParagraphStyle(
            name='ExecutiveSummary',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=16
        ))
        
        # Table cell text (for wrapping in tables)
        self.styles.add(ParagraphStyle(
            name='TableCell',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica',
            alignment=TA_LEFT
        ))
        
        # Table cell label (bold)
        self.styles.add(ParagraphStyle(
            name='TableCellBold',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Risk level styles for table cells
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskMedium',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.orange,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.green,
            fontName='Helvetica-Bold',
            alignment=TA_LEFT
        ))
        
        # Risk level styles for critical issues section
        self.styles.add(ParagraphStyle(
            name='HighRisk',
            parent=self.styles['Normal'],
            textColor=colors.red,
            fontSize=11,
            fontName='Helvetica-Bold',
            leftIndent=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='MediumRisk',
            parent=self.styles['Normal'],
            textColor=colors.orange,
            fontSize=11,
            fontName='Helvetica-Bold',
            leftIndent=20
        ))
        
        self.styles.add(ParagraphStyle(
            name='LowRisk',
            parent=self.styles['Normal'],
            textColor=colors.green,
            fontSize=11,
            fontName='Helvetica-Bold',
            leftIndent=20
        ))
    
    def _parse_analysis(self, analysis_text):
        """Parse the Claude analysis into structured data."""
        
        # Pattern to match the exact format Claude is outputting
        item_pattern = r'###\s*(\d+)\.\s*(.+?)\s*\((.+?)\)\s*-\s*\*\*Status\*\*:\s*(.+?)\s*-\s*\*\*Pages\*\*:\s*(.+?)\s*-\s*\*\*Assessment\*\*:\s*(.+?)\s*-\s*\*\*Risk Level\*\*:\s*(.+?)\s*-\s*\*\*Recommendation\*\*:\s*(.+?)\s*-\s*\*\*Legal Citation\*\*:\s*(.+?)(?=\n###|\n---|\n##|\Z)'
        
        items = []
        for match in re.finditer(item_pattern, analysis_text, re.DOTALL):
            items.append({
                'number': match.group(1).strip(),
                'title': match.group(2).strip(),
                'code': match.group(3).strip(),
                'status': match.group(4).strip(),
                'pages': match.group(5).strip(),
                'assessment': match.group(6).strip(),
                'risk': match.group(7).strip(),
                'recommendation': match.group(8).strip(),
                'citation': match.group(9).strip()
            })
        
        # Calculate accurate counts from parsed items
        compliant_count = 0
        partial_count = 0
        noncompliant_count = 0
        
        for item in items:
            status_lower = item['status'].lower()
            assessment_lower = item['assessment'].lower()
            
            # Check status and assessment for compliance
            if 'present' in status_lower and 'compliant' in assessment_lower and 'non-compliant' not in assessment_lower and 'partially' not in assessment_lower:
                compliant_count += 1
            elif 'missing' in status_lower or 'non-compliant' in assessment_lower:
                noncompliant_count += 1
            else:
                partial_count += 1
        
        # Try to extract grade from analysis
        grade_match = re.search(r'(?:Overall Compliance Grade|Grade)[:\s]*\*?\*?\s*([A-F])', analysis_text, re.IGNORECASE)
        if not grade_match:
            grade_match = re.search(r'OVERALL COMPLIANCE GRADE:\s*([A-F])', analysis_text, re.IGNORECASE)
        
        summary = {
            'compliant': str(compliant_count),
            'partial': str(partial_count),
            'noncompliant': str(noncompliant_count),
            'total': str(len(items)),
            'grade': grade_match.group(1) if grade_match else 'N/A'
        }
        
        # Extract critical issues
        critical_section = re.search(r'##\s*SUMMARY OF CRITICAL ISSUES.*?\n(.*?)(?=\n##|\Z)', analysis_text, re.DOTALL | re.IGNORECASE)
        critical_issues = []
        if critical_section:
            for match in re.finditer(r'\d+\.\s*\*\*(.+?)\*\*\s*[-:]?\s*(.+?)(?=\n\d+\.|\n##|\Z)', critical_section.group(1), re.DOTALL):
                critical_issues.append({
                    'title': match.group(1).strip(),
                    'description': match.group(2).strip()
                })
        
        return {
            'items': items,
            'summary': summary,
            'critical_issues': critical_issues
        }
    
    def _generate_executive_summary(self, parsed):
        """Generate executive summary text based on parsed data."""
        
        total = int(parsed['summary']['total'])
        compliant = int(parsed['summary']['compliant'])
        noncompliant = int(parsed['summary']['noncompliant'])
        partial = int(parsed['summary']['partial'])
        grade = parsed['summary']['grade']
        
        # Calculate compliance percentage
        compliance_rate = int((compliant / total * 100)) if total > 0 else 0
        
        # Determine overall assessment
        if compliance_rate >= 90:
            overall = "excellent"
        elif compliance_rate >= 75:
            overall = "good"
        elif compliance_rate >= 60:
            overall = "fair"
        else:
            overall = "needs significant improvement"
        
        # Build summary paragraphs
        summary_text = f"""This handbook was analyzed against {total} California employment law requirements. 
The handbook demonstrates {overall} compliance with an overall grade of {grade}. """
        
        if compliant > 0:
            summary_text += f"{compliant} items are fully compliant. "
        
        if partial > 0:
            summary_text += f"{partial} items are partially compliant and may need updates. "
        
        if noncompliant > 0:
            summary_text += f"{noncompliant} items are non-compliant and require immediate attention to avoid legal exposure. "
        
        # Add critical issues mention
        if parsed['critical_issues']:
            critical_count = len(parsed['critical_issues'])
            summary_text += f"""

There are {critical_count} critical issues that pose high legal risk and should be addressed as a priority. 
These issues are detailed in the Critical Issues section below."""
        
        return summary_text
    
    def generate_report(self, analysis_text, handbook_name, output_path):
        """Generate a professional PDF report from the analysis."""
        
        # Parse the analysis
        parsed = self._parse_analysis(analysis_text)
        
        if not parsed or not parsed['items']:
            print(f"⚠️ Could not parse analysis structure. Items found: {len(parsed['items']) if parsed else 0}")
            print("Generating basic report...")
            self._generate_basic_report(analysis_text, handbook_name, output_path)
            return
        
        print(f"✅ Parsed {len(parsed['items'])} compliance items")
        print(f"   Compliant: {parsed['summary']['compliant']}, Partial: {parsed['summary']['partial']}, Non-compliant: {parsed['summary']['noncompliant']}")
        
        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # ============ TITLE PAGE ============
        story.append(Spacer(1, 0.5*inch))
        
        story.append(Paragraph(
            "California Employee Handbook",
            self.styles['CustomTitle']
        ))
        story.append(Paragraph(
            "Compliance Analysis Report",
            self.styles['CustomTitle']
        ))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Info box
        info_data = [
            [Paragraph('Handbook Analyzed:', self.styles['TableCellBold']), 
             Paragraph(handbook_name, self.styles['TableCell'])],
            [Paragraph('Analysis Date:', self.styles['TableCellBold']), 
             Paragraph(datetime.now().strftime('%B %d, %Y'), self.styles['TableCell'])],
            [Paragraph('Generated By:', self.styles['TableCellBold']), 
             Paragraph('Axiom Legal Workflow', self.styles['TableCell'])],
            [Paragraph('Compliance Grade:', self.styles['TableCellBold']), 
             Paragraph(parsed['summary']['grade'], self.styles['TableCell'])],
        ]
        
        t = Table(info_data, colWidths=[2.2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(t)
        story.append(Spacer(1, 0.4*inch))
        
        # ============ EXECUTIVE SUMMARY ============
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        exec_summary = self._generate_executive_summary(parsed)
        story.append(Paragraph(exec_summary, self.styles['ExecutiveSummary']))
        story.append(Spacer(1, 0.3*inch))
        
        # ============ COMPLIANCE SCORE ============
        story.append(Paragraph("Compliance Score", self.styles['SectionHeader']))
        
        # Big compliance score display
        total = int(parsed['summary']['total'])
        compliant = int(parsed['summary']['compliant'])
        compliance_rate = int((compliant / total * 100)) if total > 0 else 0
        
        score_text = f"<b>{compliant} out of {total} items compliant ({compliance_rate}%)</b>"
        story.append(Paragraph(score_text, self.styles['ExecutiveSummary']))
        story.append(Spacer(1, 0.2*inch))
        
        # Detailed breakdown table
        summary_data = [
            [Paragraph('Compliant Items', self.styles['TableCell']), 
             Paragraph(parsed['summary']['compliant'], self.styles['TableCellBold'])],
            [Paragraph('Partially Compliant Items', self.styles['TableCell']), 
             Paragraph(parsed['summary']['partial'], self.styles['TableCellBold'])],
            [Paragraph('Non-Compliant Items', self.styles['TableCell']), 
             Paragraph(parsed['summary']['noncompliant'], self.styles['TableCellBold'])],
            [Paragraph('Total Items Reviewed', self.styles['TableCell']), 
             Paragraph(parsed['summary']['total'], self.styles['TableCellBold'])]
        ]
        
        st = Table(summary_data, colWidths=[4*inch, 1.5*inch])
        st.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f4ea')),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#fff4e6')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#fce8e8')),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#e6f2ff')),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ]))
        
        story.append(st)
        story.append(Spacer(1, 0.3*inch))
        
        # ============ CRITICAL ISSUES ============
        if parsed['critical_issues']:
            story.append(Paragraph("⚠️ Critical Issues Requiring Immediate Attention", self.styles['SectionHeader']))
            
            story.append(Paragraph(
                f"The following {len(parsed['critical_issues'])} high-risk items require immediate remediation to avoid potential legal liability:",
                self.styles['CustomBody']
            ))
            story.append(Spacer(1, 0.1*inch))
            
            for idx, issue in enumerate(parsed['critical_issues'], 1):
                story.append(Paragraph(
                    f"<b>{idx}. {issue['title']}</b>",
                    self.styles['HighRisk']
                ))
                story.append(Paragraph(
                    issue['description'],
                    self.styles['CustomBody']
                ))
                story.append(Spacer(1, 12))
        else:
            story.append(Paragraph("✅ No Critical Issues", self.styles['SectionHeader']))
            story.append(Paragraph(
                "No high-risk compliance issues were identified. However, please review the detailed analysis for any medium-risk items that may require attention.",
                self.styles['CustomBody']
            ))
        
        story.append(PageBreak())
        
        # ============ DETAILED ANALYSIS ============
        story.append(Paragraph("Detailed Compliance Analysis", self.styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))
        
        for item in parsed['items']:
            # Item header
            header_text = f"{item['number']}. {item['title']}"
            story.append(Paragraph(header_text, self.styles['ItemHeader']))
            
            # Determine risk level style for color coding
            if 'High' in item['risk']:
                risk_style = self.styles['RiskHigh']
            elif 'Medium' in item['risk']:
                risk_style = self.styles['RiskMedium']
            else:
                risk_style = self.styles['RiskLow']
            
            # Create a clean info table with color-coded risk level
            item_data = [
                [Paragraph('Legal Citation:', self.styles['TableCellBold']), 
                 Paragraph(item['citation'], self.styles['TableCell'])],
                [Paragraph('Status:', self.styles['TableCellBold']), 
                 Paragraph(item['status'], self.styles['TableCell'])],
                [Paragraph('Found on Pages:', self.styles['TableCellBold']), 
                 Paragraph(item['pages'], self.styles['TableCell'])],
                [Paragraph('Risk Level:', self.styles['TableCellBold']), 
                 Paragraph(item['risk'], risk_style)],  # Use colored style here
            ]
            
            item_table = Table(item_data, colWidths=[1.5*inch, 4.8*inch])
            
            # Base table style
            base_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LINEBELOW', (0, 0), (-1, 2), 0.5, colors.HexColor('#e0e0e0')),
            ])
            
            item_table.setStyle(base_style)
            
            story.append(item_table)
            story.append(Spacer(1, 10))
            
            # Assessment section
            assessment_data = [
                [Paragraph('Assessment:', self.styles['TableCellBold']), 
                 Paragraph(item['assessment'], self.styles['TableCell'])],
            ]
            
            assessment_table = Table(assessment_data, colWidths=[1.5*inch, 4.8*inch])
            assessment_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            story.append(assessment_table)
            story.append(Spacer(1, 6))
            
            # Recommendation section
            recommendation_data = [
                [Paragraph('Recommendation:', self.styles['TableCellBold']), 
                 Paragraph(item['recommendation'], self.styles['TableCell'])],
            ]
            
            recommendation_table = Table(recommendation_data, colWidths=[1.5*inch, 4.8*inch])
            recommendation_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            
            story.append(recommendation_table)
            story.append(Spacer(1, 18))
        
        # Footer/Disclaimer
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(
            "<i>This analysis is provided for informational purposes only and does not constitute legal advice. "
            "Please consult with a qualified employment law attorney for specific legal guidance.</i>",
            self.styles['CustomBody']
        ))
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ Professional PDF report generated: {output_path}")
    
    def _generate_basic_report(self, analysis_text, handbook_name, output_path):
        """Fallback: Generate a basic report if parsing fails."""
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        story.append(Paragraph(
            "California Employee Handbook<br/>Compliance Analysis Report",
            self.styles['CustomTitle']
        ))
        story.append(Spacer(1, 0.3*inch))
        
        metadata = [
            [Paragraph('Handbook Analyzed:', self.styles['TableCellBold']), 
             Paragraph(handbook_name, self.styles['TableCell'])],
            [Paragraph('Analysis Date:', self.styles['TableCellBold']), 
             Paragraph(datetime.now().strftime('%B %d, %Y'), self.styles['TableCell'])],
            [Paragraph('Generated By:', self.styles['TableCellBold']), 
             Paragraph('Axiom Legal Workflow', self.styles['TableCell'])],
        ]
        
        t = Table(metadata, colWidths=[2*inch, 4*inch])
        t.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(t)
        story.append(PageBreak())
        
        # Raw analysis
        paragraphs = analysis_text.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Remove markdown symbols for cleaner display
                cleaned = para.replace('###', '').replace('**', '')
                story.append(Paragraph(cleaned, self.styles['CustomBody']))
                story.append(Spacer(1, 0.1*inch))
        
        doc.build(story)
        print(f"✅ Basic PDF report generated: {output_path}")

# Test function
if __name__ == "__main__":
    import sys
    
    # Load the analysis results
    with open("output/analysis_results.txt", "r", encoding="utf-8") as f:
        analysis = f.read()
    
    # Get handbook name from command line or try to extract from analysis
    if len(sys.argv) > 1:
        handbook_name = sys.argv[1]
    else:
        # Try to extract from the analysis text
        name_match = re.search(r'##\s*(.+?)\s*Employee Handbook', analysis)
        if name_match:
            handbook_name = f"{name_match.group(1).strip()} Employee Handbook"
        else:
            handbook_name = "Employee Handbook"
    
    # Generate report
    generator = ReportGenerator()
    generator.generate_report(
        analysis_text=analysis,
        handbook_name=handbook_name,
        output_path="output/compliance_report_professional.pdf"
    )
    
    print(f"\n✅ Open output/compliance_report_professional.pdf to see your professional report!")