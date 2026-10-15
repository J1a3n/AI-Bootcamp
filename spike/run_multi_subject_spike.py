"""
Multi-Subject Empirical Spike:
Evaluates Qwen 2.5-VL 7B (Vision/OCR + Sycophancy vs Balanced Rubric)
and Dual-Axis Vector Misconception Matching across Science, Humanities, and Economics.
"""
import os
import json
import time
import math
import random
import base64
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SPIKE_DIR = Path("/Users/jiaen/Agy/AI Bootcamp/spike")
SUBJECTS_DATA_DIR = Path("/Users/jiaen/Agy/AI Bootcamp/harness/data/subjects")
SPIKE_DIR.mkdir(parents=True, exist_ok=True)
SUBJECTS_DATA_DIR.mkdir(parents=True, exist_ok=True)

VL_API_URL = "http://127.0.0.1:8081/v1/chat/completions"
EMBED_API_URL = "http://127.0.0.1:8083/v1/embeddings"

FONT_PATH = "/System/Library/Fonts/Noteworthy.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"

SUBJECT_SAMPLES = [
    # ==================== SCIENCE ====================
    {
        "subject": "science",
        "id": "science_sample1",
        "name": "Science Sample 1: Correct Cellular Respiration & Mass Balance",
        "filename": "science_sample1_correct.png",
        "header": "Balance & classify cellular respiration:",
        "lines": [
            "Line 1: C6H12O6 + 6O2 -> 6CO2 + 6H2O + ATP",
            "Line 2: Reactants: 6 C, 12 H, 18 O",
            "Line 3: Products: 6 C, 12 H, 18 O (Exothermic)"
        ],
        "expected_status": "CORRECT",
        "expected_line_error": None,
        "ground_truth_note": "Fully balanced equation (6 C, 12 H, 18 O on both sides) and accurately classified as exothermic energy release."
    },
    {
        "subject": "science",
        "id": "science_sample2",
        "name": "Science Sample 2: Conservation of Mass Error (Gas Mass = 0g)",
        "filename": "science_sample2_error.png",
        "header": "Conservation of Mass (Sealed Flask Reaction):",
        "lines": [
            "Line 1: 12g Carbon reacts completely with 32g Oxygen.",
            "Line 2: Total reactant mass in sealed flask = 44g.",
            "Line 3: Since CO2 is a gas, final mass in flask = 0g."
        ],
        "expected_status": "INCORRECT",
        "expected_line_error": 3,
        "ground_truth_note": "Line 3 conservation of mass error: In a sealed flask, mass is conserved (12g + 32g = 44g of CO2 gas); gases have mass and do not vanish to 0g."
    },
    {
        "subject": "science",
        "id": "science_sample3",
        "name": "Science Sample 3: Plant Biomass Source Misconception",
        "filename": "science_sample3_misconception.png",
        "header": "Explain where a tree's dry mass comes from:",
        "lines": [
            "Line 1: Trees absorb water and soil through roots.",
            "Line 2: Most of a tree's solid wood mass comes from",
            "Line 3: soil minerals turning directly into wood."
        ],
        "expected_status": "INCORRECT",
        "expected_line_error": 2,
        "ground_truth_note": "Photosynthesis biomass misconception: Most plant dry biomass comes from atmospheric carbon dioxide (CO2) fixed during photosynthesis, not from soil."
    },
    # ==================== HUMANITIES ====================
    {
        "subject": "humanities",
        "id": "humanities_sample1",
        "name": "Humanities Sample 1: Cohesive Claim-Evidence-Reasoning (History)",
        "filename": "humanities_sample1_correct.png",
        "header": "Short Argument (1833 Factory Act):",
        "lines": [
            "Line 1: Claim: The 1833 Factory Act restricted child labor.",
            "Line 2: Evidence: It banned textile work under age 9.",
            "Line 3: Reasoning: Paid inspectors enforced the age limit."
        ],
        "expected_status": "CORRECT",
        "expected_line_error": None,
        "ground_truth_note": "Historically accurate claim supported by specific statutory evidence and logical reasoning."
    },
    {
        "subject": "humanities",
        "id": "humanities_sample2",
        "name": "Humanities Sample 2: Claim-Evidence Contradiction (1920s Economy)",
        "filename": "humanities_sample2_error.png",
        "header": "Argument Analysis (1920s US Agriculture):",
        "lines": [
            "Line 1: Claim: 1920s economic boom helped US farmers.",
            "Line 2: Evidence: Crop prices fell 40% after WWI.",
            "Line 3: Reasoning: Steep price drops made farmers rich."
        ],
        "expected_status": "INCORRECT",
        "expected_line_error": 3,
        "ground_truth_note": "Logical contradiction between evidence and reasoning/claim: A 40% drop in crop prices caused severe rural debt and farm foreclosures, not wealth."
    },
    {
        "subject": "humanities",
        "id": "humanities_sample3",
        "name": "Humanities Sample 3: Primary Source Bias Misconception",
        "filename": "humanities_sample3_misconception.png",
        "header": "Source Evaluation (1914 Wartime Newspaper):",
        "lines": [
            "Line 1: Source: Front-page editorial from August 1914.",
            "Line 2: Evaluation: Because this is a primary source",
            "Line 3: written during WWI, it is 100% unbiased fact."
        ],
        "expected_status": "INCORRECT",
        "expected_line_error": 2,
        "ground_truth_note": "Primary source misconception: Equating primary/contemporaneous sources with unbiased objective fact, ignoring wartime censorship and authorial perspective."
    },
    # ==================== ECONOMICS ====================
    {
        "subject": "economics",
        "id": "economics_sample1",
        "name": "Economics Sample 1: Correct Supply Shock Analysis",
        "filename": "economics_sample1_correct.png",
        "header": "Coffee Market (Severe Frost in Brazil):",
        "lines": [
            "Line 1: Frost destroys 30% of coffee bean harvest.",
            "Line 2: Supply curve shifts left (S1 -> S2).",
            "Line 3: Equilibrium price rises, quantity falls."
        ],
        "expected_status": "CORRECT",
        "expected_line_error": None,
        "ground_truth_note": "Accurate comparative statics: negative supply shock shifts supply left, raising equilibrium price and lowering equilibrium quantity."
    },
    {
        "subject": "economics",
        "id": "economics_sample2",
        "name": "Economics Sample 2: Equilibrium Direction Error",
        "filename": "economics_sample2_error.png",
        "header": "Laptop Market (Consumer Income Rises):",
        "lines": [
            "Line 1: Higher income increases demand for laptops.",
            "Line 2: Demand curve shifts right (D1 -> D2).",
            "Line 3: Equilibrium price rises and quantity falls."
        ],
        "expected_status": "INCORRECT",
        "expected_line_error": 3,
        "ground_truth_note": "Line 3 equilibrium error: When demand shifts right (with upward-sloping supply), equilibrium price rises AND equilibrium quantity rises (not falls)."
    },
    {
        "subject": "economics",
        "id": "economics_sample3",
        "name": "Economics Sample 3: Shift vs Movement Along Curve Misconception",
        "filename": "economics_sample3_misconception.png",
        "header": "Effect of a store raising shoe prices ($50 -> $70):",
        "lines": [
            "Line 1: The price of shoes rises from $50 to $70.",
            "Line 2: This price increase causes the entire",
            "Line 3: Demand curve for shoes to shift left."
        ],
        "expected_status": "INCORRECT",
        "expected_line_error": 2,
        "ground_truth_note": "Demand shift vs movement misconception: A change in the good's own price causes a movement along the existing demand curve (decrease in quantity demanded), not a shift of the demand curve."
    }
]


