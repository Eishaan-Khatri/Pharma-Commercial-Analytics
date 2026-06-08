# A/B-Style Campaign Comparison

This is comparison analysis, not causal inference.

| campaign_flag | transactions | avg_net_sales | avg_units | avg_discount_rate | total_net_sales |
| --- | --- | --- | --- | --- | --- |
| non_campaign | 20904 | 1229.8030276502104 | 22.803434749330272 | 0.177454582854956 | 25707802.49 |
| campaign | 4096 | 1255.3812866210938 | 25.7744140625 | 0.252442822265625 | 5142041.75 |

| metric | observed_difference | bootstrap_ci_95_low | bootstrap_ci_95_high | interpretation |
| --- | --- | --- | --- | --- |
| avg_net_sales_difference_campaign_minus_non_campaign | 25.578258970883326 | -20.209014731989857 | 71.58175620722633 | Comparison only; not causal without randomized assignment. |
