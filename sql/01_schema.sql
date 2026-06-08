-- Schema for the public sample pharma commercial transaction table.
-- Raw/private data is not included in this repository.

CREATE TABLE pharma_transactions (
    transaction_id TEXT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    drug_category TEXT NOT NULL,
    product_id TEXT NOT NULL,
    region TEXT NOT NULL,
    channel TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    units_sold INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    gross_sales NUMERIC(14, 2) NOT NULL,
    discount_rate NUMERIC(6, 4) NOT NULL,
    discount_amount NUMERIC(14, 2) NOT NULL,
    net_sales NUMERIC(14, 2) NOT NULL,
    campaign_flag INTEGER NOT NULL
);

CREATE INDEX idx_transactions_date ON pharma_transactions(transaction_date);
CREATE INDEX idx_transactions_category ON pharma_transactions(drug_category);
CREATE INDEX idx_transactions_region ON pharma_transactions(region);
CREATE INDEX idx_transactions_channel ON pharma_transactions(channel);

