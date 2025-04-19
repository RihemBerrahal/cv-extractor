import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import requests
import json
import re
import os
import ast

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

# Function to clean and fix common JSON formatting issues from LLM responses
def clean_llm_json_response(text):
    """Clean and fix common JSON formatting issues from LLM responses"""
    # Replace single quotes with double quotes (but be careful with apostrophes in text)
    text = re.sub(r"(?<!\w)'", '"', text)
    text = re.sub(r"'(?!\w)", '"', text)
    
    # Handle apostrophes in words properly
    text = text.replace("d\\'", "d'")
    text = text.replace("\\'", "'")
    
    # Remove extra whitespace and newlines inside the JSON
    text = re.sub(r'\s+', ' ', text)
    
    # Try to fix missing commas between array elements
    text = re.sub(r'} {', '}, {', text)
    
    return text

# Extract JSON from output that contains Python code or examples
def extract_json_from_code_output(text):
    """Extract valid JSON from Python code output or examples"""
    # Try to find JSON output after "Output:" or similar markers
    output_match = re.search(r'Output:.*?(\{.*\})', text, re.DOTALL | re.IGNORECASE)
    if output_match:
        return output_match.group(1)
    
    # Look for json.dumps output
    json_dumps_match = re.search(r'json\.dumps\(.*?\).*?(\{.*\})', text, re.DOTALL)
    if json_dumps_match:
        return json_dumps_match.group(1)
    
    # Extract any JSON-like structure with quoted keys and values
    json_like_match = re.search(r'(\{".*?"\s*:.*?\})', text, re.DOTALL)
    if json_like_match:
        return json_like_match.group(1)
    
    return text

# Check if the JSON response is a template or example JSON
def is_template_json(json_obj):
    """Check if the JSON response is just the template/example returned back"""
    template_indicators = [
        'Full Name', 'John Doe', 'Degree Name', 'Institution Name', 'Year Range',
        'Job Title', 'Company Name', 'Duration', 'Skill 1', 'Skill 2', 'Skill 3',
        'email@example.com', 'john@example.com', 'Phone number', '123-456-7890',
        'Full', 'Name', 'Email', 'Phone'
    ]
    
    # Convert the JSON to string for checking
    json_str = json.dumps(json_obj)
    
    # Count how many template indicators are present
    count = sum(1 for indicator in template_indicators if indicator in json_str)
    
    # If we have more than 3 indicators, it's likely a template
    return count >= 3

# Customize prompt based on model to improve JSON output
def get_model_specific_prompt(text, model):
    base_prompt = f"""
    Extract the following information from this CV/resume:
    
    1. Full name 
    2. Email
    3. Phone
    4. Education (degree, institution, years)
    5. Experience (role, company, duration)
    6. Skills
    """
    
    # Model-specific prompt adjustments
    if model == 'phi':
        return f"""
        {base_prompt}
        
        IMPORTANT: You must extract the actual data from the CV below. DO NOT return the template structure.
        I need you to fill in the actual values from this specific CV.
        
        Return ONLY a JSON object WITHOUT any explanation, code examples, or commentary.
        Use this exact format but REPLACE the placeholders with actual data from the CV:
        
        {{
          "name": "[ACTUAL NAME FROM CV]",
          "email": "[ACTUAL EMAIL FROM CV]",
          "phone": "[ACTUAL PHONE FROM CV]",
          "education": [
            {{
              "degree": "[ACTUAL DEGREE FROM CV]",
              "institution": "[ACTUAL INSTITUTION FROM CV]",
              "years": "[ACTUAL YEARS FROM CV]"
            }}
          ],
          "experience": [
            {{
              "role": "[ACTUAL ROLE FROM CV]",
              "company": "[ACTUAL COMPANY FROM CV]",
              "duration": "[ACTUAL DURATION FROM CV]"
            }}
          ],
          "skills": ["[ACTUAL SKILL 1]", "[ACTUAL SKILL 2]", "[ACTUAL SKILL 3]"]
        }}
        
        CV Content:
        {text}
        """
    else:
        return f"""
        {base_prompt}
        
        Format the response as a valid JSON object, with these exact keys: name, email, phone, education, experience, skills.
        
        IMPORTANT: Use double quotes for all keys and string values, not single quotes. The output must be valid JSON that can be parsed with json.loads().
        
        Example of valid JSON format:
        {{
          "name": "John Doe",
          "email": "john@example.com",
          "phone": "123-456-7890",
          "education": [
            {{
              "degree": "Bachelor of Science",
              "institution": "University of Example",
              "years": "2015-2019"
            }}
          ],
          "experience": [
            {{
              "role": "Software Engineer",
              "company": "Tech Company",
              "duration": "2019-Present"
            }}
          ],
          "skills": ["Python", "JavaScript", "SQL"]
        }}
        
        CV Content:
        {text}
        """

