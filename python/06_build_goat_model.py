"""
NBA WINNING FORMULA
06 - Build Historical GOAT Model

Purpose
-------
Build the Historical GOAT analytical framework.

Candidates:
- LeBron James
- Michael Jordan
- Kareem Abdul-Jabbar
- Magic Johnson
- Larry Bird

Main outputs:
03_goat_master.csv
04_goat_dimensions.csv
05_goat_scenarios.csv
06_goat_peak.csv
07_goat_player_seasons.csv
08_methodology.csv

Run after:
05_prepare_player_seasons.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"
RAW_DIR = DATA_DIR / "raw"

PLAYER_SEASONS_FILE = (
    PROCESSED_DIR
    / "player_season_features.csv"
)

MVP_FILE = (
    INTERMEDIATE_DIR
    / "player_award_shares.csv"
)

EOS_FILE = (
    INTERMEDIATE_DIR
    / "end_of_season_teams.csv"
)

PLAYOFF_FILE = (
    INTERMEDIATE_DIR
    / "historical_raptor.csv"
)

CHAMPIONS_FILE = (
    INTERMEDIATE_DIR
    / "nba_champions.csv"
)


# ============================================================
# 3. GOAT CANDIDATES
# ============================================================

GOATS = [
    "LeBron James",
    "Michael Jordan",
    "Kareem Abdul-Jabbar",
    "Magic Johnson",
    "Larry Bird",
]


print("=" * 70)
print("NBA WINNING FORMULA - HISTORICAL GOAT MODEL")
print("=" * 70)


# ============================================================
# 4. LOAD PLAYER-SEASON FEATURES
# ============================================================

if not PLAYER_SEASONS_FILE.exists():

    raise FileNotFoundError(
        f"Missing player-season source: {PLAYER_SEASONS_FILE}"
    )

df_era = pd.read_csv(
    PLAYER_SEASONS_FILE
)

goat_era = df_era[
    df_era["Name"].isin(GOATS)
].copy()

print(
    "\nGOAT player-season rows:",
    len(goat_era)
)


# ============================================================
# 5. CAREER PRODUCTION
# ============================================================

production_summary = (
    goat_era
    .groupby("Name")
    .agg(
        career_production_z=(
            "PRODUCTION_Z",
            "mean"
        ),

        peak_production_z=(
            "PRODUCTION_Z",
            "max"
        ),
    )
)

print("\nProduction summary:")
print(
    production_summary
    .round(3)
)


# ============================================================
# 6. CAREER EFFICIENCY
# ============================================================

efficiency_summary = (
    goat_era
    .groupby("Name")
    .agg(
        career_ts_plus=(
            "TS_PLUS",
            "mean"
        ),

        peak_ts_plus=(
            "TS_PLUS",
            "max"
        ),
    )
)

print("\nEfficiency summary:")
print(
    efficiency_summary
    .round(3)
)


# ============================================================
# 7. LONGEVITY
# ============================================================

longevity_summary = (
    goat_era
    .groupby("Name")
    .agg(
        career_seasons=(
            "SEASON_ID",
            "nunique"
        ),

        career_games=(
            "GP",
            "sum"
        ),

        seasons_25_ppg=(
            "PPG",
            lambda x:
                (x >= 25).sum()
        ),

        elite_seasons=(
            "PRODUCTION_Z",
            lambda x:
                (x >= 1).sum()
        ),

        super_elite_seasons=(
            "PRODUCTION_Z",
            lambda x:
                (x >= 1.5).sum()
        ),

        dominant_seasons=(
            "PRODUCTION_Z",
            lambda x:
                (x >= 2).sum()
        ),
    )
)


# ============================================================
# 8. MVP / AWARDS
# ============================================================

if MVP_FILE.exists():

    df_mvp = pd.read_csv(
        MVP_FILE
    )

    df_mvp = df_mvp[
        df_mvp["player"].isin(GOATS)
    ].copy()

    mvp_summary = (
        df_mvp
        .groupby("player")
        .agg(
            mvp_wins=(
                "winner",
                "sum"
            ),

            total_mvp_share=(
                "share",
                "sum"
            ),

            best_mvp_share=(
                "share",
                "max"
            ),
        )
        .rename_axis("Name")
    )

else:

    print(
        "\nWARNING: MVP file not found."
    )

    mvp_summary = pd.DataFrame(
        index=GOATS
    )


# ============================================================
# 9. ALL-NBA / ALL-DEFENSE
# ============================================================

if EOS_FILE.exists():

    df_eos = pd.read_csv(
        EOS_FILE
    )

    df_eos = df_eos[
        df_eos["player"].isin(GOATS)
    ].copy()

    df_eos["all_nba_1st"] = (
        (df_eos["type"] == "All-NBA")
        &
        (df_eos["number_tm"] == "1st")
    ).astype(int)

    df_eos["all_nba_total"] = (
        df_eos["type"]
        == "All-NBA"
    ).astype(int)

    df_eos["all_def_1st"] = (
        (df_eos["type"] == "All-Defense")
        &
        (df_eos["number_tm"] == "1st")
    ).astype(int)

    df_eos["all_def_total"] = (
        df_eos["type"]
        == "All-Defense"
    ).astype(int)

    eos_summary = (
        df_eos
        .groupby("player")
        .agg(
            all_nba_1st=(
                "all_nba_1st",
                "sum"
            ),

            all_nba_total=(
                "all_nba_total",
                "sum"
            ),

            all_def_1st=(
                "all_def_1st",
                "sum"
            ),

            all_def_total=(
                "all_def_total",
                "sum"
            ),
        )
        .rename_axis("Name")
    )

else:

    print(
        "\nWARNING: EOS file not found."
    )

    eos_summary = pd.DataFrame(
        index=GOATS
    )


# ============================================================
# 10. CHAMPIONSHIPS
# ============================================================

if CHAMPIONS_FILE.exists():

    champions = pd.read_csv(
        CHAMPIONS_FILE
    )

    championships = (
        champions[
            champions["Name"].isin(GOATS)
        ]
        .groupby("Name")
        .size()
        .rename("championships")
        .to_frame()
    )

else:

    print(
        "\nWARNING: championship file not found."
    )

    championships = pd.DataFrame(
        index=GOATS
    )


# ============================================================
# 11. PLAYOFF PERFORMANCE
# ============================================================
#
# Historical RAPTOR source used in the validated project
# covers 1977-2020.
#
# This is acceptable for the Historical GOAT analysis,
# but was NOT reused for Future GOAT.
# ============================================================

if PLAYOFF_FILE.exists():

    df_hist = pd.read_csv(
        PLAYOFF_FILE
    )

    goat_hist = df_hist[
        df_hist["name_common"]
        .isin(GOATS)
    ].copy()

    regular = (
        goat_hist[
            goat_hist["type"] == "RS"
        ]
        .groupby("name_common")
        .agg(
            RS_TS=(
                "TS%",
                "mean"
            ),

            RS_RAPTOR=(
                "Raptor+/-",
                "mean"
            ),
        )
    )

    playoffs = (
        goat_hist[
            goat_hist["type"] == "PO"
        ]
        .groupby("name_common")
        .agg(
            PO_seasons=(
                "year_id",
                "nunique"
            ),

            PO_games=(
                "G",
                "sum"
            ),

            PO_TS=(
                "TS%",
                "mean"
            ),

            PO_RAPTOR=(
                "Raptor+/-",
                "mean"
            ),

            PO_RAPTOR_WAR=(
                "Raptor WAR",
                "sum"
            ),
        )
    )

    playoff_summary = (
        regular
        .join(
            playoffs,
            how="outer"
        )
    )

    playoff_summary[
        "RAPTOR_uplift"
    ] = (
        playoff_summary[
            "PO_RAPTOR"
        ]
        -
        playoff_summary[
            "RS_RAPTOR"
        ]
    )

    playoff_summary[
        "TS_uplift"
    ] = (
        playoff_summary[
            "PO_TS"
        ]
        -
        playoff_summary[
            "RS_TS"
        ]
    )

    playoff_summary.index.name = "Name"

else:

    print(
        "\nWARNING: playoff RAPTOR file not found."
    )

    playoff_summary = pd.DataFrame(
        index=GOATS
    )


# ============================================================
# 12. BUILD MASTER TABLE
# ============================================================

tables = [
    production_summary,
    efficiency_summary,
    mvp_summary,
    eos_summary,
    championships,
    longevity_summary,
    playoff_summary,
]

goat_master = pd.DataFrame(
    index=GOATS
)

for table in tables:

    goat_master = (
        goat_master
        .join(
            table,
            how="left"
        )
    )

goat_master.index.name = "Name"


# ============================================================
# 13. PRODUCTION SCORE V2
# ============================================================
#
# Convert historical Z-scores to percentiles.
#
# Career = 60%
# Peak   = 40%
# ============================================================

production_scores = pd.DataFrame(
    index=goat_master.index
)

production_scores[
    "career"
] = (
    norm.cdf(
        goat_master[
            "career_production_z"
        ]
    )
    * 100
)

production_scores[
    "peak"
] = (
    norm.cdf(
        goat_master[
            "peak_production_z"
        ]
    )
    * 100
)

production_scores[
    "Production"
] = (
      0.60
      * production_scores["career"]

    + 0.40
      * production_scores["peak"]
)


# ============================================================
# 14. EFFICIENCY SCORE V2
# ============================================================

def ts_plus_score(series):
    """
    Convert TS+ benchmark to a 0-100 analytical score.

    100 TS+ = league average
    125 TS+ = historical elite benchmark
    """

    return (
        (series - 100)
        / 25
        * 100
    ).clip(
        0,
        100
    )


efficiency_scores = pd.DataFrame(
    index=goat_master.index
)

efficiency_scores[
    "career"
] = ts_plus_score(
    goat_master[
        "career_ts_plus"
    ]
)

efficiency_scores[
    "peak"
] = ts_plus_score(
    goat_master[
        "peak_ts_plus"
    ]
)

efficiency_scores[
    "Efficiency"
] = (
      0.60
      * efficiency_scores["career"]

    + 0.40
      * efficiency_scores["peak"]
)


# ============================================================
# 15. PLAYOFF SCORE V2
# ============================================================

def playoff_raptor_score(series):

    return (
        series
        / 10
        * 100
    ).clip(
        0,
        100
    )


def raptor_uplift_score(series):

    return (
        (series + 2)
        / 4
        * 100
    ).clip(
        0,
        100
    )


def ts_uplift_score(series):

    return (
        (series + 5)
        / 5
        * 100
    ).clip(
        0,
        100
    )


playoff_scores = pd.DataFrame(
    index=goat_master.index
)

playoff_scores["raptor"] = (
    playoff_raptor_score(
        goat_master[
            "PO_RAPTOR"
        ]
    )
)

playoff_scores[
    "raptor_uplift"
] = (
    raptor_uplift_score(
        goat_master[
            "RAPTOR_uplift"
        ]
    )
)

playoff_scores[
    "ts_uplift"
] = (
    ts_uplift_score(
        goat_master[
            "TS_uplift"
        ]
    )
)

playoff_scores["Playoffs"] = (
      0.50
      * playoff_scores["raptor"]

    + 0.30
      * playoff_scores[
          "raptor_uplift"
      ]

    + 0.20
      * playoff_scores[
          "ts_uplift"
      ]
)


# ============================================================
# 16. INDIVIDUAL SUCCESS SCORE
# ============================================================

individual_scores = pd.DataFrame(
    index=goat_master.index
)

individual_scores[
    "mvp_score"
] = (
    goat_master["mvp_wins"]
    / 6
    * 100
).clip(
    0,
    100
)

individual_scores[
    "mvp_share_score"
] = (
    goat_master[
        "total_mvp_share"
    ]
    / 9
    * 100
).clip(
    0,
    100
)

individual_scores[
    "all_nba_1st_score"
] = (
    goat_master[
        "all_nba_1st"
    ]
    / 13
    * 100
).clip(
    0,
    100
)

individual_scores[
    "all_nba_total_score"
] = (
    goat_master[
        "all_nba_total"
    ]
    / 21
    * 100
).clip(
    0,
    100
)

individual_scores[
    "all_def_1st_score"
] = (
    goat_master[
        "all_def_1st"
    ]
    / 9
    * 100
).clip(
    0,
    100
)

individual_scores[
    "all_def_total_score"
] = (
    goat_master[
        "all_def_total"
    ]
    / 11
    * 100
).clip(
    0,
    100
)


individual_scores[
    "Individual"
] = (
      0.30
      * individual_scores[
          "mvp_score"
      ]

    + 0.20
      * individual_scores[
          "mvp_share_score"
      ]

    + 0.20
      * individual_scores[
          "all_nba_1st_score"
      ]

    + 0.10
      * individual_scores[
          "all_nba_total_score"
      ]

    + 0.10
      * individual_scores[
          "all_def_1st_score"
      ]

    + 0.10
      * individual_scores[
          "all_def_total_score"
      ]
)


# ============================================================
# 17. TEAM SUCCESS SCORE
# ============================================================

team_success_score = (
    goat_master[
        "championships"
    ]
    / 6
    * 100
).clip(
    0,
    100
)


# ============================================================
# 18. LONGEVITY SCORE
# ============================================================

career_seasons_score = (
    goat_master[
        "career_seasons"
    ]
    / 21
    * 100
).clip(
    0,
    100
)

career_games_score = (
    goat_master[
        "career_games"
    ]
    / 1560
    * 100
).clip(
    0,
    100
)

elite_seasons_score = (
    goat_master[
        "elite_seasons"
    ]
    / 21
    * 100
).clip(
    0,
    100
)

longevity_score = (
      0.40
      * career_seasons_score

    + 0.30
      * career_games_score

    + 0.30
      * elite_seasons_score
)


# ============================================================
# 19. SIX DIMENSIONS
# ============================================================

dimension_scores = pd.DataFrame(
    {
        "Production":
            production_scores[
                "Production"
            ],

        "Efficiency":
            efficiency_scores[
                "Efficiency"
            ],

        "Playoffs":
            playoff_scores[
                "Playoffs"
            ],

        "Individual":
            individual_scores[
                "Individual"
            ],

        "Team Success":
            team_success_score,

        "Longevity":
            longevity_score,
    }
)


print("\nSix GOAT dimensions:")

print(
    dimension_scores
    .round(1)
)


# ============================================================
# 20. BALANCED GOAT SCORE
# ============================================================

dimension_scores[
    "Balanced"
] = (
      0.20
      * dimension_scores[
          "Production"
      ]

    + 0.15
      * dimension_scores[
          "Efficiency"
      ]

    + 0.20
      * dimension_scores[
          "Playoffs"
      ]

    + 0.20
      * dimension_scores[
          "Individual"
      ]

    + 0.10
      * dimension_scores[
          "Team Success"
      ]

    + 0.15
      * dimension_scores[
          "Longevity"
      ]
)


# ============================================================
# 21. SCENARIOS
# ============================================================

SCENARIOS = {

    "Balanced": {
        "Production": 0.20,
        "Efficiency": 0.15,
        "Playoffs": 0.20,
        "Individual": 0.20,
        "Team Success": 0.10,
        "Longevity": 0.15,
    },

    "Peak": {
        "Production": 0.30,
        "Efficiency": 0.15,
        "Playoffs": 0.30,
        "Individual": 0.15,
        "Team Success": 0.05,
        "Longevity": 0.05,
    },

    "Longevity": {
        "Production": 0.15,
        "Efficiency": 0.10,
        "Playoffs": 0.15,
        "Individual": 0.15,
        "Team Success": 0.05,
        "Longevity": 0.40,
    },

    "Winning": {
        "Production": 0.10,
        "Efficiency": 0.10,
        "Playoffs": 0.30,
        "Individual": 0.15,
        "Team Success": 0.25,
        "Longevity": 0.10,
    },

    "Individual Dominance": {
        "Production": 0.25,
        "Efficiency": 0.10,
        "Playoffs": 0.15,
        "Individual": 0.35,
        "Team Success": 0.05,
        "Longevity": 0.10,
    },
}


scenario_scores = pd.DataFrame(
    index=dimension_scores.index
)

for scenario, weights in SCENARIOS.items():

    scenario_scores[
        scenario
    ] = sum(
        dimension_scores[
            dimension
        ]
        * weight

        for dimension, weight
        in weights.items()
    )


# ============================================================
# 22. TRUE PEAK
# ============================================================

peak_production = (
    norm.cdf(
        goat_master[
            "peak_production_z"
        ]
    )
    * 100
)

peak_efficiency = (
    ts_plus_score(
        goat_master[
            "peak_ts_plus"
        ]
    )
)

peak_mvp = (
    goat_master[
        "best_mvp_share"
    ]
    * 100
).clip(
    0,
    100
)

true_peak = pd.DataFrame(
    {
        "Peak Production":
            peak_production,

        "Peak Efficiency":
            peak_efficiency,

        "Playoffs":
            playoff_scores[
                "Playoffs"
            ],

        "Peak MVP":
            peak_mvp,
    }
)

true_peak[
    "True Peak Score"
] = (
      0.30
      * true_peak[
          "Peak Production"
      ]

    + 0.20
      * true_peak[
          "Peak Efficiency"
      ]

    + 0.30
      * true_peak[
          "Playoffs"
      ]

    + 0.20
      * true_peak[
          "Peak MVP"
      ]
)


true_peak[
    "Peak Rank"
] = (
    true_peak[
        "True Peak Score"
    ]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)


# ============================================================
# 23. GOAT PLAYER SEASONS EXPORT
# ============================================================

goat_player_seasons = (
    goat_era[
        [
            "Name",
            "PLAYER_ID",
            "SEASON_ID",
            "TEAM_ABBREVIATION",
            "PLAYER_AGE",
            "GP",
            "PPG",
            "RPG",
            "APG",
            "PPG_Z",
            "RPG_Z",
            "APG_Z",
            "PRODUCTION_Z",
            "TS_PCT",
            "TS_PLUS",
            "TS_Z",
        ]
    ]
    .copy()
)


# ============================================================
# 24. METHODOLOGY TABLE
# ============================================================

methodology = pd.DataFrame(
    [
        {
            "dimension":
                "Production",

            "weight_balanced":
                0.20,

            "metrics":
                "Career Production Z; Peak Production Z",

            "method":
                "Era-adjusted Z-scores",

            "purpose":
                "Measure statistical dominance relative to each NBA era",
        },

        {
            "dimension":
                "Efficiency",

            "weight_balanced":
                0.15,

            "metrics":
                "Career TS+; Peak TS+",

            "method":
                "True Shooting relative to league environment",

            "purpose":
                "Measure scoring efficiency adjusted for era",
        },

        {
            "dimension":
                "Playoffs",

            "weight_balanced":
                0.20,

            "metrics":
                "PO RAPTOR; RAPTOR Uplift; TS Uplift",

            "method":
                "Regular Season vs Playoffs",

            "purpose":
                "Measure postseason impact and performance retention",
        },

        {
            "dimension":
                "Individual Success",

            "weight_balanced":
                0.20,

            "metrics":
                "MVP; MVP Share; All-NBA; All-Defense",

            "method":
                "Benchmark normalization",

            "purpose":
                "Measure individual recognition and sustained elite status",
        },

        {
            "dimension":
                "Team Success",

            "weight_balanced":
                0.10,

            "metrics":
                "NBA Championships",

            "method":
                "Historical championship benchmark",

            "purpose":
                "Measure collective success context",
        },

        {
            "dimension":
                "Longevity",

            "weight_balanced":
                0.15,

            "metrics":
                "Career Seasons; Games; Elite Seasons",

            "method":
                "Career longevity benchmarks",

            "purpose":
                "Measure sustained elite performance over time",
        },
    ]
)


# ============================================================
# 25. EXPORTS
# ============================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

goat_master.reset_index().to_csv(
    PROCESSED_DIR
    / "03_goat_master.csv",
    index=False,
)

dimension_scores[
    [
        "Production",
        "Efficiency",
        "Playoffs",
        "Individual",
        "Team Success",
        "Longevity",
    ]
].reset_index().to_csv(
    PROCESSED_DIR
    / "04_goat_dimensions.csv",
    index=False,
)

scenario_scores.reset_index().to_csv(
    PROCESSED_DIR
    / "05_goat_scenarios.csv",
    index=False,
)

true_peak.reset_index().to_csv(
    PROCESSED_DIR
    / "06_goat_peak.csv",
    index=False,
)

goat_player_seasons.to_csv(
    PROCESSED_DIR
    / "07_goat_player_seasons.csv",
    index=False,
)

methodology.to_csv(
    PROCESSED_DIR
    / "08_methodology.csv",
    index=False,
)


# ============================================================
# 26. RESULTS
# ============================================================

print("\n" + "=" * 70)
print("BALANCED GOAT")
print("=" * 70)

print(
    dimension_scores[
        "Balanced"
    ]
    .sort_values(
        ascending=False
    )
    .round(1)
)


print("\n" + "=" * 70)
print("SCENARIO WINNERS")
print("=" * 70)

for scenario in scenario_scores.columns:

    print(
        scenario,
        "→",
        scenario_scores[
            scenario
        ].idxmax(),
        round(
            scenario_scores[
                scenario
            ].max(),
            1,
        ),
    )


print("\n" + "=" * 70)
print("TRUE PEAK")
print("=" * 70)

print(
    true_peak[
        [
            "True Peak Score",
            "Peak Rank",
        ]
    ]
    .sort_values(
        "Peak Rank"
    )
    .round(1)
)


# ============================================================
# 27. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("HISTORICAL GOAT MODEL COMPLETE")
print("=" * 70)

print(
    """
PLAYER-SEASON FEATURES
        ↓
PRODUCTION
EFFICIENCY
PLAYOFFS
INDIVIDUAL SUCCESS
TEAM SUCCESS
LONGEVITY
        ↓
6 GOAT DIMENSIONS
        ↓
BALANCED SCORE
        ↓
SCENARIO ANALYSIS
        ↓
TRUE PEAK
        ↓
03-08 PROCESSED DATASETS

Important:
The GOAT score is a transparent multi-criteria model.

It is not an objective universal truth.

Its results depend on the documented metrics,
benchmarks and weights.

Next step:
Run 07_build_future_goat.py
"""
)
