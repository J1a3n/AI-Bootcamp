import os
import json
import time
import base64
import urllib.request

MODEL_PATH = "/Users/jiaen/.gemini/antigravity/scratch/llama-qwen/models/Qwen2.5-VL-7B/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
API_URL = "http://127.0.0.1:8081/v1/chat/completions"
SPIKE_DIR = "/Users/jiaen/Agy/AI Bootcamp/spike"

PROMPT_A = "Look at this student's handwritten math work. Is there an error? If so, find and explain the error."

PROMPT_B = """Step 1: Transcribe the handwritten math working line-by-line into LaTeX.
Step 2: Check mathematical equivalence between consecutive lines: does Line 1 imply Line 2? Flag the exact line where equivalence breaks and state the mathematical reason."""

SAMPLES = [
    {
        "id": "sample1",
        "name": "Sample 1: Correct Multi-Step Linear Equation",
        "filename": "sample1_correct.png",
        "ground_truth_transcription": [
            "Solve 3(x - 4) = 15",
            "3x - 12 = 15",
            "3x = 27",
            "x = 9"
        ],
        "ground_truth_error": "None (Fully correct)",
        "expected_equivalence": "All lines are mathematically equivalent."
    },
    {
        "id": "sample2",
        "name": "Sample 2: Sign / Transposition Error",
        "filename": "sample2_sign_error.png",
        "ground_truth_transcription": [
            "Solve 2(x + 3) = 14",
            "2x + 6 = 14",
            "2x = 14 + 6",
            "2x = 20",
            "x = 10"
        ],
        "ground_truth_error": "Line 2 (2x = 14 + 6): Transposition error / added 6 instead of subtracting 6.",
        "expected_equivalence": "Equivalence breaks between Line 1 (2x + 6 = 14) and Line 2 (2x = 14 + 6). Correct step should be 2x = 14 - 6."
    },
    {
        "id": "sample3",
        "name": "Sample 3: Common Algebraic Misconception (Freshman's Dream)",
        "filename": "sample3_misconception.png",
        "ground_truth_transcription": [
            "Expand and simplify:",
            "(x + 3)^2 = x^2 + 9"
        ],
        "ground_truth_error": "Omission of cross-term 6x in binomial expansion (Freshman's Dream / (a+b)^2 != a^2 + b^2).",
        "expected_equivalence": "(x + 3)^2 expands to x^2 + 6x + 9, not x^2 + 9."
    }
]

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def query_model(image_base64, prompt_text):
    payload = {
        "model": MODEL_PATH,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt_text
                    }
                ]
            }
        ],
        "temperature": 0.1,
        "max_tokens": 768
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json"})
    
    start_time = time.time()
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    end_time = time.time()
    
    latency = end_time - start_time
    return res, latency

def run_all_benchmarks():
    results = []
    
    for sample in SAMPLES:
        img_path = os.path.join(SPIKE_DIR, sample["filename"])
        img_b64 = encode_image(img_path)
        
        print(f"\n==========================================")
        print(f"Running benchmarks for: {sample['name']}")
        print(f"==========================================")
        
        # Test Prompt A
        print(f"--- Running Prompt A (Naive Zero-Shot) ---")
        res_a, lat_a = query_model(img_b64, PROMPT_A)
        msg_a = res_a["choices"][0]["message"]["content"]
        timings_a = res_a.get("timings", {})
        usage_a = res_a.get("usage", {})
        tps_a = timings_a.get("predicted_per_second", usage_a.get("completion_tokens", 0) / lat_a if lat_a > 0 else 0)
        
        print(f"Prompt A Latency: {lat_a:.2f}s | TPS: {tps_a:.1f}")
        print(f"Response:\n{msg_a}\n")
        
        # Test Prompt B
        print(f"--- Running Prompt B (2-Step Decomposed) ---")
        res_b, lat_b = query_model(img_b64, PROMPT_B)
        msg_b = res_b["choices"][0]["message"]["content"]
        timings_b = res_b.get("timings", {})
        usage_b = res_b.get("usage", {})
        tps_b = timings_b.get("predicted_per_second", usage_b.get("completion_tokens", 0) / lat_b if lat_b > 0 else 0)
        
        print(f"Prompt B Latency: {lat_b:.2f}s | TPS: {tps_b:.1f}")
        print(f"Response:\n{msg_b}\n")
        
        results.append({
            "sample": sample,
            "prompt_a": {
                "response": msg_a,
                "latency_sec": round(lat_a, 2),
                "tokens_per_sec": round(tps_a, 1),
                "completion_tokens": usage_a.get("completion_tokens", 0),
                "prompt_tokens": usage_a.get("prompt_tokens", 0),
                "total_tokens": usage_a.get("total_tokens", 0)
            },
            "prompt_b": {
                "response": msg_b,
                "latency_sec": round(lat_b, 2),
                "tokens_per_sec": round(tps_b, 1),
                "completion_tokens": usage_b.get("completion_tokens", 0),
                "prompt_tokens": usage_b.get("prompt_tokens", 0),
                "total_tokens": usage_b.get("total_tokens", 0)
            }
        })
        
    # Save raw results
    raw_path = os.path.join(SPIKE_DIR, "benchmark_raw_results.json")
    with open(raw_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nRaw results saved to {raw_path}")
    
    return results

if __name__ == "__main__":
    run_all_benchmarks()
