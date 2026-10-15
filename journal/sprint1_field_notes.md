# Teacher's Field Notes — Sprint 1: The Engine & Cloud Bridge

## Module 1.1: Running AI Locally vs. In the Cloud
* **Classroom Reflection:** *When most people use AI today, every question and uploaded photo travels across the public internet to a massive data center hundreds of miles away. As a high school teacher, what comes to your mind when you think about the privacy and practical difference between uploading your students' handwritten notes to an outside cloud versus processing everything locally on your own desk?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 1.2: Speed Telemetry & Classroom Dead-Time
* **Classroom Reflection:** *In a 45-minute class with 30 students, every second of teacher dead-time counts. When we look at AI performance, we measure "Tokens per Second" (~150 tok/s means a full student solution, lab check, or paragraph analysis in ~1 second). Why does having live speed telemetry on your screen matter when deciding whether a tool is actually practical for daily teaching?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Module 1.3 - 1.6: Guarding Your Hardware & Inverting the Network
* **Classroom Reflection:** *If your home computer is acting as your private school server, why is it safer to have your PC reach OUT to a cloud queue rather than opening an inbound hole (port forwarding) in your home Wi-Fi router?*
* **My Field Observations & Insights:**
  > *(Record your thoughts and reflections here)*

---

## Architectural Decision Record (ADR 1):
* **Decision Made:** Outbound Worker Pattern with Supabase Queue & Bearer Token Authentication.
* **Trade-Off Accepted:** Slightly more software setup in exchange for 100% firewall security and zero URL instability.
