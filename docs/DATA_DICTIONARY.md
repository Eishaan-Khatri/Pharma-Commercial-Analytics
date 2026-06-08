# Data Dictionary

The public data in this repo is made by `src/generate_sample_data.py`.

Think of each row like one line on a sales bill: what was sold, where it was sold, how many units moved, and how much money came in after discounts.

| Column | Type | What it means |
|---|---|---|
| `transaction_id` | string | A unique ID for one sale row |
| `transaction_date` | date | The day the sale happened |
| `drug_category` | string | The product category |
| `product_id` | string | The product or SKU ID |
| `region` | string | The sales region |
| `channel` | string | How the product was sold, like hospital, retail, or online |
| `customer_segment` | string | The customer group |
| `units_sold` | integer | Number of units sold |
| `unit_price` | float | Price per unit before discount |
| `gross_sales` | float | Sales before discount |
| `discount_rate` | float | Discount as a value between 0 and 1 |
| `discount_amount` | float | Money reduced because of the discount |
| `net_sales` | float | Sales after discount |
| `campaign_flag` | integer | `1` for campaign-like rows, `0` for non-campaign rows |
| `month` | string | Month created during cleaning |
| `quarter` | string | Quarter created during cleaning |
| `average_selling_price` | float | Net sales divided by units sold |

## Grain

The main file is at transaction level. That means one row is one sale event.

The forecasting part groups data by month and category. The segmentation part groups data into business features, so categories can be compared like: growing, stable, high-value, or niche.

## Important Limit

This is generated data. It is useful for checking the analytics logic, but it is not proof of real pharma revenue.
