-- ============================================================
-- NBA WINNING FORMULA
-- Historical GOAT Analysis
-- ============================================================

-- 1. GOAT master profile
SELECT
    *
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_master`;


-- 2. GOAT dimensions
SELECT
    Name,
    Production,
    Efficiency,
    Playoffs,
    Individual,
    `Team Success`,
    Longevity
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_dimensions`;


-- 3. Balanced GOAT ranking
SELECT
    Name,

    ROUND(
        0.20 * Production
        + 0.15 * Efficiency
        + 0.20 * Playoffs
        + 0.20 * Individual
        + 0.10 * `Team Success`
        + 0.15 * Longevity,
        1
    ) AS balanced_goat_score

FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_dimensions`

ORDER BY balanced_goat_score DESC;


-- 4. GOAT scenarios
SELECT
    *
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_scenarios`;


-- 5. True Peak ranking
SELECT
    *
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_peak`
ORDER BY `True Peak Score` DESC;


-- 6. Player career trajectories
SELECT
    Name,
    PLAYER_ID,
    SEASON_ID,
    TEAM_ABBREVIATION,
    PLAYER_AGE,
    GP,
    PPG,
    RPG,
    APG,
    PPG_Z,
    RPG_Z,
    APG_Z,
    PRODUCTION_Z,
    TS_PCT,
    TS_PLUS,
    TS_Z
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_player_seasons`
ORDER BY Name, SEASON_ID;


-- 7. Compare GOAT candidates at age 25
SELECT
    Name,
    SEASON_ID,
    PLAYER_AGE,
    PPG,
    RPG,
    APG,
    PRODUCTION_Z,
    TS_PLUS
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_player_seasons`
WHERE ROUND(PLAYER_AGE) = 25
ORDER BY PRODUCTION_Z DESC;


-- 8. Compare GOAT candidates at age 30
SELECT
    Name,
    SEASON_ID,
    PLAYER_AGE,
    PPG,
    RPG,
    APG,
    PRODUCTION_Z,
    TS_PLUS
FROM `bootcamp-data-analytics-amadou.nba_analytics.goat_player_seasons`
WHERE ROUND(PLAYER_AGE) = 30
ORDER BY PRODUCTION_Z DESC;


-- 9. Methodology
SELECT
    *
FROM `bootcamp-data-analytics-amadou.nba_analytics.methodology`;
