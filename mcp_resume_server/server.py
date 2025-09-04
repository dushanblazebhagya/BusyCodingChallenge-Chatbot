import json
import asyncio
import re
from email.message import EmailMessage
from aiosmtplib import send
from mcp.server.fastmcp import FastMCP

with open("resume.json", "r", encoding="utf-8") as f:
    resume = json.load(f)

# MCP server
mcp = FastMCP("resume-server")

# Keywords
SECTION_KEYWORDS = {
    "personal_info": ["name", "email", "phone", "address", "linkedin", "github", "summary"],
    "experience": ["experience", "role", "position", "responsibility", "job", "work", "company", "start date", "end date"],
    "education": ["education", "degree", "study", "university", "college", "school"],
    "projects": ["project", "app", "application", "development"],
    "skills": ["skill", "technology", "framework", "programming"],
    "certificates": ["certificate", "course", "training", "AI", "artificial intelligence", "AWS", "API", "Microservices"],
    "research_publications": ["publication", "research", "paper", "doi"],
    "achievements": ["award", "achievement", "recognition"],
    "references": ["reference", "contact", "referee"]
}

def find_section(question: str):
    q = question.lower()
    for section, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in q:
                return section
    return None

def normalize_text(text: str) -> str:
    """Lowercase, strip, remove special characters for matching"""
    text = text.lower().strip()
    text = re.sub(r'\s+', '', text)  
    text = re.sub(r'[^a-z0-9]', '', text)  
    return text

def answer_question(section: str, question: str) -> str:
    q = question.lower().strip()

    if section == "personal_info":
        info = resume.get("personal_info", {})
        for key in info:
            if key.lower() in q:
                return info.get(key, "N/A")
        return ", ".join(info.values()) if info else "N/A"

    elif section == "experience":
        roles = resume.get("experience", [])
        if "present job" in q:
            return roles[0].get('role', 'N/A') if roles else 'N/A'
        elif "previous job" in q or "last job" in q:
            return roles[1].get('role', 'N/A') if len(roles) > 1 else 'N/A'
        elif "first job" in q:
            return roles[-1].get('role', 'N/A') if roles else 'N/A'

        for exp in roles:
            role_name = exp.get("role", "").lower()
            if role_name in q:
                if "start date" in q:
                    return exp.get("start", "N/A")
                elif "end date" in q:
                    return exp.get("end", "N/A")
                elif "company" in q:
                    return exp.get("company", "N/A")
                elif "responsibility" in q or "responsibilities" in q:
                    return "\n".join(exp.get("responsibilities", [])) if exp.get("responsibilities") else "N/A"
                else:
                    return exp.get("role", "N/A")
        return ", ".join([r.get('role', 'N/A') for r in roles]) if roles else "N/A"

    elif section == "certificates":
        certs = resume.get("certificates", [])
        keywords = ["api", "aws", "microservices", "artificial intelligence", "ai"]
        filtered = []
        for k in keywords:
            if k in q:
                filtered = [c for c in certs if k.lower() in c.lower()]
                break
        return "\n".join(filtered) if filtered else "\n".join(certs) if certs else "N/A"

    elif section == "projects":
        projects = resume.get("projects", [])
        q_norm = normalize_text(q)

        # Projects
        for p in projects:
            title_norm = normalize_text(p.get("title", ""))
            if title_norm == q_norm:
                details = [
                    f"Title: {p.get('title', 'N/A')}",
                    f"Description: {p.get('description', 'N/A')}",
                    f"Technologies: {', '.join(p.get('technologies', [])) if p.get('technologies') else 'N/A'}"
                ]
                return "\n".join(details)

        # Show Projects
        all_details = []
        for p in projects:
            details = [
                f"Title: {p.get('title', 'N/A')}",
                f"Description: {p.get('description', 'N/A')}",
                f"Technologies: {', '.join(p.get('technologies', [])) if p.get('technologies') else 'N/A'}"
            ]
            all_details.append("\n".join(details))
        return "\n\n".join(all_details) if all_details else "N/A"

    elif section == "education":
        edu_list = resume.get("education", [])
        return "\n".join([
            f"{edu.get('degree', '')}, {edu.get('institution', '')} ({edu.get('start', '')} - {edu.get('end', '')})"
            for edu in edu_list
        ]) if edu_list else "N/A"

    elif section == "research_publications":
        pubs = resume.get("research_publications", [])
        return "\n".join([p.get("title", "") for p in pubs]) if pubs else "N/A"

    elif section == "skills":
        skills = resume.get("key_skills", {})
        if not skills:
            return "N/A"
        formatted_skills = []
        if isinstance(skills, dict):  # categories
            for category, items in skills.items():
                formatted_skills.append(f"{category}: {', '.join(items)}")
        elif isinstance(skills, list):  # fallback
            formatted_skills = skills
        return "\n".join(formatted_skills)

    elif section == "achievements":
        items = resume.get(section, [])
        return "\n".join(items) if items else "N/A"

    elif section == "references":
        refs = resume.get("references", [])
        if not refs:
            return "N/A"
        formatted_refs = []
        for r in refs:
            name = r.get("name", "N/A")
            role = r.get("role", "N/A")
            email = r.get("email", "N/A")
            phone = r.get("phone", "N/A")
            formatted_refs.append(f"{name} ({role}) - Email: {email}, Phone: {phone}")
        return "\n".join(formatted_refs)

    return "Sorry, I don't have an answer to that question yet."

# MCP Tool function
def query_resume_tool(question: str) -> str:
    section = find_section(question)
    if not section:
        return "Sorry, I don't have an answer to that question yet."
    return answer_question(section, question)

# Send Emails
async def send_email_async(recipient: str, subject: str, body: str) -> str:
    msg = EmailMessage()
    msg["From"] = "dushandbr@gmail.com"
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        await send(
            msg,
            hostname="smtp.gmail.com",
            port=587,
            start_tls=True,
            username="dushandbr@gmail.com",
            password="xgvfgixhdoyifora"
        )
        return f"Email successfully sent to {recipient}!"
    except Exception as e:
        return f"Failed to send email: {e}"

def send_email_tool(recipient: str, subject: str, body: str) -> str:
    return asyncio.run(send_email_async(recipient, subject, body))

mcp.tool()(query_resume_tool)
mcp.tool()(send_email_tool)

if __name__ == "__main__":
    mcp.run()
