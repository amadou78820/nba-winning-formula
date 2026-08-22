# 🏀 NBA Winning Formula

## What makes NBA teams win — and who is the GOAT?

An end-to-end Data Analytics project exploring the statistical drivers of NBA team success, building a multi-dimensional GOAT framework, and identifying current players following historically exceptional career trajectories.

---

## 🎯 Project Objectives

This project addresses three main questions:

### 1. What makes an NBA team win?
Identify the performance factors most strongly associated with NBA regular-season win rate.

### 2. Who is the GOAT?
Compare five legendary players through a transparent, era-adjusted and multi-dimensional framework.

### 3. Who could follow them?
Compare current NBA stars with historical GOAT trajectories at equivalent ages.

---

# 🏆 Key Results

## Winning Formula

A regression model was built using eight team-performance indicators.

**Model performance**

| Metric | Result |
|---|---:|
| Train R² | 0.929 |
| Test R² | 0.926 |
| Test MAE | 0.032 |
| Approx. error | 2.6 wins |

The strongest statistical factors include:

- Shooting efficiency — eFG%
- Opponent shooting efficiency
- Turnover control
- Forced turnovers
- Offensive rebounding
- Defensive rebounding
- Free-throw pressure

> The model identifies statistical associations with winning. These relationships should not automatically be interpreted as causal.

---

# 👑 Historical GOAT Analysis

Five players are evaluated:

- Michael Jordan
- LeBron James
- Kareem Abdul-Jabbar
- Magic Johnson
- Larry Bird

The Balanced GOAT framework uses six dimensions:

| Dimension | Weight |
|---|---:|
| Production | 20% |
| Efficiency | 15% |
| Playoffs | 20% |
| Individual Success | 20% |
| Team Success | 10% |
| Longevity | 15% |

Multiple scenarios are also evaluated:

**Balanced · Peak · Longevity · Winning · Individual Dominance**

This allows the definition of greatness to change without hiding the assumptions behind the ranking.

---

# 🚀 Future GOAT

The Future GOAT model evaluates the **observed trajectories** of current NBA players.

The model combines:

| Component | Weight |
|---|---:|
| Age-adjusted Production | 35% |
| Age-adjusted Efficiency | 25% |
| Early Career Recognition | 25% |
| Historical GOAT Similarity | 15% |

**Data cutoff: 2023-24**

The model does **not** predict with certainty who will become the GOAT.

It measures how closely a player's observed trajectory compares with historically exceptional careers.

### Current leader

**Luka Dončić — Future GOAT Score: 73.8**

Closest historical trajectory:

**LeBron James**

---

# 🎬 Interactive Career Trajectory

Compare today's stars with NBA legends at equivalent ages:

👉 [Launch the Future GOAT interactive animation](https://amadou78820.github.io/nba-winning-formula/animations/future-goat-trajectory-premium.html)

The animation compares:

### Historical GOATs

Michael Jordan · LeBron James · Kareem Abdul-Jabbar · Magic Johnson · Larry Bird

### Future GOAT Candidates

Luka Dončić · Shai Gilgeous-Alexander · Jayson Tatum · Anthony Edwards · Victor Wembanyama · Tyrese Haliburton

---

# 🧰 Data Stack

| Layer | Technology |
|---|---|
| Data source | NBA historical dataset |
| Exploration | Python / Pandas |
| Statistical analysis | Python / Scikit-learn |
| Interactive visualization | Plotly |
| Development environment | Google Colab |
| Data warehouse | Google BigQuery |
| Dashboard | Looker Studio |
| Version control | GitHub |
| Web hosting | GitHub Pages |

---

# 🔄 Analytics Workflow

```text
NBA Raw Data
      ↓
Python / Pandas
      ↓
Data Cleaning & Feature Engineering
      ↓
Statistical & Predictive Models
      ↓
Processed Analytics Tables
      ↓
BigQuery
      ↓
Looker Studio
      ↓
Interactive Storytelling
```

---

# 📂 Repository Structure

```text
nba-winning-formula/
│
├── animations/
│   └── future-goat-trajectory-premium.html
│
├── data/
│   └── processed/
│       ├── 01_team_season.csv
│       ├── 02_winning_factors.csv
│       ├── 03_goat_master.csv
│       ├── 04_goat_dimensions.csv
│       ├── 05_goat_scenarios.csv
│       ├── 06_goat_peak.csv
│       ├── 07_goat_player_seasons.csv
│       ├── 08_methodology.csv
│       ├── 09_future_goat.csv
│       └── 10_future_goat_similarity.csv
│
├── docs/
│   ├── methodology.md
│   └── data_dictionary.md
│
├── images/
│   └── dashboard/
│
├── notebooks/
│   └── nba_winning_formula_analysis.ipynb
│
├── sql/
│   ├── 01_data_quality_checks.sql
│   ├── 02_winning_formula.sql
│   ├── 03_goat_analysis.sql
│   └── 04_future_goat.sql
│
└── README.md
```

---

# 📊 Processed Data Mart

The project produces 10 analytics-ready datasets covering:

- Team performance
- Winning factors
- Historical GOAT profiles
- GOAT dimensions
- Scenario analysis
- Peak performance
- Player career trajectories
- Methodology
- Future GOAT rankings
- Historical similarity

See [`docs/data_dictionary.md`](docs/data_dictionary.md) for detailed documentation.

---

# 🧪 Methodology

The project uses:

- Era-adjusted Z-scores
- Relative True Shooting efficiency
- Correlation analysis
- Multiple linear regression
- Temporal train/test validation
- Multi-criteria scoring
- Scenario sensitivity analysis
- Age-equivalent career comparisons
- Historical similarity analysis

Full methodology:

[`docs/methodology.md`](docs/methodology.md)

---

# ⚠️ Analytical Limitations

Historical comparisons across NBA eras require normalization and remain sensitive to methodological choices.

Awards and championships are influenced by team context, voting and opportunity.

The Future GOAT score represents an **analytical trajectory index**, not a probability or guaranteed career forecast.

---

# 📈 Dashboard

The final Looker Studio dashboard will include:

1. **NBA Winning Formula**
2. **Historical GOAT**
3. **GOAT Scenarios**
4. **Future GOAT**
5. **Interactive Career Trajectories**

Dashboard screenshots and final links will be added here.

---

## Authors

Data Analytics Bootcamp Final Project — 2026
