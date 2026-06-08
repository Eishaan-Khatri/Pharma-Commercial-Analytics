# Learning Guide

This guide explains the project like we're walking through it together.

No heavy theory first. Just the story.

## The Big Idea

A company has sales rows.

Each row says something like:

> "This product category sold this many units, in this region, through this channel, with this discount."

One row is not very useful.

Thousands of rows can be useful if we clean them and ask good questions.

That's what **Pharma Commercial Analytics** does.

## Step 1: Make The Data

The repo creates generated sample data.

Why not use real data? Because the old raw files aren't here, and pharma-style commercial data can be private.

The generated rows include:

- category,
- region,
- channel,
- units,
- price,
- discount,
- campaign flag,
- net sales.

This lets anyone run the project without needing private files.

## Step 2: Clean The Rows

Cleaning means checking that the data makes sense.

For example:

- dates should be real dates,
- sales should not be negative,
- transaction IDs should not repeat,
- numbers should be numbers,
- month and quarter fields should be created cleanly.

This is boring work.

It's also the part that keeps the rest of the project from falling apart.

## Step 3: Build KPIs

KPIs are just useful business numbers.

In this project, examples include:

- total sales,
- units sold,
- average discount,
- sales by category,
- sales by region,
- sales by channel.

Think of KPIs like a scoreboard. They don't explain everything, but they tell you where to look.

## Step 4: Forecast Sales

Forecasting means making a rough guess about future sales.

This project compares:

- last month's value,
- 3-month average,
- linear regression,
- ridge regression,
- LightGBM,
- ridge + LightGBM residual model.

The important trick is the time split.

The model trains on older months and tests on later months. That way it doesn't cheat by seeing the future.

In this run, linear regression wins. LightGBM was tested but didn't win.

That's a useful lesson: fancy doesn't always mean better.

## Step 5: Group Categories

K-means groups categories that behave in a similar way.

The project uses features like:

- sales,
- growth,
- volatility,
- discount rate,
- campaign share.

The final groups are:

- high-value growing,
- stable core,
- campaign-responsive,
- low-volume niche.

These names are meant to be readable. A business person should understand them without reading the code.

## Step 6: Compare Campaign Rows

The project compares campaign rows with non-campaign rows.

But here's the honest part:

This is not proof that the campaign caused the difference.

For a real causal answer, we'd need random assignment or a better causal setup.

Here, we only say:

> "These two groups looked different in this sample."

## Step 7: Make Outputs People Can Check

The project creates:

- CSV tables,
- metrics files,
- reports,
- charts,
- dashboard SVGs.

This matters because a good project should not hide all the proof inside a notebook.

## Small Fictional Example

Imagine a fictional analyst named Arjun.

His manager asks:

> "Why are some categories moving differently from others?"

Arjun doesn't start by showing model code. He opens the segment view and says:

> "These categories are high-value and growing. These ones are stable. These ones look more campaign-heavy. Let's inspect them separately."

That's the kind of practical thinking this repo tries to show.

## What To Say In An Interview

Say this:

> I rebuilt a pharma commercial analytics workflow with generated transaction-style data. It covers cleaning, KPI analysis, forecasting, category segmentation, campaign comparison, and dashboard reporting. I kept the claims conservative because the public data is synthetic.

Don't say this:

> I built a real pharma revenue optimization system.

That would be too much.
