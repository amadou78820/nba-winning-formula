# NBA Winning Formula — Reproduction Guide

## 1. Purpose

This guide explains how to reproduce the **NBA Winning Formula** project from raw data to the final dashboards and interactive visualizations.

The project answers three main analytical questions:

1. **What statistical factors are most associated with winning in the NBA?**
2. **Who is the historical GOAT according to a transparent multi-criteria framework?**
3. **Which current players are following the strongest GOAT-like trajectory?**

---

# 2. Project Architecture

The complete analytical workflow is:

```text
RAW DATA
   │
   ▼
PYTHON EXTRACTION
   │
   ▼
DATA INSPECTION
   │
   ▼
DATA PREPARATION
   │
   ├───────────────┐
   ▼               ▼
TEAM ANALYTICS   PLAYER ANALYTICS
   │               │
   ▼               ▼
WINNING          HISTORICAL
FORMULA          GOAT MODEL
                   │
                   ▼
                FUTURE GOAT
                   │
   └───────────┬───┘
               ▼
          DATA MART
               │
        ┌──────┴──────┐
        ▼             ▼
     BIGQUERY       PLOTLY
        │             │
        ▼             ▼
 LOOKER STUDIO    GITHUB PAGES
```

---

# 3. Repository Structure

```text
nba-winning-formula/
│
├── architecture/
│   ├── 01_project_overview.md
│   ├── 02_data_architecture.md
│   ├── 03_data_pipeline.md
│   ├── 04_analytics_methodology.md
│   └── 05_reproduction_guide.md
│
├── python/
│   ├── 01_download_data.py
│   ├── 02_inspect_sources.py
│   ├── 03_prepare_team_data.py
│   ├── 04_build_winning_formula.py
│   ├── 05_prepare_player_seasons.py
│   ├── 06_build_goat_model.py
│   ├── 07_build_future_goat.py
│   ├── 08_export_datamart.py
│   └── 09_build_plotly_animation.py
│
├── data/
│   ├── raw/
│   ├── intermediate/
│   └── processed/
│
├── animations/
│   └── future-goat-trajectory-premium.html
│
├── requirements.txt
└── README.md
```

---

# 4. Requirements

Recommended environment:

- Python 3.11+
- Jupyter Notebook or Google Colab
- VS Code optional
- Git
- GitHub account
- Google Cloud account
- BigQuery
- Looker Studio

---

# 5. Clone the Repository

```bash
git clone https://github.com/amadou78820/nba-winning-formula.git
```

Then enter the project directory:

```bash
cd nba-winning-formula
```

---

# 6. Create a Python Virtual Environment

Recommended:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

---

# 7. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

Main Python libraries used in the project include:

- pandas
- numpy
- scipy
- scikit-learn
- plotly
- kagglehub
- duckdb

---

# 8. Step 1 — Download the Data

Run:

```bash
python python/01_download_data.py
```

Purpose:

- retrieve the NBA source dataset;
- identify downloaded files;
- prepare the raw-data layer.

Primary source used by the project:

**Kaggle — Basketball Dataset by Wyatt Walsh**

Dataset version used during the original analysis:

```text
wyattowalsh/basketball
version 237
```

---

# 9. Step 2 — Inspect the Sources

Run:

```bash
python python/02_inspect_sources.py
```

Purpose:

- inspect available files;
- inspect SQLite / DuckDB tables;
- identify useful tables;
- understand columns and data coverage;
- verify the analytical grain.

At this stage, no business model is built.

The objective is purely:

```text
UNDERSTAND THE DATA
```

---

# 10. Step 3 — Prepare Team Data

Run:

```bash
python python/03_prepare_team_data.py
```

Purpose:

Transform game-level data into:

```text
1 row = 1 team × 1 season
```

Main metrics include:

- games played;
- wins;
- losses;
- win rate;
- offensive statistics;
- defensive statistics;
- shooting;
- rebounds;
- assists;
- turnovers.

Main output:

```text
01_team_season.csv
```

---

# 11. Step 4 — Build the Winning Formula

Run:

```bash
python python/04_build_winning_formula.py
```

Purpose:

Identify the statistical factors most associated with NBA team success.

Target variable:

```text
win_rate
```

The model evaluates team-level performance indicators and estimates their relative importance.

Main output:

```text
02_winning_factors.csv
```

This section answers:

> What factors are most associated with winning NBA games?

---

