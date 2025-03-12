from fastapi import APIRouter, HTTPException,Request
from fastapi.responses import PlainTextResponse
import os
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

router = APIRouter(prefix="/ai", tags=["ai"])

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

prompt = """Attached is an image of a clinical report. 
Go over the the clinical report and identify biomarkers that show slight or large abnormalities. Then summarize in 100 words. You may increase the word limit if the report has multiple pages. Do not output patient name, date etc. Make sure to include numerical values and key details from the report, including report title.
## Summary: """

def file_to_generative_part(image_data: str) -> Dict[str, Any]:
    """Convert base64 image data to the format required by Gemini API"""
    # Split data from the base64 string
    parts = image_data.split(",")
    if len(parts) > 1:
        # Extract mime type and base64 data
        mime_type = image_data.split(";")[0].split(":")[1]
        data = parts[1]
    else:
        # If there's no data URI scheme prefix
        data = image_data
        mime_type = "image/jpeg"  # Default mime type
    
    return {
        "inline_data": {
            "data": data,
            "mime_type": mime_type
        }
    }

@router.post("/analyze-report", response_class=PlainTextResponse)
async def analyze_report(request: Request) -> str:
    """Process clinical report image and return analysis"""
    # Parse the request body
    body = await request.json()
    base64_image = body.get("base64")
    
    if not base64_image:
        return PlainTextResponse("Missing base64 image data", status_code=400)
    
    # Convert the image to the required format
    file_part = file_to_generative_part(base64_image)
    print(f"File part: {file_part}")
    
    try:
        # Generate content using the Gemini model
        response = model.generate_content([prompt, file_part])
        print(f"Generated response: {response}")
        
        # Extract the text response
        text_response = response.text
        return text_response
    
    except Exception as e:
        print(f"Error generating content: {e}")
        return PlainTextResponse(f"Error processing request: {str(e)}", status_code=500)