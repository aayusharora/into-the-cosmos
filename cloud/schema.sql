-- BigQuery: where 500 parallel searches land, and how you score them.
--
-- The scoring query at the bottom is the point of the whole exercise. It is
-- the only thing that tells you whether your agent's tools actually work.

-- 1. What the workers write -------------------------------------------------

CREATE TABLE IF NOT EXISTS cosmos.transit_signals (
  target          STRING   NOT NULL,   -- e.g. "KIC 11442793"
  rank            INT64    NOT NULL,   -- 1 = strongest remaining signal
  period_days     FLOAT64  NOT NULL,
  depth_ppm       FLOAT64,
  duration_hours  FLOAT64,
  power           FLOAT64,
  radius_earth    FLOAT64,
  found_at        TIMESTAMP NOT NULL
)
PARTITION BY DATE(found_at);

-- 2. Ground truth, loaded once from the NASA Exoplanet Archive --------------
--
--   curl -sG "https://exoplanetarchive.ipac.caltech.edu/TAP/sync" \
--     --data-urlencode "query=select hostname,pl_name,pl_orbper from \
--        pscomppars where disc_facility='Kepler' and pl_orbper is not null" \
--     --data-urlencode "format=csv" > known.csv
--   bq load --autodetect --source_format=CSV cosmos.known_planets known.csv
--
-- Snapshotting it here is lesson 5: the archive is flaky behind Cloudflare,
-- so you read your copy, not theirs.

CREATE TABLE IF NOT EXISTS cosmos.known_planets (
  hostname     STRING,
  pl_name      STRING,
  pl_orbper    FLOAT64,
  kic          STRING          -- join key back to `target`
);

-- 3. The scoreboard ---------------------------------------------------------
--
-- A recovered period counts as a hit if it is within 1% of a published one.
-- Everything else we reported is a false alarm. Everything published that we
-- never reported is a miss.

WITH matched AS (
  SELECT
    s.target,
    s.period_days,
    k.pl_name,
    ABS(s.period_days - k.pl_orbper) / k.pl_orbper AS rel_err
  FROM cosmos.transit_signals s
  LEFT JOIN cosmos.known_planets k
    ON k.kic = s.target
   AND ABS(s.period_days - k.pl_orbper) / k.pl_orbper < 0.01
),
per_star AS (
  SELECT
    target,
    COUNTIF(pl_name IS NOT NULL)                      AS hits,
    COUNTIF(pl_name IS NULL)                          AS false_alarms,
    (SELECT COUNT(*) FROM cosmos.known_planets k2
      WHERE k2.kic = m.target)                        AS truth,
    APPROX_QUANTILES(IF(pl_name IS NOT NULL, rel_err, NULL), 2)[OFFSET(1)]
                                                      AS median_rel_err
  FROM matched m
  GROUP BY target
)
SELECT
  COUNT(*)                                            AS stars,
  SUM(hits)                                           AS planets_recovered,
  SUM(truth)                                          AS planets_known,
  SAFE_DIVIDE(SUM(hits), SUM(truth))                  AS recall,
  SUM(false_alarms)                                   AS false_alarms,
  SAFE_DIVIDE(SUM(false_alarms), COUNT(*))            AS false_alarms_per_star,
  ROUND(100 * AVG(median_rel_err), 4)                 AS median_period_error_pct
FROM per_star;

-- One row. That row is the only honest answer to "does my agent work?"
