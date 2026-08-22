# Python Pipeline

This directory contains the ordered Python pipeline used to build the NBA Winning Formula project.

The scripts are designed to be read and executed sequentially.

## Execution Order

1. `01_download_data.py`
   - Download the NBA datasets.
   - Locate source files.
   - Define project paths.

2. `02_inspect_sources.py`
   - Inspect tables, schemas and available columns.
   - Validate file availability.
   - Check data coverage.

3. `03_prepare_team_data.py`
   - Build team-season datasets.
   - Convert game-level data into one row per team and season.
   - Prepare possession-adjusted team metrics.

4. `04_build_winning_formula.py`
   - Analyze correlations.
   - Build the final Winning Formula regression.
   - Perform temporal train/test validation.
   - Export model factors.

5. `05_prepare_player_seasons.py`
   - Build one row per player and season.
   - Calculate PPG, RPG, APG, TS%, TS+ and era-adjusted Z-scores.

6. `06_build_goat_model.py`
   - Build the historical GOAT framework.
   - Calculate Production, Efficiency, Playoffs, Individual Success, Team Success and Longevity.
   - Build Balanced, Peak, Longevity, Winning and Individual Dominance scenarios.

7. `07_build_future_goat.py`
   - Identify current candidates.
   - Compare players at equivalent ages.
   - Calculate historical GOAT similarity.
   - Build the Future GOAT V2 score.

8. `08_export_datamart.py`
   - Export the final analytics-ready CSV files.

9. `09_build_plotly_animation.py`
   - Build the interactive Future GOAT career trajectory.
   - Export the final HTML used with GitHub Pages.

---

## Simplified Pipeline

```text
NBA DATA
   ↓
01 Download
   ↓
02 Inspect
   ↓
03 Team Preparation
   ↓
04 Winning Formula
   ↓
05 Player Seasons
   ↓
06 Historical GOAT
   ↓
07 Future GOAT
   ↓
08 Data Mart Export
   ↓
09 Plotly Animation
