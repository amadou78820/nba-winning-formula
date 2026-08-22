"""
NBA WINNING FORMULA
02 - Inspect Data Sources

Purpose
-------
Explore and document the raw NBA dataset before transformation.

This script:
1. Opens the SQLite database.
2. Lists all available tables.
3. Inspects table dimensions.
4. Displays schemas and sample rows.
5. Checks season coverage.
6. Identifies the main tables used by the project.

Run after:
01_download_data.py
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path
import sqlite3
import pandas as pd
import kagglehub


# ============================================================
# 2. DATASET CONFIGURATION
# ============================================================

KAGGLE_DATASET = "wyattowalsh/basketball"
KAGGLE_VERSION = 238

dataset_path = kagglehub.dataset_download(
    f"{KAGGLE_DATASET}/versions/{KAGGLE_VERSION}"
)

DATASET_DIR = Path(dataset_path)

NBA_SQLITE = DATASET_DIR / "nba.sqlite"
CSV_DIR = DATASET_DIR / "csv"

print("=" * 70)
print("NBA WINNING FORMULA - SOURCE INSPECTION")
print("=" * 70)

print("\nDataset directory:")
print(DATASET_DIR)

print("\nSQLite database:")
print(NBA_SQLITE)


# ============================================================
# 3. CONNECT TO SQLITE
# ============================================================

if not NBA_SQLITE.exists():
    raise FileNotFoundError(
        f"SQLite database not found: {NBA_SQLITE}"
    )

conn = sqlite3.connect(NBA_SQLITE)

print("\nSQLite connection established.")


# ============================================================
# 4. LIST AVAILABLE TABLES
# ============================================================

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
    """,
    conn
)

print("\n" + "=" * 70)
print("AVAILABLE SQLITE TABLES")
print("=" * 70)

print(tables.to_string(index=False))

print(
    "\nNumber of tables:",
    len(tables)
)


# ============================================================
# 5. TABLE DIMENSIONS
# ============================================================

print("\n" + "=" * 70)
print("TABLE DIMENSIONS")
print("=" * 70)

table_summary = []

for table_name in tables["name"]:

    try:

        row_count = pd.read_sql_query(
            f'SELECT COUNT(*) AS n FROM "{table_name}"',
            conn
        )["n"].iloc[0]

        columns = pd.read_sql_query(
            f'PRAGMA table_info("{table_name}")',
            conn
        )

        table_summary.append(
            {
                "table": table_name,
                "rows": row_count,
                "columns": len(columns),
            }
        )

    except Exception as error:

        print(
            f"Could not inspect {table_name}: {error}"
        )


table_summary = pd.DataFrame(table_summary)

if not table_summary.empty:

    table_summary = table_summary.sort_values(
        "rows",
        ascending=False
    )

    print(
        table_summary.to_string(
            index=False
        )
    )


# ============================================================
# 6. HELPER FUNCTION
# ============================================================

def inspect_table(table_name, sample_size=5):
    """
    Display basic information about a SQLite table.
    """

    print("\n" + "=" * 70)
    print(table_name.upper())
    print("=" * 70)

    if table_name not in tables["name"].values:
        print("Table not found.")
        return

    schema = pd.read_sql_query(
        f'PRAGMA table_info("{table_name}")',
        conn
    )

    print("\nColumns:")

    for column in schema["name"]:
        print(" -", column)

    row_count = pd.read_sql_query(
        f'SELECT COUNT(*) AS n FROM "{table_name}"',
        conn
    )["n"].iloc[0]

    print("\nRows:", row_count)

    sample = pd.read_sql_query(
        f'SELECT * FROM "{table_name}" LIMIT {sample_size}',
        conn
    )

    print("\nSample:")
    print(sample.to_string(index=False))


# ============================================================
# 7. INSPECT IMPORTANT SQLITE TABLES
# ============================================================

# These were among the important sources identified
# during the exploratory phase of the project.

important_tables = [
    "game",
    "player",
]

for table_name in important_tables:

    inspect_table(table_name)


# ============================================================
# 8. INSPECT CSV DIRECTORY
# ============================================================

print("\n" + "=" * 70)
print("CSV SOURCES")
print("=" * 70)

csv_files = sorted(
    CSV_DIR.rglob("*.csv")
) if CSV_DIR.exists() else []

print(
    "\nCSV files detected:",
    len(csv_files)
)

for path in csv_files:

    size_mb = path.stat().st_size / (1024 ** 2)

    print(
        f"{path.relative_to(DATASET_DIR)}"
        f" -> {size_mb:.2f} MB"
    )


# ============================================================
# 9. SEARCH FOR PROJECT-RELEVANT FILES
# ============================================================

