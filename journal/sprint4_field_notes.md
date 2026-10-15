# Teacher's Field Notes — Sprint 4: Grounding & The Analytical Assistant

## Module 3.2: High-Dimensional Concept Maps & Student Misconceptions
* **Classroom Reflection:** *Why does standard keyword search (like Ctrl+F or SQL LIKE) fail to find all students who share the same underlying misconception (whether a sign error in Math, a conservation-of-mass mistake in Science, a primary-source bias assumption in History, or a curve-shift mix-up in Economics)? How does mapping student work across a 768-Slider Concept Profile (`pgvector` in R^768) allow a computer to group students by how they are thinking rather than the exact words they wrote?*
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
