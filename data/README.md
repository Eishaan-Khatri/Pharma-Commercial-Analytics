# Data Notes

The old portfolio version of this project mentioned a pharma analytics workflow over `600K+` transactions and `57` categories. The raw data is not in this public repo.

That matters.

If a dataset may contain business information, customer patterns, pricing, or internal sales details, it should not be uploaded publicly just to make a GitHub repo look stronger.

So this rebuilt version uses generated sample data:

- `data/sample/pharma_transactions_sample.csv`

The sample lets someone run the project and check the code. It should not be presented as real pharma revenue.

## Why Use Generated Data?

Public analytics projects often need a safe sample. The honest way to do that is:

1. explain what the original project was about,
2. share a generated or anonymized sample,
3. make the code and outputs easy to run,
4. avoid fake business-impact claims.

## Columns

See `docs/DATA_DICTIONARY.md` for the full column list.
