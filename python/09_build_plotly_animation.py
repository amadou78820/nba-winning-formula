"""
NBA WINNING FORMULA
09 - Build Plotly Career Trajectory Animation

Purpose
-------
Create the interactive Future GOAT career trajectory animation.

The animation compares:

Historical GOATs
- Michael Jordan
- LeBron James
- Kareem Abdul-Jabbar
- Magic Johnson
- Larry Bird

Future GOAT Candidates
- Luka Doncic
- Shai Gilgeous-Alexander
- Jayson Tatum
- Anthony Edwards
- Victor Wembanyama
- Tyrese Haliburton

Metric:
Era-adjusted Production Z-score

Comparison:
Players are compared at equivalent ages.

Output:
animations/future-goat-trajectory-premium.html

Run after:
08_export_datamart.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path

import pandas as pd
import plotly.express as px


# ============================================================
# 2. PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

ANIMATION_DIR = (
    PROJECT_ROOT
    / "animations"
)

PLAYER_SEASONS_FILE = (
    PROCESSED_DIR
    / "player_season_features.csv"
)

OUTPUT_HTML = (
    ANIMATION_DIR
    / "future-goat-trajectory-premium.html"
)


# ============================================================
# 3. CONFIGURATION
# ============================================================

HISTORICAL_GOATS = [
    "Michael Jordan",
    "LeBron James",
    "Kareem Abdul-Jabbar",
    "Magic Johnson",
    "Larry Bird",
]

FUTURE_CANDIDATES = [
    "Luka Dončić",
    "Shai Gilgeous-Alexander",
    "Jayson Tatum",
    "Anthony Edwards",
    "Victor Wembanyama",
    "Tyrese Haliburton",
]

MIN_AGE = 20
MAX_AGE = 30


# ============================================================
# 4. LOAD PLAYER-SEASON FEATURES
# ============================================================

if not PLAYER_SEASONS_FILE.exists():

    raise FileNotFoundError(
        f"Missing player-season file: {PLAYER_SEASONS_FILE}"
    )

df = pd.read_csv(
    PLAYER_SEASONS_FILE
)

print("=" * 70)
print("NBA WINNING FORMULA - PLOTLY ANIMATION")
print("=" * 70)

print(
    "\nInput:",
    PLAYER_SEASONS_FILE
)

print(
    "Shape:",
    df.shape
)


# ============================================================
# 5. REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Name",
    "SEASON_ID",
    "PLAYER_AGE",
    "TEAM_ABBREVIATION",
    "GP",
    "PPG",
    "RPG",
    "APG",
    "PRODUCTION_Z",
    "TS_PLUS",
]

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:

    raise ValueError(
        f"Missing required columns: {missing}"
    )


# ============================================================
# 6. BUILD FUTURE CANDIDATE TRAJECTORIES
# ============================================================

candidate_trajectory = (
    df[
        df["Name"]
        .isin(
            FUTURE_CANDIDATES
        )
    ][
        required_columns
    ]
    .copy()
)

candidate_trajectory[
    "group"
] = "Future GOAT Candidate"


# ============================================================
# 7. BUILD HISTORICAL GOAT TRAJECTORIES
# ============================================================

goat_trajectory = (
    df[
        df["Name"]
        .isin(
            HISTORICAL_GOATS
        )
    ][
        required_columns
    ]
    .copy()
)

goat_trajectory[
    "group"
] = "Historical GOAT"


# ============================================================
# 8. AGE FILTER
# ============================================================

candidate_trajectory = (
    candidate_trajectory[
        candidate_trajectory[
            "PLAYER_AGE"
        ].between(
            MIN_AGE,
            MAX_AGE
        )
    ]
    .copy()
)

goat_trajectory = (
    goat_trajectory[
        goat_trajectory[
            "PLAYER_AGE"
        ].between(
            MIN_AGE,
            MAX_AGE
        )
    ]
    .copy()
)


# ============================================================
# 9. COMBINE TRAJECTORIES
# ============================================================

career_trajectory = pd.concat(
    [
        goat_trajectory,
        candidate_trajectory,
    ],
    ignore_index=True,
)

career_trajectory = (
    career_trajectory
    .sort_values(
        [
            "PLAYER_AGE",
            "group",
            "Name",
        ]
    )
    .reset_index(
        drop=True
    )
)


print("\n" + "=" * 70)
print("CAREER TRAJECTORY")
print("=" * 70)

print(
    "Rows:",
    len(
        career_trajectory
    )
)

print(
    "Players:",
    career_trajectory[
        "Name"
    ].nunique()
)

print("\nPopulation:")

print(
    career_trajectory
    .groupby(
        "group"
    )["Name"]
    .nunique()
)


# ============================================================
# 10. COVERAGE CHECK
# ============================================================

coverage = (
    career_trajectory
    .groupby(
        [
            "group",
            "Name",
        ]
    )
    .agg(
        seasons=(
            "SEASON_ID",
            "nunique"
        ),

        first_age=(
            "PLAYER_AGE",
            "min"
        ),

        last_age=(
            "PLAYER_AGE",
            "max"
        ),

        latest_production_z=(
            "PRODUCTION_Z",
            "last"
        ),
    )
)


print("\n" + "=" * 70)
print("PLAYER COVERAGE")
print("=" * 70)

print(
    coverage
    .round(2)
    .to_string()
)


# ============================================================
# 11. BUILD ANIMATION FRAMES
# ============================================================
#
# At each age:
# retain every observation already reached.
#
# This creates career lines that progressively grow.
# ============================================================

frames = []

for current_age in range(
    MIN_AGE,
    MAX_AGE + 1,
):

    temp = career_trajectory[
        career_trajectory[
            "PLAYER_AGE"
        ]
        <= current_age
    ].copy()

    temp[
        "animation_age"
    ] = current_age

    frames.append(
        temp
    )


career_animation = pd.concat(
    frames,
    ignore_index=True,
)


# ============================================================
# 12. FRAME VALIDATION
# ============================================================

final_frame = (
    career_animation[
        career_animation[
            "animation_age"
        ]
        == MAX_AGE
    ]
)

final_players = (
    final_frame[
        "Name"
    ]
    .nunique()
)


print("\n" + "=" * 70)
print("ANIMATION CHECK")
print("=" * 70)

print(
    "Final frame players:",
    final_players
)

expected_players = (
    len(HISTORICAL_GOATS)
    +
    len(FUTURE_CANDIDATES)
)

print(
    "Expected players:",
    expected_players
)


if final_players != expected_players:

    print(
        "\nWARNING:"
        " Some configured players "
        "are missing from the final frame."
    )


# ============================================================
# 13. PLAYER TYPE LABEL
# ============================================================

career_animation[
    "player_type"
] = (
    career_animation[
        "group"
    ]
    .map(
        {
            "Historical GOAT":
                "NBA Legend",

            "Future GOAT Candidate":
                "Future GOAT Candidate",
        }
    )
)


# ============================================================
# 14. PLOTLY ANIMATION
# ============================================================

y_min = (
    career_trajectory[
        "PRODUCTION_Z"
    ].min()
    - 0.4
)

y_max = (
    career_trajectory[
        "PRODUCTION_Z"
    ].max()
    + 0.5
)


fig = px.line(
    career_animation,

    x="PLAYER_AGE",
    y="PRODUCTION_Z",

    color="Name",

    line_dash="player_type",

    animation_frame="animation_age",

    markers=True,

    hover_name="Name",

    hover_data={
        "SEASON_ID":
            True,

        "TEAM_ABBREVIATION":
            True,

        "PLAYER_AGE":
            True,

        "PPG":
            ":.1f",

        "RPG":
            ":.1f",

        "APG":
            ":.1f",

        "TS_PLUS":
            ":.1f",

        "PRODUCTION_Z":
            ":.2f",

        "player_type":
            True,

        "animation_age":
            False,
    },

    title=(
        "<b>FUTURE GOAT RACE</b>"
        "<br>"
        "<sup>"
        "How today's stars compare with NBA legends "
        "at equivalent ages"
        "</sup>"
    ),

    labels={
        "PLAYER_AGE":
            "Age",

        "PRODUCTION_Z":
            "Era-Adjusted Production Z",

        "SEASON_ID":
            "Season",

        "TEAM_ABBREVIATION":
            "Team",

        "PPG":
            "Points / Game",

        "RPG":
            "Rebounds / Game",

        "APG":
            "Assists / Game",

        "TS_PLUS":
            "TS+",

        "player_type":
            "Profile",

        "animation_age":
            "Age reached",
    },

    range_x=[
        MIN_AGE - 0.5,
        MAX_AGE + 0.5,
    ],

    range_y=[
        y_min,
        y_max,
    ],
)


# ============================================================
# 15. VISUAL SETTINGS
# ============================================================

fig.update_traces(
    line=dict(
        width=3
    ),

    marker=dict(
        size=9
    ),
)


fig.update_layout(

    height=760,

    title=dict(
        x=0.03,
        xanchor="left",
        font=dict(
            size=25
        ),
    ),

    xaxis=dict(
        dtick=1,
        title="PLAYER AGE",
    ),

    yaxis=dict(
        title=(
            "ERA-ADJUSTED "
            "PRODUCTION"
        ),
    ),

    legend=dict(
        title="PLAYER",
        orientation="v",
        x=1.02,
        y=1,
    ),

    margin=dict(
        l=80,
        r=230,
        t=110,
        b=80,
    ),

    hovermode="closest",
)


# ============================================================
# 16. DISPLAY
# ============================================================

fig.show()


# ============================================================
# 17. EXPORT HTML
# ============================================================

ANIMATION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

fig.write_html(

    OUTPUT_HTML,

    include_plotlyjs="cdn",

    full_html=True,

    config={
        "displayModeBar":
            False,

        "responsive":
            True,
    },
)


print("\n" + "=" * 70)
print("HTML EXPORT")
print("=" * 70)

print(
    "Exported:",
    OUTPUT_HTML
)


# ============================================================
# 18. GITHUB PAGES URL
# ============================================================

print("\nPublic URL after GitHub Pages deployment:")

print(
    "https://amadou78820.github.io/"
    "nba-winning-formula/"
    "animations/"
    "future-goat-trajectory-premium.html"
)


# ============================================================
# 19. INTERPRETATION
# ============================================================

print("\n" + "=" * 70)
print("HOW TO READ THE CHART")
print("=" * 70)

print(
    """
X-axis:
Player age.

Y-axis:
Era-adjusted Production Z-score.

Higher values indicate stronger production relative
to the statistical environment of that player's era.

Historical players and current candidates are compared
at equivalent ages.

The chart shows OBSERVED career trajectories only.

It does not extrapolate future seasons.

For example:
Victor Wembanyama's curve stops at age 20 because
the project data cutoff is the end of 2023-24.
"""
)


# ============================================================
# 20. PIPELINE COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("PYTHON PIPELINE COMPLETE")
print("=" * 70)

print(
    """
01_download_data.py
        ↓
02_inspect_sources.py
        ↓
03_prepare_team_data.py
        ↓
04_build_winning_formula.py
        ↓
05_prepare_player_seasons.py
        ↓
06_build_goat_model.py
        ↓
07_build_future_goat.py
        ↓
08_export_datamart.py
        ↓
09_build_plotly_animation.py
        ↓
BIGQUERY + LOOKER STUDIO + GITHUB PAGES
"""
)