keywords = [
    "game",
    "player",
    "team",
    "award",
    "mvp",
    "season",
    "advanced",
    "per_100",
    "opponent",
    "summary",
]

relevant_files = []

for path in csv_files:

    filename = path.name.lower()

    if any(
        keyword in filename
        for keyword in keywords
    ):

        relevant_files.append(path)


print("\n" + "=" * 70)
print("PROJECT-RELEVANT FILES")
print("=" * 70)

for path in relevant_files:
    print(path.relative_to(DATASET_DIR))


# ============================================================
# 10. INSPECT GAME DATA
# ============================================================

GAME_CSV = CSV_DIR / "game.csv"

if GAME_CSV.exists():

    print("\n" + "=" * 70)
    print("GAME DATA")
    print("=" * 70)

    df_game_sample = pd.read_csv(
        GAME_CSV,
        nrows=5
    )

    print("\nColumns:")

    for column in df_game_sample.columns:
        print(" -", column)

    print(
        "\nNumber of columns:",
        len(df_game_sample.columns)
    )

    print("\nSample:")
    print(
        df_game_sample.head().to_string()
    )

else:

    print(
        "\ngame.csv was not found at:",
        GAME_CSV
    )


# ============================================================
# 11. SEARCH CSV SCHEMAS
# ============================================================

print("\n" + "=" * 70)
print("CSV SCHEMA SEARCH")
print("=" * 70)

schema_summary = []

for path in relevant_files:

    try:

        sample = pd.read_csv(
            path,
            nrows=3
        )

        schema_summary.append(
            {
                "file": str(
                    path.relative_to(DATASET_DIR)
                ),
                "columns": len(sample.columns),
                "column_names": ", ".join(
                    sample.columns.astype(str)
                ),
            }
        )

    except Exception as error:

        print(
            f"Could not inspect {path.name}: {error}"
        )


schema_summary = pd.DataFrame(schema_summary)

if not schema_summary.empty:

    pd.set_option(
        "display.max_colwidth",
        200
    )

    print(
        schema_summary[
            ["file", "columns"]
        ].to_string(index=False)
    )


# ============================================================
# 12. PROJECT SOURCE MAP
# ============================================================

print("\n" + "=" * 70)
print("PROJECT SOURCE MAP")
print("=" * 70)

source_map = {
    "Winning Formula":
        "Team and game-level historical data",

    "GOAT Production":
        "Player season statistics",

    "GOAT Efficiency":
        "Player statistics + league context",

    "GOAT Playoffs":
        "Historical regular season / playoff data",

    "Individual Success":
        "MVP and end-of-season award data",

    "Team Success":
        "Historical championship results",

    "Longevity":
        "Player-season career histories",

    "Future GOAT":
        "Player seasons + awards + historical GOAT benchmarks",
}

for analysis, source in source_map.items():

    print(
        f"{analysis:<25} -> {source}"
    )


# ============================================================
# 13. PROJECT GRAIN
# ============================================================

print("\n" + "=" * 70)
print("ANALYTICAL GRAINS")
print("=" * 70)

print(
    """
Winning Formula
---------------
1 row = 1 NBA team × 1 season

Historical GOAT Master
----------------------
1 row = 1 historical GOAT candidate

GOAT Player Seasons
-------------------
1 row = 1 player × 1 season

Future GOAT
-----------
1 row = 1 current NBA candidate

Future GOAT Similarity
----------------------
1 row = 1 current player × 1 historical GOAT
"""
)


# ============================================================
# 14. DATA VOLUME PRINCIPLE
# ============================================================

print("\n" + "=" * 70)
print("DATA VOLUME PRINCIPLE")
print("=" * 70)

print(
    """
Only load the tables required by the analytical question.

The complete play-by-play dataset is optional because it
contains millions of events and is not required for the
core Winning Formula or GOAT analyses.

This keeps the project:
- easier to reproduce,
- faster to process,
- easier to explain,
- compatible with the project data-volume constraints.
"""
)


# ============================================================
# 15. CLOSE CONNECTION
# ============================================================

conn.close()

print("\nSQLite connection closed.")


# ============================================================
# 16. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SOURCE INSPECTION COMPLETE")
print("=" * 70)

print(
    """
Raw data inspected successfully.

Main analytical levels identified:

GAME LEVEL
      ↓
TEAM × SEASON
      ↓
WINNING FORMULA


PLAYER DATA
      ↓
PLAYER × SEASON
      ↓
ERA ADJUSTMENT
      ↓
HISTORICAL GOAT
      ↓
FUTURE GOAT


Next step:
Run 03_prepare_team_data.py
"""
)
