"""
NBA WINNING FORMULA
08 - Export and Validate Analytics Data Mart

Purpose
-------
Validate the final analytics-ready datasets before loading
them into BigQuery and connecting them to Looker Studio.

This script:
1. Checks that all expected files exist.
2. Reports rows, columns, duplicates and null values.
3. Validates important logical keys.
4. Produces a simple Data Mart audit.
5. Confirms that the project is ready for BigQuery.

Run after:
07_build_future_goat.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path
import pandas as pd


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


# ============================================================
# 3. EXPECTED DATA MART FILES
# ============================================================

FILES = {
    "team_season":
        "01_team_season.csv",

    "winning_factors":
        "02_winning_factors.csv",

    "goat_master":
        "03_goat_master.csv",

    "goat_dimensions":
        "04_goat_dimensions.csv",

    "goat_scenarios":
        "05_goat_scenarios.csv",

    "goat_peak":
        "06_goat_peak.csv",

    "goat_player_seasons":
        "07_goat_player_seasons.csv",

    "methodology":
        "08_methodology.csv",

    "future_goat":
        "09_future_goat.csv",

    "future_goat_similarity":
        "10_future_goat_similarity.csv",
}


print("=" * 70)
print("NBA WINNING FORMULA - DATA MART VALIDATION")
print("=" * 70)

print(
    "\nProcessed directory:",
    PROCESSED_DIR
)


# ============================================================
# 4. CHECK FILE EXISTENCE
# ============================================================

missing_files = []

for table_name, filename in FILES.items():

    path = PROCESSED_DIR / filename

    if path.exists():

        print(
            f"✓ {filename}"
        )

    else:

        print(
            f"✗ MISSING: {filename}"
        )

        missing_files.append(
            filename
        )


if missing_files:

    raise FileNotFoundError(
        "Missing Data Mart files: "
        + ", ".join(
            missing_files
        )
    )


# ============================================================
# 5. LOAD TABLES
# ============================================================

tables = {}

for table_name, filename in FILES.items():

    path = PROCESSED_DIR / filename

    tables[
        table_name
    ] = pd.read_csv(
        path
    )


# ============================================================
# 6. GLOBAL AUDIT
# ============================================================

audit_rows = []

for table_name, df in tables.items():

    audit_rows.append(
        {
            "table":
                table_name,

            "rows":
                len(df),

            "columns":
                len(
                    df.columns
                ),

            "duplicate_rows":
                df.duplicated()
                .sum(),

            "null_values":
                int(
                    df.isna()
                    .sum()
                    .sum()
                ),
        }
    )


audit = pd.DataFrame(
    audit_rows
)


print("\n" + "=" * 70)
print("GLOBAL DATA MART AUDIT")
print("=" * 70)

print(
    audit.to_string(
        index=False
    )
)


# ============================================================
# 7. TEAM-SEASON KEY CHECK
# ============================================================

team_season = tables[
    "team_season"
]

required_team_columns = [
    "season",
    "abbreviation",
    "win_rate",
]

missing = [
    col
    for col in required_team_columns
    if col not in team_season.columns
]

if missing:

    raise ValueError(
        "team_season missing columns: "
        f"{missing}"
    )


team_duplicate_keys = (
    team_season
    .duplicated(
        subset=[
            "season",
            "abbreviation",
        ]
    )
    .sum()
)


print("\n" + "=" * 70)
print("TEAM-SEASON CHECK")
print("=" * 70)

print(
    "Rows:",
    len(team_season)
)

print(
    "Duplicate season/team keys:",
    team_duplicate_keys
)

print(
    "Season coverage:",
    team_season[
        "season"
    ].min(),
    "→",
    team_season[
        "season"
    ].max()
)


if team_duplicate_keys > 0:

    raise ValueError(
        "Duplicate team-season keys detected."
    )


# ============================================================
# 8. GOAT MASTER CHECK
# ============================================================

goat_master = tables[
    "goat_master"
]

goat_name_col = (
    "Name"
    if "Name" in goat_master.columns
    else "name"
)

goat_duplicates = (
    goat_master[
        goat_name_col
    ]
    .duplicated()
    .sum()
)


print("\n" + "=" * 70)
print("GOAT MASTER CHECK")
print("=" * 70)

print(
    "Players:",
    goat_master[
        goat_name_col
    ].nunique()
)

print(
    "Duplicate players:",
    goat_duplicates
)


if goat_duplicates > 0:

    raise ValueError(
        "Duplicate GOAT players detected."
    )


# ============================================================
# 9. GOAT DIMENSIONS CHECK
# ============================================================

goat_dimensions = tables[
    "goat_dimensions"
]

dimension_name_col = (
    "Name"
    if "Name" in goat_dimensions.columns
    else "name"
)

dimension_duplicates = (
    goat_dimensions[
        dimension_name_col
    ]
    .duplicated()
    .sum()
)


print("\nGOAT dimension duplicates:",
      dimension_duplicates)


# ============================================================
# 10. PLAYER-SEASON KEY CHECK
# ============================================================

goat_player_seasons = tables[
    "goat_player_seasons"
]

player_season_key = [
    "PLAYER_ID",
    "SEASON_ID",
]

available_key = [
    col
    for col in player_season_key
    if col in goat_player_seasons.columns
]


if len(
    available_key
) == 2:

    player_season_duplicates = (
        goat_player_seasons
        .duplicated(
            subset=
            player_season_key
        )
        .sum()
    )

else:

    player_season_duplicates = None


print("\n" + "=" * 70)
print("GOAT PLAYER-SEASON CHECK")
print("=" * 70)

print(
    "Rows:",
    len(
        goat_player_seasons
    )
)

print(
    "Duplicate player-season keys:",
    player_season_duplicates
)


if (
    player_season_duplicates
    is not None
    and
    player_season_duplicates
    > 0
):

    raise ValueError(
        "Duplicate player-season keys detected."
    )


# ============================================================
# 11. FUTURE GOAT CHECK
# ============================================================

future_goat = tables[
    "future_goat"
]

required_future_columns = [
    "player",
    "future_goat_rank",
    "future_goat_score",
    "data_cutoff",
    "model_version",
]

missing = [
    col
    for col in required_future_columns
    if col not in future_goat.columns
]

if missing:

    raise ValueError(
        "future_goat missing columns: "
        f"{missing}"
    )


future_player_duplicates = (
    future_goat[
        "player"
    ]
    .duplicated()
    .sum()
)


future_missing_scores = (
    future_goat[
        "future_goat_score"
    ]
    .isna()
    .sum()
)


print("\n" + "=" * 70)
print("FUTURE GOAT CHECK")
print("=" * 70)

print(
    "Candidates:",
    future_goat[
        "player"
    ].nunique()
)

print(
    "Duplicate players:",
    future_player_duplicates
)

print(
    "Missing scores:",
    future_missing_scores
)

print(
    "Data cutoff:",
    future_goat[
        "data_cutoff"
    ].unique()
)

print(
    "Model version:",
    future_goat[
        "model_version"
    ].unique()
)


if future_player_duplicates > 0:

    raise ValueError(
        "Duplicate Future GOAT players detected."
    )


if future_missing_scores > 0:

    raise ValueError(
        "Missing Future GOAT scores detected."
    )


# ============================================================
# 12. FUTURE GOAT SIMILARITY CHECK
# ============================================================

future_similarity = tables[
    "future_goat_similarity"
]

possible_name_cols = [
    "player",
    "Name",
]

possible_goat_cols = [
    "goat",
    "GOAT",
]

player_col = next(
    (
        col
        for col
        in possible_name_cols
        if col in future_similarity.columns
    ),
    None,
)

goat_col = next(
    (
        col
        for col
        in possible_goat_cols
        if col in future_similarity.columns
    ),
    None,
)


if (
    player_col
    and goat_col
):

    similarity_duplicates = (
        future_similarity
        .duplicated(
            subset=[
                player_col,
                goat_col,
            ]
        )
        .sum()
    )

else:

    similarity_duplicates = None


print("\n" + "=" * 70)
print("SIMILARITY CHECK")
print("=" * 70)

print(
    "Rows:",
    len(
        future_similarity
    )
)

print(
    "Duplicate player/GOAT pairs:",
    similarity_duplicates
)


# ============================================================
# 13. FINAL DATA MART SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATA MART")
print("=" * 70)

for table_name, filename in FILES.items():

    df = tables[
        table_name
    ]

    print(
        f"{filename:<32}"
        f"{len(df):>8,} rows"
    )


# ============================================================
# 14. BIGQUERY TABLE MAP
# ============================================================

BIGQUERY_TABLES = {
    "01_team_season.csv":
        "team_season",

    "02_winning_factors.csv":
        "winning_factors",

    "03_goat_master.csv":
        "goat_master",

    "04_goat_dimensions.csv":
        "goat_dimensions",

    "05_goat_scenarios.csv":
        "goat_scenarios",

    "06_goat_peak.csv":
        "goat_peak",

    "07_goat_player_seasons.csv":
        "goat_player_seasons",

    "08_methodology.csv":
        "methodology",

    "09_future_goat.csv":
        "future_goat",

    "10_future_goat_similarity.csv":
        "future_goat_similarity",
}


print("\n" + "=" * 70)
print("BIGQUERY TABLE MAP")
print("=" * 70)

for filename, table in BIGQUERY_TABLES.items():

    print(
        f"{filename:<32}"
        f"→ {table}"
    )


# ============================================================
# 15. DATA MART ARCHITECTURE
# ============================================================

print("\n" + "=" * 70)
print("ANALYTICAL ARCHITECTURE")
print("=" * 70)

print(
    """
