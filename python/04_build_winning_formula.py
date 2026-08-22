"""
NBA WINNING FORMULA
04 - Build Winning Formula

Purpose
-------
Build and evaluate the final Winning Formula model.

Input:
01_team_season.csv

Output:
02_winning_factors.csv

Method:
- Team-season grain
- Possession-adjusted features
- Temporal train/test split
- StandardScaler
- LinearRegression
- R² and MAE evaluation

Run after:
03_prepare_team_data.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
)


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

INPUT_FILE = (
    DATA_DIR
    / "01_team_season.csv"
)

OUTPUT_FILE = (
    DATA_DIR
    / "02_winning_factors.csv"
)


# ============================================================
# 3. LOAD TEAM-SEASON DATA
# ============================================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Input file not found: {INPUT_FILE}"
    )

team_season = pd.read_csv(
    INPUT_FILE
)

print("=" * 70)
print("NBA WINNING FORMULA")
print("=" * 70)

print(
    "\nInput:",
    INPUT_FILE
)

print(
    "Shape:",
    team_season.shape
)


# ============================================================
# 4. FINAL MODEL FEATURES
# ============================================================

features = [
    "e_fg_percent",
    "tov_percent",
    "orb_percent",
    "drb_percent",
    "ft_fga",
    "opp_e_fg_percent",
    "opp_tov_percent",
    "opp_ft_fga",
]

target = "win_rate"

required_columns = (
    features
    + [target, "season"]
)

missing_columns = [
    column
    for column in required_columns
    if column not in team_season.columns
]

if missing_columns:
    raise ValueError(
        "Missing required columns: "
        f"{missing_columns}"
    )


# ============================================================
# 5. DESCRIPTIVE CORRELATIONS
# ============================================================

corr_data = (
    team_season[
        [target] + features
    ]
    .dropna()
)

correlations = (
    corr_data
    .corr(numeric_only=True)[target]
    .drop(target)
    .sort_values(
        ascending=False
    )
)

print("\n" + "=" * 70)
print("CORRELATION WITH WIN RATE")
print("=" * 70)

print(
    correlations
    .round(3)
    .to_string()
)


# ============================================================
# 6. ANALYSIS PERIOD
# ============================================================
#
# The source includes seasons through 2026.
# The validated project model excludes the latest
# non-comparable / future-labelled observations.
#
# The final analysis uses seasons <= 2025.
# ============================================================

analysis = team_season[
    team_season["season"] <= 2025
].copy()


# ============================================================
# 7. TEMPORAL SPLIT
# ============================================================
#
# TRAIN: seasons through 2017
# TEST : seasons 2018+
#
# This avoids random leakage between historical periods.
# ============================================================

train = analysis[
    analysis["season"] <= 2017
].copy()

test = analysis[
    analysis["season"] >= 2018
].copy()


train_data = (
    train[
        features + [target]
    ]
    .dropna()
)

test_data = (
    test[
        features + [target]
    ]
    .dropna()
)


print("\n" + "=" * 70)
print("TEMPORAL SPLIT")
print("=" * 70)

print(
    "Train observations:",
    len(train_data)
)

print(
    "Test observations:",
    len(test_data)
)


# ============================================================
# 8. DEFINE X / y
# ============================================================

X_train = train_data[
    features
]

y_train = train_data[
    target
]

X_test = test_data[
    features
]

y_test = test_data[
    target
]


# ============================================================
# 9. STANDARDIZATION
# ============================================================
#
# Important:
# fit_transform ONLY on train.
#
# transform ONLY on test.
#
# This prevents data leakage.
# ============================================================

scaler = StandardScaler()

X_train_scaled = (
    scaler.fit_transform(
        X_train
    )
)

X_test_scaled = (
    scaler.transform(
        X_test
    )
)


# ============================================================
# 10. LINEAR REGRESSION
# ============================================================

model = LinearRegression()

model.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# 11. PREDICTIONS
# ============================================================

train_pred = model.predict(
    X_train_scaled
)

test_pred = model.predict(
    X_test_scaled
)


# ============================================================
# 12. MODEL PERFORMANCE
# ============================================================

train_r2 = r2_score(
    y_train,
    train_pred
)

test_r2 = r2_score(
    y_test,
    test_pred
)

test_mae = mean_absolute_error(
    y_test,
    test_pred
)

approx_win_error = (
    test_mae * 82
)


print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(
    f"Train R² : {train_r2:.3f}"
)

print(
    f"Test R²  : {test_r2:.3f}"
)

print(
    f"Test MAE : {test_mae:.3f}"
)

print(
    "Approximate error "
    f"over 82 games: "
    f"{approx_win_error:.1f} wins"
)


# ============================================================
# 13. STANDARDIZED COEFFICIENTS
# ============================================================

winning_factors = pd.DataFrame(
    {
        "factor": features,
        "coefficient": model.coef_,
    }
)

winning_factors[
    "abs_coefficient"
] = (
    winning_factors[
        "coefficient"
    ]
    .abs()
)

winning_factors = (
    winning_factors
    .sort_values(
        "abs_coefficient",
        ascending=False
    )
    .reset_index(drop=True)
)

winning_factors[
    "importance_rank"
] = (
    np.arange(
        1,
        len(winning_factors) + 1
    )
)


# ============================================================
# 14. DISPLAY LABELS
# ============================================================

factor_labels = {
    "e_fg_percent":
        "Shooting Efficiency",

    "opp_e_fg_percent":
        "Opponent Shooting Defense",

    "tov_percent":
        "Ball Security",

    "opp_tov_percent":
        "Turnover Creation",

    "orb_percent":
        "Offensive Rebounding",

    "drb_percent":
        "Defensive Rebounding",

    "ft_fga":
        "Free Throw Pressure",

    "opp_ft_fga":
        "Opponent Free Throw Prevention",
}


factor_categories = {
    "e_fg_percent":
        "Shooting",

    "opp_e_fg_percent":
        "Defense",

    "tov_percent":
        "Possession",

    "opp_tov_percent":
        "Possession",

    "orb_percent":
        "Rebounding",

    "drb_percent":
        "Rebounding",

    "ft_fga":
        "Free Throws",

    "opp_ft_fga":
        "Free Throws",
}


winning_factors[
    "factor_name"
] = (
    winning_factors[
        "factor"
    ]
    .map(
        factor_labels
    )
)


winning_factors[
    "category"
] = (
    winning_factors[
        "factor"
    ]
    .map(
        factor_categories
    )
)


# ============================================================
# 15. DIRECTION
# ============================================================

winning_factors[
    "direction"
] = np.where(
    winning_factors[
        "coefficient"
    ] > 0,
    "Positive",
    "Negative",
)


# ============================================================
# 16. ADD SIMPLE CORRELATIONS
# ============================================================

winning_factors[
    "correlation"
] = (
    winning_factors[
        "factor"
    ]
    .map(
        correlations.to_dict()
    )
)


# ============================================================
# 17. ADD MODEL PERFORMANCE
# ============================================================

winning_factors[
    "train_r2"
] = train_r2

winning_factors[
    "test_r2"
] = test_r2

winning_factors[
    "test_mae"
] = test_mae

winning_factors[
    "approx_win_error"
] = approx_win_error


# ============================================================
# 18. FINAL COLUMN ORDER
# ============================================================

winning_factors = winning_factors[
    [
        "importance_rank",
        "factor",
        "factor_name",
        "category",
        "coefficient",
        "abs_coefficient",
        "correlation",
        "direction",
        "train_r2",
        "test_r2",
        "test_mae",
        "approx_win_error",
    ]
]


# ============================================================
# 19. FINAL PREVIEW
# ============================================================

print("\n" + "=" * 70)
print("FINAL WINNING FACTORS")
print("=" * 70)

print(
    winning_factors
    .round(4)
    .to_string(
        index=False
    )
)


# ============================================================
# 20. EXPORT
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

winning_factors.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "\nExported:",
    OUTPUT_FILE
)


# ============================================================
# 21. FINAL INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)

print(
    """
The final model evaluates eight possession-adjusted
team-performance factors.

The strongest associations with winning are expected
to reflect four major basketball principles:

1. SHOOTING EFFICIENCY
   - eFG%
   - Opponent eFG%

2. POSSESSION CONTROL
   - Turnover %
   - Opponent Turnover %

3. REBOUNDING
   - Offensive Rebound %
   - Defensive Rebound %

4. FREE THROW PRESSURE
   - FT/FGA
   - Opponent FT/FGA

Important:
Regression coefficients describe statistical
associations within this model.

They should not automatically be interpreted
as causal effects.
"""
)


# ============================================================
# 22. PIPELINE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("WINNING FORMULA COMPLETE")
print("=" * 70)

print(
    """
01_team_season.csv
        ↓
8 possession-adjusted features
        ↓
Temporal split
        ↓
StandardScaler
        ↓
Linear Regression
        ↓
R² + MAE
        ↓
Standardized coefficients
        ↓
02_winning_factors.csv

Next step:
Run 05_prepare_player_seasons.py
"""
)
