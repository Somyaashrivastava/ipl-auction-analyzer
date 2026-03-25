-- ================================================================
-- IPL Auction Value vs Performance — SQL Queries
-- Author: Somya Shrivastava
-- ================================================================

-- ── TABLE CREATION ─────────────────────────────────────────────
CREATE TABLE ipl_players (
    season            INT,
    player_name       VARCHAR(50),
    team              VARCHAR(10),
    role              VARCHAR(20),
    nationality       VARCHAR(20),
    matches_played    INT,
    runs_scored       INT,
    batting_avg       DECIMAL(5,2),
    strike_rate       DECIMAL(5,2),
    fifties           INT,
    hundreds          INT,
    wickets           INT,
    economy_rate      DECIMAL(4,2),
    bowling_avg       DECIMAL(5,2),
    auction_price_cr  DECIMAL(5,2),
    performance_score DECIMAL(5,3),
    value_for_money   DECIMAL(6,3),
    overpaid          TINYINT,
    hidden_gem        TINYINT
);

-- ── QUERY 1: Hidden Gems — Best Value Players ──────────────────
SELECT
    player_name, team, role,
    auction_price_cr,
    performance_score,
    value_for_money,
    RANK() OVER (ORDER BY value_for_money DESC) AS value_rank
FROM ipl_players
WHERE season = 2024
ORDER BY value_for_money DESC
LIMIT 10;

-- ── QUERY 2: Most Overpaid Players ────────────────────────────
SELECT
    player_name, team, role,
    auction_price_cr,
    performance_score,
    value_for_money,
    ROUND(auction_price_cr / NULLIF(performance_score, 0), 2) AS price_per_point
FROM ipl_players
WHERE season = 2024 AND overpaid = 1
ORDER BY auction_price_cr DESC;

-- ── QUERY 3: Team Spend vs Performance ─────────────────────────
SELECT
    team,
    COUNT(*)                             AS squad_size,
    SUM(auction_price_cr)                AS total_spend_cr,
    ROUND(AVG(performance_score), 3)     AS avg_performance,
    ROUND(AVG(value_for_money), 3)       AS avg_value,
    SUM(hidden_gem)                      AS hidden_gems,
    SUM(overpaid)                        AS overpaid_players
FROM ipl_players
WHERE season = 2024
GROUP BY team
ORDER BY total_spend_cr DESC;

-- ── QUERY 4: Role-wise Efficiency ──────────────────────────────
SELECT
    role,
    COUNT(*)                             AS players,
    ROUND(AVG(auction_price_cr), 2)      AS avg_price_cr,
    ROUND(AVG(performance_score), 3)     AS avg_performance,
    ROUND(AVG(value_for_money), 3)       AS avg_value_for_money,
    MAX(player_name)                     AS best_value_player
FROM ipl_players
WHERE season = 2024
GROUP BY role
ORDER BY avg_value_for_money DESC;

-- ── QUERY 5: Season-wise Price Inflation ───────────────────────
SELECT
    season,
    ROUND(AVG(auction_price_cr), 2)      AS avg_price_cr,
    MAX(auction_price_cr)                AS highest_bid_cr,
    SUM(auction_price_cr)                AS total_spend_cr,
    SUM(hidden_gem)                      AS hidden_gems,
    SUM(overpaid)                        AS overpaid_count
FROM ipl_players
GROUP BY season
ORDER BY season;

-- ── QUERY 6: Indian vs Overseas Value ──────────────────────────
SELECT
    CASE WHEN nationality = 'Indian' THEN 'Indian' ELSE 'Overseas' END AS player_type,
    COUNT(*)                             AS players,
    ROUND(AVG(auction_price_cr), 2)      AS avg_price_cr,
    ROUND(AVG(performance_score), 3)     AS avg_performance,
    ROUND(AVG(value_for_money), 3)       AS avg_value_for_money
FROM ipl_players
WHERE season = 2024
GROUP BY player_type;

-- ── QUERY 7: Window — Player Rank Within Team ──────────────────
SELECT
    player_name, team, role,
    auction_price_cr,
    value_for_money,
    RANK() OVER (PARTITION BY team ORDER BY value_for_money DESC) AS value_rank_in_team,
    RANK() OVER (PARTITION BY team ORDER BY auction_price_cr DESC) AS spend_rank_in_team
FROM ipl_players
WHERE season = 2024
ORDER BY team, value_rank_in_team;

-- ── QUERY 8: YoY Performance Change ────────────────────────────
SELECT
    a.player_name,
    a.team,
    a.auction_price_cr                   AS price_2024,
    a.performance_score                  AS perf_2024,
    b.performance_score                  AS perf_2023,
    ROUND(a.performance_score - b.performance_score, 3) AS perf_change,
    CASE
        WHEN a.performance_score > b.performance_score THEN '📈 Improved'
        WHEN a.performance_score < b.performance_score THEN '📉 Declined'
        ELSE '➡️ Stable'
    END AS trend
FROM ipl_players a
JOIN ipl_players b ON a.player_name = b.player_name AND b.season = 2023
WHERE a.season = 2024
ORDER BY perf_change DESC;
