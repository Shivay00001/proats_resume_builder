
from exporters.base_exporter import BaseExporter
from models.resume_data import ResumeData
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

class DocxExporter(BaseExporter):
    def __init__(self):
        # Color Map
        self.colors = {
            "Navy": RGBColor(0x00, 0x1F, 0x3F),
            "Emerald": RGBColor(0x2E, 0xCC, 0x71), # Slightly darker for print? 2ECC71 is bright. Let's go decent green
            "Forest": RGBColor(0x11, 0x7A, 0x65),
            "Crimson": RGBColor(0x92, 0x2B, 0x21),
            "Charcoal": RGBColor(0x21, 0x2F, 0x3D),
            "Violet": RGBColor(0x5B, 0x2C, 0x6F),
            "Blue": RGBColor(0x2E, 0x86, 0xC1)
        }
        self.white = RGBColor(0xFF, 0xFF, 0xFF)
        self.black = RGBColor(0x00, 0x00, 0x00)

    def _get_color(self, name):
        return self.colors.get(name, self.colors["Navy"])

    def _set_shading(self, paragraph, color_hex):
        """
        Apply background shading to a paragraph (XML hack).
        color_hex: string like "001F3F" (no hash)
        """
        p = paragraph._p
        pPr = p.get_or_add_pPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), color_hex)
        pPr.append(shd)

    def _add_border(self, paragraph, side='bottom', sz='6'):
        p = paragraph._p
        pPr = p.get_or_add_pPr()
        pBdr = pPr.find(qn('w:pBdr'))
        if pBdr is None:
            pBdr = OxmlElement('w:pBdr')
            pPr.append(pBdr)
        
        bdr = OxmlElement(f'w:{side}')
        bdr.set(qn('w:val'), 'single')
        bdr.set(qn('w:sz'), sz)
        bdr.set(qn('w:space'), '1')
        bdr.set(qn('w:color'), 'auto')
        pBdr.append(bdr)

    def export(self, data: ResumeData, output_path: str):
        doc = Document()
        style_name = data.design_style
        primary_color_obj = self._get_color(data.theme_color)
        primary_hex = "{:02x}{:02x}{:02x}".format(primary_color_obj.r, primary_color_obj.g, primary_color_obj.b)
        
        # Base Font settings
        style = doc.styles['Normal']
        font = style.font
        font.name = "Calibri" if style_name in ["Glacier", "Quartz"] else "Arial"
        if style_name == "Executive": font.name = "Cambria"
        font.size = Pt(11)

        # Margins
        section = doc.sections[0]
        margin_size = 0.75 if style_name in ["Glacier", "Onyx"] else 1.0
        section.top_margin = Inches(margin_size)
        section.bottom_margin = Inches(margin_size)
        section.left_margin = Inches(margin_size)
        section.right_margin = Inches(margin_size)

        # --- HEADER BLOCK ---
        if style_name == "Obsidian":
            # Dark Header Background
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._set_shading(p, primary_hex)
            
            run = p.add_run(f"\n{data.full_name.upper()}\n")
            run.bold = True
            run.font.size = Pt(24)
            run.font.color.rgb = self.white
            
            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._set_shading(p2, primary_hex)
            parts = [c for c in [data.location, data.phone, data.email, data.linkedin, data.portfolio] if c]
            r2 = p2.add_run(" | ".join(parts) + "\n")
            r2.font.color.rgb = self.white
            r2.font.size = Pt(10)
            
        else: # Standard layout
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if style_name == "Quartz" else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(data.full_name.upper())
            run.bold = True
            run.font.size = Pt(26 if style_name == "Executive" else 22)
            run.font.color.rgb = primary_color_obj
            
            p2 = doc.add_paragraph()
            p2.alignment = WD_ALIGN_PARAGRAPH.CENTER if style_name == "Quartz" else WD_ALIGN_PARAGRAPH.LEFT
            parts = [c for c in [data.location, data.phone, data.email, data.linkedin, data.portfolio] if c]
            r2 = p2.add_run(" | ".join(parts))
            r2.font.size = Pt(10)
            p2.paragraph_format.space_after = Pt(12)

        # --- HELPER FOR SECTIONS ---
        def add_section_title(text):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            
            if style_name == "Glacier":
                # Shaded Bar
                self._set_shading(p, "EAECEE") # Light Grey/Blue
                r = p.add_run(f"  {text.upper()}") # Indent slightly
                r.bold = True
                r.font.color.rgb = primary_color_obj
                r.font.size = Pt(12)
            elif style_name == "Onyx":
                # Bordered Box look (Top and Bottom border imply box)
                self._add_border(p, 'bottom')
                self._add_border(p, 'top')
                r = p.add_run(text.upper())
                r.bold = True
                r.font.color.rgb = primary_color_obj
                r.font.size = Pt(14)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif style_name == "Obsidian":
                 # Simple bold with color
                r = p.add_run(text.upper())
                r.bold = True
                r.font.color.rgb = primary_color_obj
                r.font.size = Pt(12)
                self._add_border(p, 'bottom')
            else: # Quartz/Default
                r = p.add_run(text.upper())
                r.bold = True
                r.font.size = Pt(12)
                # No color, strictly black classic? Or use theme? Use theme for "Pop".
                r.font.color.rgb = primary_color_obj
                if style_name == "Executive":
                    self._add_border(p, 'bottom', '12') # Thicker line

        # Add sections
        if data.summary:
            add_section_title("Professional Summary")
            doc.add_paragraph(data.summary)

        if data.skills:
            add_section_title("Skills")
            doc.add_paragraph(", ".join(data.skills))

        # Experience (Tab Stop Logic)
        if data.experience:
            add_section_title("Work Experience")
            for job in data.experience:
                max_width = 8.5 - (doc.sections[0].left_margin.inches * 2)
                p = doc.add_paragraph()
                
                # Title
                r = p.add_run(job.title)
                r.bold = True
                r.font.size = Pt(11)
                
                # Date (Right aligned)
                p.paragraph_format.tab_stops.add_tab_stop(Inches(max_width), WD_TAB_ALIGNMENT.RIGHT)
                r2 = p.add_run(f"\t{job.start_date} - {job.end_date}")
                r2.bold = True
                
                # Company (Below)
                p2 = doc.add_paragraph()
                p2.paragraph_format.space_after = Pt(2)
                r3 = p2.add_run(job.company)
                r3.italic = True
                r3.font.color.rgb = primary_color_obj # Make company color match theme? nice touch.
                
                # Bullets
                bullets = [b.strip() for b in job.responsibilities.split('\n') if b.strip()]
                for b in bullets:
                    pb = doc.add_paragraph(b, style='List Bullet')
                    pb.paragraph_format.space_after = Pt(0)
                
                doc.add_paragraph().paragraph_format.space_after = Pt(4)

        if data.projects:
            add_section_title("Projects")
            for proj in data.projects:
                p = doc.add_paragraph()
                r = p.add_run(proj.name)
                r.bold = True
                
                if proj.tech_stack:
                    p.add_run(f" | {proj.tech_stack}")
                
                 # Bullets
                bullets = [b.strip() for b in proj.description.split('\n') if b.strip()]
                for b in bullets:
                   pb = doc.add_paragraph(b, style='List Bullet')
                   pb.paragraph_format.space_after = Pt(0)
                doc.add_paragraph().paragraph_format.space_after = Pt(4)

        if data.education:
            add_section_title("Education")
            for edu in data.education:
                max_width = 8.5 - (doc.sections[0].left_margin.inches * 2)
                p = doc.add_paragraph()
                p.add_run(edu.institution).bold = True
                p.paragraph_format.tab_stops.add_tab_stop(Inches(max_width), WD_TAB_ALIGNMENT.RIGHT)
                p.add_run(f"\t{edu.start_date} - {edu.end_date}")
                
                p2 = doc.add_paragraph(edu.degree)
                if edu.gpa: p2.add_run(f" | GPA: {edu.gpa}")
                p2.paragraph_format.space_after = Pt(6)

        if data.certifications:
            add_section_title("Certifications")
            for cert in data.certifications:
                 doc.add_paragraph(cert, style='List Bullet')

        doc.save(output_path)
