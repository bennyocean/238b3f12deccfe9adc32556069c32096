SELECT
  DATE_TRUNC('day', block_time) AS day, -- Extract the day from block time
  project, -- Include the project name (DEX)
  SUM(amount_usd) AS daily_volume_usd, -- Total USD volume for USDC
  COUNT(*) AS trade_count -- Number of trades involving USDC
FROM
  dex.trades
WHERE
  -- Convert the string token address to varbinary using FROM_HEX
  (token_bought_address = FROM_HEX('A0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48')
  OR token_sold_address = FROM_HEX('A0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'))
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
