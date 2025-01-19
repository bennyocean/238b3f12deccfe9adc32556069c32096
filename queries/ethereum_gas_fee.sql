SELECT
    DATE_TRUNC('day', block_time) AS day, -- Extract day from block time
    SUM(CAST(gas_used AS DECIMAL) * CAST(gas_price AS DECIMAL) / 1e18) AS total_gas_fee_eth, -- Total gas fee (converted to ETH)
    COUNT(*) AS transaction_count -- Number of transactions
FROM
    ethereum.transactions -- Ethereum transactions table
WHERE
    block_time >= TIMESTAMP '2024-01-01 00:00:00'
    AND block_time < TIMESTAMP '2025-01-01 00:00:00'
GROUP BY
    DATE_TRUNC('day', block_time)
ORDER BY
    DATE_TRUNC('day', block_time) ASC
;
