# ProATS Resume Builder

A professional, ATS-compliant (Applicant Tracking System) resume builder built with Python and Tkinter. Generate high-quality, ATS-optimized resumes in PDF, DOCX, and TXT formats directly from your desktop.

## 🚀 Key Features

- **ATS-Optimized Formatting**: Ensures your resume can be correctly parsed by Applicant Tracking Systems.
- **Dynamic GUI Form**: Easy-to-use scrolling interface for entering Personal Info, Summary, Skills, Experience, Projects, Education, and Certifications.
- **Multiple Design Styles**: Choose between Quartz, Obsidian, Glacier, Onyx, and Executive layouts.
- **Color Themes**: Customize your resume with elegant accent colors (Navy, Emerald, Forest, Crimson, Charcoal, Violet, Blue).
- **Real-Time ATS Scoring**: Evaluates your input and provides an estimated ATS compatibility score and actionable feedback.
- **Multi-Format Export**: Export your generated resume to `.pdf`, `.docx`, or `.txt`.

## ⚙️ Prerequisites

- Python 3.8+
- Required libraries: `python-docx` and `reportlab`
- Built-in `tkinter` module

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shivay00001/proats_resume_builder.git
   cd proats_resume_builder
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the main application:
```bash
python main.py
```

1. **Fill Out Your Profile**: Use the left panel to input your personal information, work experience, projects, and education. You can dynamically add new job or education entries.
2. **Select Design**: In the right panel, select your preferred "Design Style" and "Accent Color".
3. **Check Your Score**: Click **Refresh Preview & Score** to generate a live preview and see your ATS optimization score.
4. **Export**: Click the corresponding export button (Export PDF, Export DOCX, Export TXT) to save your polished resume to your computer.

## License
This project is licensed under the terms provided in the LICENSE file.

## 🐳 Docker Support

Run the system seamlessly using Docker (requires X11 forwarding on host):

`ash
docker compose up --build
`
