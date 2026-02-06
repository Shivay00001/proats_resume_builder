
from models.resume_data import ResumeData
import re

def calculate_ats_score(data: ResumeData) -> tuple[int, list[str]]:
    """
    Analyzes resume data and returns a score (0-100) and feedback list.
    """
    score = 100
    feedback = []

    # 1. Content Checks
    if not data.full_name:
        score -= 20
        feedback.append("Missing Full Name (Critical).")
    
    if not data.email:
        score -= 20
        feedback.append("Missing Email Address (Critical).")
    
    if not data.phone:
        score -= 10
        feedback.append("Missing Phone Number.")

    # 2. Section Checks
    if not data.summary or len(data.summary.split()) < 20:
        score -= 10
        feedback.append("Professional Summary is too short or missing. Aim for 3-4 sentences.")
    
    if not data.skills:
        score -= 15
        feedback.append("No skills listed. ATS scanners rely heavily on skills.")
    elif len(data.skills) < 5:
        score -= 5
        feedback.append("List more skills (aim for 8-10 relevant technical/soft skills).")

    if not data.experience:
        score -= 15
        feedback.append("No work experience listed.")
    else:
        # Deep dive into experience
        total_bullets = 0
        measurable_results = 0
        # Simple regex for numbers/metrics
        metric_pattern = r"(\d+%|\$\d+|\d+k|\d+M|increased|reduced|saved|improved)"
        
        for job in data.experience:
            bullets = [b for b in job.responsibilities.split('\n') if b.strip()]
            total_bullets += len(bullets)
            for b in bullets:
                if re.search(metric_pattern, b, re.IGNORECASE):
                    measurable_results += 1
        
        if total_bullets < 3:
            score -= 5
            feedback.append("Work experience descriptions are very brief.")
        
        if measurable_results == 0:
            score -= 10
            feedback.append("No measurable results found in experience (e.g., 'Increased revenue by 20%').")

    # 3. Formatting/Safety Checks (Data layer only)
    # Check for suspicious characters in text
    all_text = f"{data.summary} {' '.join(data.skills)}"
    if re.search(r"[^\x00-\x7F]+", all_text): # Non-ASCII check (simple)
        # Not necessarily a formatting error, but warning for icons
        # We might allow accents, but emojis are bad.
        # Let's target specific emoji ranges or just warn widely if unsafe chars found.
        # For now, just a soft warning.
        pass 

    return max(0, score), feedback
