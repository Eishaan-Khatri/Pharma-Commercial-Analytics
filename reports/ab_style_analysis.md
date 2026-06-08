# A/B-Style Campaign Comparison

This is comparison analysis, not causal inference.

| campaign_flag | transactions | avg_net_sales | avg_units | avg_discount_rate | total_net_sales |
| --- | --- | --- | --- | --- | --- |
| non_campaign | 20865 | 2355.488705487659 | 32.18360891445003 | 0.1768708123652049 | 49147271.84 |
| campaign | 4135 | 2188.5664256348246 | 35.11656590084643 | 0.2532675453446191 | 9049722.17 |

| metric | observed_difference | bootstrap_ci_95_low | bootstrap_ci_95_high | interpretation |
| --- | --- | --- | --- | --- |
| avg_net_sales_difference_campaign_minus_non_campaign | -166.92227985283444 | -227.40882153958898 | -109.6992272973089 | Comparison only; not causal without randomized assignment. |
