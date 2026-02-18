# 🎬 Persona-Driven Cine-Agent

*A Multi-Agent Movie Recommendation System using LLMs, SQL Reasoning & Semantic Retrieval*

---

## 🧠 Overview

**Persona-Driven Cine-Agent** is an intelligent multi-agent recommendation system that behaves like a personal movie concierge.

Instead of giving generic recommendations, the system:

* Learns **how a user thinks**
* Understands **what they emotionally mean**
* Uses both **behavioral data** and **story similarity**
* Produces **personalized explanations**

This is not a simple recommender — it is a **reasoning system**.

---

## 🚀 Key Idea

Traditional recommenders answer:

> *“Users like you watched this.”*

Cine-Agent answers:

> *“Based on your past taste in melancholic psychological dramas and your current request for something emotionally dark, here’s a curated recommendation and why.”*

---

## 🏗 Architecture

The system uses a **4-agent cognitive architecture**.

```
User Query
   ↓
Agent 1 — Persona Compiler
   ↓
 ┌───────────────┬───────────────┐
 │               │               │
SQL Agent     RAG Agent      User Profile
(popularity)  (semantic)     (history)
 │               │
 └───────► Decision Agent ◄───────┘
                  ↓
        Final Personalized Recommendation
```

---

## 🧩 Agents Explained

### 1️⃣ Persona & Query Refiner

**Role:** Understand what the user *actually means*

Input:

```
"I want something visually stunning and philosophical"
```

Output (structured plan):

```json
{
  "intent": "philosophical emotional film",
  "target_tags": ["thought-provoking","existential","atmospheric"],
  "target_genres": ["drama","sci-fi"]
}
```

It uses:

* User’s top rated movies
* User’s personal tags
* Global tag vocabulary
* Fuzzy matching

---

### 2️⃣ SQL ReAct Agent — Structured Intelligence

**Role:** Find socially strong candidates

Uses:

* Ratings
* Tags
* Average rating computation

Example reasoning:

```
Thought: find psychological movies
Action: SQL query
Observation: candidate movies
Thought: rank by average rating
```

This agent performs **dynamic SQL reasoning**, not static queries.

---

### 3️⃣ Semantic RAG Agent — Narrative Intelligence

**Role:** Find movies with similar *story feeling*

Uses:

* Plot overview embeddings
* Vector similarity search

Understands:

> tone, atmosphere, emotion, narrative theme

Not popularity.

---

### 4️⃣ Profile-Aware Summarizer — Decision Maker

**Role:** Final human-like explanation

It merges:

| Source  | What it means       |
| ------- | ------------------- |
| SQL     | socially good       |
| RAG     | emotionally similar |
| Persona | personally relevant |

Then explains:

> why *you* will like it

---

## 📊 Data Sources

### MovieLens Dataset

Used for:

* Ratings
* User tags
* Collaborative filtering

### TMDB Dataset

Used for:

* Plot overview
* Semantic similarity
* Story understanding

---

## 🗄 Database Design

Tables:

```
movies(movieId, title, genres)
ratings(userId, movieId, rating, timestamp)
tags(userId, movieId, tag, timestamp)
tmdb_info(tmdbId, title, overview, release_date, genres)
```

No aggregation stored — agents compute dynamically.

---

## 🔍 Retrieval Strategy

| Method     | Purpose                  | Intelligence Type      |
| ---------- | ------------------------ | ---------------------- |
| SQL Agent  | best rated tagged movies | Social intelligence    |
| Vector RAG | story similarity         | Emotional intelligence |
| Summarizer | ranking & explanation    | Cognitive reasoning    |

---

## 🧠 Why Multi-Agent?

Single LLM systems hallucinate because they try to:

* Understand
* Retrieve
* Rank
* Explain

All at once.

We separate thinking into roles:

| Agent      | Thinking Type          |
| ---------- | ---------------------- |
| Persona    | interpretive reasoning |
| SQL        | symbolic reasoning     |
| RAG        | semantic reasoning     |
| Summarizer | narrative reasoning    |

This dramatically increases reliability.

---

## 🛠 Tech Stack

| Component  | Technology                    |
| ---------- | ----------------------------- |
| LLM        | Ollama (Llama 3.1)            |
| Embeddings | nomic-embed-text              |
| Vector DB  | ChromaDB                      |
| Database   | SQLite                        |
| Framework  | LangChain Classic + LangGraph |
| Similarity | RapidFuzz                     |

---

## 📦 How It Works End-to-End

1. User asks:

```
Find a dark emotional psychological movie
```

2. Persona Agent:
   → interprets meaning

3. SQL Agent:
   → finds highly rated psychological movies

4. RAG Agent:
   → finds narratively similar stories

5. Decision Agent:
   → merges and explains

6. Final Output:

```
Based on your past preference for character-driven dramas and
your request for a dark emotional film, I recommend...
```

---

## 🧪 Example Output

> **Recommendation: Memento (2000)**
> Because you tend to rate introspective psychological narratives highly and requested a dark emotional experience, this film aligns with both your historical taste and current mood.

---

## 🎯 What Makes This Special

This project demonstrates:

* LLM reasoning orchestration
* Structured + semantic retrieval fusion
* Tool-using agents
* Deterministic AI behavior
* Explainable recommendations

Not just AI output — **AI decision making**.

---

## 🧭 Future Extensions

* Streaming watch history adaptation
* Reinforcement feedback learning
* Memory across sessions (LangGraph state)
* Conversational follow-up recommendations
* Hybrid ranking scoring

---
