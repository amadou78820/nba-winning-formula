"""
NBA WINNING FORMULA
07 - Build Future GOAT Model

Purpose
-------
Identify current NBA players whose early-career trajectory
most closely resembles historically great players.

IMPORTANT
---------
This model measures TRAJECTORY.

It does NOT predict with certainty who will become
the future GOAT.

Data cutoff:
2023-24

Historical reference players:
- Michael Jordan
- LeBron James
- Kareem Abdul-Jabbar
- Magic Johnson
- Larry Bird

Future GOAT V2 dimensions:
- Production Trajectory
- Efficiency Trajectory
- Recognition Trajectory
- Historical GOAT Similarity

Run after:
06_build_goat_model.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import pairwise_distances


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"

PLAYER_FILE = (
    PROCESSED_DIR
    / "player_season_features.csv"
)

GOAT_SEASONS_FILE = (
    PROCESSED_DIR
    / "07_goat_player_seasons.csv"
)

MVP_FILE = (
    INTERMEDIATE_DIR
    / "player_award_shares.csv"
)

EOS_FILE = (
    INTERMEDIATE_DIR
    / "end_of_season_teams.csv"
)

OUTPUT_FILE = (
    PROCESSED_DIR
    / "09_future_goat.csv"
)

SIMILARITY_FILE = (
    PROCESSED_DIR
    / "10_future_goat_similarity.csv"
)


# ============================================================
# 3. MODEL CONFIGURATION
# ============================================================

DATA_CUTOFF = "2023-24"

MAX_AGE = 27

GOATS = [
    "Michael Jordan",
    "LeBron James",
    "Kareem Abdul-Jabbar",
    "Magic Johnson",
    "Larry Bird",
]

DISPLAY_CANDIDATES = [
    "Luka Dončić",
    "Shai Gilgeous-Alexander",
    "Jayson Tatum",
    "Anthony Edwards",
    "Tyrese Haliburton",
    "Victor Wembanyama",
]


# ============================================================
# 4. LOAD DATA
# ============================================================

print("=" * 70)
print("NBA WINNING FORMULA - FUTURE GOAT")
print("=" * 70)

if not PLAYER_FILE.exists():
    raise FileNotFoundError(
        f"Missing player file: {PLAYER_FILE}"
    )

if not GOAT_SEASONS_FILE.exists():
    raise FileNotFoundError(
        f"Missing GOAT seasons file: {GOAT_SEASONS_FILE}"
    )

players = pd.read_csv(
    PLAYER_FILE
)

goat_seasons = pd.read_csv(
    GOAT_SEASONS_FILE
)

print(
    "\nPlayer seasons:",
    players.shape
)

print(
    "Historical GOAT seasons:",
    goat_seasons.shape
)


# ============================================================
# 5. CURRENT PLAYER SNAPSHOT
# ============================================================
#
# Only players appearing in the 2023-24 season
# and aged 27 or younger are eligible.
# ============================================================

latest = players[
    players["SEASON_ID"]
    == DATA_CUTOFF
].copy()

latest = latest[
    latest["PLAYER_AGE"]
    <= MAX_AGE
].copy()

latest = (
    latest
    .sort_values(
        ["Name", "GP"],
        ascending=[True, False]
    )
    .drop_duplicates(
        subset=["Name"],
        keep="first"
    )
)

print(
    "\nEligible current players:",
    latest["Name"].nunique()
)


# ============================================================
# 6. CANDIDATE CAREER HISTORY
# ============================================================

candidate_names = (
    latest["Name"]
    .dropna()
    .unique()
)

candidate_history = players[
    players["Name"].isin(
        candidate_names
    )
].copy()

candidate_history = candidate_history[
    candidate_history["PLAYER_AGE"]
    <= MAX_AGE
].copy()


# ============================================================
# 7. HISTORICAL GOAT AGE BENCHMARK
# ============================================================
#
# Compare current players with historical GOATs
# at equivalent ages.
# ============================================================

goat_age_benchmark = (
    goat_seasons
    .groupby("PLAYER_AGE")
    .agg(
        goat_avg_production=(
            "PRODUCTION_Z",
            "mean"
        ),

        goat_avg_ts_plus=(
            "TS_PLUS",
            "mean"
        ),

        goat_count=(
            "Name",
            "nunique"
        ),
    )
    .reset_index()
)


# ============================================================
# 8. CURRENT PLAYER TRAJECTORY
# ============================================================

trajectory = (
    candidate_history
    .merge(
        goat_age_benchmark,
        on="PLAYER_AGE",
        how="left",
    )
)

trajectory[
    "production_gap_vs_goat"
] = (
    trajectory["PRODUCTION_Z"]
    -
    trajectory["goat_avg_production"]
)

trajectory[
    "efficiency_gap_vs_goat"
] = (
    trajectory["TS_PLUS"]
    -
    trajectory["goat_avg_ts_plus"]
)


# ============================================================
# 9. LATEST TRAJECTORY SNAPSHOT
# ============================================================

future_model = (
    trajectory[
        trajectory["SEASON_ID"]
        == DATA_CUTOFF
    ]
    .copy()
)

future_model = (
    future_model
    .sort_values(
        ["Name", "GP"],
        ascending=[True, False]
    )
    .drop_duplicates(
        "Name"
    )
)


# ============================================================
# 10. PRODUCTION TRAJECTORY SCORE
# ============================================================
#
# Relative score among eligible current candidates.
# ============================================================

production_scaler = MinMaxScaler(
    feature_range=(0, 100)
)

future_model[
    "Production_Trajectory"
] = production_scaler.fit_transform(
    future_model[
        ["production_gap_vs_goat"]
    ]
)


# ============================================================
# 11. EFFICIENCY TRAJECTORY SCORE
# ============================================================

efficiency_scaler = MinMaxScaler(
    feature_range=(0, 100)
)

future_model[
    "Efficiency_Trajectory"
] = efficiency_scaler.fit_transform(
    future_model[
        ["efficiency_gap_vs_goat"]
    ]
)


# ============================================================
# 12. EARLY-CAREER MVP RECOGNITION
# ============================================================

recognition = pd.DataFrame(
    {
        "Name":
            future_model[
                "Name"
            ].unique()
    }
)

recognition[
    "early_mvp_wins"
] = 0.0

recognition[
    "early_mvp_share"
] = 0.0


if MVP_FILE.exists():

    mvp = pd.read_csv(
        MVP_FILE
    )

    # --------------------------------------------------------
    # IMPORTANT:
    # Keep only awards available by the project cutoff.
    # --------------------------------------------------------

    if "season" in mvp.columns:

        mvp = mvp[
            mvp["season"] <= 2024
        ].copy()

    mvp_candidates = mvp[
        mvp["player"].isin(
            recognition["Name"]
        )
    ].copy()

    if len(mvp_candidates) > 0:

        mvp_summary = (
            mvp_candidates
            .groupby("player")
            .agg(
                early_mvp_wins=(
                    "winner",
                    "sum"
                ),

                early_mvp_share=(
                    "share",
                    "sum"
                ),
            )
            .reset_index()
            .rename(
                columns={
                    "player": "Name"
                }
            )
        )

        recognition = (
            recognition
            .drop(
                columns=[
                    "early_mvp_wins",
                    "early_mvp_share",
                ]
            )
            .merge(
                mvp_summary,
                on="Name",
                how="left",
            )
        )


# ============================================================
# 13. EARLY ALL-NBA RECOGNITION
# ============================================================

recognition[
    "early_all_nba"
] = 0.0

recognition[
    "early_all_nba_1st"
] = 0.0


if EOS_FILE.exists():

    eos = pd.read_csv(
        EOS_FILE
    )

    if "season" in eos.columns:

        eos = eos[
            eos["season"] <= 2024
        ].copy()

    eos = eos[
        eos["player"].isin(
            recognition["Name"]
        )
    ].copy()

    eos = eos[
        eos["type"]
        == "All-NBA"
    ].copy()

    eos[
        "all_nba"
    ] = 1

    eos[
        "all_nba_1st"
    ] = (
        eos["number_tm"]
        .astype(str)
        .str.contains(
            "1",
            na=False
        )
    ).astype(int)

    allnba_summary = (
        eos
        .groupby("player")
        .agg(
            early_all_nba=(
                "all_nba",
                "sum"
            ),

            early_all_nba_1st=(
                "all_nba_1st",
                "sum"
            ),
        )
        .reset_index()
        .rename(
            columns={
                "player": "Name"
            }
        )
    )

    recognition = (
        recognition
        .drop(
            columns=[
                "early_all_nba",
                "early_all_nba_1st",
            ]
        )
        .merge(
            allnba_summary,
            on="Name",
            how="left",
        )
    )


# ============================================================
# 14. FILL MISSING RECOGNITION
# ============================================================

recognition_columns = [
    "early_mvp_wins",
    "early_mvp_share",
    "early_all_nba",
    "early_all_nba_1st",
]

recognition[
    recognition_columns
] = (
    recognition[
        recognition_columns
    ]
    .fillna(0)
)


# ============================================================
# 15. RECOGNITION TRAJECTORY
# ============================================================
#
# Transparent early-career recognition index.
#
# MVP win      = 40 points
# MVP share    = 20 points
# All-NBA      = 5 points
# All-NBA 1st  = 10 points
#
# Final score capped at 100.
# ============================================================

recognition[
    "Recognition_Trajectory"
] = (
      40
      * recognition[
          "early_mvp_wins"
      ]

    + 20
      * recognition[
          "early_mvp_share"
      ]

    + 5
      * recognition[
          "early_all_nba"
      ]

    + 10
      * recognition[
          "early_all_nba_1st"
      ]
).clip(
    0,
    100
)


future_model = (
    future_model
    .merge(
        recognition,
        on="Name",
        how="left",
    )
)


# ============================================================
# 16. HISTORICAL GOAT SIMILARITY
# ============================================================
#
# Compare each current candidate with each GOAT
# at equivalent ages using:
#
# - PRODUCTION_Z
# - TS_PLUS
#
# Distance is calculated after standardization.
# ============================================================

similarity_rows = []


for candidate in future_model["Name"]:

    candidate_data = (
        candidate_history[
            candidate_history["Name"]
            == candidate
        ][
            [
                "PLAYER_AGE",
                "PRODUCTION_Z",
                "TS_PLUS",
            ]
        ]
        .dropna()
    )

    for goat in GOATS:

        goat_data = (
            goat_seasons[
                goat_seasons["Name"]
                == goat
            ][
                [
                    "PLAYER_AGE",
                    "PRODUCTION_Z",
                    "TS_PLUS",
                ]
            ]
            .dropna()
        )

        comparison = (
            candidate_data
            .merge(
                goat_data,
                on="PLAYER_AGE",
                suffixes=(
                    "_candidate",
                    "_goat",
                ),
            )
        )

        if comparison.empty:
            continue

        candidate_matrix = comparison[
            [
                "PRODUCTION_Z_candidate",
                "TS_PLUS_candidate",
            ]
        ].values

        goat_matrix = comparison[
            [
                "PRODUCTION_Z_goat",
                "TS_PLUS_goat",
            ]
        ].values

        combined = np.vstack(
            [
                candidate_matrix,
                goat_matrix,
            ]
        )

        scaler = StandardScaler()

        combined_scaled = (
            scaler.fit_transform(
                combined
            )
        )

        n = len(candidate_matrix)

        candidate_scaled = (
            combined_scaled[:n]
        )

        goat_scaled = (
            combined_scaled[n:]
        )

        distances = np.sqrt(
            np.sum(
                (
                    candidate_scaled
                    - goat_scaled
                ) ** 2,
                axis=1,
            )
        )

        distance = (
            distances.mean()
        )

        similarity = (
            100
            / (1 + distance)
        )

        similarity_rows.append(
            {
                "Name":
                    candidate,

                "AGE":
                    future_model.loc[
                        future_model["Name"]
                        == candidate,
                        "PLAYER_AGE",
                    ].iloc[0],

                "GOAT":
                    goat,

                "Similarity":
                    similarity,

                "Distance":
                    distance,

                "Age_Overlap":
                    len(comparison),
            }
        )


future_similarity = pd.DataFrame(
    similarity_rows
)


# ============================================================
# 17. CLOSEST HISTORICAL GOAT
# ============================================================

closest_goat = (
    future_similarity
    .sort_values(
        [
            "Name",
            "Similarity",
        ],
        ascending=[
            True,
            False,
        ],
    )
    .drop_duplicates(
        "Name"
    )
    .rename(
        columns={
            "GOAT":
                "Closest_GOAT",

            "Similarity":
                "GOAT_Similarity",
        }
    )
)


future_model = (
    future_model
    .merge(
        closest_goat[
            [
                "Name",
                "Closest_GOAT",
                "GOAT_Similarity",
            ]
        ],
        on="Name",
        how="left",
    )
)


# ============================================================
# 18. AGE-ADJUST GOAT SIMILARITY
# ============================================================
#
# Similarity based on only one season is less robust
# than similarity based on several seasons.
#
# We therefore apply a career-observation adjustment.
# ============================================================

career_observations = (
    candidate_history
    .groupby("Name")
    .size()
    .rename(
        "career_observations"
    )
)

future_model = (
    future_model
    .merge(
        career_observations,
        on="Name",
        how="left",
    )
)

future_model[
    "similarity_reliability"
] = np.minimum(
    future_model[
        "career_observations"
    ]
    / 6,
    1,
)

future_model[
    "Adjusted_GOAT_Similarity"
] = (
    future_model[
        "GOAT_Similarity"
    ]
    *
    future_model[
        "similarity_reliability"
    ]
)


# ============================================================
# 19. FUTURE GOAT SCORE V2
# ============================================================
#
# Final validated philosophy:
#
# Production   35%
# Efficiency   25%
# Recognition  25%
# Similarity   15%
# ============================================================

future_model[
    "Future_GOAT_Score_V2"
] = (
      0.35
      * future_model[
          "Production_Trajectory"
      ]

    + 0.25
      * future_model[
          "Efficiency_Trajectory"
      ]

    + 0.25
      * future_model[
          "Recognition_Trajectory"
      ]

    + 0.15
      * future_model[
          "Adjusted_GOAT_Similarity"
      ]
)


# ============================================================
# 20. RANKING
# ============================================================

future_model[
    "Future_GOAT_Rank_V2"
] = (
    future_model[
        "Future_GOAT_Score_V2"
    ]
    .rank(
        ascending=False,
        method="min",
    )
    .astype(int)
)


# ============================================================
# 21. TRAJECTORY TIER
# ============================================================

future_model[
    "Trajectory_Tier"
] = pd.cut(
    future_model[
        "Future_GOAT_Score_V2"
    ],
    bins=[
        -np.inf,
        30,
        50,
        70,
        np.inf,
    ],
    labels=[
        "Developing trajectory",
        "Emerging trajectory",
        "Strong historical trajectory",
        "Elite historical trajectory",
    ],
)


# ============================================================
# 22. FINAL EXPORT TABLE
# ============================================================

future_goat_export = pd.DataFrame(
    {
        "future_goat_rank":
            future_model[
                "Future_GOAT_Rank_V2"
            ],

        "player":
            future_model[
                "Name"
            ],

        "age":
            future_model[
                "PLAYER_AGE"
            ],

        "team":
            future_model[
                "TEAM_ABBREVIATION"
            ],

        "production_z":
            future_model[
                "PRODUCTION_Z"
            ],

        "ts_plus":
            future_model[
                "TS_PLUS"
            ],

        "production_score":
            future_model[
                "Production_Trajectory"
            ],

        "efficiency_score":
            future_model[
                "Efficiency_Trajectory"
            ],

        "recognition_score":
            future_model[
                "Recognition_Trajectory"
            ],

        "closest_goat":
            future_model[
                "Closest_GOAT"
            ],

        "goat_similarity":
            future_model[
                "GOAT_Similarity"
            ],

        "adjusted_goat_similarity":
            future_model[
                "Adjusted_GOAT_Similarity"
            ],

        "future_goat_score":
            future_model[
                "Future_GOAT_Score_V2"
            ],

        "data_cutoff":
            DATA_CUTOFF,

        "model_version":
            "V2",

        "trajectory_tier":
            future_model[
                "Trajectory_Tier"
            ],
    }
)


future_goat_export = (
    future_goat_export
    .sort_values(
        "future_goat_rank"
    )
    .reset_index(drop=True)
)


# ============================================================
# 23. QUALITY CHECKS
# ============================================================

print("\n" + "=" * 70)
print("QUALITY CHECKS")
print("=" * 70)

print(
    "Dimensions:",
    future_goat_export.shape
)

print(
    "Duplicate players:",
    future_goat_export[
        "player"
    ]
    .duplicated()
    .sum()
)

print(
    "Missing scores:",
    future_goat_export[
        "future_goat_score"
    ]
    .isna()
    .sum()
)


# ============================================================
# 24. TOP 20
# ============================================================

print("\n" + "=" * 70)
print("FUTURE GOAT V2 - TOP 20")
print("=" * 70)

print(
    future_goat_export
    .head(20)
    .round(2)
    .to_string(
        index=False
    )
)


# ============================================================
# 25. PRESENTATION CANDIDATES
# ============================================================

presentation = (
    future_goat_export[
        future_goat_export[
            "player"
        ].isin(
            DISPLAY_CANDIDATES
        )
    ]
    .sort_values(
        "future_goat_rank"
    )
)

print("\n" + "=" * 70)
print("6 PRESENTATION CANDIDATES")
print("=" * 70)

print(
    presentation
    .round(2)
    .to_string(
        index=False
    )
)


# ============================================================
# 26. EXPORT
# ============================================================

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

future_goat_export.to_csv(
    OUTPUT_FILE,
    index=False,
)

future_similarity.to_csv(
    SIMILARITY_FILE,
    index=False,
)


print(
    "\nExported:",
    OUTPUT_FILE
)

print(
    "Exported:",
    SIMILARITY_FILE
)


# ============================================================
# 27. MODEL INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("MODEL INTERPRETATION")
print("=" * 70)

print(
    """
The Future GOAT Score measures how historically unusual
a player's trajectory appears at the current data cutoff.

It combines:

35% Production trajectory
25% Efficiency trajectory
25% Early-career recognition
15% Historical GOAT similarity

The model does NOT mean:

"Player X has a 74% probability of becoming the GOAT."

A score of 74 is an analytical trajectory index,
not a probability.

The model should therefore be presented as:

"Who is currently following the strongest
historical GOAT-like trajectory?"
"""
)


# ============================================================
# 28. PIPELINE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FUTURE GOAT MODEL COMPLETE")
print("=" * 70)

print(
    """
CURRENT PLAYERS <= AGE 27
            ↓
2023-24 DATA CUTOFF
            ↓
AGE-MATCHED GOAT BENCHMARK
            ↓
PRODUCTION TRAJECTORY
EFFICIENCY TRAJECTORY
            +
EARLY RECOGNITION
            +
GOAT SIMILARITY
            ↓
RELIABILITY ADJUSTMENT
            ↓
FUTURE GOAT SCORE V2
            ↓
09_future_goat.csv
10_future_goat_similarity.csv

Next step:
Run 08_export_datamart.py
"""
)
