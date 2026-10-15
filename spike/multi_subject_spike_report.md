# Multi-Subject Technical & Pedagogical Spike Report: Expanding the AI Systems Bootcamp to All Subject Teachers

**Date:** October 15, 2026  
**Models Evaluated:**
- **Vision & Rubric Evaluation:** `Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` (`http://127.0.0.1:8081`)
- **Fast Text / Speedometer Engine:** `qwen2.5-0.5b-instruct-q4_k_m.gguf` (`http://127.0.0.1:8082`)
- **768-D Semantic Vector Engine:** `gte-Qwen2-7B-instruct-Q5_K_M.gguf` (`http://127.0.0.1:8083`)  
**Target Tracks Tested:** Mathematics (`math`), Science (`science`), Humanities (`humanities`), Social Sciences / Economics (`economics`)

---

## 1. Executive Summary

This spike investigated how to make the **AI Bootcamp: Systems Architecture, Local Infrastructure & Applied AI** relevant, rigorous, and turn-key for high-school educators across **all subject disciplines**—not only Mathematics.

### Core Findings
1. **The Systems Architecture is 100% Universal Across Classroom Subjects:**
   Every pain point that drives the 4-Sprint progression—cloud privacy concerns (Sprint 1), capturing handwritten student notebook work on a dim classroom projector in `< 1s` (Sprint 2), the 18-second synchronous AI freeze requiring Fast-Lane/Slow-Lane decoupling (Sprint 3), and searching student archives by underlying misconception rather than exact keywords (Sprint 4)—applies identically to Chemistry lab notebooks, AP History DBQ short-answer paragraphs, and Microeconomics Supply & Demand responses.
2. **100% Optical Character Recognition (OCR) Across Prose, Chemical Formulas, and Causal Arrows:**
   Across 12 handwritten student samples spanning 4 subjects, local **Qwen 2.5-VL 7B** sustained **152.0–153.1 tokens/sec** (`1.25s–2.20s` end-to-end latency) and achieved **100% transcription accuracy** on chemical equations ($\text{C}_6\text{H}_{12}\text{O}_6 + 6\text{O}_2 \to 6\text{CO}_2 + 6\text{H}_2\text{O} + \text{ATP}$), multi-line historical arguments, and economic shift notation ($S_1 \to S_2$, $\$50 \to \$70$).
3. **The "Error Hunter" Sycophancy Trap Generalizes—and Needs Domain-Anchored Null Hypotheses:**
   - Under a naive prompt (*"Is there an error or flaw?"*), Qwen 2.5-VL hallucinated atom-balancing flaws on a 100% balanced cellular respiration equation (`science_sample1_correct.png`), echoing the exact sycophancy bias seen in algebra.
   - Furthermore, multi-line prose introduces **Line-Wrap Fragmentation**: when a sentence wraps across two physical lines on notebook paper (`Line 2` -> `Line 3`), a generic line-by-line equivalence prompt flags Line 2 as an "incomplete sentence" while missing the actual conceptual error. Anchoring the Balanced Null-Hypothesis prompt with a lightweight **Subject Rubric Rule** achieved **12/12 (100%) classification accuracy** across all four disciplines.