TEAM ANALYTICS
--------------
01_team_season
        ↓
02_winning_factors


HISTORICAL GOAT
---------------
03_goat_master
04_goat_dimensions
05_goat_scenarios
06_goat_peak
07_goat_player_seasons
08_methodology


FUTURE GOAT
-----------
09_future_goat
        ↕
10_future_goat_similarity
"""
)


# ============================================================
# 16. BIGQUERY LOAD READINESS
# ============================================================

critical_errors = (
    team_duplicate_keys
    + goat_duplicates
    + dimension_duplicates
    + future_player_duplicates
    + future_missing_scores
)

if (
    player_season_duplicates
    is not None
):

    critical_errors += (
        player_season_duplicates
    )


if (
    similarity_duplicates
    is not None
):

    critical_errors += (
        similarity_duplicates
    )


print("\n" + "=" * 70)

if critical_errors == 0:

    print(
        "✓ DATA MART READY FOR BIGQUERY"
    )

else:

    print(
        "✗ DATA MART REQUIRES REVIEW"
    )

print("=" * 70)


# ============================================================
# 17. PIPELINE SUMMARY
# ============================================================

print(
    """
PYTHON ANALYSIS
      ↓
10 PROCESSED DATASETS
      ↓
DATA QUALITY CHECKS
      ↓
KEY VALIDATION
      ↓
BIGQUERY TABLE MAPPING
      ↓
BIGQUERY
      ↓
LOOKER STUDIO

Next step:
Run 09_build_plotly_animation.py
"""
)
