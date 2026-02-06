
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from models.resume_data import Job, Project, Education

class SectionFrame(ttk.LabelFrame):
    def __init__(self, parent, title):
        super().__init__(parent, text=title)
        self.parent = parent
        self.pack(fill="x", padx=10, pady=5)

class ExperienceForm(ttk.Frame):
    def __init__(self, parent, job=None, delete_cb=None):
        super().__init__(parent)
        self.delete_cb = delete_cb
        self.pack(fill="x", pady=5)
        
        # Grid layout
        ttk.Label(self, text="Title:").grid(row=0, column=0, sticky="w")
        self.e_title = ttk.Entry(self, width=25)
        self.e_title.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(self, text="Company:").grid(row=0, column=2, sticky="w")
        self.e_comp = ttk.Entry(self, width=25)
        self.e_comp.grid(row=0, column=3, sticky="w", padx=5)
        
        ttk.Label(self, text="Dates:").grid(row=1, column=0, sticky="w")
        f_dates = ttk.Frame(self)
        f_dates.grid(row=1, column=1, columnspan=3, sticky="w")
        self.e_start = ttk.Entry(f_dates, width=12)
        self.e_start.pack(side="left")
        ttk.Label(f_dates, text=" to ").pack(side="left")
        self.e_end = ttk.Entry(f_dates, width=12)
        self.e_end.pack(side="left")

        ttk.Label(self, text="Responsibilities (Bullets):").grid(row=2, column=0, sticky="nw")
        self.t_resp = tk.Text(self, height=4, width=50)
        self.t_resp.grid(row=2, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        
        if delete_cb:
            ttk.Button(self, text="X", width=3, command=lambda: delete_cb(self)).grid(row=0, column=4)

    def get_data(self):
        return Job(
            title=self.e_title.get(),
            company=self.e_comp.get(),
            start_date=self.e_start.get(),
            end_date=self.e_end.get(),
            responsibilities=self.t_resp.get("1.0", "end-1c")
        )

class ProjectForm(ttk.Frame):
    def __init__(self, parent, delete_cb=None):
        super().__init__(parent)
        self.delete_cb = delete_cb
        self.pack(fill="x", pady=5)

        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        self.e_name = ttk.Entry(self, width=25)
        self.e_name.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(self, text="Tech:").grid(row=0, column=2, sticky="w")
        self.e_tech = ttk.Entry(self, width=25)
        self.e_tech.grid(row=0, column=3, sticky="w", padx=5)
        
        ttk.Label(self, text="Description:").grid(row=1, column=0, sticky="nw")
        self.t_desc = tk.Text(self, height=3, width=50)
        self.t_desc.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        
        if delete_cb:
            ttk.Button(self, text="X", width=3, command=lambda: delete_cb(self)).grid(row=0, column=4)

    def get_data(self):
        return Project(
            name=self.e_name.get(),
            tech_stack=self.e_tech.get(),
            description=self.t_desc.get("1.0", "end-1c")
        )

class EducationForm(ttk.Frame):
    def __init__(self, parent, delete_cb=None):
        super().__init__(parent)
        self.delete_cb = delete_cb
        self.pack(fill="x", pady=5)
        
        ttk.Label(self, text="School:").grid(row=0, column=0, sticky="w")
        self.e_school = ttk.Entry(self, width=25)
        self.e_school.grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(self, text="Degree:").grid(row=0, column=2, sticky="w")
        self.e_degree = ttk.Entry(self, width=25)
        self.e_degree.grid(row=0, column=3, sticky="w", padx=5)
        
        ttk.Label(self, text="Dates:").grid(row=1, column=0, sticky="w")
        f_dates = ttk.Frame(self)
        f_dates.grid(row=1, column=1, columnspan=3, sticky="w")
        self.e_start = ttk.Entry(f_dates, width=10)
        self.e_start.pack(side="left")
        ttk.Label(f_dates, text="-").pack(side="left")
        self.e_end = ttk.Entry(f_dates, width=10)
        self.e_end.pack(side="left")
        
        if delete_cb:
            ttk.Button(self, text="X", width=3, command=lambda: delete_cb(self)).grid(row=0, column=4)

    def get_data(self):
        return Education(
            institution=self.e_school.get(),
            degree=self.e_degree.get(),
            start_date=self.e_start.get(),
            end_date=self.e_end.get()
        )
