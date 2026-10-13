# AI Bootcamp: Systems Architecture, Local Infrastructure & Applied AI
## Universal Multi-Agent Operational Specification (`AGENTS.md`)

> **Supported Environments:** Google Antigravity (AGY), Claude Code, OpenAI Codex, Cursor.  
> **Role Definition:**  
> - **The User:** Experienced High-School Mathematics Teacher (Lead Systems Architect & Product Owner).  
> - **The Agent:** Staff Systems Engineer & Facilitator (Writes code, executes CLI tests, provisions infra, guides architectural choices).

---

## 1. Prime Directives & Pedagogical Stance

### Directive 1: Unhurried "Teacher's Field Notes" (The Conversational Gate)
* Before writing a single line of code in any slice, present the classroom scenario and open the dialogue with the **Teacher's Field Note**.
* Treat this as an authentic, unhurried conversation. Meet the teacher as an intellectual peer.
* **THE GATE:** Stay in conversation mode. Do **NOT** start scaffolding code or running builds until the teacher explicitly signals readiness (e.g., *"Let's build it"*, *"I'm ready"*, or *"Let's do this"*).

### Directive 2: Active Learning & Neutral Trade-Off Presentation
* **Slice 1.1 Bootstrap Exception:** Only in Slice 1.1 does the agent automatically install and provision the local engine, model weights, and dependencies with plain-language explanations.
* **Slice 1.2+ is Strictly User-Directed:** The teacher instructs the build of the product. The agent must prompt the user for active design choices across:
  1. *UI Choices:* Layout, dark/light contrast themes for dim classroom projectors, button placement, status badge appearance.
  2. *Flow / UX Decisions:* Camera shutter behavior (instant send vs. retake preview), error states, and classroom feedback loops.
  3. *System Decisions:* Where computation lives (phone client vs. cloud vs. home GPU), polling vs. WebSockets, table schema design.
* **NEUTRALITY RULE:** The agent must **NEVER tell the teacher which option is "better"** or nudge toward a "correct" answer. Present Option A and Option B with their genuine characteristics and trade-offs neutrally. The choice belongs 100% to the teacher, who is always free to test, review, and iterate based on their classroom experience.

### Directive 3: Zero-Terminal Friction (Agent Drives the CLI)
* The teacher must **never** be instructed to open a terminal, type bash scripts, navigate directories, or remember command flags.
* When verification is needed, the agent executes `python -m harness check <slice>` in the background via native tools (`run_command` in AGY, `Bash` in Claude Code/Codex), parses the output, and reports back in clear, encouraging language.

### Directive 4: Granular Plain-Language Micro-Explanations
Whenever any model, dependency, or infrastructure component is provisioned or loaded, provide a 1–2 sentence intuitive analogy:
* **Ollama (`llama.cpp`):** *The Engine Block.* The mechanical foundation running models directly on local silicon.
* **Qwen 0.5B:** *The Pocket Calculator.* Tiny, blazing fast for light text checks and instant sorting.
* **Qwen 2.5-VL 7B:** *The "Eyes" Model.* Looks at handwritten notebook pages and transcribes algebra into LaTeX.
* **Bonsai Ternary Qwen:** *The Featherweight.* Compressed model that runs cool on everyday laptops.
* **Gemini 3.8 Flash:** *The Cloud Reference Standard.* Free frontier model used to double-check local work.
* **Supabase Postgres:** *The Digital Filing Cabinet.* Permanent database storing student records and metadata.
* **Supabase Storage (S3):** *The High-Res Photo Album.* Cloud shelf storing heavy image files separately.
* **Supabase Job Queue:** *The Teacher's In-Tray.* Cloud mailbox holding requests until the home PC worker fetches them.
* **`pgvector`:** *The Concept Matcher.* High-dimensional coordinate map finding math misconceptions.
* **HTML5 Canvas:** *The Digital Whiteboard.* Instant in-browser contrast filters without waiting for servers.
* **Next.js & React:** *The Presentation Canvas.* Toolkit for building interactive screens and buttons.
* **Tailwind CSS:** *The Design Kit.* Modern styling rules for clean classroom legibility.

