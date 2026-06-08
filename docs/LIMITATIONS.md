# Limitations

This project is useful, but it has clear limits.

That isn't a weakness. It's better to say the limits clearly than to make the project sound bigger than it is.

## 1. The Public Data Is Generated

The repo uses generated sample data.

So the project proves:

- the workflow,
- the code structure,
- the metrics,
- the dashboard output,
- the way I explain the results.

It does **not** prove real pharma sales impact.

## 2. This Is Not Clinical Work

This project is about commercial sales-style data.

It does not study:

- patients,
- drug safety,
- treatment results,
- side effects,
- medical decisions.

So it should not be called a medical AI project.

## 3. Campaign Comparison Is Not Proof

The campaign section compares campaign rows with non-campaign rows.

That is not the same as saying:

> "The campaign caused this change."

To say that, we'd need a proper randomized test or stronger causal design.

Here, the honest wording is:

> "Campaign rows looked different in this generated sample, but this is not causal proof."

## 4. LightGBM Did Not Win

I added LightGBM because it's a strong model for tabular data.

But in this checked-in run, the best final-test RMSE comes from linear regression.

That means the resume claim should say:

> "Compared six forecasting baselines."

It should **not** say:

> "LightGBM won."

## 5. K-Means Needs Human Review

K-means can group categories, but it doesn't understand business context.

For example, if it puts two categories in the same group, a domain expert should still ask:

- Are they really similar?
- Do they need the same business action?
- Is the cluster useful, or just mathematically neat?

## 6. The Dashboard Is Static

The dashboard files are SVG images.

They are good for GitHub Pages and quick review, but they are not a full Tableau, Power BI, or Streamlit app.

## Safe Way To Describe The Project

Use this:

> A reproducible commercial analytics workflow using generated pharma-style transaction data.

Don't use this:

> A real pharma revenue optimization system.
