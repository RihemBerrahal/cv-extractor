import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import requests
import json
import re
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# List of available models
AVAILABLE_MODELS = ['llama3', 'mistral', 'phi']

# 📄 Extract text from PDF (text-based or scanned)
def extract_text_from_pdf(filepath):
    try:
        # First try with pdfminer
        text = extract_text(filepath)
        if text.strip():
            return text
        else:
            return extract_text_from_images(filepath)
    except Exception as e:
        print(f"Error extracting text: {e}")
        return extract_text_from_images(filepath)

# 📸 OCR fallback
def extract_text_from_images(filepath):
    text = ""
    doc = fitz.open(filepath)
    
    # Get tesseract path from environment variable
    tesseract_cmd = os.getenv("TESSERACT_PATH", "tesseract")
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img)
    
    return text

# 🧠 Send prompt to Ollama LLM
def call_llm_model(text, model='llama3'):
    if model not in AVAILABLE_MODELS:
        model = 'llama3'  # Default to llama3 if invalid model specified
        
    prompt = f"""
    Extract the following information from this CV/resume and format it as JSON:
    
    1. Full name (string)
    2. Email (string)
    3. Phone (string)
    4. Education (array of objects with fields: degree, institution, years)
    5. Experience (array of objects with fields: role, company, duration)
    6. Skills (array of strings)
    
    Format the response as a valid JSON object, with these exact keys: name, email, phone, education, experience, skills.
    
    CV Content:
    {text}
    """
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        
        if response.status_code == 200:
            result = response.json().get("response", "")
            # Extract JSON from response if there's surrounding text
            json_match = re.search(r'```json\s*(.*?)\s*```', result, re.DOTALL)
            if json_match:
                result = json_match.group(1)
            else:
                # Try to find JSON without code blocks
                json_match = re.search(r'(\{.*\})', result, re.DOTALL)
                if json_match:
                    result = json_match.group(1)
            
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"error": "Failed to parse LLM response as JSON", "raw_response": result}
        else:
            return {"error": f"API request failed with status {response.status_code}"}
    except Exception as e:
        return {"error": f"Error calling LLM: {str(e)}"}

# Process CV with all available models
def process_cv_with_all_models(text):
    results = {}
    for model in AVAILABLE_MODELS:
        results[model] = call_llm_model(text, model)
    return results