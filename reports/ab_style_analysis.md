# Campaign Comparison

This is a comparison, not a real A/B test.

That means we can say:

> "Campaign rows looked different from non-campaign rows in this sample."

We cannot say:

> "The campaign caused the difference."

## Group Summary

| group | transactions | avg_net_sales | avg_units | avg_discount_rate | total_net_sales |
|---|---:|---:|---:|---:|---:|
| non_campaign | 20,865 | 2,355.49 | 32.18 | 0.1769 | 49,147,271.84 |
| campaign | 4,135 | 2,188.57 | 35.12 | 0.2533 | 9,049,722.17 |

## Difference

| metric | value |
|---|---:|
| campaign minus non-campaign average sale | -166.92 |
| 95% bootstrap CI low | -227.41 |
| 95% bootstrap CI high | -109.70 |

## What This Means

In this generated sample, campaign rows had a lower average net sale than non-campaign rows.

But don't jump to a business conclusion. Campaign rows may come from different categories, channels, discounts, or months.

The safe takeaway is:

> Campaign rows need deeper review. This table alone does not prove campaign impact.
