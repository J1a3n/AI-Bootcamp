import os
import json
import base64
import urllib.request

MODEL_PATH = "/Users/jiaen/.gemini/antigravity/scratch/llama-qwen/models/Qwen2.5-VL-7B/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
API_URL = "http://127.0.0.1:8081/v1/chat/completions"
SPIKE_DIR = "/Users/jiaen/Agy/AI Bootcamp/spike"

# Prompt B with balanced null-hypothesis condition
PROMPT_B_BALANCED = """Step 1: Transcribe the handwritten math working line-by-line into LaTeX.
Step 2: Check mathematical equivalence between each pair of consecutive lines.
If all lines are mathematically correct, state 'STATUS: CORRECT' and explain why.
If equivalence breaks, state 'STATUS: ERROR', identify the exact line where the error first appears, and explain why."""

def test_balanced(filename):
    with open(os.path.join(SPIKE_DIR, filename), "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
        
    payload = {
        "model": MODEL_PATH,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                    {"type": "text", "text": PROMPT_B_BALANCED}
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 512
    }
    
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

res1 = test_balanced("sample1_correct.png")
print("=== Sample 1 Balanced Prompt ===")
print(res1["choices"][0]["message"]["content"])

res2 = test_balanced("sample2_sign_error.png")
print("\n=== Sample 2 Balanced Prompt ===")
print(res2["choices"][0]["message"]["content"])
