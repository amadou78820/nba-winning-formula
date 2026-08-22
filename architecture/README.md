# 🏗️ NBA Winning Formula — Project Architecture

This directory explains how the NBA Winning Formula analytics project works from raw data to final storytelling.

The objective is to provide a simple technical and analytical reference for every member of the project team.

---

# 🌍 Global Architecture

```text
                    NBA DATASET
                         │
                         ▼
                ┌─────────────────┐
                │ GOOGLE COLAB    │
                │ Python / Pandas │
                └────────┬────────┘
                         │
                         ▼
                DATA PREPARATION
                • Cleaning
                • Joins
                • Aggregations
                • Feature engineering
                • Era adjustment
                         │
                         ▼
                ANALYTICAL MODELS
                • Winning Formula
                • Historical GOAT
                • Future GOAT
                         │
                         ▼
                ANALYTICS DATA MART
                10 processed tables
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        ┌───────────┐         ┌───────────┐
        │ BIGQUERY  │         │  GITHUB   │
        │ Warehouse │         │ Versioning│
        └─────┬─────┘         └─────┬─────┘
              │                     │
              ▼                     ▼
      ┌───────────────┐     ┌────────────────┐
      │ LOOKER STUDIO │     │ GITHUB PAGES   │
      │ Dashboards    │     │ Plotly / HTML  │
      └───────┬───────┘     └───────┬────────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                  FINAL STORYTELLING
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      WINNING          GOAT         FUTURE GOAT
      FORMULA         ANALYSIS       TRAJECTORY
```

---

# 🎯 Three Analytical Pillars

## 1 — Winning Formula

**Question**

> What makes an NBA team win?

### Grain

One row = one team × one season.

### Main analysis

- Shooting efficiency
- Turnovers
- Rebounding
- Free throws
- Offensive performance
- Defensive performance

### Model

Multiple Linear Regression.

### Final performance

- Train R² = 0.929
- Test R² = 0.926
- MAE = 0.032
- Approximate error = 2.6 wins

---

# 👑 2 — Historical GOAT

**Question**

> Who is the greatest NBA player of all time?

Six dimensions are evaluated:

```text
Production
    +
Efficiency
    +
Playoffs
    +
Individual Success
    +
Team Success
    +
Longevity
        ↓
   GOAT SCORE
```

Several scenarios are tested:

- Balanced
- Peak
- Longevity
- Winning
- Individual Dominance

This avoids relying on only one definition of greatness.

---

# 🚀 3 — Future GOAT

**Question**

> Which current players are following historically exceptional trajectories?

Current players are compared with historical GOATs at equivalent ages.

The model combines:

```text
Age-adjusted Production
            +
Age-adjusted Efficiency
            +
Early Career Recognition
            +
Historical GOAT Similarity
            ↓
     FUTURE GOAT SCORE
```

Important:

The Future GOAT Score is a **trajectory index**, not a probability of becoming the GOAT.

---

# 🧰 Technology Stack

| Step | Tool | Role |
|---|---|---|
| Source | NBA Dataset | Historical NBA data |
| Exploration | Google Colab | Analysis environment |
| Transformation | Python / Pandas | Cleaning and feature engineering |
| Modeling | Scikit-learn | Statistical modeling |
| Data Mart | CSV | Analytics-ready datasets |
| Warehouse | BigQuery | Central analytical storage |
| BI | Looker Studio | Dashboard and exploration |
| Interactive charts | Plotly | Animated visualizations |
| Versioning | GitHub | Project repository |
| Hosting | GitHub Pages | Public interactive HTML |
| Presentation | Dashboard + GitHub | Final storytelling |

---

# 🔄 Simplified Workflow

Remember the project through seven verbs:

**COLLECT → CLEAN → TRANSFORM → MODEL → STORE → VISUALIZE → EXPLAIN**

```text
COLLECT
NBA Dataset
   ↓
CLEAN
Python / Pandas
   ↓
TRANSFORM
Feature Engineering
   ↓
MODEL
Winning + GOAT + Future GOAT
   ↓
STORE
BigQuery
   ↓
VISUALIZE
Looker Studio + Plotly
   ↓
EXPLAIN
Final Presentation
```

---

# 📁 Architecture Documentation

This directory contains:

### `01_project_workflow.md`

Explains the complete project workflow step by step.

### `02_data_architecture.md`

Explains datasets, tables, grains and relationships.

### `03_data_pipeline.md`

Explains how data moves from the original dataset to the dashboards.

### `04_presentation_guide.md`

Provides a simple explanation that team members can use during the final presentation.

---

# 🧠 The Architecture in One Sentence

> We transform historical NBA data with Python, build analytics-ready datasets and statistical models, store the results in BigQuery, visualize them in Looker Studio, and use GitHub Pages for interactive storytelling.