# 12. Step 5 — Prepare Player Seasons

Run:

```bash
python python/05_prepare_player_seasons.py
```

Analytical grain:

```text
1 row = 1 player × 1 season
```

Main derived metrics:

```text
PPG
RPG
APG
SPG
BPG
MPG
PPG_Z
RPG_Z
APG_Z
PRODUCTION_Z
TS_PCT
LEAGUE_TS
TS_PLUS
TS_Z
```

### Era adjustment

Players from different eras cannot be compared using raw statistics alone.

The project therefore standardizes production within each season.

Example:

```text
PRODUCTION_Z =
50% PPG_Z
+ 25% RPG_Z
+ 25% APG_Z
```

Efficiency is measured relative to the league environment using:

```text
TS+
```

Interpretation:

```text
TS+ = 100 → league average
TS+ > 100 → above league average
TS+ < 100 → below league average
```

---

# 13. Step 6 — Build the Historical GOAT Model

Run:

```bash
python python/06_build_goat_model.py
```

Historical candidates:

```text
Michael Jordan
LeBron James
Kareem Abdul-Jabbar
Magic Johnson
Larry Bird
```

The framework evaluates six dimensions:

```text
Production
Efficiency
Playoffs
Individual Success
Team Success
Longevity
```

Balanced model:

```text
Production          20%
Efficiency          15%
Playoffs            20%
Individual Success  20%
Team Success        10%
Longevity           15%
```

The project also evaluates alternative GOAT philosophies:

```text
Balanced
Peak
Longevity
Winning
Individual Dominance
```

This allows sensitivity analysis.

The objective is not to claim that one definition of the GOAT is universally correct.

Instead, the project asks:

> Who becomes the GOAT when the definition of greatness changes?

Outputs:

```text
03_goat_master.csv
04_goat_dimensions.csv
05_goat_scenarios.csv
06_goat_peak.csv
07_goat_player_seasons.csv
08_methodology.csv
```

---

# 14. Step 7 — Build the Future GOAT Model

Run:

```bash
python python/07_build_future_goat.py
```

Data cutoff:

```text
2023-24
```

Eligible players:

```text
Age <= 27
```

The Future GOAT V2 framework uses four components:

```text
Production Trajectory      35%
Efficiency Trajectory      25%
Recognition Trajectory     25%
Historical GOAT Similarity 15%
```

The model compares current players with historical GOATs at equivalent ages.

Example:

```text
Luka at age 22
vs
LeBron at age 22
```

rather than:

```text
Luka age 22
vs
LeBron entire career
```

This reduces career-stage bias.

---

# 15. Important Future GOAT Interpretation

The Future GOAT Score is an **analytical trajectory index**.

It is NOT a probability.

For example:

```text
Future GOAT Score = 73.8
```

does NOT mean:

```text
73.8% probability of becoming the GOAT
```

It means:

> According to the project's metrics, historical benchmarks and weights, the player currently follows a particularly strong GOAT-like trajectory.

Outputs:

```text
09_future_goat.csv
10_future_goat_similarity.csv
```

---

# 16. Step 8 — Validate the Data Mart

Run:

```bash
python python/08_export_datamart.py
```

This script verifies:

- file existence;
- table dimensions;
- duplicate rows;
- logical keys;
- missing scores;
- player-season uniqueness;
- Future GOAT uniqueness;
- similarity-table consistency.

Expected final message:

```text
✓ DATA MART READY FOR BIGQUERY
```

---

# 17. Final Analytics Data Mart

The project produces ten analytical datasets:

| # | Dataset | Purpose |
|---|---|---|
| 01 | team_season | Team × season performance |
| 02 | winning_factors | Winning Formula model |
| 03 | goat_master | Historical GOAT source metrics |
| 04 | goat_dimensions | Six GOAT dimensions |
| 05 | goat_scenarios | Sensitivity analysis |
| 06 | goat_peak | True Peak analysis |
| 07 | goat_player_seasons | Historical career trajectories |
| 08 | methodology | Model documentation |
| 09 | future_goat | Future GOAT ranking |
| 10 | future_goat_similarity | Candidate × historical GOAT similarity |

---

# 18. Step 9 — Generate the Plotly Animation

Run:

```bash
python python/09_build_plotly_animation.py
```

The animation compares six current candidates:

```text
Luka Dončić
Shai Gilgeous-Alexander
Jayson Tatum
Anthony Edwards
Tyrese Haliburton
Victor Wembanyama
```

