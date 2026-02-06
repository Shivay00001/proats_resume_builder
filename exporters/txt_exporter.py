
from exporters.base_exporter import BaseExporter
from models.resume_data import ResumeData

class TxtExporter(BaseExporter):
    def export(self, data: ResumeData, output_path: str):
        lines = []
        
        # Header
        lines.append(data.full_name.upper())
        lines.append("=" * len(data.full_name))
        contact = [c for c in [data.email, data.phone, data.location, data.linkedin, data.portfolio] if c]
        lines.append(" | ".join(contact))
        lines.append("")
        
        # Summary
        if data.summary:
            lines.append("PROFESSIONAL SUMMARY")
            lines.append("-" * 20)
            lines.append(data.summary)
            lines.append("")
        
        # Skills
        if data.skills:
            lines.append("SKILLS")
            lines.append("-" * 20)
            # Grouping simple list
            lines.append(", ".join(data.skills))
            lines.append("")
            
        # Experience
        if data.experience:
            lines.append("WORK EXPERIENCE")
            lines.append("-" * 20)
            for job in data.experience:
                lines.append(f"{job.title.upper()} | {job.company}")
                lines.append(f"{job.start_date} - {job.end_date}")
                
                bullets = [b.strip() for b in job.responsibilities.split('\n') if b.strip()]
                for b in bullets:
                    lines.append(f"* {b}")
                lines.append("")

        # Projects
        if data.projects:
            lines.append("PROJECTS")
            lines.append("-" * 20)
            for proj in data.projects:
                lines.append(f"{proj.name.upper()} | {proj.tech_stack}")
                desc_bullets = [b.strip() for b in proj.description.split('\n') if b.strip()]
                for b in desc_bullets:
                    lines.append(f"* {b}")
                if proj.link:
                    lines.append(f"Link: {proj.link}")
                lines.append("")

        # Education
        if data.education:
            lines.append("EDUCATION")
            lines.append("-" * 20)
            for edu in data.education:
                lines.append(f"{edu.institution}")
                lines.append(f"{edu.degree} ({edu.start_date} - {edu.end_date})")
                if edu.gpa:
                    lines.append(f"GPA: {edu.gpa}")
                lines.append("")
        
        # Certifications
        if data.certifications:
            lines.append("CERTIFICATIONS")
            lines.append("-" * 20)
            for cert in data.certifications:
                if cert.strip():
                    lines.append(f"* {cert.strip()}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
