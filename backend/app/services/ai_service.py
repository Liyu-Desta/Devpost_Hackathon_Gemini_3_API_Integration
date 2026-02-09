"""AI service for interacting with Gemini Vision API."""
import json
import base64
import logging
from typing import Optional
from google import genai

from app.core.config import settings
from app.models.domain import AnalysisResult

logger = logging.getLogger(__name__)


class AIService:
    """Service for processing images with Gemini Vision API."""
    
    def __init__(self):
        """Initialize the AI service with Gemini API."""
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL
    
    def process_image(
        self, 
        image_data: bytes, 
        description: str
    ) -> AnalysisResult:
        """
        Process image and description to generate code.
        
        Args:
            image_data: Raw image bytes
            description: Text description of the application
            
        Returns:
            AnalysisResult with generated code files
            
        Raises:
            ValueError: If API response is invalid
            Exception: If API call fails
        """
        try:
            # Construct the prompt
            prompt = self._build_prompt(description)
            
            # Prepare contents - combine image and text
            # The new API format expects a list of content parts
            from google.genai import types
            
            # Create content parts with image and text
            contents = [
                types.Part.from_bytes(
                    data=image_data,
                    mime_type="image/jpeg"
                ),
                types.Part.from_text(text=prompt)
            ]
            
            # Call Gemini API using the new format
            logger.info(f"Calling Gemini API ({self.model_name}) for code generation")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents
            )
            
            # Extract text from response
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            # Parse response
            result = self._parse_response(response_text, description)
            logger.info("Successfully generated code from Gemini API")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing image with Gemini API: {str(e)}")
            raise
    
    def _build_prompt(self, description: str) -> str:
        """Build an enhanced prompt for Gemini API to generate full-stack applications."""
        return f"""## ROLE
You are an Expert Senior Full-Stack Engineer with 15+ years of experience in React, FastAPI, PostgreSQL, and modern web development.

## TASK
Analyze the provided UI image and this description: "{description}"

Generate a complete, production-ready, deployable full-stack application that exactly matches the visual design and functional requirements.

## OUTPUT FORMAT
Return ONLY a valid JSON object with this structure:
{{
    "analysis_summary": "Concise analysis (3-4 sentences) of what the image shows and the application purpose",
    "technical_stack": {{
        "frontend": "React 18 + TypeScript + Vite + Tailwind CSS",
        "backend": "FastAPI + SQLAlchemy + PostgreSQL + Pydantic",
        "deployment": "Docker + Nginx + environment-based config"
    }},
    "generated_files": {{
        "models.py": "SQLAlchemy ORM models with proper relationships, constraints, and migrations setup",
        "schemas.py": "Pydantic schemas for request/response validation",
        "main.py": "Complete FastAPI app with all endpoints, middleware, error handling, and CORS",
        "database.py": "Database connection and session management",
        "requirements.txt": "Production and development dependencies with versions",
        "docker-compose.yml": "Complete Docker setup with services, networks, and volumes",
        "Dockerfile.backend": "Optimized Dockerfile for Python backend",
        "Dockerfile.frontend": "Optimized Dockerfile for React frontend",
        "nginx.conf": "Nginx configuration for production deployment",
        "vite.config.ts": "Vite configuration with TypeScript and aliases",
        "tsconfig.json": "TypeScript configuration for strict type checking",
        "tailwind.config.js": "Tailwind CSS configuration",
        "postcss.config.js": "PostCSS configuration",
        "App.jsx": "SINGLE self-contained React component in JavaScript (NOT TypeScript). Must include ALL sub-components inline. NO imports except React. Use emojis for icons. Use fetch() for API calls. Use Tailwind classes for styling.",
        "env.example": "Environment variables template",
        "README.md": "Comprehensive setup, development, and deployment guide"
    }}
}}

## PREVIEW ENVIRONMENT CONSTRAINTS
IMPORTANT: The generated App.jsx/App.tsx will be rendered in a browser iframe with limited dependencies:
- React and ReactDOM are available globally (via CDN)
- NO module system (no import/export for components)
- NO external libraries (no axios, no icon libraries, etc.)
- NO relative imports (./components, ./services, etc.)
- Use ONLY React hooks: useState, useEffect, useReducer, useContext, useCallback, useMemo, useRef
- Use inline styles or Tailwind CSS classes (Tailwind CDN is available)
- Keep the App component self-contained - define all sub-components inline or as simple functions
- Use simple HTML elements and emojis instead of icon libraries
- Use fetch() API directly instead of axios or other HTTP libraries

### 1. VISUAL FIDELITY
- Recreate EXACTLY what's shown in the image
- Match colors, spacing, typography, and layout precisely
- If colors aren't clear, use a modern color scheme (slate/zinc/neutral)
- Use responsive design that matches the image's structure
- Use Tailwind CSS classes for styling (available via CDN)

### 2. FRONTEND CODE STRUCTURE (CRITICAL FOR PREVIEW)
- App.jsx MUST be a single, self-contained file
- DO NOT use: import statements for local files (./components, ./services, etc.)
- DO NOT use: external icon libraries (lucide-react, heroicons, react-icons)
- DO use: Simple HTML elements, emojis (📝, ✏️, 🗑️, ➕, etc.) for icons
- DO use: Inline component definitions within App.jsx
- DO use: fetch() API for any API calls (if needed)
- DO use: useState and useEffect hooks for state management
- Example structure (use double curly braces {{}} in f-strings):
```jsx
function App() {{
  const [data, setData] = useState([]);
  
  useEffect(() => {{
    // Fetch data if needed
  }}, []);
  
  // Define sub-components inline
  const Header = () => <header>...</header>;
  const Sidebar = () => <aside>...</aside>;
  
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <Sidebar />
      {{/* Main content */}}
    </div>
  );
}}
```

### 3. BACKEND REQUIREMENTS
- FastAPI with async/await support
- SQLAlchemy 2.0 with async support
- Alembic migrations ready
- JWT authentication setup (even if not in image, include foundation)
- Comprehensive error handling (HTTPException, validation errors)
- Request/response validation with Pydantic
- Proper CORS configuration
- Environment-based configuration
- Health check endpoint
- Logging configuration

### 4. FRONTEND REQUIREMENTS (FOR PREVIEW COMPATIBILITY)
- React 18 with functional components and hooks ONLY
- JavaScript (not TypeScript) for App.jsx to avoid transpilation issues
- Tailwind CSS classes for styling (available via CDN in preview)
- NO React Router (use conditional rendering for different views)
- State management with useState/useReducer only
- API integration with fetch() and loading/error states
- Responsive design with Tailwind classes
- All components defined in a single App.jsx file
- NO separate component files - everything inline in App.jsx

### 5. DATABASE DESIGN
- Analyze entities from image (Users, Products, Orders, etc.)
- Create proper SQLAlchemy models with:
  - Correct data types
  - Relationships (Foreign Keys, Many-to-Many if needed)
  - Indexes for performance
  - Constraints (unique, nullable, defaults)
  - Timestamps (created_at, updated_at)
- Include migration setup with Alembic

### 6. API DESIGN
- RESTful endpoints matching CRUD operations for each entity
- Proper HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Request/response schemas
- Query parameters for filtering/sorting/pagination
- Proper status codes (200, 201, 400, 401, 404, 500)

### 7. PRODUCTION READINESS
- Docker setup for development and production
- Nginx reverse proxy configuration
- Environment variable management
- Security headers and CORS
- Error boundaries in React
- API rate limiting foundation
- Database connection pooling
- Production-ready logging

### 8. CODE QUALITY
- Type hints everywhere
- Docstrings for functions and classes
- Proper error handling (try-catch blocks)
- Input validation
- Security best practices (password hashing, SQL injection prevention)
- Clean, maintainable code structure
- Follow PEP 8 (Python) and ESLint (TypeScript) standards

## APPLICATION SPECIFICS FROM IMAGE
Analyze these aspects from the image:

### Layout Analysis:
- Number of columns/sections
- Navigation structure (topbar, sidebar, tabs)
- Content organization (cards, tables, forms, lists)
- Color scheme and typography
- Interactive elements (buttons, inputs, modals)

### Functionality Analysis:
- Data display format (cards, tables, charts)
- User interactions (click, hover, forms)
- Data flow (what loads when, what updates what)
- User roles if shown (admin/user views)

### Entity Analysis:
- Identify main data entities (User, Product, Order, etc.)
- Relationships between entities
- Attributes for each entity
- Required CRUD operations

## GENERATION RULES FOR App.jsx (CRITICAL)
1. App.jsx MUST be a single, self-contained JavaScript file (NOT TypeScript)
2. NO import statements except for React (which is available globally in preview)
3. NO relative imports (./components, ./services, ./hooks, etc.)
4. Define ALL components inline within App.jsx
5. Use emojis (📝, ✏️, 🗑️, ➕, 📊, 👤, etc.) instead of icon libraries
6. Use fetch() API directly, not axios or other libraries
7. Use Tailwind CSS classes for all styling
8. Keep the code simple and functional - avoid complex patterns that might break in preview
9. Use useState and useEffect for all state management
10. Make the UI match the image EXACTLY
11. Include proper loading and error states
12. The App component should be the default export: export default function App() { ... }

## GENERATION RULES FOR OTHER FILES
1. Backend files (models.py, main.py, etc.) can use proper structure
2. Include proper imports, dependencies, and configurations for backend
3. Create a FULLY FUNCTIONAL application structure
4. All code must be production-ready, not just examples
5. Match the visual design EXACTLY - if the image shows blue buttons, make blue buttons
6. If the image shows a data table, create the full CRUD for that entity
7. Include authentication foundation even if not in image (for scalability)
8. Use modern patterns for backend code
9. Implement proper loading and error states
10. Add comprehensive comments for complex logic

## IMPORTANT
- Return ONLY valid JSON
- No markdown formatting
- No explanations outside the JSON
- Ensure all code is syntactically correct
- All file paths should be relative to project root

## FINAL CHECK
Before responding, verify:
1. The UI matches the image perfectly
2. All generated code is functional and runnable
3. All necessary files are included
4. The Docker setup works
5. API endpoints match the frontend needs
6. Database models support all required operations

Now generate the complete application based on the image and description."""
    
    def _parse_response(self, response_text: str, description: str) -> AnalysisResult:
        """
        Parse Gemini API response into AnalysisResult.
        
        Args:
            response_text: Raw response from Gemini API
            description: Original description for fallback
            
        Returns:
            AnalysisResult object
        """
        try:
            # Clean the response - remove markdown code blocks if present
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            # Log the cleaned response for debugging
            logger.info(f"Parsing AI response (first 500 chars): {cleaned_text[:500]}")
            
            # Parse JSON
            data = json.loads(cleaned_text)
            
            # Extract fields
            summary = data.get("analysis_summary", f"Generated application based on: {description}")
            files_dict = data.get("generated_files", {})
            
            # Log what files were received
            logger.info(f"Files received from AI: {list(files_dict.keys())}")
            
            # Normalize file names - handle variations
            normalized_files = {}
            for key, value in files_dict.items():
                # Keep original key but also check for common variations
                normalized_files[key] = value
            
            # Check for React component files with different names/extensions
            react_file_found = False
            react_file_key = None
            for key in normalized_files.keys():
                if key in ["App.jsx", "App.tsx", "app.jsx", "app.tsx", "App.js", "app.js"]:
                    react_file_found = True
                    react_file_key = key
                    break
            
            # If we found a React file with a different name, ensure "App.jsx" exists
            if react_file_found and react_file_key != "App.jsx":
                if "App.jsx" not in normalized_files:
                    # Use the found React file content for App.jsx
                    normalized_files["App.jsx"] = normalized_files[react_file_key]
                    logger.info(f"Mapped {react_file_key} to App.jsx")
            
            # Ensure critical files exist, but only add placeholders if truly missing
            # Don't overwrite existing files with placeholders
            if "App.jsx" not in normalized_files:
                logger.warning("App.jsx not found in AI response, adding placeholder")
                normalized_files["App.jsx"] = f"# App.jsx\n# File not generated by AI\n# Please check the AI response"
            
            # Only add placeholders for other files if they're completely missing
            critical_files = {
                "models.py": "# SQLAlchemy models\n# File not generated by AI",
                "main.py": "# FastAPI application\n# File not generated by AI",
                "README.md": "# README\n# File not generated by AI"
            }
            
            for file_name, placeholder in critical_files.items():
                if file_name not in normalized_files:
                    logger.warning(f"{file_name} not found in AI response, adding placeholder")
                    normalized_files[file_name] = placeholder
            
            logger.info(f"Final files to return: {list(normalized_files.keys())}")
            
            return AnalysisResult(
                summary=summary,
                files=normalized_files
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response text (first 1000 chars): {response_text[:1000]}")
            raise ValueError(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            logger.error(f"Response text (first 1000 chars): {response_text[:1000]}")
            raise ValueError(f"Failed to parse AI response: {str(e)}")
