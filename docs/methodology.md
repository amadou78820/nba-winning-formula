# Methodology

## Project Overview

The NBA Winning Formula project explores three main questions:

1. What performance factors are most strongly associated with winning in the NBA?
2. Who is the greatest NBA player of all time according to a transparent multi-criteria model?
3. Which current players are following historically exceptional trajectories?

---

## 1. Winning Formula

The team-level analysis uses season-level NBA data adjusted per 100 possessions.

The final model includes:

- Effective Field Goal Percentage (eFG%)
- Opponent eFG%
- Turnover Percentage
- Opponent Turnover Percentage
- Offensive Rebound Percentage
- Defensive Rebound Percentage
- Free Throw Rate
- Opponent Free Throw Rate

### Model performance

- Train R²: 0.929
- Test R²: 0.926
- Test MAE: 0.032
- Approximate error: 2.6 wins over an 82-game season

The model is used to identify statistical factors associated with winning.

Correlation and regression results should not be interpreted as proof of causality.

---

## 2. Historical GOAT Model

The historical GOAT model evaluates five players:

- Michael Jordan
- LeBron James
- Kareem Abdul-Jabbar
- Magic Johnson
- Larry Bird

The model uses six dimensions:

| Dimension | Balanced Weight |
|---|---:|
| Production | 20% |
| Efficiency | 15% |
| Playoffs | 20% |
| Individual Success | 20% |
| Team Success | 10% |
| Longevity | 15% |

### Production

Production is adjusted relative to the statistical environment of each NBA era using Z-scores.

### Efficiency

Scoring efficiency is evaluated using True Shooting Plus (TS+), relative to league context.

### Playoffs

The playoff dimension combines postseason impact and changes in performance relative to the regular season.

### Individual Success

Includes MVP awards, MVP vote share, All-NBA selections and All-Defensive selections.

### Team Success

Uses NBA championships as a collective-success indicator.

### Longevity

Measures both career duration and sustained elite-level performance.

---

## 3. GOAT Scenarios

Several weighting scenarios are used to test the robustness of the GOAT ranking:

- Balanced
- Peak
- Longevity
- Winning
- Individual Dominance

The objective is not to claim that one definition of greatness is universally correct.

Instead, the analysis shows how the ranking changes when the definition of greatness changes.

---

## 4. Future GOAT Model

The Future GOAT analysis is a trajectory model.

It does NOT estimate the probability that a player will become the GOAT.

The data cutoff is the end of the 2023-24 NBA season.

The V2 model uses:

| Dimension | Weight |
|---|---:|
| Age-adjusted Production | 35% |
| Age-adjusted Efficiency | 25% |
| Early Career Recognition | 25% |
| Adjusted Historical GOAT Similarity | 15% |

### Historical Similarity

Current players are compared with historical GOATs at comparable ages.

The Trajectory Similarity Index measures similarity across:

- Era-adjusted production
- Relative scoring efficiency
- Early-career recognition

The similarity value is an analytical index, not a probability.

---

## 5. Data Quality

Key checks include:

- Unique team-season grain
- Duplicate detection
- Null-value checks
- Date and season coverage
- Temporal train/test validation
- Prevention of future-data leakage in the Future GOAT analysis

---

## 6. Main Limitations

- Historical data availability is not identical across every NBA era.
- Some advanced playoff datasets have incomplete recent coverage.
- Awards and team success depend partly on context and voting.
- Future GOAT results measure observed trajectory, not future career outcomes.
- Model weights are analytical choices and are therefore documented explicitly.

---

## 7. Tools

- Python
- Pandas
- Scikit-learn
- Plotly
- Google Colab
- BigQuery
- Looker Studio
- GitHub
- GitHub Pages
