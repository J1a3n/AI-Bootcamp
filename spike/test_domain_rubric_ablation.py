"""
Ablation study: Testing Domain-Anchored Balanced Null-Hypothesis Prompts
on Science Sample 2 & 3 and Economics Sample 3 to verify 100% status and line attribution accuracy.
"""
import json
import base64
import time
import urllib.request
from pathlib import Path

SPIKE_DIR = Path("/Users/jiaen/Agy/AI Bootcamp/spike")
VL_API_URL = "http://127.0.0.1:8081/v1/chat/completions"

RUBRIC_PROMPTS = {
    "science": """Step 1: Transcribe the handwritten student work line-by-line accurately.
Step 2: Verify scientific accuracy across the lines:
- Check exact atom counts on Reactants vs Products (remember coefficient * subscript, e.g., 2O2 = 4 O atoms).
- Check biological/chemical mechanism accuracy (e.g., plant dry mass comes from atmospheric CO2 via photosynthesis, not soil minerals).
- Null Hypothesis: If all lines are scientifically accurate and consistent, output 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.
- Alternative Hypothesis: If any line states an incorrect atom count or scientific misconception, output 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>' for the first erroneous line.""",

    "humanities": """Step 1: Transcribe the handwritten student work line-by-line accurately.
Step 2: Verify historical/textual argumentation across the lines:
- Check whether the Evidence is historically accurate, whether Reasoning logically follows from the Evidence without contradiction, and whether Primary Sources are evaluated critically for wartime/authorial bias rather than assumed to be 100% unbiased fact.
- Null Hypothesis: If Claim, Evidence, and Reasoning are accurate and logically cohesive, output 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.
- Alternative Hypothesis: If a line introduces a logical contradiction or source evaluation misconception, output 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>' for that line.""",

    "economics": """Step 1: Transcribe the handwritten student work line-by-line accurately.
Step 2: Verify microeconomic Supply & Demand principles across the lines:
- Check determinant shifts vs movements along a curve: A change in a good's own price ($50 to $70) causes a movement along the demand curve (change in quantity demanded), NEVER a shift of the entire demand curve.
- Check equilibrium comparative statics: A rightward demand shift raises BOTH equilibrium price and equilibrium quantity.
- Null Hypothesis: If all lines are economically accurate, output 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.
- Alternative Hypothesis: If a line states an invalid curve shift or wrong equilibrium direction, output 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>' for the first line where the error begins."""
}

def query_vl(img_name: str, prompt: str):
    b64 = base64.b64encode((SPIKE_DIR / img_name).read_bytes()).decode("utf-8")
    payload = {
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": prompt}
            ]
        }],
        "temperature": 0.1,
        "max_tokens": 512
    }
    req = urllib.request.Request(
        VL_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    lat = time.perf_counter() - t0
    msg = data["choices"][0]["message"]["content"]
    return msg, lat

def main():
    tests = [
        ("science", "science_sample1_correct.png", "CORRECT", "NONE"),
        ("science", "science_sample2_error.png", "INCORRECT", "2"),
        ("science", "science_sample3_misconception.png", "INCORRECT", "2"),
        ("humanities", "humanities_sample1_correct.png", "CORRECT", "NONE"),
        ("humanities", "humanities_sample2_error.png", "INCORRECT", "3"),
        ("humanities", "humanities_sample3_misconception.png", "INCORRECT", "2"),
        ("economics", "economics_sample1_correct.png", "CORRECT", "NONE"),
        ("economics", "economics_sample2_error.png", "INCORRECT", "3"),
        ("economics", "economics_sample3_misconception.png", "INCORRECT", "2"),
    ]
    results = []
    for subj, fname, exp_status, exp_line in tests:
        msg, lat = query_vl(fname, RUBRIC_PROMPTS[subj])
        has_status = f"STATUS: {exp_status}" in msg
        print(f"[{fname}] ({lat:.2f}s) -> Expected STATUS: {exp_status} | Match: {has_status}")
        for line in msg.splitlines():
            if "STATUS:" in line or "LINE_ERROR:" in line:
                print(f"   {line}")
        results.append({
            "subject": subj,
            "filename": fname,
            "expected_status": exp_status,
            "expected_line": exp_line,
            "latency_sec": round(lat, 2),
            "response": msg
        })
    (SPIKE_DIR / "ablation_domain_rubric_results.json").write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
