"""API routes for the application."""
import logging
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.schemas import AnalyzeRequest, AnalysisResponse
from app.services.ai_service import AIService
from app.services.example_service import ExampleService

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
ai_service = AIService()
example_service = ExampleService()


@router.post("/analyze")
async def analyze_image(
    image: UploadFile = File(..., description="Image file to analyze"),
    description: str = Form(..., max_length=200, description="Text description of the application")
):
    """
    Analyze an image and generate code using Gemini Vision API.
    
    Args:
        image: Uploaded image file
        description: Text description (max 200 characters)
        
    Returns:
        AnalysisResponse with generated code files and summary
    """
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Read image data
        image_data = await image.read()
        
        # Validate file size (10MB limit)
        from app.core.config import settings
        if len(image_data) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        # Process image with AI service
        logger.info(f"Processing image: {image.filename}, description: {description[:50]}...")
        result = ai_service.process_image(image_data, description)
        
        # Convert to response format
        response_data = result.to_response()
        logger.info(f"Response data keys: {list(response_data.get('generated_files', {}).keys())}")
        response = AnalysisResponse(**response_data)
        # Return all files as-is (Dict[str, str] preserves all file names)
        return response.model_dump()
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}"
        )


@router.get("/examples", response_model=list[str])
async def list_examples():
    """
    List all available pre-built examples.
    
    Returns:
        List of example IDs
    """
    return example_service.list_examples()


@router.get("/examples/{example_id}")
async def get_example(example_id: str):
    """
    Get a pre-built example by ID.
    
    Args:
        example_id: Identifier for the example (food-pantry, library, clinic)
        
    Returns:
        AnalysisResponse with pre-generated code files
    """
    try:
        result = example_service.get_example(example_id)
        response_data = result.to_response()
        response = AnalysisResponse(**response_data)
        # Return all files as-is (Dict[str, str] preserves all file names)
        return response.model_dump()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "SPATIALCODE API"}
