-- ============================================================
-- NBA WINNING FORMULA
-- Data Quality Checks
-- ============================================================

-- 1. Check team-season uniqueness
SELECT
    COUNT(*) AS total_rows,
    COUNT(
        DISTINCT CONCAT(
            CAST(season AS STRING),
            '-',
            abbreviation
        )
    ) AS unique_team_seasons,
    MIN(season) AS first_season,
    MAX(season) AS last_season
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`;


-- 2. Check duplicates
SELECT
    season,
    abbreviation,
    COUNT(*) AS row_count
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
GROUP BY
    season,
    abbreviation
HAVING COUNT(*) > 1
ORDER BY row_count DESC;


-- 3. Check null values on key fields
SELECT
    COUNTIF(season IS NULL) AS null_season,
    COUNTIF(abbreviation IS NULL) AS null_team,
    COUNTIF(win_rate IS NULL) AS null_win_rate
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`;


-- 4. Check win-rate range
SELECT
    MIN(win_rate) AS min_win_rate,
    AVG(win_rate) AS avg_win_rate,
    MAX(win_rate) AS max_win_rate
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`;


-- 5. Season coverage
SELECT
    season,
    COUNT(*) AS teams,
    ROUND(AVG(win_rate), 3) AS avg_win_rate,
    ROUND(MIN(win_rate), 3) AS min_win_rate,
    ROUND(MAX(win_rate), 3) AS max_win_rate
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
GROUP BY season
ORDER BY season DESC;
