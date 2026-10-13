import base64
import json
import time
import urllib.request

MODEL_PATH = "/Users/jiaen/.gemini/antigravity/scratch/llama-qwen/models/Qwen2.5-VL-7B/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf"
API_URL = "http://127.0.0.1:8081/v1/chat/completions"

with open("/Users/jiaen/Agy/AI Bootcamp/spike/sample1_correct.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": MODEL_PATH,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{b64}"
                    }
                },
                {
                    "type": "text",
                    "text": "Look at this student's handwritten math work. Is there an error? If so, find and explain the error."
                }
            ]
        }
    ],
    "temperature": 0.1,
    "max_tokens": 512
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(API_URL, data=data, headers={"Content-Type": "application/json"})

start_t = time.time()
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
latency = time.time() - start_t

print(f"Latency: {latency:.2f}s")
print(json.dumps(res, indent=2))
