
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from models.resume_data import ResumeData
from ui.form_panels import ExperienceForm, ProjectForm, EducationForm, SectionFrame
from ui.preview_panel import PreviewPanel
from exporters.txt_exporter import TxtExporter
from exporters.docx_exporter import DocxExporter
from exporters.pdf_exporter import PdfExporter
from utils.ats_rules import calculate_ats_score

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas

class ProATSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ProATS Resume Builder - Professional & Compliant")
        self.geometry("1400x900")
        
        # State
        self.exp_forms = []
        self.proj_forms = []
        self.edu_forms = []
        self.profile_image_path = None

        # Layout
        self.paned = ttk.PanedWindow(self, orient="horizontal")
        self.paned.pack(fill="both", expand=True)
        
        # Left: Form
        self.left_frame = ttk.Frame(self.paned, width=800)
        self.paned.add(self.left_frame, weight=3)
        
        self.form_container = ScrollableFrame(self.left_frame)
        self.form_container.pack(fill="both", expand=True)
        self.form = self.form_container.scrollable_frame
        
        # Right: Preview & Actions
        self.right_frame = ttk.Frame(self.paned, width=500)
        self.paned.add(self.right_frame, weight=1)
        
        self._build_form()
        self._build_sidebar()
        
        # Scroll binding
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.form_container.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _build_form(self):
        # 0. Profile Image
        f_img = SectionFrame(self.form, "Profile Image (Optional)")
        self.lbl_img_path = ttk.Label(f_img, text="No image selected")
        self.lbl_img_path.pack(side="left", padx=5)
        ttk.Button(f_img, text="Select Image", command=self._select_image).pack(side="left")

        # 1. Personal Info
        f_info = SectionFrame(self.form, "Personal Information")
        self.entries = {}
        fields = [("Full Name", "full_name"), ("Email", "email"), ("Phone", "phone"), 
                  ("Location", "location"), ("LinkedIn", "linkedin"), ("Portfolio", "portfolio")]
        
        for i, (lbl, key) in enumerate(fields):
            r = i // 2
            c = (i % 2) * 2
            ttk.Label(f_info, text=lbl).grid(row=r, column=c, sticky="w", padx=5, pady=2)
            e = ttk.Entry(f_info, width=30)
            e.grid(row=r, column=c+1, sticky="w", padx=5, pady=2)
            self.entries[key] = e
            
        # 2. Summary
        f_sum = SectionFrame(self.form, "Professional Summary")
        self.t_summary = tk.Text(f_sum, height=4, width=80)
        self.t_summary.pack(fill="x", padx=5, pady=5)
        
        # 3. Skills
        f_skills = SectionFrame(self.form, "Skills (Comma Separated)")
        self.t_skills = tk.Text(f_skills, height=3, width=80)
        self.t_skills.pack(fill="x", padx=5, pady=5)
        
        # 4. Experience
        f_exp = SectionFrame(self.form, "Work Experience")
        self.exp_container = ttk.Frame(f_exp)
        self.exp_container.pack(fill="x")
        ttk.Button(f_exp, text="+ Add Job", command=self._add_job).pack(anchor="w", pady=5)
        self._add_job() # Default
        
        # 5. Projects
        f_proj = SectionFrame(self.form, "Projects")
        self.proj_container = ttk.Frame(f_proj)
        self.proj_container.pack(fill="x")
        ttk.Button(f_proj, text="+ Add Project", command=self._add_project).pack(anchor="w", pady=5)
        
        # 6. Education
        f_edu = SectionFrame(self.form, "Education")
        self.edu_container = ttk.Frame(f_edu)
        self.edu_container.pack(fill="x")
        ttk.Button(f_edu, text="+ Add Education", command=self._add_education).pack(anchor="w", pady=5)
        self._add_education()
        
        # 7. Certifications
        f_cert = SectionFrame(self.form, "Certifications (One per line)")
        self.t_certs = tk.Text(f_cert, height=3, width=80)
        self.t_certs.pack(fill="x", padx=5, pady=5)

    def _build_sidebar(self):
        # Actions
        f_actions = ttk.LabelFrame(self.right_frame, text="Design & Export")
        f_actions.pack(fill="x", padx=10, pady=10)
        
        # Design Style
        ttk.Label(f_actions, text="Design Style:").pack(anchor="w", padx=5)
        self.style_var = tk.StringVar(value="Quartz")
        ttk.Combobox(f_actions, textvariable=self.style_var, 
                    values=["Quartz", "Obsidian", "Glacier", "Onyx", "Executive"], state="readonly").pack(fill="x", padx=5, pady=2)
        
        # Theme Color
        ttk.Label(f_actions, text="Accent Color:").pack(anchor="w", padx=5)
        self.color_var = tk.StringVar(value="Navy")
        ttk.Combobox(f_actions, textvariable=self.color_var, 
                    values=["Navy", "Emerald", "Forest", "Crimson", "Charcoal", "Violet", "Blue"], state="readonly").pack(fill="x", padx=5, pady=2)
        
        ttk.Separator(f_actions, orient="horizontal").pack(fill="x", pady=10)
        
        ttk.Button(f_actions, text="Refresh Preview & Score", command=self._refresh_preview).pack(fill="x", padx=5, pady=5)
        
        ttk.Separator(f_actions, orient="horizontal").pack(fill="x", pady=5)
        
        ttk.Button(f_actions, text="Export PDF", command=lambda: self._export('pdf')).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_actions, text="Export DOCX", command=lambda: self._export('docx')).pack(fill="x", padx=5, pady=2)
        ttk.Button(f_actions, text="Export TXT", command=lambda: self._export('txt')).pack(fill="x", padx=5, pady=2)

        ttk.Separator(f_actions, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(f_actions, text="Contact Support", command=self._open_support).pack(fill="x", padx=5, pady=5)

        # Score
        self.lbl_score = ttk.Label(self.right_frame, text="ATS Score: - / 100", font=("Arial", 16, "bold"))
        self.lbl_score.pack(pady=10)
        
        self.list_feedback = tk.Listbox(self.right_frame, height=6)
        self.list_feedback.pack(fill="x", padx=10)

        # Preview
        self.preview_panel = PreviewPanel(self.right_frame)

    def _open_support(self):
        # Support Dialog
        top = tk.Toplevel(self)
        top.title("Contact Support")
        top.geometry("400x300")
        
        ttk.Label(top, text="Send us a message", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Label(top, text="Your Email:").pack(anchor="w", padx=20)
        e_email = ttk.Entry(top, width=40)
        e_email.pack(padx=20, pady=2)
        
        ttk.Label(top, text="Message:").pack(anchor="w", padx=20)
        t_msg = tk.Text(top, height=5, width=40)
        t_msg.pack(padx=20, pady=2)
        
        def send():
            email = e_email.get()
            msg = t_msg.get("1.0", "end-1c")
            if not email or not msg.strip():
                messagebox.showerror("Error", "Email and Message are required.")
                return
            
            try:
                import urllib.request
                import json
                
                url = "https://formspree.io/f/mdkyoyna"
                data = json.dumps({"email": email, "message": msg}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        messagebox.showinfo("Sent", "Support request sent successfully!")
                        top.destroy()
                    else:
                        messagebox.showerror("Error", f"Failed with status: {response.status}")
                        
            except Exception as e:
                 messagebox.showerror("Error", f"Failed to send: {e}")

        ttk.Button(top, text="Send Message", command=send).pack(pady=15)

    # Dynamic Form Helpers
    def _add_job(self):
        f = ExperienceForm(self.exp_container, delete_cb=lambda x: self._remove_form(x, self.exp_forms))
        self.exp_forms.append(f)
    
    def _add_project(self):
        f = ProjectForm(self.proj_container, delete_cb=lambda x: self._remove_form(x, self.proj_forms))
        self.proj_forms.append(f)
        
    def _add_education(self):
        f = EducationForm(self.edu_container, delete_cb=lambda x: self._remove_form(x, self.edu_forms))
        self.edu_forms.append(f)
        
    def _remove_form(self, form_widget, list_ref):
        form_widget.destroy()
        if form_widget in list_ref:
            list_ref.remove(form_widget)

    def _select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if path:
            self.profile_image_path = path
            self.lbl_img_path.config(text=os.path.basename(path))

    def _collect_data(self) -> ResumeData:
        data = ResumeData()
        data.full_name = self.entries['full_name'].get().strip()
        data.email = self.entries['email'].get().strip()
        data.phone = self.entries['phone'].get().strip()
        data.location = self.entries['location'].get().strip()
        data.linkedin = self.entries['linkedin'].get().strip()
        data.portfolio = self.entries['portfolio'].get().strip()
        
        data.items = [] # Wait, dataclass doesn't have items.
        
        data.summary = self.t_summary.get("1.0", "end-1c").strip()
        
        raw_skills = self.t_skills.get("1.0", "end-1c").strip()
        data.skills = [s.strip() for s in raw_skills.split(',') if s.strip()]
        
        data.experience = [f.get_data() for f in self.exp_forms]
        data.projects = [f.get_data() for f in self.proj_forms]
        data.education = [f.get_data() for f in self.edu_forms]
        
        certs = self.t_certs.get("1.0", "end-1c").strip().split('\n')
        data.certifications = [c for c in certs if c.strip()]
        
        data.profile_image_path = self.profile_image_path
        
        # Style
        data.design_style = self.style_var.get()
        data.theme_color = self.color_var.get()
        
        return data

    def _refresh_preview(self):
        data = self._collect_data()
        self.preview_panel.update_preview(data)
        
        score, feedback = calculate_ats_score(data)
        self.lbl_score.config(text=f"ATS Score: {score} / 100", foreground="green" if score > 75 else "red")
        
        self.list_feedback.delete(0, "end")
        for f in feedback:
            self.list_feedback.insert("end", f)

    def _export(self, fmt):
        data = self._collect_data()
        # template = self.template_var.get() # Handled by data now
        
        if not data.full_name:
            messagebox.showerror("Error", "Full Name is required!")
            return

        file_types = {
            'pdf': ("PDF Document", "*.pdf"),
            'docx': ("Word Document", "*.docx"),
            'txt': ("Text File", "*.txt")
        }
        
        path = filedialog.asksaveasfilename(defaultextension=f".{fmt}", filetypes=[file_types[fmt]], initialfile=f"Resume_{data.full_name.replace(' ', '_')}")
        
        if path:
            try:
                if fmt == 'txt':
                    TxtExporter().export(data, path)
                elif fmt == 'docx':
                    DocxExporter().export(data, path)
                elif fmt == 'pdf':
                    PdfExporter().export(data, path)
                
                messagebox.showinfo("Success", f"Exported to {path}")
            except Exception as e:
                messagebox.showerror("Export Failed", str(e))
                # raise e # Uncomment for debug

if __name__ == "__main__":
    app = ProATSApp()
    app.mainloop()
