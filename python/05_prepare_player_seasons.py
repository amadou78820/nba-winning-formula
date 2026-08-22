"""
NBA WINNING FORMULA
05 - Prepare Player Seasons

Purpose
-------
Build the player-season analytical table used by the
Historical GOAT and Future GOAT models.

Final grain:
1 row = 1 NBA player x 1 season

Main outputs:
- PPG
- RPG
- APG
- SPG
- BPG
- MPG
- Era-adjusted production Z-score
- True Shooting %
- League True Shooting %
- TS+
- TS Z-score

Run after:
04_build_winning_formula.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import zscore


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

# ----------------------------------------------------------------
# This script expects a raw / intermediate player-season source.
#
# In the project notebook, df_player_season was created before
# the final exports.
#
# Replace this path if reproducing from a different raw source.
# ----------------------------------------------------------------

RAW_PLAYER_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "player_season_raw.csv"
)

OUTPUT_FILE = (
    DATA_DIR
    / "player_season_features.csv"
)


# ============================================================
# 3. LOAD SOURCE
# ============================================================

if not RAW_PLAYER_FILE.exists():
    raise FileNotFoundError(
        "Raw player-season source not found.\n"
        f"Expected: {RAW_PLAYER_FILE}\n\n"
        "Create/export the raw player-season table first, "
        "or update RAW_PLAYER_FILE to the correct source."
    )

df = pd.read_csv(
    RAW_PLAYER_FILE
)

print("=" * 70)
print("NBA WINNING FORMULA - PLAYER SEASONS")
print("=" * 70)

print(
    "\nInput:",
    RAW_PLAYER_FILE
)

print(
    "Shape:",
    df.shape
)


# ============================================================
# 4. REQUIRED SOURCE COLUMNS
# ============================================================

required = [
    "PLAYER_ID",
    "Name",
    "SEASON_ID",
    "TEAM_ID",
    "TEAM_ABBREVIATION",
    "PLAYER_AGE",
    "GP",
    "MIN",
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "FGA",
    "FTA",
]

missing = [
    column
    for column in required
    if column not in df.columns
]

if missing:
    raise ValueError(
        f"Missing required columns: {missing}"
    )


# ============================================================
# 5. BASIC QUALITY FILTERS
# ============================================================

df_player_season = df.copy()

df_player_season = df_player_season[
    df_player_season["GP"] > 0
].copy()

print(
    "\nRows after GP > 0:",
    len(df_player_season)
)


# ============================================================
# 6. PER-GAME METRICS
# ============================================================

df_player_season["PPG"] = (
    df_player_season["PTS"]
    / df_player_season["GP"]
)

df_player_season["RPG"] = (
    df_player_season["REB"]
    / df_player_season["GP"]
)

df_player_season["APG"] = (
    df_player_season["AST"]
    / df_player_season["GP"]
)

df_player_season["SPG"] = (
    df_player_season["STL"]
    / df_player_season["GP"]
)

df_player_season["BPG"] = (
    df_player_season["BLK"]
    / df_player_season["GP"]
)

df_player_season["MPG"] = (
    df_player_season["MIN"]
    / df_player_season["GP"]
)


# ============================================================
# 7. TRUE SHOOTING PERCENTAGE
# ============================================================

ts_denominator = (
    2
    * (
        df_player_season["FGA"]
        + 0.44
        * df_player_season["FTA"]
    )
)

df_player_season["TS_PCT"] = np.where(
    ts_denominator > 0,
    df_player_season["PTS"]
    / ts_denominator,
    np.nan,
)


# ============================================================
# 8. SEASON / ERA NORMALIZATION
# ============================================================
#
# The goal is to compare players relative to the statistical
# environment of their own season.
#
# PPG, RPG and APG are standardized within SEASON_ID.
# ============================================================


def season_zscore(series):
    """
    Safe Z-score calculation within a season.
    """

    if series.notna().sum() < 2:
        return pd.Series(
            np.nan,
            index=series.index
        )

    std = series.std(ddof=0)

    if std == 0:
        return pd.Series(
            0.0,
            index=series.index
        )

    return (
        series - series.mean()
    ) / std


df_player_season["PPG_Z"] = (
    df_player_season
    .groupby("SEASON_ID")["PPG"]
    .transform(season_zscore)
)

df_player_season["RPG_Z"] = (
    df_player_season
    .groupby("SEASON_ID")["RPG"]
    .transform(season_zscore)
)

df_player_season["APG_Z"] = (
    df_player_season
    .groupby("SEASON_ID")["APG"]
    .transform(season_zscore)
)


# ============================================================
# 9. COMPOSITE PRODUCTION Z-SCORE
# ============================================================
#
# The project uses scoring as the dominant component,
# while rebounding and playmaking remain meaningful.
#
# Final weights:
# PPG Z = 50%
# RPG Z = 25%
# APG Z = 25%
# ============================================================

df_player_season["PRODUCTION_Z"] = (
      0.50 * df_player_season["PPG_Z"]
    + 0.25 * df_player_season["RPG_Z"]
    + 0.25 * df_player_season["APG_Z"]
)


# ============================================================
# 10. LEAGUE TS%
# ============================================================

league_ts = (
    df_player_season
    .groupby("SEASON_ID")
    .agg(
        league_pts=("PTS", "sum"),
        league_fga=("FGA", "sum"),
        league_fta=("FTA", "sum"),
    )
    .reset_index()
)

league_ts["LEAGUE_TS"] = (
    league_ts["league_pts"]
    /
    (
        2
        * (
            league_ts["league_fga"]
            + 0.44
            * league_ts["league_fta"]
        )
    )
)

league_ts = league_ts[
    [
        "SEASON_ID",
        "LEAGUE_TS",
    ]
]


df_player_season = (
    df_player_season
    .merge(
        league_ts,
        on="SEASON_ID",
        how="left",
        validate="many_to_one",
    )
)


# ============================================================
# 11. TRUE SHOOTING PLUS
# ============================================================
#
# TS+ = player TS% / league TS% * 100
#
# 100 = league average
# >100 = above league average
# <100 = below league average
# ============================================================

df_player_season["TS_PLUS"] = np.where(
    df_player_season["LEAGUE_TS"] > 0,
    (
        df_player_season["TS_PCT"]
        / df_player_season["LEAGUE_TS"]
        * 100
    ),
    np.nan,
)


# ============================================================
# 12. TS Z-SCORE
# ============================================================

df_player_season["TS_Z"] = (
    df_player_season
    .groupby("SEASON_ID")["TS_PCT"]
    .transform(season_zscore)
)


# ============================================================
# 13. DATA QUALITY
# ============================================================

print("\n" + "=" * 70)
print("DATA QUALITY")
print("=" * 70)

duplicate_count = (
    df_player_season
    .duplicated(
        subset=[
            "PLAYER_ID",
            "SEASON_ID",
        ]
    )
    .sum()
)

print(
    "Rows:",
    len(df_player_season)
)

print(
    "Players:",
    df_player_season["PLAYER_ID"].nunique()
)

print(
    "Seasons:",
    df_player_season["SEASON_ID"].nunique()
)

print(
    "Duplicate player-season keys:",
    duplicate_count
)

print(
    "Missing PRODUCTION_Z:",
    df_player_season["PRODUCTION_Z"]
    .isna()
    .sum()
)

print(
    "Missing TS_PLUS:",
    df_player_season["TS_PLUS"]
    .isna()
    .sum()
)


# ============================================================
# 14. SAMPLE CHECK
# ============================================================

sample_players = [
    "Michael Jordan",
    "LeBron James",
    "Kareem Abdul-Jabbar",
    "Magic Johnson",
    "Larry Bird",
]

sample = (
    df_player_season[
        df_player_season["Name"]
        .isin(sample_players)
    ][
        [
            "Name",
            "SEASON_ID",
            "PLAYER_AGE",
            "GP",
            "PPG",
            "RPG",
            "APG",
            "PRODUCTION_Z",
            "TS_PCT",
            "LEAGUE_TS",
            "TS_PLUS",
            "TS_Z",
        ]
    ]
    .sort_values(
        ["Name", "SEASON_ID"]
    )
)

print("\n" + "=" * 70)
print("GOAT SAMPLE")
print("=" * 70)

print(
    sample
    .head(30)
    .round(3)
    .to_string(index=False)
)


# ============================================================
# 15. EXPORT INTERMEDIATE TABLE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df_player_season.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "\nExported:",
    OUTPUT_FILE
)


# ============================================================
# 16. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PLAYER-SEASON FEATURES COMPLETE")
print("=" * 70)

print(
    """
RAW PLAYER-SEASON DATA
          ↓
PER-GAME METRICS
PPG / RPG / APG
          ↓
SEASON NORMALIZATION
PPG_Z / RPG_Z / APG_Z
          ↓
ERA-ADJUSTED PRODUCTION
PRODUCTION_Z
          ↓
TRUE SHOOTING
TS_PCT
          ↓
LEAGUE CONTEXT
LEAGUE_TS
          ↓
RELATIVE EFFICIENCY
TS_PLUS / TS_Z
          ↓
player_season_features.csv

Final grain:
1 row = 1 player x 1 season

Next step:
Run 06_build_goat_model.py
"""
)