4. **The 0.5B "Pocket Calculator" Boundary in Humanities vs. STEM:**
   - While `qwen2.5-0.5b` (running at **379–397 tok/s**) reliably solves simple linear equations (`3(x - 4) = 15`) and stoichiometry coefficients (`CH4 + 2O2`), asking it open-domain historical trivia (*"What was the minimum working age in the 1833 Factory Act?"*) caused it to hallucinate `14` instead of `9`.
   - **Architectural Lesson for Non-STEM Tracks:** Tiny 0.5B models have minimal parametric memory for historical facts, dates, or quotes; they excel when framed as **extractive processors** (extracting a student's claim or age citation from a provided source excerpt).
5. **Cross-Subject 768-D Vector Retrieval Achieves 100% Top-1 Recall:**
   Using unit-sphere normalized 768-D embeddings (`gte-Qwen2-7B`), natural-language teacher queries accurately matched canonical misconceptions across Science, Humanities, and Economics (`0.589–0.775` cosine similarity, with `+0.051` to `+0.244` separation margin over the runner-up).

---

## 2. Empirical Benchmark 1: Vision & Rubric Evaluation Across Subjects

In addition to the 3 baseline Mathematics samples, 9 new synthetic handwritten worksheets were generated in `spike/` and `harness/data/subjects/<subject>/`:

| Subject Track | Sample 1 (100% Valid Work) | Sample 2 (Procedural / Logical Error) | Sample 3 (Canonical Conceptual Misconception) |
| :--- | :--- | :--- | :--- |
| **Mathematics (`math`)** | `sample1_correct.png`<br>$3(x-4)=15 \implies x=9$ | `sample2_sign_error.png`<br>$2x+6=14 \implies 2x=14+6$ (Line 2 sign error) | `sample3_misconception.png`<br>$(x+3)^2 = x^2 + 9$ (Omitted cross-term $6x$) |
| **Science (`science`)** | `science_sample1_correct.png`<br>Balanced cellular respiration & atom count ($6\text{C}, 12\text{H}, 18\text{O}$) | `science_sample2_error.png`<br>Sealed flask: $12\text{g C} + 32\text{g O}_2 = 44\text{g}$, claims gas product mass $= 0\text{g}$ | `science_sample3_misconception.png`<br>Claims tree dry wood mass comes from soil minerals rather than air $\text{CO}_2$ |
| **Humanities (`humanities`)** | `humanities_sample1_correct.png`<br>Cohesive Claim-Evidence-Reasoning on 1833 Factory Act | `humanities_sample2_error.png`<br>Evidence cites 40% crop price drop, but Reasoning claims drop made farmers rich | `humanities_sample3_misconception.png`<br>Claims 1914 wartime editorial is 100% unbiased fact because it is a primary source |
| **Economics (`economics`)** | `economics_sample1_correct.png`<br>Brazil frost shifts coffee Supply left ($S_1 \to S_2$), $P \uparrow, Q \downarrow$ | `economics_sample2_error.png`<br>Rising income shifts Demand right ($D_1 \to D_2$), claims $Q \downarrow$ instead of $Q \uparrow$ | `economics_sample3_misconception.png`<br>Shoe price rises $\$50 \to \$70$; claims own-price change shifts entire Demand curve left |

### Quantitative Results (`Qwen2.5-VL-7B-Instruct-Q4_K_M`)

| Sample File | OCR Accuracy | Throughput (tok/s) | Naive Prompt A ("Find the error") | Generic Balanced Prompt B | Domain-Anchored Balanced Prompt |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `science_sample1_correct.png` | 100% | 152.6 tok/s | **FAIL** (False Positive on ATP O atoms) | **PASS** (`CORRECT`, `1.52s`) | **PASS** (`CORRECT`, `1.57s`) |
| `science_sample2_error.png` | 100% | 152.5 tok/s | **PASS** (Caught mass error) | **PASS** (`INCORRECT`, `1.66s`) | **PASS** (`INCORRECT`, `1.82s`) |
| `science_sample3_misconception.png` | 100% | 153.1 tok/s | **PASS** (Caught $\text{CO}_2$ vs soil) | **PASS** (`INCORRECT`, `1.77s`) | **PASS** (`INCORRECT`, `0.67s`) |
| `humanities_sample1_correct.png` | 100% | 152.9 tok/s | **PARTIAL** (Nitpicked redundant age) | **PASS** (`CORRECT`, `1.57s`) | **PASS** (`CORRECT`, `1.29s`) |
| `humanities_sample2_error.png` | 100% | 152.8 tok/s | **PASS** (Caught Line 3 contradiction) | **PASS** (`INCORRECT`, `1.62s`) | **PASS** (`INCORRECT`, `1.68s`) |
| `humanities_sample3_misconception.png` | 100% | 152.5 tok/s | **PASS** (Caught wartime bias) | **PASS** (`INCORRECT`, `1.66s`) | **PASS** (`INCORRECT`, `1.36s`) |
| `economics_sample1_correct.png` | 100% | 152.0 tok/s | **PASS** (No false positive) | **PASS** (`CORRECT`, `1.28s`) | **PASS** (`CORRECT`, `1.29s`) |
| `economics_sample2_error.png` | 100% | 152.6 tok/s | **PASS** (Caught Line 3 $Q$ direction) | **PASS** (`INCORRECT`, `1.59s`) | **PASS** (`INCORRECT`, `0.64s`) |
| `economics_sample3_misconception.png` | 100% | 152.8 tok/s | **PASS** (Caught shift vs movement) | **FAIL** (Line-wrap distraction) | **PASS** (`INCORRECT`, `0.09s`) |

---

## 3. Empirical Benchmark 2: Cross-Subject Dual-Axis 768-D Vector Retrieval

Each subject track defines two axes in $\mathbb{R}^{768}$:
- **Axis 1 (Curriculum Standard / Skill):** e.g., NGSS `HS-LS1-5` (Science), AP Historical Thinking Skill 2 `Sourcing` (Humanities), CEE Microeconomics Standard 8 `Role of Prices` (Economics).
- **Axis 2 (Canonical Student Misconceptions):** Mapped into unit-sphere normalized 768-D vectors.

| Subject Track | Teacher Natural-Language Query | Top Matched Misconception in $\mathbb{R}^{768}$ | Top Cosine Similarity | Runner-Up Similarity | Separation Margin | Status |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Science** | *"Students who think trees get their mass from soil instead of carbon dioxide in the air"* | `Photosynthesis Biomass Source Misconception (Soil vs Air CO2)` | **0.5890** | 0.3448 | `+0.2442` | **PASS** |
| **Science** | *"Students who miscounted atoms when balancing a combustion reaction"* | `Stoichiometry Atom Count / Conservation of Mass Error` | **0.6973** | 0.4735 | `+0.2238` | **PASS** |
| **Humanities** | *"Students who think primary sources from wartime are completely unbiased facts"* | `Primary Source Neutrality Misconception` | **0.5994** | 0.4954 | `+0.1040` | **PASS** |
| **Humanities** | *"Students whose cited evidence contradicts their main argument claim"* | `Claim-Evidence Logical Contradiction` | **0.7654** | 0.6111 | `+0.1543` | **PASS** |
| **Economics** | *"Students who shifted the whole demand curve when only the item's own price changed"* | `Shift of Demand Curve vs Movement Along Curve Misconception` | **0.7044** | 0.6539 | `+0.0506` | **PASS** |
| **Economics** | *"Students who said equilibrium quantity falls when demand shifts right"* | `Demand Shift Equilibrium Quantity Direction Error` | **0.7753** | 0.6371 | `+0.1382` | **PASS** |

---

## 4. Curriculum & Mental Model Adaptation for Non-Math Educators

In the original curriculum blueprint, Principle 3 (*Mathematical Grounding*) explained AI systems using linear algebra ($\mathbb{R}^{768}$, cosine similarity $\frac{\mathbf{u}\cdot\mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}$), graph theory (DAGs), and probability distributions ($p50/p95/p99$).

To make the course equally empowering for Humanities, Science, and Social Science teachers—without losing an ounce of technical rigor—we introduce **Domain-Bridged Mental Models**:

| Engineering Concept | Universal Educator Analogy (All Teachers) | Science Bridge (`science`) | Humanities Bridge (`humanities`) | Economics Bridge (`economics`) | Math Bridge (`math`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **High-Dimensional Vectors ($\mathbb{R}^{768}$)** | **The 768-Slider Rubric Card:** Instead of grading on 4 rubric rows, imagine a profile card with 768 sliders capturing every nuance of a student's thought. | **Chemical Spectrum Fingerprint:** Classifying a sample across 768 measurable wavelengths or lab traits. | **Literary & Historical Trait Profile:** Cataloging an essay across 768 sliders for tone, sourcing, thesis, and era. | **768-Indicator Economic Basket:** Tracking 768 market signals to locate the exact state of an argument. | **Coordinate Space ($\mathbb{R}^{768}$):** Plotting a point along 768 orthogonal axes. |
| **Cosine Similarity ($\frac{\mathbf{u}\cdot\mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}$)** | **Compass Direction Match:** Checks whether two student responses point toward the same underlying idea (1.0 = identical direction), even if they use completely different words. | **Spectrometer Alignment:** Comparing a student's lab conclusion against a reference absorption spectrum. | **Thematic Alignment:** Finding essays that share the same logical flaw without relying on `Ctrl+F` exact words. | **Directional Co-Movement:** Measuring whether two arguments move in the exact same conceptual direction. | **Normalized Dot Product:** Cosine of the angle between unit vectors on $S^{767}$. |
| **Git Branches & Merge (DAG)** | **The Lesson Plan Sandbox:** Copying your master lesson plan onto scratch paper to test a risky new activity, and only stapling it into the master binder once it works. | **Controlled Lab Trial vs Control Group:** Running an experimental protocol on a side bench before updating the lab manual. | **Rough Draft Margin Revision:** Drafting an alternate paragraph in the margin before pasting it into the final manuscript. | **Policy Counterfactual Simulation:** Testing a policy shock in a model before deploying it to the real economy. | **Directed Acyclic Graph (DAG):** Diverging and merging commit nodes without cycles. |
| **Tail Latencies ($p50 / p95 / p99$)** | **The Slowest Lab Group Rule:** Average speed ($p50$) hides the one student whose tablet freezes for 18 seconds ($p99$) and derails the whole class discussion. | **Rate-Limiting Step:** The slowest bottleneck step that determines when the whole lab period finishes. | **Seminar Pacing:** Waiting for the last student's page to load before starting a Socratic discussion. | **Income vs Outlier Distribution:** Why median ($p50$) vs top 1% ($p99$) matters for system bottlenecks. | **Quantiles of the Latency PDF:** 50th, 95th, and 99th percentile response times. |

---

## 5. Pluggable Subject Pack Architecture (`harness/subjects/`)

The repository now implements a clean **Pluggable Subject Pack** pattern:

```text
harness/
├── cli.py                       # Supports `tracks`, `select <subject>`, and `check <slice> --subject <id>`
├── preflight.py                 # Reports active Subject Track during `check 0`
├── subjects/
│   ├── __init__.py
│   └── registry.py              # Self-contained packs: math, science, humanities, economics
└── data/
    └── subjects/
        ├── math/                # Algebra handwritten samples
        ├── science/             # Chemistry & Biology handwritten samples
        ├── humanities/          # History & English CER handwritten samples
        └── economics/           # Supply & Demand handwritten samples
```

### How a Teacher Selects Their Subject Track
1. **Conversational Onboarding (Zero-Terminal):** During Module 1.0, the Mentor asks the teacher what subject they teach and automatically runs `python -m harness select <subject>` in the background.
2. **CLI Commands:**
   - `python -m harness tracks` — Lists all installed Subject Packs and highlights the active track.
   - `python -m harness select science` — Persists `BOOTCAMP_SUBJECT=science` in `.env.local` so all subsequent checkpoints (`1.1` through `4.2`) use Science prompts, worksheets, and misconceptions.
   - `python -m harness check 3.1 --subject humanities` — Runs any individual checkpoint against a specific subject track on the fly.
