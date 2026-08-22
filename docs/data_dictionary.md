# Data Dictionary

## NBA Winning Formula — Analytics Data Mart

This document describes the processed datasets produced for the NBA Winning Formula project.

---

## 01 — team_season

**File:** `01_team_season.csv`

**Grain:** One row per NBA team and season.

**Purpose:** Main dataset for the Winning Formula analysis.

**Period:** 1974–2026

**Key:** `season + abbreviation`

### Main fields

| Field | Description |
|---|---|
| season | NBA season |
| team | Team name |
| abbreviation | Team abbreviation |
| w | Wins |
| l | Losses |
| win_rate | Percentage of games won |
| o_rtg | Offensive Rating |
| d_rtg | Defensive Rating |
| n_rtg | Net Rating |
| pace | Estimated possessions per game |
| e_fg_percent | Effective Field Goal Percentage |
| tov_percent | Turnover Percentage |
| orb_percent | Offensive Rebound Percentage |
| drb_percent | Defensive Rebound Percentage |
| ft_fga | Free Throw Rate |
| opp_e_fg_percent | Opponent eFG% |
| opp_tov_percent | Opponent Turnover Percentage |
| opp_ft_fga | Opponent Free Throw Rate |

---

## 02 — winning_factors

**File:** `02_winning_factors.csv`

**Grain:** One row per model factor.

**Purpose:** Stores the final regression results used to identify the statistical factors associated with winning.

### Main fields

| Field | Description |
|---|---|
| importance_rank | Factor importance ranking |
| factor | Technical variable name |
| factor_name | Display name |
| category | Analytical category |
| coefficient | Regression coefficient |
| abs_coefficient | Absolute coefficient |
| correlation | Correlation with win rate |
| direction | Positive or negative relationship |
| train_r2 | Training R² |
| test_r2 | Test R² |
| test_mae | Test Mean Absolute Error |
| approx_win_error | Approximate prediction error expressed in wins |

### Final model performance

- Train R²: 0.929
- Test R²: 0.926
- Test MAE: 0.032
- Approximate error: 2.6 wins

---

## 03 — goat_master

**File:** `03_goat_master.csv`

**Grain:** One row per historical GOAT candidate.

**Players included:**

- LeBron James
- Michael Jordan
- Kareem Abdul-Jabbar
- Magic Johnson
- Larry Bird

**Purpose:** Consolidated source containing the core metrics used by the historical GOAT model.

### Metric families

- Career production
- Peak production
- Era-adjusted efficiency
- MVP performance
- All-NBA selections
- All-Defensive selections
- Championships
- Career longevity
- Elite seasons
- Playoff performance

---

## 04 — goat_dimensions

**File:** `04_goat_dimensions.csv`

**Grain:** One row per GOAT candidate.

**Purpose:** Contains normalized scores for the six dimensions of greatness.

### Dimensions

| Dimension | Meaning |
|---|---|
| Production | Statistical production |
| Efficiency | Era-adjusted scoring efficiency |
| Playoffs | Postseason performance |
| Individual | Individual awards and recognition |
| Team Success | Championships |
| Longevity | Career and elite-performance longevity |

---

## 05 — goat_scenarios

**File:** `05_goat_scenarios.csv`

**Grain:** One row per GOAT candidate.

**Purpose:** Compares GOAT rankings under different definitions of greatness.

### Scenarios

- Balanced
- Peak
- Longevity
- Winning
- Individual Dominance

This dataset is used for sensitivity analysis of the GOAT ranking.

---

## 06 — goat_peak

**File:** `06_goat_peak.csv`

**Grain:** One row per historical GOAT candidate.

**Purpose:** Measures peak-level greatness.

### Main indicators

- Peak Production
- Peak Efficiency
- Playoffs
- Peak MVP
- True Peak Score
- Peak Rank

---

## 07 — goat_player_seasons

**File:** `07_goat_player_seasons.csv`

**Grain:** One row per player and season.

**Purpose:** Reconstructs historical career trajectories and enables age-to-age comparisons.

### Main fields

| Field | Description |
|---|---|
| Name | Player |
| PLAYER_ID | Player identifier |
| SEASON_ID | NBA season |
| TEAM_ABBREVIATION | Team |
| PLAYER_AGE | Player age |
| GP | Games played |
| PPG | Points per game |
| RPG | Rebounds per game |
| APG | Assists per game |
| PRODUCTION_Z | Era-adjusted production Z-score |
| TS_PCT | True Shooting Percentage |
| TS_PLUS | True Shooting relative to league environment |
| TS_Z | Era-adjusted TS Z-score |

---

## 08 — methodology

**File:** `08_methodology.csv`

**Grain:** One row per GOAT model dimension.

**Purpose:** Documents the model rather than representing basketball observations.

### Main fields

- dimension
- weight_balanced
- metrics
- method
- purpose

This table makes the GOAT scoring framework transparent and reproducible.

---

## 09 — future_goat

**File:** `09_future_goat.csv`

**Grain:** One row per current NBA candidate.

**Data cutoff:** 2023-24

**Model:** V2

**Purpose:** Ranks current players according to their observed historical trajectory.

### Main fields

| Field | Description |
|---|---|
| future_goat_rank | Final trajectory ranking |
| player | Player |
| age | Age at data cutoff |
| team | Team |
| production_z | Era-adjusted production |
| ts_plus | Era-adjusted scoring efficiency |
| production_score | Age-adjusted production trajectory |
| efficiency_score | Age-adjusted efficiency trajectory |
| recognition_score | Early-career recognition trajectory |
| closest_goat | Most similar historical GOAT profile |
| goat_similarity | Raw similarity index |
| adjusted_goat_similarity | Age-adjusted similarity |
| future_goat_score | Composite trajectory score |
| data_cutoff | Latest season used |
| model_version | Model version |
| trajectory_tier | Trajectory classification |

### Important

`future_goat_score` is **not a probability** of becoming the GOAT.

It measures the strength of a player's observed trajectory relative to historical benchmarks.

---

## 10 — future_goat_similarity

**File:** `10_future_goat_similarity.csv`

**Grain:** One row per current player × historical GOAT comparison.

**Purpose:** Supports historical player similarity analysis.

### Main fields

| Field | Description |
|---|---|
| Name | Current player |
| AGE | Current player's age |
| GOAT | Historical comparison player |
| Similarity | Similarity index |
| Distance | Statistical distance |

A higher similarity score indicates a closer statistical trajectory according to the selected features.

---

# Data Model Overview

The project contains three main analytical layers:

### Team Performance

`team_season`  
→ `winning_factors`

### Historical GOAT

`goat_master`  
→ `goat_dimensions`  
→ `goat_scenarios`  
→ `goat_peak`

with:

`goat_player_seasons`

for season-level trajectory analysis.

### Future GOAT

`future_goat`  
↔ `future_goat_similarity`

Historical benchmarks from the GOAT analysis are used to contextualize current-player trajectories.

---

# Data Quality

The processed datasets were checked for:

- Duplicate keys
- Missing critical values
- Season coverage
- Player-season uniqueness
- Team-season uniqueness
- Temporal consistency
- Model train/test separation

The main `team_season` dataset contains no duplicate `season + team` keys.