def create_notebook_background(width=760, height=360, line_spacing=48, margin_x=65):
    img = Image.new("RGB", (width, height), (252, 252, 250))
    draw = ImageDraw.Draw(img)
    for y in range(line_spacing, height, line_spacing):
        draw.line([(0, y), (width, y)], fill=(210, 225, 240), width=1)
    draw.line([(margin_x, 0), (margin_x, height)], fill=(240, 180, 180), width=2)
    return img


def render_handwritten_sample(sample: dict):
    img = create_notebook_background(width=780, height=340, line_spacing=50, margin_x=65)
    draw = ImageDraw.Draw(img)
    try:
        font_header = ImageFont.truetype(FONT_PATH, 26)
        font_body = ImageFont.truetype(FONT_PATH, 27)
    except Exception:
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()

    ink_color = (22, 32, 72)
    random.seed(hash(sample["id"]))

    # Draw header
    draw.text((82, 30), sample["header"], fill=(60, 20, 40), font=font_header)

    # Draw student lines
    y_pos = 90
    for line in sample["lines"]:
        jx = 85 + random.randint(-1, 1)
        jy = y_pos + random.randint(-1, 1)
        draw.text((jx, jy), line, fill=ink_color, font=font_body)
        y_pos += 50

    # Save to spike/ and harness/data/subjects/<subject>/
    spike_path = SPIKE_DIR / sample["filename"]
    img.save(spike_path)

    subj_dir = SUBJECTS_DATA_DIR / sample["subject"]
    subj_dir.mkdir(parents=True, exist_ok=True)
    img.save(subj_dir / sample["filename"])
    return spike_path