with five historical GOATs:

```text
Michael Jordan
LeBron James
Kareem Abdul-Jabbar
Magic Johnson
Larry Bird
```

Comparison variable:

```text
Era-Adjusted Production Z
```

X-axis:

```text
Player Age
```

The objective is to visualize:

> How did today's stars compare with NBA legends at the same age?

Output:

```text
animations/future-goat-trajectory-premium.html
```

---

# 19. BigQuery Layer

The processed CSV files can then be loaded into BigQuery.

Recommended dataset:

```text
nba_analytics
```

Recommended tables:

```text
nba_analytics.team_season
nba_analytics.winning_factors
nba_analytics.goat_master
nba_analytics.goat_dimensions
nba_analytics.goat_scenarios
nba_analytics.goat_peak
nba_analytics.goat_player_seasons
nba_analytics.methodology
nba_analytics.future_goat
nba_analytics.future_goat_similarity
```

BigQuery acts as the analytical warehouse between Python and Looker Studio.

---

# 20. Looker Studio Layer

Connect Looker Studio to the BigQuery dataset.

Recommended dashboard structure:

```text
PAGE 1
NBA Winning Formula
What makes teams win?

PAGE 2
Historical GOAT
Who is the GOAT?

PAGE 3
GOAT Scenarios
Does the winner change when the definition changes?

PAGE 4
Future GOAT
Who is currently following the strongest trajectory?

PAGE 5
Methodology
How were the scores calculated?
```

---

# 21. GitHub Pages Layer

Interactive Plotly visualizations are stored in:

```text
animations/
```

and published through GitHub Pages.

Example architecture:

```text
Python
   ↓
Plotly
   ↓
HTML
   ↓
GitHub
   ↓
GitHub Pages
   ↓
Public URL
   ↓
Presentation / Dashboard
```

---

# 22. Complete Execution Order

For a complete rebuild, execute:

```bash
python python/01_download_data.py
python python/02_inspect_sources.py
python python/03_prepare_team_data.py
python python/04_build_winning_formula.py
python python/05_prepare_player_seasons.py
python python/06_build_goat_model.py
python python/07_build_future_goat.py
python python/08_export_datamart.py
python python/09_build_plotly_animation.py
```

---

# 23. Pipeline Summary

```text
KAGGLE NBA DATA
      ↓
01 DOWNLOAD
      ↓
02 INSPECT
      ↓
03 TEAM DATA
      ↓
04 WINNING FORMULA
      │
      └─────────────────┐
                        │
05 PLAYER SEASONS       │
      ↓                 │
06 HISTORICAL GOAT      │
      ↓                 │
07 FUTURE GOAT          │
      │                 │
      └────────┬────────┘
               ↓
        08 DATA MART
               ↓
       ┌───────┴────────┐
       ↓                ↓
    BIGQUERY       09 PLOTLY
       ↓                ↓
LOOKER STUDIO      GITHUB PAGES
```

---

# 24. Key Methodological Principle

The project separates:

```text
DATA
↓
METRICS
↓
NORMALIZATION
↓
MODELS
↓
BUSINESS / SPORTS INTERPRETATION
↓
VISUALIZATION
```

This separation makes the analysis:

- easier to understand;
- easier to audit;
- easier to reproduce;
- easier to modify;
- easier to explain during the final presentation.

---

# 25. Reproducibility Checklist

Before considering the project successfully reproduced, verify:

- [ ] Repository cloned
- [ ] Python environment created
- [ ] Dependencies installed
- [ ] Raw NBA data downloaded
- [ ] Source tables inspected
- [ ] Team-season dataset generated
- [ ] Winning Formula generated
- [ ] Player-season features generated
- [ ] Historical GOAT model generated
- [ ] Future GOAT model generated
- [ ] Ten Data Mart tables validated
- [ ] Plotly animation generated
- [ ] Tables loaded into BigQuery
- [ ] Looker Studio connected
- [ ] GitHub Pages animation accessible

---

# 26. Final Project Philosophy

The project does not attempt to provide an absolute answer to:

> Who is the greatest basketball player ever?

Instead, it builds a transparent analytical framework where every result can be traced back to:

```text
DATA
+
METRICS
+
BENCHMARKS
+
WEIGHTS
```

This allows the audience to understand not only **who wins**, but more importantly:

> **Why does this player win under this definition of greatness?**
