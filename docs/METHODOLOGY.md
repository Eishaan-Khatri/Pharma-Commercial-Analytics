# Methodology

This page explains how the project works without hiding behind big words.

The short version:

> I made fake-but-realistic sales rows, cleaned them, grouped them by month and category, tried a few forecast models, grouped product categories, compared campaign rows, and made dashboard files.

## 1. Data

The public repo uses generated data.

Why? The older project talked about a larger private-style pharma sales dataset, but those raw files aren't here. So I rebuilt the project with sample data that has the same kind of fields:

- date,
- drug category,
- product ID,
- region,
- channel,
- customer segment,
- units sold,
- price,
- discount,
- campaign flag,
- net sales.

Think of it like a practice cricket pitch. It isn't the real match, but it lets you show your batting technique clearly.

## 2. Cleaning

Before making charts or models, the rows need basic checks.

The cleaning step:

- reads dates correctly,
- checks duplicate transaction IDs,
- removes bad rows,
- fixes numeric fields,
- creates month and quarter fields,
- calculates average selling price.

Why this matters: if the input rows are wrong, the dashboard will still look neat, but it won't mean much.

## 3. Sales Summaries

The project then makes simple business summaries:

- monthly sales,
- top categories,
- sales by region,
- sales by channel,
- campaign vs non-campaign rows.

These are the kinds of numbers a sales or strategy team would ask for before trusting any model.

## 4. Forecasting

The forecast target is monthly net sales for each category.

I compare six models:

- naive last-period model,
- 3-month moving average,
- linear regression,
- ridge regression,
- LightGBM,
- ridge + LightGBM residual model.

The split is time-based:

- older months are used for training,
- the next block is used for validation,
- the final months are used for testing.

In plain English: the model doesn't get to peek at the future.

Current result:

- best final-test model: `linear_regression`,
- best RMSE: `14,687.75`,
- naive RMSE: `18,373.13`,
- improvement over naive: `20.06%`.

LightGBM was tested, but it didn't win. That's fine. A simpler model winning is still a useful result.

## 5. Category Segmentation

I use K-means to group the 57 categories.

The model looks at things like:

- total sales,
- units sold,
- average order value,
- discount rate,
- campaign share,
- growth,
- volatility.

The output has four readable groups:

- high-value growing,
- stable core,
- campaign-responsive,
- low-volume niche.

These labels are not magic. A business team would still need to check whether the groups make sense.

## 6. Campaign Comparison

This part compares campaign rows with non-campaign rows.

It does **not** prove the campaign caused the difference.

Why not? Because a real A/B test needs random assignment. Without that, campaign rows may be different for many reasons: timing, product mix, channel mix, region mix, or discount strategy.

So the project reports:

- average sales in each group,
- observed difference,
- bootstrap confidence interval,
- a warning that the result is comparison-only.

## 7. Dashboard Files

The dashboard files are generated from the same output tables.

They include:

- executive summary,
- category view,
- forecast view,
- segment view,
- campaign comparison view.

The goal is simple: a reviewer should be able to open the repo and understand the work without running a notebook first.

## What I'd Add Next

If this were a real business project, I'd add:

- real anonymized aggregate data,
- a proper BI dashboard,
- stronger causal testing,
- more time history,
- business review of segment labels.
