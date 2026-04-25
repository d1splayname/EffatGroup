import subprocess
import json

requirements = {
    "REQ-1a": "Biological hazards must be evaluated",
    "REQ-1b": "Chemical hazards must be evaluated",
    "REQ-2a": "Preventive controls must be implemented",
    "REQ-3a": "Monitoring procedures must be established",
    "REQ-4a": "Corrective actions must be documented"
}

def run_model(model, prompt):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

results = {
    "mistral": {},
    "quantized_mistral": {}
}

for req_id, req_text in requirements.items():
    prompt = f"""
Generate a software test case for the following requirement:

"{req_text}"

Return ONLY valid JSON with:
- test_case_id
- requirement_id
- description
- input_data
- expected_output
"""

    results["mistral"][req_id] = run_model("mistral", prompt)
    results["quantized_mistral"][req_id] = run_model("mistral:7b-instruct-q4_0", prompt)

with open("llm_test_cases.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done. Output saved to llm_test_cases.json")