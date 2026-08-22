"""
NBA WINNING FORMULA
01 - Download Data

Purpose
-------
Download and locate the source datasets used in the project.

This script:
1. Downloads the main NBA dataset from Kaggle.
2. Lists the files available in the downloaded dataset.
3. Detects SQLite, DuckDB and CSV sources.
4. Stores useful paths for the next scripts.

The script does NOT perform analytical transformations.
"""

# ============================================================
# 1. IMPORTS
# ============================================================

from pathlib import Path
import os

import kagglehub


# ============================================================
# 2. PROJECT CONFIGURATION
# ============================================================

KAGGLE_DATASET = "wyattowalsh/basketball"
KAGGLE_VERSION = 238

print("=" * 70)
print("NBA WINNING FORMULA - DATA DOWNLOAD")
print("=" * 70)

print(f"\nDataset : {KAGGLE_DATASET}")
print(f"Version : {KAGGLE_VERSION}")


# ============================================================
# 3. DOWNLOAD MAIN NBA DATASET
# ============================================================

dataset_path = kagglehub.dataset_download(
    f"{KAGGLE_DATASET}/versions/{KAGGLE_VERSION}"
)

DATASET_DIR = Path(dataset_path)

print("\nDataset downloaded.")
print("Dataset directory:")
print(DATASET_DIR)


# ============================================================
# 4. VERIFY DIRECTORY
# ============================================================

if not DATASET_DIR.exists():
    raise FileNotFoundError(
        f"Dataset directory not found: {DATASET_DIR}"
    )

print("\nDirectory exists:", DATASET_DIR.exists())


# ============================================================
# 5. LIST ALL FILES
# ============================================================

print("\n" + "=" * 70)
print("AVAILABLE FILES")
print("=" * 70)

all_files = sorted(
    [
        path
        for path in DATASET_DIR.rglob("*")
        if path.is_file()
    ]
)

for file_path in all_files:
    size_mb = file_path.stat().st_size / (1024 ** 2)

    print(
        f"{file_path.relative_to(DATASET_DIR)}"
        f" -> {size_mb:.2f} MB"
    )

print(
    "\nTotal files:",
    len(all_files)
)


# ============================================================
# 6. DETECT DATABASE FILES
# ============================================================

sqlite_files = [
    path for path in all_files
    if path.suffix.lower() in [".sqlite", ".db"]
]

duckdb_files = [
    path for path in all_files
    if path.suffix.lower() == ".duckdb"
]

csv_files = [
    path for path in all_files
    if path.suffix.lower() == ".csv"
]

print("\n" + "=" * 70)
print("DATABASE SOURCES")
print("=" * 70)

print("\nSQLite files:")
for path in sqlite_files:
    print("-", path)

print("\nDuckDB files:")
for path in duckdb_files:
    print("-", path)

print("\nCSV files:")
print("Count:", len(csv_files))


# ============================================================
# 7. DEFINE MAIN SOURCE PATHS
# ============================================================

GAME_CSV = DATASET_DIR / "csv" / "game.csv"

NBA_SQLITE = DATASET_DIR / "nba.sqlite"
NBA_DUCKDB = DATASET_DIR / "nba.duckdb"

print("\n" + "=" * 70)
print("MAIN SOURCE PATHS")
print("=" * 70)

print(
    "game.csv:",
    GAME_CSV,
    "| exists:",
    GAME_CSV.exists()
)

print(
    "nba.sqlite:",
    NBA_SQLITE,
    "| exists:",
    NBA_SQLITE.exists()
)

print(
    "nba.duckdb:",
    NBA_DUCKDB,
    "| exists:",
    NBA_DUCKDB.exists()
)


# ============================================================
# 8. FIND USEFUL CSV FILES
# ============================================================

useful_keywords = [
    "game",
    "player",
    "team",
    "award",
    "season",
    "advanced",
    "per 100",
    "summary",
]

print("\n" + "=" * 70)
print("POTENTIALLY USEFUL CSV FILES")
print("=" * 70)

for path in csv_files:

    filename = path.name.lower()

    if any(
        keyword in filename
        for keyword in useful_keywords
    ):
        print(path.relative_to(DATASET_DIR))


# ============================================================
# 9. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DOWNLOAD COMPLETE")
print("=" * 70)

print(
    f"""
Dataset directory:
{DATASET_DIR}

Main game source:
{GAME_CSV}

SQLite database:
{NBA_SQLITE}

DuckDB database:
{NBA_DUCKDB}

CSV files detected:
{len(csv_files)}

Next step:
Run 02_inspect_sources.py
"""
)
