
import tkinter as tk
from tkinter import ttk
from models.resume_data import ResumeData

class PreviewPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        
        ttk.Label(self, text="Live Plain Text Validation (Simulates ATS Read)", font=("Arial", 10, "bold")).pack(pady=5)
        
        self.text_area = tk.Text(self, font=("Courier New", 10), wrap="word")
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)
        
    def update_preview(self, data: ResumeData):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", "end")
        
        # We can reuse TxtExporter logic or just do a quick dump here
        # Quick dump logic for speed
        lines = []
        lines.append(f"NAME: {data.full_name}")
        lines.append(f"CONTACT: {data.email} | {data.phone} | {data.location}")
        lines.append("-" * 40)
        lines.append(f"SUMMARY: {data.summary}")
        lines.append("-" * 40)
        lines.append(f"SKILLS: {', '.join(data.skills)}")
        lines.append("-" * 40)
        lines.append("EXPERIENCE:")
        for job in data.experience:
            lines.append(f"* {job.title} at {job.company} ({job.start_date}-{job.end_date})")
        
        self.text_area.insert("1.0", "\n".join(lines))
        self.text_area.config(state="disabled")