PROMPT_A_NAIVE = (
    "Look at this student's handwritten work. Is there an error or flaw? "
    "If so, find and explain the error."
)

PROMPT_B_BALANCED = """Step 1: Transcribe the handwritten student work line-by-line accurately.
Step 2: Evaluate each line for domain accuracy, factual validity, and logical consistency.
- Null Hypothesis (Default): Assume the student's work may be completely valid. If all lines are accurate and logically sound, output 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.
- Alternative Hypothesis: Only if a clear factual, logical, or procedural error exists, output 'STATUS: INCORRECT', identify the line number where the error occurs (e.g., 'LINE_ERROR: 2' or 'LINE_ERROR: 3'), and briefly explain the misconception."""


def query_vl_model(image_path: Path, prompt_text: str):
    b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                    {"type": "text", "text": prompt_text}
                ]
            }
        ],
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
    latency = time.perf_counter() - t0
    msg = data["choices"][0]["message"]["content"]
    timings = data.get("timings", {})
    usage = data.get("usage", {})
    tps = timings.get("predicted_per_second", usage.get("completion_tokens", 0) / max(latency, 0.001))
    return {
        "response": msg,
        "latency_sec": round(latency, 2),
        "tokens_per_sec": round(tps, 1),
        "completion_tokens": usage.get("completion_tokens", 0),
        "prompt_tokens": usage.get("prompt_tokens", 0)
    }


