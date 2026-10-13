# Teacher's Field Notes — Sprint 2: The Classroom Collector (PWA)

## Module 2.1: The 2-Second Classroom Rule
* **Classroom Reflection:** *When you are teaching 30 high schoolers, what happens to the classroom momentum if you snap a photo of a student's work and the screen sits on a loading spinner for 15 seconds? Why must the photo show up on the screen in under 2 seconds—even before any AI or transcription has even touched it?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 2.2: Ephemeral State & The Classroom Catastrophe
* **Classroom Reflection:** *What happens during a live presentation if the browser tab reloads while holding student work only in temporary memory? Why does an educator need persistence?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 2.3: Photo Album vs. Filing Cabinet
* **Classroom Reflection:** *If you snap 150 photos a day, why is it better to store heavy image files in Object Storage (S3) while keeping lightweight index cards (names, dates, links) in a Postgres database?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Architectural Decision Record (ADR 2):
* **Decision Made:** Bifurcated UX (Projector Canvas vs Mobile Controller) + S3 Object Storage & Postgres Indexing.
* **Trade-Off Accepted:** Maintaining two views in exchange for ergonomic one-handed capture and uncluttered student presentation.