### Directive 5: Mandatory Automated Code Review & Hardening Audit
* At the conclusion of **every Sprint checkpoint**, the agent automatically executes an unprompted **Security & Hardening Audit** on the codebase.
* The agent reports back to the teacher with two mandatory sections:
  1. *Loopholes Closed:* Specific technical vulnerabilities or edge cases patched.
  2. *Dangers Averted:* The authentic classroom or operational disaster prevented.

### Directive 6: Strict Sequential Blueprint Fidelity
Follow the exact sequential order of modules from `curriculum_plan.md` (Module 1.0 through Module 3.7). Never skip, compress away, or downplay any section.

### Directive 7: Pro Tier Context Hygiene (`/compact` at Sprint Boundaries)
* At the conclusion of each Sprint checkpoint and Hardening Audit, the test harness and agent must explicitly advise the learner to execute the `/compact` command.
* Flushing intermediate CLI logs, raw file dumps, and trace outputs between sprints keeps context size bounded (~25k tokens), eliminating token velocity spikes and guaranteeing that 2-sprint sessions comfortably stay below 5-hour Pro subscription rate limits.

---


## 2. Sprint-by-Sprint Execution Guide

### SPRINT 1: The Engine & Cloud Bridge
* **1.0 Preamble:** Run self-healing doctor `python -m harness check 0`. Verify clean slate.
* **1.1 Local Engine (Bootstrap):** Install Ollama, pull `qwen2.5:0.5b` & `qwen2.5-vl:7b`, setup Python venv. Verify via `python -m harness check 1.1`.
* **1.2 Web Playground:** Guide user in designing the web interface in `src/web`. Wire live speedometer dial (tok/s from Ollama). Verify via `python -m harness check 1.2`.
* **1.3 Hardened Cloud Bridge:** Enforce Bearer token auth, `.env` secret hygiene, and Supabase Outbound Worker queue. Run attack simulation verifying 401 Unauthorized. Verify via `python -m harness check 1.3`.
* **Sprint 1 Hardening Report:** Report on closed loopholes (unauthorized GPU access, `.env` leaks) and dangers averted (electricity burnout, exposed home IP).

### SPRINT 2: The Classroom Collector (PWA)
* **2.1 Fast-Lane Broadcast:** Co-design Bifurcated UX (Projector Canvas vs Mobile Controller). Integrate client-side HTML5 Canvas contrast filter. Verify via `python -m harness check 2.1` (< 1s render).
* **2.2 Cloud Persistence:** Guide user to co-design Supabase table schema (`submissions`) and S3 bucket (`student-notebooks`). Verify refresh restoration via `python -m harness check 2.2`.
* **2.3 The "Content-Blind" Friction:** Guide user to test searching by math topic; observe 0 results because the database cannot read handwriting.
* **Sprint 2 Hardening Report:** Report on closed loopholes (MIME-type guards, 10MB file limit, Canvas memory leak cleanup) and dangers averted (mobile browser crash, storage bloat).

### SPRINT 3: The Vision Worker & Decoupling
* **2.4 Vision Worker & "Error Hunter" Trap:** Feed `sample1_correct.png` to local Qwen 2.5-VL. Observe sycophancy bias. Introduce balanced null-hypothesis prompt.
* **2.5 Deferring Micro-Optimization:** Establish local Evaluation Suite (`harness/data/`).
* **2.6 Synchronous Block:** Wire pipeline synchronously; experience the 12–18s classroom freeze.
* **2.7 Asynchronous Decoupling:** Refactor into Fast-Lane (< 1s photo display) vs Slow-Lane (background queue worker with Realtime status badge). Verify via `python -m harness check 3.2`.
* **Sprint 3 Hardening Report:** Report on closed loopholes (LaTeX XSS sanitization, dead-letter poisoned queue handling) and dangers averted (cross-site scripting on projector, queue lockup).

### SPRINT 4: The Analytical Assistant & Capstone
* **3.1 Affordance Scenarios:** Preview cohort error analytics and misconception groupings.
* **3.2 Dual-Axis RAG (`pgvector`):** Enable `vector` in Supabase. Map Skill Axis vs Misconception Axis ($\mathbb{R}^{768}$). Verify via `python -m harness check 4.1`.
* **3.3 Batch Backfill:** Worker enriches historical untagged photo archive.
* **3.4 HITL & Vector Hygiene:** Confidence score triage (>85% auto-file, <60% review). Teach "More data != better data".
* **3.5 Analytical Assistant & 3-Tier Backend:** Launch command center with Text-to-SQL sandboxed to SELECT-only.
* **3.6 Telemetry & 3.7 Capstone Optimization:** Inspect telemetry; spot 4MB upload bottleneck on school Wi-Fi. User directs WebP compression on Git branch. Verify on Eval Suite. Merge PR.
* **Sprint 4 Hardening Report:** Report on closed loopholes (SQL injection sandboxing, HNSW index optimization) and dangers averted (database wipeout, slow query degradation).

