"""
Pluggable Subject Pack Registry (`harness/subjects/registry.py`)

Defines domain-specific packs for:
  - math:       High-School Mathematics (Algebra & Symbolic Equivalence)
  - science:    High-School Science (Chemistry Stoichiometry & Biology Mechanisms)
  - humanities: High-School Humanities (History & English Claim-Evidence-Reasoning)
  - economics:  High-School Social Sciences (Microeconomics Supply & Demand)

Also provides a simple interface to read/write the active subject track in `.env.local`
or override via `BOOTCAMP_SUBJECT` environment variable.
"""
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

SUBJECT_PACKS: Dict[str, Dict[str, Any]] = {
    "math": {
        "id": "math",
        "title": "Mathematics (Algebra & Functions)",
        "teacher_persona": "Experienced High-School Mathematics Teacher",
        "notation_label": "LaTeX",
        "status_badge_ready": "LaTeX Ready",
        # Sprint 1: Engine Ignition & Telemetry Prompt
        "ignition_prompt": "Solve 3(x - 4) = 15",
        "ignition_expected_token": "9",
        "queue_task_type": "algebra_verification",
        # Sprint 2: Collector & Cloud Persistence Metadata
        "sample_student_alias": "Maya_Period_3",
        "sample_topic": "Algebra I - Multi-step Equations",
        "content_blind_search_example": "distributive property or negative sign error",
        # Sprint 3: Vision Worker & Balanced Null-Hypothesis Rubric
        "samples": {
            "sample1_correct": {
                "filename": "sample1_correct.png",
                "path": "harness/data/sample1_correct.png",
                "expected_status": "CORRECT",
                "expected_line_error": None,
                "description": "Solve 3(x - 4) = 15 -> 3x - 12 = 15 -> 3x = 27 -> x = 9"
            },
            "sample2_error": {
                "filename": "sample2_sign_error.png",
                "path": "harness/data/sample2_sign_error.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 2,
                "description": "Solve 2(x + 3) = 14 -> 2x + 6 = 14 -> 2x = 14 + 6 (Line 2 sign error)"
            },
            "sample3_misconception": {
                "filename": "sample3_misconception.png",
                "path": "harness/data/sample3_misconception.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 1,
                "description": "Expand (x + 3)^2 = x^2 + 9 (Freshman's Dream / omitted cross-term 6x)"
            }
        },
        "balanced_rubric_prompt": (
            "Step 1: Transcribe the handwritten math working line-by-line into LaTeX.\n"
            "Step 2: Check mathematical equivalence between consecutive lines and verify by substitution.\n"
            "- Null Hypothesis: If all lines are mathematically valid, state 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.\n"
            "- Alternative Hypothesis: If equivalence breaks, state 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>'."
        ),
        # Sprint 4: Dual-Axis pgvector Misconceptions & Queries
        "curriculum_skills": [
            "REI.B.3: Solve linear equations and inequalities in one variable",
            "APR.A.1: Expand and factor polynomial expressions"
        ],
        "misconceptions": [
            {
                "id": "math_sign_error",
                "matched_misconception": "Transposition Sign Error (Adding instead of Subtracting across '=' sign)",
                "category": "Linear Equations & Inverse Operations",
                "sample_reference": "sample2_sign_error.png",
                "keywords": ["sign", "transposition", "subtract", "add", "plus", "minus", "inverse"]
            },
            {
                "id": "math_distributive",
                "matched_misconception": "Distributive Property / Binomial Expansion Cross-Term Omission",
                "category": "Polynomial & Algebraic Expansion",
                "sample_reference": "sample3_misconception.png",
                "keywords": ["distributive", "parentheses", "binomial", "expand", "second term", "cross-term"]
            }
        ],
        "verification_queries": [
            {
                "query": "Students who made a transposition sign error",
                "expected_substring": "Sign Error",
                "expected_sample": "sample2_sign_error.png"
            },
            {
                "query": "Students who omitted multiplying parentheses on the second term",
                "expected_substring": "Distributive",
                "expected_sample": "sample3_misconception.png"
            }
        ],
        # Pedagogical Mental Model Bridge
        "mental_models": {
            "vector_space": "High-Dimensional Coordinate Space (R^768): Just like plotting (x, y, z) coordinates in geometry, the AI plots each student response across 768 mathematical concept axes.",
            "cosine_similarity": "Cosine Similarity (u · v / ||u||||v||): Measures the angle between two concept vectors—0 degrees (1.0) means identical mathematical reasoning.",
            "percentiles": "Latency Distribution (p50 / p95 / p99): Like median vs top-1% exam scores, p99 reveals the worst classroom lag experienced by the unluckiest student upload."
        }
    },

    "science": {
        "id": "science",
        "title": "Science (Chemistry & Biology)",
        "teacher_persona": "Experienced High-School Science Teacher (Chemistry & Biology)",
        "notation_label": "Chemical & Scientific Notation",
        "status_badge_ready": "LaTeX Ready",
        # Sprint 1
        "ignition_prompt": "Balance the chemical equation CH4 + O2 -> CO2 + H2O and state the coefficient of O2.",
        "ignition_expected_token": "2",
        "queue_task_type": "science_verification",
        # Sprint 2
        "sample_student_alias": "Liam_Lab_Group_2",
        "sample_topic": "Chemistry - Stoichiometry & Conservation of Mass",
        "content_blind_search_example": "unbalanced oxygen atoms or photosynthesis mass misconception",
        # Sprint 3
        "samples": {
            "sample1_correct": {
                "filename": "science_sample1_correct.png",
                "path": "harness/data/subjects/science/science_sample1_correct.png",
                "expected_status": "CORRECT",
                "expected_line_error": None,
                "description": "C6H12O6 + 6O2 -> 6CO2 + 6H2O + ATP | 6 C, 12 H, 18 O on both sides (Exothermic)"
            },
            "sample2_error": {
                "filename": "science_sample2_error.png",
                "path": "harness/data/subjects/science/science_sample2_error.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 3,
                "description": "12g C + 32g O2 = 44g in sealed flask, but Line 3 claims final mass = 0g because CO2 is a gas"
            },
            "sample3_misconception": {
                "filename": "science_sample3_misconception.png",
                "path": "harness/data/subjects/science/science_sample3_misconception.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 2,
                "description": "Claims tree solid wood mass comes from soil minerals rather than atmospheric CO2"
            }
        },
        "balanced_rubric_prompt": (
            "Step 1: Transcribe the handwritten student science work line-by-line.\n"
            "Step 2: Verify scientific accuracy across lines (check exact reactant/product atom counts where 2O2 = 4 O atoms, and check biological carbon fixation mechanisms).\n"
            "- Null Hypothesis: If all lines are scientifically accurate, state 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.\n"
            "- Alternative Hypothesis: If a line contains an atom-counting error or scientific misconception, state 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>'."
        ),
        # Sprint 4
        "curriculum_skills": [
            "NGSS HS-PS1-7: Use mathematical representations to support the claim that atoms, and therefore mass, are conserved during a chemical reaction",
            "NGSS HS-LS1-5: Use a model to illustrate how photosynthesis transforms light energy into stored chemical energy and plant biomass from CO2"
        ],
        "misconceptions": [
            {
                "id": "sci_mass_conservation",
                "matched_misconception": "Stoichiometry Atom Count / Conservation of Mass Error",
                "category": "Chemical Equations & Stoichiometry",
                "sample_reference": "science_sample2_error.png",
                "keywords": ["atom", "oxygen", "stoichiometry", "combustion", "conservation", "balance", "miscount"]
            },
            {
                "id": "sci_plant_biomass",
                "matched_misconception": "Photosynthesis Biomass Source Misconception (Soil vs Air CO2)",
                "category": "Cellular Energetics & Carbon Cycle",
                "sample_reference": "science_sample3_misconception.png",
                "keywords": ["tree", "soil", "mass", "wood", "photosynthesis", "carbon dioxide", "roots"]
            }
        ],
        "verification_queries": [
            {
                "query": "Students who miscounted atoms when balancing a combustion reaction",
                "expected_substring": "Conservation of Mass",
                "expected_sample": "science_sample2_error.png"
            },
            {
                "query": "Students who think trees get their mass from soil instead of carbon dioxide in the air",
                "expected_substring": "Photosynthesis Biomass",
                "expected_sample": "science_sample3_misconception.png"
            }
        ],
        "mental_models": {
            "vector_space": "Chemical / Traits Spectrum (768 Dimensions): Just like classifying organisms or elements across 768 measurable lab traits (pH, reactivity, mass, polarity), the database gives every student idea a 768-part chemical fingerprint.",
            "cosine_similarity": "Spectral Fingerprint Match (Cosine Similarity): Like comparing two absorption spectra in a spectrometer—when two student ideas align across the same traits, their similarity approaches 1.0.",
            "percentiles": "Reaction Rate Tail (p50 / p95 / p99): p50 is your typical lab group finishing on time; p99 is the slowest bottleneck group that keeps you cleaning beakers after the bell."
        }
    },

    "humanities": {
        "id": "humanities",
        "title": "Humanities (History & English Argumentation)",
        "teacher_persona": "Experienced High-School Humanities Teacher (History & English)",
        "notation_label": "Structured Argument & Source Analysis",
        "status_badge_ready": "LaTeX Ready",
        # Sprint 1
        "ignition_prompt": "Identify the historical claim and the minimum age mentioned in this excerpt: 'The 1833 Factory Act curbed child labor by banning textile work under age 9.'",
        "ignition_expected_token": "9",
        "queue_task_type": "argument_verification",
        # Sprint 2
        "sample_student_alias": "Elena_AP_History",
        "sample_topic": "Industrial Revolution & 1920s Primary Source DBQ",
        "content_blind_search_example": "claim-evidence contradiction or primary source bias misconception",
        # Sprint 3
        "samples": {
            "sample1_correct": {
                "filename": "humanities_sample1_correct.png",
                "path": "harness/data/subjects/humanities/humanities_sample1_correct.png",
                "expected_status": "CORRECT",
                "expected_line_error": None,
                "description": "Cohesive Claim-Evidence-Reasoning on 1833 Factory Act (banned textile work under age 9, enforced by inspectors)"
            },
            "sample2_error": {
                "filename": "humanities_sample2_error.png",
                "path": "harness/data/subjects/humanities/humanities_sample2_error.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 3,
                "description": "Claim-Evidence contradiction: cites 40% crop price drop but concludes in Line 3 that price drops made farmers rich"
            },
            "sample3_misconception": {
                "filename": "humanities_sample3_misconception.png",
                "path": "harness/data/subjects/humanities/humanities_sample3_misconception.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 2,
                "description": "Evaluates a 1914 WWI wartime newspaper editorial as 100% unbiased objective fact simply because it is a primary source"
            }
        },
        "balanced_rubric_prompt": (
            "Step 1: Transcribe the handwritten student argument line-by-line.\n"
            "Step 2: Evaluate Claim-Evidence-Reasoning coherence and historical source sourcing.\n"
            "- Null Hypothesis: If Claim, Evidence, and Reasoning are historically accurate and logically aligned, state 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.\n"
            "- Alternative Hypothesis: If Reasoning contradicts Evidence or treats wartime primary sources as automatically unbiased fact, state 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>'."
        ),
        # Sprint 4
        "curriculum_skills": [
            "CCSS.ELA-LITERACY.RH.11-12.1: Cite specific textual evidence to support analysis of primary and secondary sources",
            "AP Historical Thinking Skill 2 (Sourcing): Explain the point of view, purpose, historical situation, and audience of a source"
        ],
        "misconceptions": [
            {
                "id": "hum_evidence_contradiction",
                "matched_misconception": "Claim-Evidence Logical Contradiction (Non-Sequitur Reasoning)",
                "category": "Argumentation & Essay Structure",
                "sample_reference": "humanities_sample2_error.png",
                "keywords": ["contradicts", "evidence", "claim", "reasoning", "argument", "crop prices", "logical"]
            },
            {
                "id": "hum_primary_source_bias",
                "matched_misconception": "Primary Source Neutrality Misconception (Ignoring Authorial Bias)",
                "category": "Historical Sourcing & Historiography",
                "sample_reference": "humanities_sample3_misconception.png",
                "keywords": ["primary source", "unbiased", "wartime", "newspaper", "bias", "objective", "perspective"]
            }
        ],
        "verification_queries": [
            {
                "query": "Students whose cited evidence contradicts their main argument claim",
                "expected_substring": "Claim-Evidence",
                "expected_sample": "humanities_sample2_error.png"
            },
            {
                "query": "Students who think primary sources from wartime are completely unbiased facts",
                "expected_substring": "Primary Source",
                "expected_sample": "humanities_sample3_misconception.png"
            }
        ],
        "mental_models": {
            "vector_space": "768-Trait Literary & Historical Rubric Card (R^768): Imagine a library catalog card with 768 sliders—tone, thesis strength, evidence relevance, historical era, perspective. Every paragraph gets a precise 768-slider profile.",
            "cosine_similarity": "Thematic Alignment Score (Cosine Similarity): Instead of matching exact words (like Ctrl+F), it checks whether two essays point toward the exact same underlying theme or logical flaw, from 0.0 (unrelated) to 1.0 (identical meaning).",
            "percentiles": "Pacing Across the Class (p50 / p95 / p99): p50 is when half your class has turned the page; p99 is the single slowest loading screen that interrupts a Socratic seminar."
        }
    },

    "economics": {
        "id": "economics",
        "title": "Social Sciences (Economics & Supply/Demand)",
        "teacher_persona": "Experienced High-School Economics & Social Studies Teacher",
        "notation_label": "Comparative Statics & Graph Logic",
        "status_badge_ready": "LaTeX Ready",
        # Sprint 1
        "ignition_prompt": "If a severe frost destroys 30% of coffee crops, does the coffee supply curve shift left or right?",
        "ignition_expected_token": "left",
        "queue_task_type": "economics_verification",
        # Sprint 2
        "sample_student_alias": "Marcus_AP_Micro",
        "sample_topic": "Microeconomics - Supply & Demand Equilibrium",
        "content_blind_search_example": "demand shift vs movement along curve or equilibrium quantity error",
        # Sprint 3
        "samples": {
            "sample1_correct": {
                "filename": "economics_sample1_correct.png",
                "path": "harness/data/subjects/economics/economics_sample1_correct.png",
                "expected_status": "CORRECT",
                "expected_line_error": None,
                "description": "Frost destroys 30% of coffee harvest -> Supply shifts left (S1 -> S2) -> Equilibrium P rises, Q falls"
            },
            "sample2_error": {
                "filename": "economics_sample2_error.png",
                "path": "harness/data/subjects/economics/economics_sample2_error.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 3,
                "description": "Higher income shifts laptop demand right (D1 -> D2), but Line 3 wrongly says equilibrium quantity falls"
            },
            "sample3_misconception": {
                "filename": "economics_sample3_misconception.png",
                "path": "harness/data/subjects/economics/economics_sample3_misconception.png",
                "expected_status": "INCORRECT",
                "expected_line_error": 2,
                "description": "Store raises shoe prices $50 -> $70; student claims this own-price change shifts the entire Demand curve left"
            }
        },
        "balanced_rubric_prompt": (
            "Step 1: Transcribe the handwritten student economics work line-by-line.\n"
            "Step 2: Verify microeconomic Supply & Demand rules (own-price changes cause movement along the curve, never a shift of the entire curve; rightward demand shift raises both P and Q).\n"
            "- Null Hypothesis: If all lines are economically accurate, state 'STATUS: CORRECT' and 'LINE_ERROR: NONE'.\n"
            "- Alternative Hypothesis: If a line confuses movement along a curve with a curve shift or states the wrong equilibrium direction, state 'STATUS: INCORRECT' and 'LINE_ERROR: <line_number>'."
        ),
        # Sprint 4
        "curriculum_skills": [
            "CEE Microeconomics Standard 7: Markets and Prices — Analyze how changes in non-price determinants shift supply and demand curves",
            "CEE Microeconomics Standard 8: Role of Prices — Distinguish between changes in quantity demanded (movement along curve) and changes in demand (curve shift)"
        ],
        "misconceptions": [
            {
                "id": "econ_equilibrium_direction",
                "matched_misconception": "Demand Shift Equilibrium Quantity Direction Error",
                "category": "Market Equilibrium & Comparative Statics",
                "sample_reference": "economics_sample2_error.png",
                "keywords": ["equilibrium", "quantity falls", "demand shifts right", "income", "direction"]
            },
            {
                "id": "econ_shift_vs_movement",
                "matched_misconception": "Shift of Demand Curve vs Movement Along Curve Misconception",
                "category": "Determinants of Demand vs Price Changes",
                "sample_reference": "economics_sample3_misconception.png",
                "keywords": ["shifted", "whole demand curve", "own price", "movement along", "shoe prices"]
            }
        ],
        "verification_queries": [
            {
                "query": "Students who said equilibrium quantity falls when demand shifts right",
                "expected_substring": "Equilibrium Quantity",
                "expected_sample": "economics_sample2_error.png"
            },
            {
                "query": "Students who shifted the whole demand curve when only the item's own price changed",
                "expected_substring": "Shift of Demand Curve vs Movement",
                "expected_sample": "economics_sample3_misconception.png"
            }
        ],
        "mental_models": {
            "vector_space": "Multi-Factor Economic Basket (768 Indicators): Like tracking a basket of 768 economic indicators for every student response, locating each argument's exact position in economic concept space.",
            "cosine_similarity": "Directional Correlation (Cosine Similarity): Measures whether a student's written reasoning moves in the same conceptual direction as a known economic misconception (1.0 = exact match).",
            "percentiles": "Income/Latency Distribution (p50 / p95 / p99): Just as median household income (p50) hides extreme outliers at the 99th percentile (p99), p99 latency exposes worst-case classroom Wi-Fi bottlenecks."
        }
    }
}


