SELECT
  DATE_TRUNC('day', block_time) AS day, -- Extract the day from block time
  project, -- Include the project name (DEX)
  SUM(amount_usd) AS daily_volume_usd, -- Total USD volume for POL
  COUNT(*) AS trade_count -- Number of trades involving POL
FROM
  dex.trades
WHERE
  -- Convert the string token address to varbinary using FROM_HEX
  (token_bought_address = FROM_HEX('455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6')
  OR token_sold_address = FROM_HEX('455e53CBB86018Ac2B8092FdCd39d8444aFFC3F6'))
  -- Use date filter for the year 2024
  AND block_time >= TIMESTAMP '2024-01-01 00:00:00'
  AND block_time < TIMESTAMP '2025-01-01 00:00:00'
GROUP BY
  DATE_TRUNC('day', block_time),
  project
ORDER BY
  DATE_TRUNC('day', block_time) ASC,
  project
;