# Fallback function to extract basic CV data when model fails
def extract_basic_cv_data(cv_text):
    """Extract basic CV data using regex as a fallback"""
    data = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": [],
        "skills": []
    }
    
    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', cv_text)
    if email_match:
        data["email"] = email_match.group(0)
    
    # Extract phone (basic pattern)
    phone_match = re.search(r'\b\d{8,12}\b', cv_text)
    if phone_match:
        data["phone"] = phone_match.group(0)
    
    # Extract name (assume it's at the beginning, before email)
    if data["email"]:
        name_section = cv_text.split(data["email"])[0].strip()
        # First line or first few words could be the name
        possible_name = name_section.split('\n')[0].strip()
        if len(possible_name.split()) <= 5:  # Reasonable name length
            data["name"] = possible_name
    
    # Look for education keywords
    education_keywords = ['Education', 'Faculté', 'institut', 'Lycée', 'University', 'College', 'School']
    education_section = None
    
    for keyword in education_keywords:
        edu_match = re.search(f'(?:{keyword}.*?)(?=\n\n|\Z)', cv_text, re.IGNORECASE | re.DOTALL)
        if edu_match:
            education_section = edu_match.group(0)
            # Extract one education entry
            data["education"].append({
                "degree": "Education found",
                "institution": education_section.split('\n')[0] if '\n' in education_section else education_section,
                "years": ""
            })
            break
    
    # Look for experience keywords
    experience_keywords = ['Experience', 'Professional Experience', 'Stage', 'Work']
    experience_section = None
    
    for keyword in experience_keywords:
        exp_match = re.search(f'(?:{keyword}.*?)(?=\n\n|\Z)', cv_text, re.IGNORECASE | re.DOTALL)
        if exp_match:
            experience_section = exp_match.group(0)
            # Extract one experience entry
            data["experience"].append({
                "role": "Experience found",
                "company": experience_section.split('\n')[0] if '\n' in experience_section else experience_section,
                "duration": ""
            })
            break
    
    # Extract basic skills (look for common skill keywords)
    skill_keywords = ['Python', 'SQL', 'Java', 'C++', 'HTML', 'CSS', 'JavaScript', 'Flask']
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', cv_text, re.IGNORECASE):
            data["skills"].append(skill)
    
    # Look for skills section
    skills_match = re.search(r'(?:Skills|Compétences|Maîtrise).*', cv_text, re.IGNORECASE)
    if skills_match and not data["skills"]:
        # Just add a placeholder if we found a skills section but no specific skills
        data["skills"] = ["Skills found"]
    
    return data

# 🧠 Send prompt to Ollama LLM with special phi handling
def call_llm_model(text, model='llama3'):
    if model not in AVAILABLE_MODELS:
        model = 'llama3'  # Default to llama3 if invalid model specified
    
    # For phi model, first try a simple basic extraction
    if model == 'phi':
        try:
            basic_data = extract_basic_cv_data(text)
            if basic_data and basic_data["name"] and basic_data["email"]:
                return basic_data
        except Exception as e:
            print(f"Basic extraction for phi failed: {e}")
    
    # Get model-specific prompt
    prompt = get_model_specific_prompt(text, model)
    
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
            
            # Special handling for the phi model which often returns code examples
            if model == 'phi' and ('print' in result or 'json.dumps' in result or 'Output:' in result):
                result = extract_json_from_code_output(result)
            
            try:
                # First try to parse as is
                parsed_json = json.loads(result)
                
                # Check if the parsed JSON is just the template
                if is_template_json(parsed_json):
                    if model == 'phi':
                        # Fall back to basic extraction
                        return extract_basic_cv_data(text)
                    else:
                        return {"error": "Model returned template JSON", "raw_response": result}
                
                return parsed_json
            except json.JSONDecodeError:
                # If that fails, try to clean up the response
                cleaned_result = clean_llm_json_response(result)
                try:
                    parsed_json = json.loads(cleaned_result)
                    
                    # Check if the parsed JSON is just the template
                    if is_template_json(parsed_json):
                        if model == 'phi':
                            # Fall back to basic extraction
                            return extract_basic_cv_data(text)
                        else:
                            return {"error": "Model returned template JSON", "raw_response": result}
                    
                    return parsed_json
                except json.JSONDecodeError:
                    # If still failing and it's phi, use our basic extraction
                    if model == 'phi':
                        return extract_basic_cv_data(text)
                    else:
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