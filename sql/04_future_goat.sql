-- ============================================================
-- NBA WINNING FORMULA
-- Future GOAT Analysis
-- ============================================================

-- IMPORTANT
-- "Future GOAT" is a trajectory score based on historical
-- comparisons. It is not a prediction of future awards,
-- championships or career outcomes.


-- ============================================================
-- 1. FUTURE GOAT RANKING
-- ============================================================

SELECT
    future_goat_rank,
    player,
    age,
    team,
    production_z,
    ts_plus,
    production_score,
    efficiency_score,
    recognition_score,
    closest_goat,
    goat_similarity,
    adjusted_goat_similarity,
    future_goat_score,
    trajectory_tier,
    data_cutoff,
    model_version
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat`
ORDER BY future_goat_rank;


-- ============================================================
-- 2. TOP 10 FUTURE GOAT CANDIDATES
-- ============================================================

SELECT
    future_goat_rank,
    player,
    age,
    team,
    ROUND(future_goat_score, 1) AS future_goat_score,
    trajectory_tier,
    closest_goat,
    ROUND(goat_similarity, 1) AS goat_similarity
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat`
WHERE future_goat_rank <= 10
ORDER BY future_goat_rank;


-- ============================================================
-- 3. ELITE / EMERGING TRAJECTORIES
-- ============================================================

SELECT
    future_goat_rank,
    player,
    age,
    production_score,
    efficiency_score,
    recognition_score,
    future_goat_score,
    trajectory_tier
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat`
WHERE trajectory_tier IN (
    'Elite historical trajectory',
    'Emerging trajectory'
)
ORDER BY future_goat_score DESC;


-- ============================================================
-- 4. HISTORICAL GOAT SIMILARITY
-- ============================================================

SELECT
    Name AS player,
    AGE AS age,
    GOAT AS historical_goat,
    Similarity AS similarity,
    Distance AS distance
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat_similarity`
ORDER BY player, similarity DESC;


-- ============================================================
-- 5. BEST HISTORICAL COMPARISON FOR EACH PLAYER
-- ============================================================

WITH ranked_similarity AS (

    SELECT
        Name AS player,
        AGE AS age,
        GOAT AS historical_goat,
        Similarity AS similarity,
        Distance AS distance,

        ROW_NUMBER() OVER (
            PARTITION BY Name
            ORDER BY Similarity DESC
        ) AS similarity_rank

    FROM
        `bootcamp-data-analytics-amadou.nba_analytics.future_goat_similarity`
)

SELECT
    player,
    age,
    historical_goat,
    ROUND(similarity, 1) AS similarity,
    ROUND(distance, 2) AS distance
FROM ranked_similarity
WHERE similarity_rank = 1
ORDER BY similarity DESC;


-- ============================================================
-- 6. YOUNG CANDIDATES
-- ============================================================

SELECT
    future_goat_rank,
    player,
    age,
    team,
    production_score,
    efficiency_score,
    recognition_score,
    future_goat_score,
    closest_goat
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat`
WHERE age <= 23
ORDER BY future_goat_score DESC;


-- ============================================================
-- 7. COMPONENTS OF THE FUTURE GOAT SCORE
-- ============================================================

SELECT
    player,
    age,
    ROUND(production_score, 1) AS production,
    ROUND(efficiency_score, 1) AS efficiency,
    ROUND(recognition_score, 1) AS recognition,
    ROUND(adjusted_goat_similarity, 1) AS historical_similarity,
    ROUND(future_goat_score, 1) AS final_score
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat`
ORDER BY future_goat_score DESC;


-- ============================================================
-- 8. DATA / MODEL VERSION
-- ============================================================

SELECT
    data_cutoff,
    model_version,
    COUNT(*) AS candidates
FROM `bootcamp-data-analytics-amadou.nba_analytics.future_goat`
GROUP BY
    data_cutoff,
    model_version;
