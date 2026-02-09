# SPATIALCODE

**Transform your sketches and images into full-stack applications in seconds.**

SPATIALCODE leverages **Google’s Gemini 3 AI** to analyze images and descriptions, generating a complete codebase for your application. Users can upload UI sketches, describe the functionality, and instantly receive frontend and backend code, along with configuration files for deployment. It’s an AI-powered bridge between design and code.

---

## Features

- Upload images or sketches of UI designs.  
- Provide a short description of the app you want.  
- Generate full-stack code: React + Tailwind CSS frontend, FastAPI + SQLAlchemy backend.  
- Preview the generated application in real-time.  
- AI-powered analysis summary explaining the code generated.  
- Example selector to explore pre-built use cases.  

---

## Gemini 3 Integration

SPATIALCODE is powered by **Gemini 3**, which interprets both visual design and textual instructions to generate complete code. Gemini 3 identifies layouts, UI elements, and implied functionalities, producing frontend, backend, and deployment-ready code. It also provides a summary of the generated application, ensuring users understand how their input was translated into working code.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Lamrotibsa/hackathon-project.git
cd hackathon-project
Set up the backend:

cd backend
python -m venv venv
# On Windows
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload
Set up the frontend:

cd frontend
npm install
npm run dev
Open the app at http://localhost:5173 in your browser.

Usage
Go to the Input tab.

Upload a UI sketch or image.

Enter a description of the desired app functionality.

Click Generate Code to receive the full-stack application.

Switch tabs to view generated code, preview, or AI analysis.