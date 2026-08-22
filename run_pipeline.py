"""
NBA WINNING FORMULA
Master Pipeline Runner

Purpose
-------
Run the complete NBA Winning Formula Python pipeline
in the correct order.

Usage
-----
python run_pipeline.py

Optional:
python run_pipeline.py --start 4
python run_pipeline.py --only 7
"""

from pathlib import Path
import argparse
import subprocess
import sys
import time


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON_DIR = PROJECT_ROOT / "python"


# ============================================================
# 2. PIPELINE DEFINITION
# ============================================================

PIPELINE = [
    (
        1,
        "Download data",
        "01_download_data.py",
    ),
    (
        2,
        "Inspect sources",
        "02_inspect_sources.py",
    ),
    (
        3,
        "Prepare team data",
        "03_prepare_team_data.py",
    ),
    (
        4,
        "Build Winning Formula",
        "04_build_winning_formula.py",
    ),
    (
        5,
        "Prepare player seasons",
        "05_prepare_player_seasons.py",
    ),
    (
        6,
        "Build Historical GOAT",
        "06_build_goat_model.py",
    ),
    (
        7,
        "Build Future GOAT",
        "07_build_future_goat.py",
    ),
    (
        8,
        "Validate Data Mart",
        "08_export_datamart.py",
    ),
    (
        9,
        "Build Plotly animation",
        "09_build_plotly_animation.py",
    ),
]


# ============================================================
# 3. COMMAND-LINE OPTIONS
# ============================================================

parser = argparse.ArgumentParser(
    description=(
        "Run the NBA Winning Formula "
        "analytics pipeline."
    )
)

parser.add_argument(
    "--start",
    type=int,
    default=1,
    help=(
        "Start execution from a specific step. "
        "Example: --start 5"
    ),
)

parser.add_argument(
    "--only",
    type=int,
    default=None,
    help=(
        "Run only one specific pipeline step. "
        "Example: --only 7"
    ),
)

args = parser.parse_args()


# ============================================================
# 4. VALIDATE PIPELINE FILES
# ============================================================

missing_scripts = []

for step, label, filename in PIPELINE:

    script_path = PYTHON_DIR / filename

    if not script_path.exists():

        missing_scripts.append(
            filename
        )


if missing_scripts:

    print("\nERROR: Missing scripts:")

    for filename in missing_scripts:
        print(" -", filename)

    sys.exit(1)


# ============================================================
# 5. SELECT STEPS
# ============================================================

if args.only is not None:

    selected_steps = [
        item
        for item in PIPELINE
        if item[0] == args.only
    ]

    if not selected_steps:

        print(
            f"Invalid step: {args.only}"
        )

        sys.exit(1)

else:

    selected_steps = [
        item
        for item in PIPELINE
        if item[0] >= args.start
    ]


# ============================================================
# 6. HEADER
# ============================================================

print("=" * 72)
print("NBA WINNING FORMULA")
print("MASTER PYTHON PIPELINE")
print("=" * 72)

print(
    f"\nProject root:\n{PROJECT_ROOT}"
)

print("\nSteps to execute:")

for step, label, filename in selected_steps:

    print(
        f"{step}. {label}"
        f" ({filename})"
    )


# ============================================================
# 7. EXECUTE PIPELINE
# ============================================================

pipeline_start = time.time()

completed = []

for step, label, filename in selected_steps:

    script_path = (
        PYTHON_DIR
        / filename
    )

    print("\n" + "=" * 72)

    print(
        f"STEP {step}/9"
    )

    print(
        label.upper()
    )

    print("=" * 72)

    start_time = time.time()

    command = [
        sys.executable,
        str(script_path),
    ]

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
    )

    elapsed = (
        time.time()
        - start_time
    )

    if result.returncode != 0:

        print("\n" + "!" * 72)

        print(
            f"PIPELINE STOPPED AT STEP {step}"
        )

        print(
            f"Script: {filename}"
        )

        print(
            f"Exit code: {result.returncode}"
        )

        print(
            f"Elapsed: {elapsed:.1f}s"
        )

        print("!" * 72)

        sys.exit(
            result.returncode
        )

    completed.append(
        {
            "step": step,
            "label": label,
            "seconds": elapsed,
        }
    )

    print(
        f"\n✓ Step {step} complete"
        f" in {elapsed:.1f}s"
    )


# ============================================================
# 8. FINAL SUMMARY
# ============================================================

total_elapsed = (
    time.time()
    - pipeline_start
)

print("\n" + "=" * 72)
print("PIPELINE COMPLETE")
print("=" * 72)

for item in completed:

    print(
        f"✓ {item['step']}. "
        f"{item['label']}"
        f" — {item['seconds']:.1f}s"
    )


print(
    "\nTotal execution time:"
    f" {total_elapsed:.1f}s"
)


print(
    """
Final workflow:

RAW NBA DATA
      ↓
SOURCE INSPECTION
      ↓
TEAM DATA
      ↓
WINNING FORMULA
      ↓
PLAYER-SEASON FEATURES
      ↓
HISTORICAL GOAT
      ↓
FUTURE GOAT
      ↓
DATA MART VALIDATION
      ↓
PLOTLY ANIMATION
      ↓
BIGQUERY / LOOKER STUDIO / GITHUB PAGES
"""
)


print(
    "\nNext:"
    "\n- review data/processed/"
    "\n- load validated tables into BigQuery"
    "\n- refresh Looker Studio"
    "\n- publish animations through GitHub Pages"
)
