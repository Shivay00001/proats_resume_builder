
from exporters.base_exporter import BaseExporter
from models.resume_data import ResumeData
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import os

class PdfExporter(BaseExporter):
    def __init__(self):
        # Colors
        self.colors = {
            "Navy": colors.navy,
            "Emerald": colors.Color(0.18, 0.8, 0.44),
            "Forest": colors.Color(0.06, 0.47, 0.39),
            "Crimson": colors.Color(0.57, 0.16, 0.12),
            "Charcoal": colors.Color(0.12, 0.18, 0.23),
            "Violet": colors.Color(0.35, 0.17, 0.43),
            "Blue": colors.Color(0.18, 0.52, 0.75)
        }
    
    def _get_color(self, name):
        return self.colors.get(name, colors.navy)
        
    def export(self, data: ResumeData, output_path: str):
        style_name = data.design_style
        primary_color = self._get_color(data.theme_color)
        
        # Margins
        margin = 0.5 * inch if style_name in ["Glacier", "Onyx"] else 0.75 * inch
        doc = SimpleDocTemplate(
            output_path,
            pagesize=LETTER,
            rightMargin=margin, leftMargin=margin,
            topMargin=margin if style_name != "Obsidian" else 0, # Top 0 for full bleed header
            bottomMargin=margin
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Fonts
        font_main = "Helvetica"
        if style_name == "Executive": font_main = "Times-Roman"
        font_bold = f"{font_main}-Bold"
        
        # Styles
        s_body = ParagraphStyle('Body', parent=styles['Normal'], fontName=font_main, fontSize=11, spaceAfter=2)
        s_bullet = ParagraphStyle('Bullet', parent=s_body, leftIndent=15, bulletIndent=5, spaceAfter=1, bulletText='•')
        
        # --- HEADER ---
        if style_name == "Obsidian":
            # Full Bleed Dark Header using Table
            # Need to push content into a Table with background
            s_u_name = ParagraphStyle('UName', parent=styles['Normal'], fontName=font_bold, fontSize=24, alignment=TA_CENTER, textColor=colors.white)
            s_u_contact = ParagraphStyle('UContact', parent=styles['Normal'], fontName=font_main, fontSize=10, alignment=TA_CENTER, textColor=colors.lightgrey)
            
            parts = [c for c in [data.location, data.phone, data.email, data.linkedin] if c]
            
            # 2 Rows: Name, Contact
            # Padding needed
            header_data = [
                [Paragraph(data.full_name.upper(), s_u_name)],
                [Paragraph(" | ".join(parts), s_u_contact)]
            ]
            t = Table(header_data, colWidths=[7.5*inch]) # Full width approx
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), primary_color),
                ('TOPPADDING', (0,0), (-1,-1), 30),
                ('BOTTOMPADDING', (0,0), (-1,-1), 30),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')
            ]))
            story.append(t)
            story.append(Spacer(1, 20))
            
        else: # Standard Headers
            doc.topMargin = margin # Reset margin if not Obsidian override
            align = TA_CENTER if style_name == "Quartz" else TA_LEFT
            s_name = ParagraphStyle('Name', parent=styles['Normal'], fontName=font_bold, fontSize=24, alignment=align, textColor=primary_color, spaceAfter=6)
            s_contact = ParagraphStyle('Contact', parent=styles['Normal'], fontName=font_main, fontSize=10, alignment=align, textColor=colors.darkgrey, spaceAfter=12)
            
            story.append(Paragraph(data.full_name.upper(), s_name))
            parts = [c for c in [data.location, data.phone, data.email, data.linkedin] if c]
            story.append(Paragraph(" | ".join(parts), s_contact))
            
            if style_name == "Onyx":
                # Add a Line
                pass # Drawing line is complex, skipping for simplicity

        # --- SECTIONS ---
        def add_section_header(text):
            if style_name == "Glacier":
                # Shaded Bar
                s_h = ParagraphStyle('H', parent=styles['Normal'], fontName=font_bold, fontSize=12, textColor=primary_color, backColor=colors.whitesmoke, borderPadding=5)
                story.append(Paragraph(text.upper(), s_h))
                story.append(Spacer(1, 6))
            elif style_name == "Obsidian":
                s_h = ParagraphStyle('H', parent=styles['Normal'], fontName=font_bold, fontSize=12, textColor=primary_color, spaceBefore=12, spaceAfter=6)
                story.append(Paragraph(text.upper(), s_h))
                # Add a manual underline via Drawing? ReportLab Paragraphs have textDecoration but not Borders easily.
                # Use Table with bottom border.
                t = Table([[Paragraph("", s_h)]], colWidths=[100]) # Fake line?
                # Actually, easier to just accept bold color for now given constraints.
                
            else:
                s_h = ParagraphStyle('H', parent=styles['Normal'], fontName=font_bold, fontSize=12, textColor=primary_color, spaceBefore=12, spaceAfter=6)
                story.append(Paragraph(text.upper(), s_h))

        # Content
        if data.summary:
            add_section_header("Professional Summary")
            story.append(Paragraph(data.summary, s_body))
            
        if data.skills:
            add_section_header("Skills")
            story.append(Paragraph(", ".join(data.skills), s_body))
            
        if data.experience:
            add_section_header("Work Experience")
            for job in data.experience:
                # 2-Column Table for Layout (Title ... Dates)
                s_left = ParagraphStyle('L', parent=s_body, fontName=font_bold, fontSize=11)
                s_right = ParagraphStyle('R', parent=s_body, alignment=TA_RIGHT, fontSize=11)
                
                # Calculate widths based on margins roughly
                w = 7.5 * inch # approx usable width?
                t = Table([[Paragraph(job.title, s_left), Paragraph(f"{job.start_date} - {job.end_date}", s_right)]], colWidths=[None, 1.5*inch])
                t.setStyle(TableStyle([
                    ('ALIGN', (1,0), (1,0), 'RIGHT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('LEFTPADDING', (0,0), (-1,-1), 0),
                    ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ]))
                story.append(t)
                
                s_comp = ParagraphStyle('C', parent=s_body, fontName=f"{font_main}-Oblique", textColor=primary_color)
                story.append(Paragraph(job.company, s_comp))
                
                bullets = [b.strip() for b in job.responsibilities.split('\n') if b.strip()]
                for b in bullets:
                    story.append(Paragraph(b, s_bullet))
                story.append(Spacer(1, 6))

        if data.projects:
            add_section_header("Projects")
            for proj in data.projects:
                story.append(Paragraph(f"<b>{proj.name}</b>", s_body))
                bullets = [b.strip() for b in proj.description.split('\n') if b.strip()]
                for b in bullets:
                    story.append(Paragraph(b, s_bullet))
                story.append(Spacer(1, 6))
                
        if data.education:
            add_section_header("Education")
            for edu in data.education:
                 t = Table([[Paragraph(edu.institution, ParagraphStyle('B', parent=s_body, fontName=font_bold)), 
                             Paragraph(f"{edu.start_date} - {edu.end_date}", ParagraphStyle('R', parent=s_body, alignment=TA_RIGHT))]])
                 t.setStyle(TableStyle([('ALIGN', (1,0), (1,0), 'RIGHT'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
                 story.append(t)
                 story.append(Paragraph(edu.degree, s_body))
                 story.append(Spacer(1, 6))
                 
        if data.certifications:
             add_section_header("Certifications")
             for cert in data.certifications:
                 story.append(Paragraph(cert, s_bullet))

        doc.build(story)