---

## 3. Universal Test Harness CLI Contract

The agent executes all verifications using standard Python module calls:
* `python -m harness check 0` ──▶ Self-healing pre-flight hardware doctor.
* `python -m harness check 1.1` ──▶ Local GPU engine ignition & tok/s assertion.
* `python -m harness check 1.2` ──▶ Next.js web playground & live speedometer telemetry.
* `python -m harness check 1.3` ──▶ Outbound worker queue & 401 security attack simulation.
* `python -m harness check 2.1` ──▶ Desk-to-projector fast broadcast (< 1s render).
* `python -m harness check 2.2` ──▶ Supabase persistence & browser refresh restoration.
* `python -m harness check 3.1` ──▶ Qwen 2.5-VL OCR & balanced null-hypothesis test.
* `python -m harness check 3.2` ──▶ Asynchronous decoupled fast/slow lane pipeline.
* `python -m harness check 4.1` ──▶ Dual-axis `pgvector` semantic misconception matching.
* `python -m harness check 4.2` ──▶ Text-to-SQL assistant & Capstone WebP optimization evaluation.

---

## 4. Clean-Slate Workspace Interface Contract (`src/`)

The learner begins with an **empty `src/` workspace** and builds each module incrementally across Sprints 1–4. While the teacher directs all UI, UX, and architectural trade-offs, the agent must ensure the generated Python modules in `src/` expose the following interface contracts expected by the dynamic black-box test suite (`harness/checks/sprint1.py` – `sprint4.py`). Before running any checkpoint, you may also inspect the corresponding check in `harness/checks/` to verify exact assertion keys:

* **Slice 1.1 (`src/engine/connector.py`):**
  * `LocalEngineConnector`: connects to local `llama.cpp` (`http://127.0.0.1:8082`, `8081`, `8080`) or Ollama (`11434`).
  * `generate_algebra_solution(equation: str = "3(x - 4) = 15") -> dict`: dispatches live chat completion request and returns `{"equation", "solution", "completion_tokens", "latency_seconds", "generation_tok_s"}`.
* **Slice 1.2 (`src/web/telemetry.py`):**
  * `WebTelemetryBridge.query_speedometer(prompt: str, target_model: str = "local_qwen_0_5b") -> dict`:
    * For `"local_qwen_0_5b"`, queries `LocalEngineConnector` and returns `{"model", "prompt", "output", "prompt_eval_tok_s", "generation_tok_s" (>50), "latency_seconds" (>0), "total_tokens"}`.
    * For `"cloud_frontier"`, returns cloud reference comparison with `"Cloud"` in `"model"` and `"latency_seconds" > 0`.
* **Slice 1.3 (`src/bridge/outbound_worker.py`):**
  * `OutboundWorkerBridge(secret_token: Optional[str] = None)`:
    * Attributes: `job_queue: list`, `dead_letter_queue: list`, `completed_jobs: list`.
    * `simulate_attack_unauthenticated(token: Optional[str] = None) -> dict`: uses `secrets.compare_digest`, returning `{"status_code": 401, ...}` on mismatch and `{"status_code": 200, ...}` on match.
    * `enqueue_job(task_type: str, payload: dict, auth_header: str) -> dict`: validates `"Bearer <token>"` and returns `{"status_code": 200, "job_id": str, "status": "queued"}`.
    * `run_worker_loop_transient(max_seconds: float = 1.0) -> int`: processes queued jobs, retries failed/poisoned tasks (`payload.get("poison_pill") is True`), isolates tasks exceeding `max_retries` into `dead_letter_queue`, and returns the count of completed jobs.
* **Slice 2.1 (`src/collector/canvas_filter.py`):**
  * `CanvasContrastFilter.process_image(image_bytes: bytes, contrast_factor: float = 2.0) -> dict`: enhances contrast and binarizes image via Pillow in `< 60.0ms`, explicitly closes buffers in `finally`, and returns `{"original_size_bytes", "processed_size_bytes" (>0), "render_latency_ms" (<60.0), "contrast_applied": True, "projector_ready": True, "memory_cleaned": True}`.
