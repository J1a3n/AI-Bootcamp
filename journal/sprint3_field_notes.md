# Teacher's Field Notes — Sprint 3: The Vision Worker & Decoupling

## Module 2.4: The "Error Hunter" Trap (AI Bias)
* **Classroom Reflection:** *Why does asking an AI "Find the error in this student's work" cause it to hallucinate mistakes even on 100% sound equations, balanced chemical reactions, or well-reasoned historical arguments? How does a domain-anchored balanced null-hypothesis prompt ("If all lines are accurate and logically sound, state STATUS: CORRECT") restore instructional integrity?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 2.6 - 2.7: The Synchronous Freeze & Asynchronous Decoupling
* **Classroom Reflection:** *Why did waiting synchronously for AI OCR cause an 18-second freeze? How does the "Fast-Food Counter" model (Fast-lane preview < 1s vs. Slow-lane background OCR) preserve teacher authority and classroom focus?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Architectural Decision Record (ADR 3):
* **Decision Made:** Asynchronous Decoupling using Supabase Job Queue and Realtime Status Badge.
* **Trade-Off Accepted:** Background worker complexity in exchange for instant sub-second classroom visual display.
