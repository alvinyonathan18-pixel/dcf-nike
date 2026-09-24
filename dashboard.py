import streamlit as st
import pandas as pd

st.title("Nike (NKE) Financial Analysis Dashboard")

# --- load & hitung ulang data, mandiri dari notebook ---
income_stmt = pd.read_csv("nike_income_statement_raw.csv", index_col=0)

profitability = income_stmt.loc[["Total Revenue", "Gross Profit", "Operating Income", "Net Income"]]
profitability = profitability.dropna(axis=1)

margins = pd.DataFrame(index=profitability.columns)
margins["Gross Margin %"] = (profitability.loc["Gross Profit"] / profitability.loc["Total Revenue"]) * 100
margins["Operating Margin %"] = (profitability.loc["Operating Income"] / profitability.loc["Total Revenue"]) * 100
margins["Net Margin %"] = (profitability.loc["Net Income"] / profitability.loc["Total Revenue"]) * 100
margins = margins.round(2).sort_index()

# --- Bagian 1: Overview ---
st.header("Overview")

latest_year = profitability.columns[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Revenue (FY26)", f"${profitability.loc['Total Revenue', latest_year]/1e9:.2f}B")
col2.metric("Gross Margin", f"{margins.loc[latest_year, 'Gross Margin %']}%")
col3.metric("Operating Margin", f"{margins.loc[latest_year, 'Operating Margin %']}%")
col4.metric("Net Margin", f"{margins.loc[latest_year, 'Net Margin %']}%")

st.subheader("Margin Trend (4 Years)")
st.line_chart(margins)
# --- Bagian 2: DCF Interaktif ---
st.header("DCF Valuation (Interactive)")

balance_sheet = pd.read_csv("nike_balance_sheet_raw.csv", index_col=0)
market_data = pd.read_csv("nike_market_data_manual.csv")

shares_outstanding = income_stmt.loc["Diluted Average Shares"]["2026-05-31"]
current_price = market_data["current_price"].iloc[0]
total_debt_val = balance_sheet.loc["Total Debt"]["2026-05-31"]
cash_val = balance_sheet.loc["Cash And Cash Equivalents"]["2026-05-31"]
base_revenue = income_stmt.loc["Total Revenue"]["2026-05-31"]

col_a, col_b = st.columns(2)
with col_a:
    wacc_input = st.slider("WACC (%)", 5.0, 12.0, 8.44, 0.01) / 100
    growth_input = st.slider("Revenue Growth Rate (%)", 0.0, 6.0, 3.0, 0.1) / 100
with col_b:
    fcf_margin_input = st.slider("FCF Margin (%)", 4.0, 10.0, 7.2, 0.01) / 100
    terminal_growth_input = st.slider("Terminal Growth Rate (%)", 1.0, 4.0, 3.0, 0.1) / 100

# proyeksi 5 tahun
years = list(range(2027, 2032))
rev = base_revenue
pv_fcf_total = 0
for i, year in enumerate(years):
    rev = rev * (1 + growth_input)
    fcf = rev * fcf_margin_input
    pv_fcf_total += fcf / (1 + wacc_input) ** (i + 1)

fcf_final = rev * fcf_margin_input
terminal_value = fcf_final * (1 + terminal_growth_input) / (wacc_input - terminal_growth_input)
pv_terminal_value = terminal_value / (1 + wacc_input) ** len(years)

enterprise_value = pv_fcf_total + pv_terminal_value
net_debt = total_debt_val - cash_val
equity_value = enterprise_value - net_debt
implied_price = equity_value / shares_outstanding

col_c, col_d = st.columns(2)
col_c.metric("Implied Share Price", f"${implied_price:.2f}")
col_d.metric("Actual Market Price", f"${current_price:.2f}",
             delta=f"{((current_price - implied_price) / implied_price * 100):.1f}%")
# --- Bagian 3: Comparable Company Analysis ---
st.header("Comparable Company Analysis")

peer_metrics_df = pd.read_csv("peer_metrics_raw.csv", index_col=0)

comp_display = pd.DataFrame(index=peer_metrics_df.index)
comp_display["Name"] = peer_metrics_df["name"]

ev = peer_metrics_df["marketCap"] + peer_metrics_df["totalDebt"] - peer_metrics_df["totalCash"]

comp_display["P/E"] = peer_metrics_df.apply(
    lambda row: round(row["price"] / row["trailingEPS"], 2) if row["trailingEPS"] > 0 else "N/M",
    axis=1
)
comp_display["EV/EBITDA"] = [
    round(ev[i] / peer_metrics_df["ebitda"][i], 2) if peer_metrics_df["ebitda"][i] > 0 else "N/M"
    for i in peer_metrics_df.index
]


nike_eps = income_stmt.loc["Diluted EPS"]["2026-05-31"]
nike_ebitda_val = income_stmt.loc["EBITDA"]["2026-05-31"]
nike_market_cap = current_price * shares_outstanding
nike_ev = nike_market_cap + total_debt_val - cash_val

nike_pe_val = round(current_price / nike_eps, 2)
nike_ev_ebitda_val = round(nike_ev / nike_ebitda_val, 2)

nike_row = pd.DataFrame({
    "Name": ["Nike, Inc. (this analysis)"],
    "P/E": [nike_pe_val],
    "EV/EBITDA": [nike_ev_ebitda_val],
}, index=["NKE"])

comp_display_full = pd.concat([nike_row, comp_display])

st.dataframe(comp_display, use_container_width=True)

st.caption(
    "Under Armour's P/E is not meaningful (negative trailing EPS — the company posted "
    "a net loss). Puma's P/E and EV/EBITDA are both not meaningful (negative EBITDA — "
    "an operating loss, not just a net loss)."
)