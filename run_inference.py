import os
import subprocess
import json

MODELS = ["llama3", "mistral", "phi"]
PROMPT_TEMPLATE = """
Extract the following fields from this resume:
- Name
- Email
- Phone
- Education
- Experience
- Skills

Return the output in JSON format with these keys:
name, email, phone, education, experience, skills.

Resume:
{text}
"""

def call_ollama(model, prompt):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode("utf-8")

    # Try to extract JSON from response
    try:
        start = output.find("{")
        end = output.rfind("}") + 1
        json_str = output[start:end]
        return json.loads(json_str)
    except:
        return {"error": "Invalid response", "raw": output}

def run_inference():
    os.makedirs("results", exist_ok=True)
    for file in os.listdir("sample_cvs"):
        if file.endswith(".txt"):
            file_path = os.path.join("sample_cvs", file)
            cv_id = file.replace(".txt", "")
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            results = {}
            for model in MODELS:
                print(f"Running {model} on {cv_id}...")
                prompt = PROMPT_TEMPLATE.format(text=text)
                results[model] = call_ollama(model, prompt)
            # Save results
            with open(f"results/{cv_id}.json", "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"Saved: results/{cv_id}.json")

if __name__ == "__main__":
    run_inference()
