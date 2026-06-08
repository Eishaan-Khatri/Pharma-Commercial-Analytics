-- Core business analytics queries.

-- 1. Monthly revenue by category
SELECT
    DATE_TRUNC('month', transaction_date) AS month,
    drug_category,
    SUM(net_sales) AS monthly_net_sales,
    SUM(units_sold) AS monthly_units,
    COUNT(*) AS transaction_count
FROM pharma_transactions
GROUP BY 1, 2
ORDER BY 1, monthly_net_sales DESC;

-- 2. Top categories by total revenue
SELECT
    drug_category,
    SUM(net_sales) AS total_net_sales,
    SUM(units_sold) AS total_units,
    COUNT(*) AS transaction_count
FROM pharma_transactions
GROUP BY drug_category
ORDER BY total_net_sales DESC
LIMIT 10;

-- 3. Region and channel contribution
SELECT
    region,
    channel,
    SUM(net_sales) AS total_net_sales,
    COUNT(*) AS transaction_count,
    AVG(discount_rate) AS avg_discount_rate
FROM pharma_transactions
GROUP BY region, channel
ORDER BY total_net_sales DESC;

-- 4. Campaign versus non-campaign comparison
SELECT
    campaign_flag,
    AVG(net_sales) AS avg_net_sales_per_transaction,
    AVG(units_sold) AS avg_units_per_transaction,
    AVG(discount_rate) AS avg_discount_rate,
    COUNT(*) AS transaction_count
FROM pharma_transactions
GROUP BY campaign_flag;

-- 5. High-discount categories
SELECT
    drug_category,
    AVG(discount_rate) AS avg_discount_rate,
    SUM(net_sales) AS total_net_sales
FROM pharma_transactions
GROUP BY drug_category
HAVING COUNT(*) >= 50
ORDER BY avg_discount_rate DESC
LIMIT 15;

