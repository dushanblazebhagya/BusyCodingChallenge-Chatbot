# MCP CV Chat & Email

A **Model Context Protocol (MCP) server** with a React/Next.js frontend that allows users to:

1. Ask questions about a resume (CV) and get relevant answers.  
2. Send emails directly via Gmail.  

This project demonstrates API design, asynchronous email sending, and frontend integration with FastAPI backend.

---

## Features

- **Resume Query:** Ask questions like "What is my present job?" or "List my certificates."  
- **Email Sending:** Send emails using Gmail SMTP securely with an app password.  
- **Frontend Interface:** Minimal React/Next.js interface to interact with backend endpoints.  

---

## Project Structure

mcp_resume_server/
│
├─ bridge.py # FastAPI backend serving endpoints
├─ server.py # MCP tools for resume queries and email sending
├─ resume.json # Resume data in JSON format
├─ requirements.txt # Python dependencies
├─ index.js # React frontend
└─ README.md # Project documentation

---

## Backend (FastAPI + MCP)

### Requirements

- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt

requirements.txt contains:

mcp @ git+https://github.com/modelcontextprotocol/python-sdk.git
rapidfuzz
aiosmtplib

### Run Backend

uvicorn bridge:app --reload --host 0.0.0.0 --port 8001

Frontend (React / Next.js)
Requirements

Node.js 18+

npm or yarn

Run Frontend
    npm install
    npm run dev

Open http://localhost:3000 in your browser.