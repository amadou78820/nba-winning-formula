"""
NBA WINNING FORMULA
03 - Prepare Team Data

Purpose
-------
Build the analytical team-season dataset used by the
Winning Formula model.

Final grain:
1 row = 1 NBA team x 1 season

Main sources:
- Team per-100-possession statistics
- Opponent per-100-possession statistics
- Team advanced / summary statistics

Final output:
01_team_season.csv

Run after:
01_download_data.py
02_inspect_sources.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path

import kagglehub
import numpy as np
import pandas as pd


# ============================================================
# 2. CONFIGURATION
# ============================================================

KAGGLE_DATASET = "wyattowalsh/basketball"
KAGGLE_VERSION = 238

dataset_path = kagglehub.dataset_download(
    f"{KAGGLE_DATASET}/versions/{KAGGLE_VERSION}"
)

DATASET_DIR = Path(dataset_path)
CSV_DIR = DATASET_DIR / "csv"

print("=" * 70)
print("NBA WINNING FORMULA - TEAM DATA PREPARATION")
print("=" * 70)

print("\nDataset:")
print(DATASET_DIR)


# ============================================================
# 3. FIND SOURCE FILES
# ============================================================

all_csv = list(CSV_DIR.rglob("*.csv"))

print("\nCSV files detected:", len(all_csv))


def search_files(keywords):
    """
    Find CSV files whose names contain all requested keywords.
    """

    matches = []

    for path in all_csv:

        name = path.name.lower()

        if all(
            keyword.lower() in name
            for keyword in keywords
        ):
            matches.append(path)

    return matches


search_groups = {
    "team_per_100": ["team", "100"],
    "opponent_per_100": ["opponent", "100"],
    "team_summary": ["team"],
}

print("\nPotential source files:")

for label, keywords in search_groups.items():

    matches = search_files(keywords)

    print(f"\n{label}:")

    for path in matches[:20]:
        print(" -", path.relative_to(DATASET_DIR))


# ============================================================
# 4. SOURCE FILE CONFIGURATION
# ============================================================
#
# IMPORTANT:
# Dataset versions can use slightly different filenames.
#
# After running the search above, replace these paths if needed.
# ============================================================

TEAM100_FILE = None
OPP100_FILE = None
TEAM_SUMMARY_FILE = None


# ============================================================
# 5. SAFE CSV LOADER
# ============================================================

def load_source(path, label):
    """
    Load a configured CSV source.
    """

    if path is None:

        print(
            f"\n{label}: path not configured."
        )

        return None

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(
            f"{label} not found: {path}"
        )

    df = pd.read_csv(path)

    print(
        f"\n{label}: "
        f"{df.shape[0]:,} rows x "
        f"{df.shape[1]} columns"
    )

    return df


team100 = load_source(
    TEAM100_FILE,
    "TEAM100"
)

opp100 = load_source(
    OPP100_FILE,
    "OPP100"
)

team_summary = load_source(
    TEAM_SUMMARY_FILE,
    "TEAM SUMMARY"
)


# ============================================================
# 6. STANDARDIZE COLUMN NAMES
# ============================================================

def standardize_columns(df):
    """
    Standardize column names for reproducible joins.
    """

    if df is None:
        return None

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("%", "percent", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


team100 = standardize_columns(team100)
opp100 = standardize_columns(opp100)
team_summary = standardize_columns(team_summary)


# ============================================================
# 7. VERIFY REQUIRED JOIN KEYS
# ============================================================

JOIN_KEYS = [
    "season",
    "lg",
    "team",
    "abbreviation",
    "playoffs",
]


def check_keys(df, name):

    if df is None:
        return

    missing = [
        col
        for col in JOIN_KEYS
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"{name} missing join keys: {missing}"
        )

    print(
        f"{name}: join keys OK"
    )


check_keys(team100, "TEAM100")
check_keys(opp100, "OPP100")
check_keys(team_summary, "TEAM SUMMARY")


# ============================================================
# 8. FILTER NBA
# ============================================================

def nba_only(df):

    if df is None:
        return None

    result = df.copy()

    if "lg" in result.columns:

        result = result[
            result["lg"].eq("NBA")
        ].copy()

    return result


team100_nba = nba_only(team100)
opp100_nba = nba_only(opp100)
summary_nba = nba_only(team_summary)


# ============================================================
# 9. CHECK SOURCE COVERAGE
# ============================================================

def source_report(df, name):

    if df is None:
        return

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("Rows:", len(df))

    if "season" in df.columns:

        print(
            "Period:",
            df["season"].min(),
            "→",
            df["season"].max()
        )

        print(
            "Seasons:",
            df["season"].nunique()
        )

    print("Columns:", len(df.columns))


source_report(
    team100_nba,
    "TEAM100 NBA"
)

source_report(
    opp100_nba,
    "OPP100 NBA"
)

source_report(
    summary_nba,
    "TEAM SUMMARY NBA"
)


# ============================================================
# 10. MERGE TEAM + OPPONENT DATA
# ============================================================

if (
    team100_nba is not None
    and opp100_nba is not None
):

    team_advanced = team100_nba.merge(
        opp100_nba,
        on=JOIN_KEYS,
        how="inner",
        validate="one_to_one",
    )

    print(
        "\nTEAM + OPPONENT:",
        team_advanced.shape
    )

else:

    team_advanced = None


# ============================================================
# 11. ADD TEAM SUMMARY
# ============================================================

if (
    team_advanced is not None
    and summary_nba is not None
):

    analysis = team_advanced.merge(
        summary_nba,
        on=JOIN_KEYS,
        how="inner",
        validate="one_to_one",
        suffixes=("", "_summary"),
    )

    print(
        "TEAM + OPPONENT + SUMMARY:",
        analysis.shape
    )

else:

    analysis = None


# ============================================================
# 12. CREATE TARGET VARIABLE
# ============================================================

if analysis is not None:

    if not {"w", "l"}.issubset(analysis.columns):

        raise ValueError(
            "Columns w and l are required "
            "to calculate win_rate."
        )

    analysis["games"] = (
        analysis["w"]
        + analysis["l"]
    )

    analysis["win_rate"] = np.where(
        analysis["games"] > 0,
        analysis["w"] / analysis["games"],
        np.nan,
    )


# ============================================================
# 13. NET RATING
# ============================================================

if analysis is not None:

    if {
        "pts_per_100_poss",
        "opp_pts_per_100_poss",
    }.issubset(analysis.columns):

        analysis["net_rating_calc"] = (
            analysis["pts_per_100_poss"]
            - analysis["opp_pts_per_100_poss"]
        )

    elif {
        "o_rtg",
        "d_rtg",
    }.issubset(analysis.columns):

        analysis["net_rating_calc"] = (
            analysis["o_rtg"]
            - analysis["d_rtg"]
        )


# ============================================================
# 14. WINNING FORMULA FEATURES
# ============================================================

MODEL_FEATURES = [
    "e_fg_percent",
    "tov_percent",
    "orb_percent",
    "drb_percent",
    "ft_fga",
    "opp_e_fg_percent",
    "opp_tov_percent",
    "opp_ft_fga",
]


if analysis is not None:

    missing_features = [
        feature
        for feature in MODEL_FEATURES
        if feature not in analysis.columns
    ]

    if missing_features:

        raise ValueError(
            "Missing Winning Formula features: "
            f"{missing_features}"
        )

    print(
        "\nAll 8 Winning Formula features available."
    )


# ============================================================
# 15. FINAL TEAM-SEASON TABLE
# ============================================================

FINAL_COLUMNS = [
    "season",
    "team",
    "abbreviation",
    "playoffs",
    "w",
    "l",
    "games",
    "win_rate",
    "o_rtg",
    "d_rtg",
    "n_rtg",
    "pace",
    "e_fg_percent",
    "tov_percent",
    "orb_percent",
    "drb_percent",
    "ft_fga",
    "opp_e_fg_percent",
    "opp_tov_percent",
    "opp_ft_fga",
    "pts_per_100_poss",
    "opp_pts_per_100_poss",
    "net_rating_calc",
]


if analysis is not None:

    available_final_columns = [
        col
        for col in FINAL_COLUMNS
        if col in analysis.columns
    ]

    team_season_final = (
        analysis[
            available_final_columns
        ]
        .copy()
        .sort_values(
            ["season", "abbreviation"]
        )
        .reset_index(drop=True)
    )

else:

    team_season_final = pd.DataFrame()


# ============================================================
# 16. DATA QUALITY CHECKS
# ============================================================

if not team_season_final.empty:

    print("\n" + "=" * 70)
    print("DATA QUALITY")
    print("=" * 70)

    duplicate_count = (
        team_season_final
        .duplicated(
            subset=[
                "season",
                "abbreviation",
            ]
        )
        .sum()
    )

    print(
        "Rows:",
        len(team_season_final)
    )

    print(
        "Duplicate season/team keys:",
        duplicate_count
    )

    print(
        "First season:",
        team_season_final["season"].min()
    )

    print(
        "Last season:",
        team_season_final["season"].max()
    )

    print(
        "Unique seasons:",
        team_season_final["season"].nunique()
    )

    print(
        "Missing win_rate:",
        team_season_final["win_rate"]
        .isna()
        .sum()
    )

    if duplicate_count > 0:

        raise ValueError(
            "Duplicate season/team keys detected."
        )


# ============================================================
# 17. MODEL DATA COVERAGE
# ============================================================

if not team_season_final.empty:

    model_ready = (
        team_season_final[
            ["win_rate"] + MODEL_FEATURES
        ]
        .dropna()
    )

    print(
        "\nModel-ready observations:",
        len(model_ready)
    )


# ============================================================
# 18. PREVIEW
# ============================================================

if not team_season_final.empty:

    print("\nPreview:")

    print(
        team_season_final
        .head(10)
        .to_string(index=False)
    )


# ============================================================
# 19. OPTIONAL EXPORT
# ============================================================
#
# The repository's validated final table is:
# data/processed/01_team_season.csv
#
# Uncomment when running locally with the repository structure.
# ============================================================

# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# EXPORT_DIR = PROJECT_ROOT / "data" / "processed"
# EXPORT_DIR.mkdir(parents=True, exist_ok=True)
#
# OUTPUT_FILE = EXPORT_DIR / "01_team_season.csv"
#
# team_season_final.to_csv(
#     OUTPUT_FILE,
#     index=False
# )
#
# print(
#     f"\nExported: {OUTPUT_FILE}"
# )


# ============================================================
# 20. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("TEAM DATA PREPARATION COMPLETE")
print("=" * 70)

print(
    """
RAW TEAM STATS
      +
RAW OPPONENT STATS
      +
TEAM SUMMARY
      ↓
NBA FILTER
      ↓
TEAM-SEASON JOIN
      ↓
WIN RATE
      ↓
ADVANCED FEATURES
      ↓
DATA QUALITY CHECKS
      ↓
01_team_season.csv

Final grain:
1 row = 1 NBA team x 1 season

Next step:
Run 04_build_winning_formula.py
"""
)