def get_embedding_768(text: str) -> list:
    payload = {"input": text}
    req = urllib.request.Request(
        EMBED_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    raw_vec = data["data"][0]["embedding"]
    # Project / slice to 768-D and normalize to unit sphere
    vec_768 = raw_vec[:768]
    norm = math.sqrt(sum(x * x for x in vec_768)) or 1.0
    return [x / norm for x in vec_768]


def cosine_sim(u: list, v: list) -> float:
    return sum(a * b for a, b in zip(u, v))


def run_vector_benchmark():
    catalog = [
        {
            "subject": "science",
            "id": "sci_mass_conservation",
            "title": "Stoichiometry Atom Count / Conservation of Mass Error",
            "description": "Student miscounts oxygen or hydrogen atoms across reactants and products when balancing a chemical reaction.",
            "sample_ref": "science_sample2_error.png"
        },
        {
            "subject": "science",
            "id": "sci_plant_biomass",
            "title": "Photosynthesis Biomass Source Misconception (Soil vs Air CO2)",
            "description": "Student believes plant dry wood mass comes from absorbing soil minerals through roots instead of fixing atmospheric carbon dioxide (CO2).",
            "sample_ref": "science_sample3_misconception.png"
        },
        {
            "subject": "humanities",
            "id": "hum_evidence_contradiction",
            "title": "Claim-Evidence Logical Contradiction",
            "description": "Student cites historical or textual evidence (such as falling farm crop prices) that directly contradicts their thesis claim of universal prosperity.",
            "sample_ref": "humanities_sample2_error.png"
        },
        {
            "subject": "humanities",
            "id": "hum_primary_source_bias",
            "title": "Primary Source Neutrality Misconception",
            "description": "Student assumes that because a newspaper or diary is a primary source from the time period, it is automatically unbiased objective fact.",
            "sample_ref": "humanities_sample3_misconception.png"
        },
        {
            "subject": "economics",
            "id": "econ_equilibrium_direction",
            "title": "Demand Shift Equilibrium Quantity Direction Error",
            "description": "Student shifts the demand curve right correctly but states that equilibrium quantity falls instead of rises.",
            "sample_ref": "economics_sample2_error.png"
        },
        {
            "subject": "economics",
            "id": "econ_shift_vs_movement",
            "title": "Shift of Demand Curve vs Movement Along Curve Misconception",
            "description": "Student confuses a change in a good's own price (movement along the demand curve) with a shift of the entire demand curve.",
            "sample_ref": "economics_sample3_misconception.png"
        }
    ]

    teacher_queries = [
        ("science", "Students who think trees get their mass from soil instead of carbon dioxide in the air", "sci_plant_biomass"),
        ("science", "Students who miscounted atoms when balancing a combustion reaction", "sci_mass_conservation"),
        ("humanities", "Students who think primary sources from wartime are completely unbiased facts", "hum_primary_source_bias"),
        ("humanities", "Students whose cited evidence contradicts their main argument claim", "hum_evidence_contradiction"),
        ("economics", "Students who shifted the whole demand curve when only the item's own price changed", "econ_shift_vs_movement"),
        ("economics", "Students who said equilibrium quantity falls when demand shifts right", "econ_equilibrium_direction"),
    ]

    for item in catalog:
        item["vec"] = get_embedding_768(f"{item['title']}: {item['description']}")

    vector_results = []
    for subj, q_text, expected_id in teacher_queries:
        q_vec = get_embedding_768(q_text)
        scored = []
        for item in catalog:
            sim = cosine_sim(q_vec, item["vec"])
            scored.append((sim, item))
        scored.sort(key=lambda x: x[0], reverse=True)
        top_sim, top_item = scored[0]
        second_sim, second_item = scored[1]
        vector_results.append({
            "subject": subj,
            "query": q_text,
            "expected_id": expected_id,
            "matched_id": top_item["id"],
            "matched_title": top_item["title"],
            "sample_ref": top_item["sample_ref"],
            "top_cosine_sim": round(top_sim, 4),
            "runner_up_sim": round(second_sim, 4),
            "margin": round(top_sim - second_sim, 4),
            "passed": top_item["id"] == expected_id
        })
    return vector_results


def main():
    print("1. Rendering 9 synthetic student handwriting samples across Science, Humanities, and Economics...")
    for sample in SUBJECT_SAMPLES:
        p = render_handwritten_sample(sample)
        print(f"   [✓] Generated {p.name}")

    print("\n2. Running Qwen 2.5-VL-7B Vision & Rubric Benchmarks (Naive Prompt A vs Balanced Prompt B)...")
    vl_results = []
    for sample in SUBJECT_SAMPLES:
        img_path = SPIKE_DIR / sample["filename"]
        print(f"\n--- Benchmarking {sample['name']} ---")
        res_a = query_vl_model(img_path, PROMPT_A_NAIVE)
        print(f"  Prompt A (Naive): {res_a['latency_sec']}s @ {res_a['tokens_per_sec']} tok/s")
        res_b = query_vl_model(img_path, PROMPT_B_BALANCED)
        print(f"  Prompt B (Balanced): {res_b['latency_sec']}s @ {res_b['tokens_per_sec']} tok/s")
        vl_results.append({
            "sample": sample,
            "prompt_a": res_a,
            "prompt_b": res_b
        })

    print("\n3. Running Cross-Subject Dual-Axis 768-D Vector Retrieval Benchmark...")
    vec_results = run_vector_benchmark()
    for vr in vec_results:
        status = "PASS" if vr["passed"] else "FAIL"
        print(f"  [{status}] ({vr['subject']}) '{vr['query'][:50]}...' -> {vr['matched_title']} (sim={vr['top_cosine_sim']}, margin=+{vr['margin']})")

    output = {
        "vision_benchmarks": vl_results,
        "vector_benchmarks": vec_results
    }
    out_path = SPIKE_DIR / "multi_subject_benchmark_results.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\nSaved full multi-subject spike results to {out_path}")


if __name__ == "__main__":
    main()