def get_active_subject(override: Optional[str] = None) -> str:
    """
    Returns the active subject ID ('math', 'science', 'humanities', 'economics').
    Checks explicit override -> BOOTCAMP_SUBJECT env var -> .env.local -> defaults to 'math'.
    """
    if override and override.lower() in SUBJECT_PACKS:
        return override.lower()

    env_val = os.getenv("BOOTCAMP_SUBJECT", "").strip().lower()
    if env_val in SUBJECT_PACKS:
        return env_val

    for env_filename in [".env.local", ".env"]:
        env_path = Path.cwd() / env_filename
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if line.startswith("BOOTCAMP_SUBJECT="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'").lower()
                    if val in SUBJECT_PACKS:
                        return val
    return "math"


def set_active_subject(subject_id: str) -> Dict[str, Any]:
    """
    Persists the chosen subject track into `.env.local` and sets `BOOTCAMP_SUBJECT` in os.environ.
    """
    subject_id = subject_id.strip().lower()
    if subject_id not in SUBJECT_PACKS:
        valid = ", ".join(SUBJECT_PACKS.keys())
        raise ValueError(f"Unknown subject '{subject_id}'. Available tracks: {valid}")

    os.environ["BOOTCAMP_SUBJECT"] = subject_id
    env_path = Path.cwd() / ".env.local"
    lines: List[str] = []
    found = False
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.strip().startswith("BOOTCAMP_SUBJECT="):
                lines.append(f"BOOTCAMP_SUBJECT={subject_id}")
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f"BOOTCAMP_SUBJECT={subject_id}")
    env_path.write_text("\n".join(lines) + "\n")
    return SUBJECT_PACKS[subject_id]


def get_subject_pack(subject_id: Optional[str] = None) -> Dict[str, Any]:
    """Returns the full subject configuration dictionary for the active or specified subject."""
    active_id = get_active_subject(subject_id)
    return SUBJECT_PACKS[active_id]


def list_subject_packs() -> List[Dict[str, Any]]:
    """Returns all registered subject packs."""
    return list(SUBJECT_PACKS.values())
