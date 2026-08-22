-- ============================================================
-- NBA WINNING FORMULA
-- Winning Factors Analysis
-- ============================================================

-- 1. Top teams by win rate
SELECT
    season,
    team,
    abbreviation,
    w,
    l,
    win_rate,
    o_rtg,
    d_rtg,
    n_rtg,
    pace
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
ORDER BY win_rate DESC
LIMIT 50;


-- 2. Average performance by season
SELECT
    season,
    ROUND(AVG(win_rate), 3) AS avg_win_rate,
    ROUND(AVG(o_rtg), 2) AS avg_offensive_rating,
    ROUND(AVG(d_rtg), 2) AS avg_defensive_rating,
    ROUND(AVG(n_rtg), 2) AS avg_net_rating,
    ROUND(AVG(pace), 2) AS avg_pace
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
GROUP BY season
ORDER BY season;


-- 3. Winning factors ordered by model importance
SELECT
    importance_rank,
    factor,
    factor_name,
    category,
    coefficient,
    abs_coefficient,
    correlation,
    direction,
    train_r2,
    test_r2,
    test_mae,
    approx_win_error
FROM `bootcamp-data-analytics-amadou.nba_analytics.winning_factors`
ORDER BY importance_rank;


-- 4. Shooting efficiency vs win rate
SELECT
    season,
    team,
    abbreviation,
    win_rate,
    e_fg_percent,
    opp_e_fg_percent
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
WHERE e_fg_percent IS NOT NULL
  AND opp_e_fg_percent IS NOT NULL
ORDER BY season, win_rate DESC;


-- 5. Possession control indicators
SELECT
    season,
    team,
    abbreviation,
    win_rate,
    tov_percent,
    opp_tov_percent,
    orb_percent,
    drb_percent
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
WHERE tov_percent IS NOT NULL
ORDER BY season, win_rate DESC;


-- 6. Free throw pressure
SELECT
    season,
    team,
    abbreviation,
    win_rate,
    ft_fga,
    opp_ft_fga
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
WHERE ft_fga IS NOT NULL
ORDER BY season, win_rate DESC;


-- 7. Best net-rating teams
SELECT
    season,
    team,
    abbreviation,
    win_rate,
    o_rtg,
    d_rtg,
    n_rtg,
    net_rating_calc
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
ORDER BY net_rating_calc DESC
LIMIT 50;


-- 8. Modern era analysis
SELECT
    season,
    team,
    abbreviation,
    win_rate,
    e_fg_percent,
    tov_percent,
    orb_percent,
    drb_percent,
    ft_fga,
    opp_e_fg_percent,
    opp_tov_percent,
    opp_ft_fga
FROM `bootcamp-data-analytics-amadou.nba_analytics.team_season`
WHERE season >= 2010
ORDER BY season DESC, win_rate DESC;
