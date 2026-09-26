# Nike (NKE) Financial Analysis & DCF Valuation

Python-based financial statement analysis and discounted cash flow 
valuation of Nike, Inc., covering FY2023–FY2026.

## Key Findings

- Operating Margin fell twice as fast as Gross Margin (FY24→FY25) — driven 
  by operating deleverage (SG&A costs didn't shrink as fast as revenue), 
  not a strategic spending increase.
- ROE dropped 38.3% (FY24→FY25), driven almost entirely by falling Net 
  Margin. Rising leverage actually cushioned the decline rather than 
  worsening it.
- A three-scenario DCF (Bear/Base/Bull, WACC 8.44%) implies a share price 
  range of USD 32.57–48.31. The actual market price (~USD 36, Sept 2026) 
  sits closer to the Bear case — consistent with the operating deleverage 
  thesis found in the historical data.
- Comparable company analysis (P/E, EV/EBITDA vs. Adidas, Under Armour, 
  Lululemon, Puma) shows Nike trading at a premium to its peer average 
  (+27% on P/E, +12% on EV/EBITDA) — but this reflects a peer group in 
  worse shape (Under Armour posted a net loss, Puma a negative EBITDA), 
  not strength in absolute terms. Consistent with a broader apparel 
  industry downturn, where Nike is weathering the weakness better than 
  its competitors rather than being exempt from it.

## Methodology

- **Data:** Nike's income statement, balance sheet, and cash flow 
  statement (FY2023–FY2026), sourced via the `yfinance` library
- **Ratio analysis:** profitability margins, DuPont decomposition (ROE), 
  leverage ratios, working capital analysis
- **Valuation:** 5-year FCF projection (3 scenarios) discounted at WACC, 
  with a Gordon Growth terminal value. Cross-checked against a comparable 
  company analysis (P/E, EV/EBITDA) using four apparel-sector peers.

## SQL Analysis

In addition to the pandas-based analysis, `sql_analysis.ipynb` loads the same 
financial data into a local SQLite database (`nike_finance.db`) and 
recreates key calculations using SQL, as a cross-check and to demonstrate 
SQL proficiency:

- Self-joins to compute Gross Margin directly from raw revenue and profit rows
- A cross-table JOIN between the income statement and balance sheet to calculate ROA
- Aggregate functions (AVG, GROUP BY) to summarize metrics across fiscal years
- A window function (LAG) to calculate year-over-year revenue growth

All SQL-derived figures were cross-validated against the equivalent pandas 
calculations in `analysis.ipynb` and matched exactly.

## Repository Structure

- `analysis.ipynb` — full analysis notebook (ratios + DCF + Comps)
- `dashboard.py` — interactive Streamlit dashboard (run with 
  `streamlit run dashboard.py`)
- `nike_income_statement_raw.csv`, `nike_balance_sheet_raw.csv`, 
  `nike_cash_flow_raw.csv` — raw financial statement data
- `nike_market_data_manual.csv` — market data (beta, share price, market 
  cap), manually sourced Sept 16, 2026 due to a `yfinance` API limitation
- `sql_analysis.ipynb` — SQL-based analysis (JOINs, aggregation, window 
  functions), cross-validated against `analysis.ipynb`
- `nike_finance.db` — SQLite database built from the CSV files, used by 
  `sql_analysis.ipynb`
- `peer_metrics_raw.csv` — raw comparable company data (Adidas, Under 
  Armour, Lululemon, Puma)

## Running This Notebook
pip install -r requirements.txt
jupyter notebook analysis.i

All cells read from the included CSV files — no live API calls required 
to reproduce the analysis.

## Limitations

This model is built entirely from historical financial statement data. It 
does not capture qualitative factors (competitive dynamics, regional 
execution, forward guidance) that the market also prices in. Published 
analyst price targets for NKE spanned an unusually wide range (~USD 23–75) 
as of September 2026, reflecting genuine disagreement in the market 
itself, not just uncertainty in this specific model.