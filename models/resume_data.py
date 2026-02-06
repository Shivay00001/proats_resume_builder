
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Job:
    title: str = ""
    company: str = ""
    start_date: str = ""
    end_date: str = ""
    responsibilities: str = "" # Stored as raw string, split by newline for bullets

@dataclass
class Education:
    institution: str = ""
    degree: str = ""
    start_date: str = ""
    end_date: str = ""
    gpa: str = "" # Optional

@dataclass
class Project:
    name: str = ""
    description: str = ""
    tech_stack: str = "" # Comma separated
    link: str = ""

@dataclass
class ResumeData:
    # Personal Info
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    portfolio: str = "" # GitHub or other
    profile_image_path: Optional[str] = None # Path to local file

    # Sections
    summary: str = ""
    
    # Styling Preferences (passed from UI)
    theme_color: str = "Navy" # Navy, Emerald, Crimson, Charcoal, Violet
    design_style: str = "Quartz" # Quartz, Obsidian, Glacier, Onyx

    # Lists
    skills: List[str] = field(default_factory=list)
    experience: List[Job] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)

    def to_dict(self):
        """Helper for serialization if needed, though dataclasses can be used directly."""
        return self.__dict__