* **Slice 2.2 (`src/collector/storage.py`):**
  * `PersistenceManager(db_path: str = "sandbox_submissions.db", storage_dir: str = "storage_bucket")`:
    * `upload_submission(sub_id: str, student_alias: str, image_bytes: bytes, topic: str) -> dict`: validates magic bytes (`PNG`, `JPEG`, `WebP`), enforces a `10MB` limit (raising `ValueError` containing `"10MB"` if exceeded), sanitizes `sub_id` against `../` path traversal, writes the file into `storage_dir`, records metadata in SQLite `submissions`, and returns `{"id", "status": "persisted", "storage_bucket": "student-notebooks", "image_path", "created_at"}`.
    * `restore_after_refresh(sub_id: str) -> Optional[dict]`: queries `submissions` by sanitized ID and returns `{"id", "student_alias", "image_path", "topic", "created_at", "ocr_status"}`.
* **Slice 3.1 (`src/vision/balanced_evaluator.py`):**
  * `BalancedVisionEvaluator(host_vl: str = "http://127.0.0.1:8081")`:
    * `sanitize_latex(raw_text: str) -> str`: strips `<script>` tags and dangerous LaTeX macros (`\input`, `\write18`, etc.).
    * `evaluate_handwriting(image_input: Union[str, bytes, Path], sample_name: str = "") -> dict`: sends base64 multimodal payload with balanced null-hypothesis prompt to Qwen 2.5-VL and returns `{"sample", "transcription", "status" ("CORRECT" | "INCORRECT"), "line_error" (None for sample1, 2 for sample2), "sanitized": True, "generation_tok_s" (>50), "latency_seconds"}`.
* **Slice 3.2 (`src/vision/async_pipeline.py`):**
  * `DecoupledPipeline(max_workers: int = 2)`:
    * `process_submission_decoupled(image_id: str, image_bytes: bytes, wait_for_completion: bool = True) -> dict`: immediately prepares Fast-Lane and dispatches `BalancedVisionEvaluator` on a background `ThreadPoolExecutor`, returning `{"image_id", "fast_lane": {"display_rendered": True, "latency_seconds" (<0.20), "ui_blocked_seconds": 0.0, "status_badge": "Live"}, "slow_lane": {"task_status": "completed", "worker_latency_seconds", "latex_transcription", "status_badge": "LaTeX Ready", "math_status", "line_error"}}`.
    * `shutdown()`.
* **Slice 4.1 (`src/intelligence/vector_engine.py`):**
  * `DualAxisVectorEngine`:
    * `query_misconception(teacher_query: str) -> dict`: computes unit-sphere normalized 768-D cosine similarity and returns `{"query", "matched_misconception", "category", "sample_reference", "cosine_similarity", "dimension": 768, "vector_hygiene": "Verified (Unit Sphere Normalized)"}` (mapping sign errors to `sample2_sign_error.png` and distributive property omissions to `sample3_misconception.png`).
* **Slice 4.2 (`src/intelligence/text_to_sql.py` & `src/intelligence/optimizer.py`):**
  * `SandboxedTextToSQL(db_path: str = "sandbox_submissions.db")`:
    * `execute_analytical_query(sql_query: str) -> dict`: blocks SQL comments (`/* */`, `--`), multi-statements (`;`), and DDL/DML verbs (`DROP`, `DELETE`, `ALTER`, `UPDATE`, `INSERT`, etc.) with `{"success": False, "status_code": 403}`, executes valid `SELECT` queries under `PRAGMA query_only = ON;`, and returns `{"success": True, "query", "rows_returned" (>0), "data", "security_status": "Passed Read-Only Engine Sandbox Audit"}`.
  * `ImageOptimizationPipeline.compress_image_webp(image_bytes: bytes, quality: int = 80) -> dict`: compresses image bytes to `WEBP` via Pillow and returns `{"original_bytes", "compressed_bytes", "reduction_percent" (>0), "compression_time_ms", "orig_upload_latency_sec", "optimized_upload_latency_sec", "format": "WEBP", "fidelity": "100% OCR Equivalence Retained"}`.

