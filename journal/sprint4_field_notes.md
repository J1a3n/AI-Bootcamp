# Teacher's Field Notes — Sprint 4: Grounding & The Analytical Assistant

## Module 3.2: High-Dimensional Vector Spaces & Math Concepts
* **Classroom Reflection:** *Why does standard database search (SQL LIKE '%-%') fail to find all student sign errors? How does mapping math problems into coordinate vectors (Cosine Distance in R^768) allow a computer to understand mathematical intent and failure modes?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 3.4: Vector Hygiene & Active Learning
* **Classroom Reflection:** *Why is "More data NOT better data" in vector databases? Why should we only curate boundary cases and unique misconceptions into our reference database rather than 500 identical correct submissions?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 3.7: Telemetry-Driven Optimization
* **Classroom Reflection:** *When inspecting our latency breakdown, we discovered that mobile image upload was taking 70% of total time. How did client-side WebP compression solve this without sacrificing OCR accuracy?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Architectural Decision Record (ADR 4):
* **Decision Made:** Dual-Axis Vector Search (`pgvector`) + 3-Tier Sandboxed Text-to-SQL + Client-side WebP Compression.
* **Trade-Off Accepted:** Extra client preprocessing in exchange for a 7X speedup and deep pedagogical insight.
