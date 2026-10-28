# ============================================================
# 18. Visualization & Final Research Report
# Append below Section 17 in the main analysis script.
# ============================================================

from pathlib import Path
import matplotlib.pyplot as plt

out_dir = Path("outputs")
out_dir.mkdir(exist_ok=True)

cost_levels = [0, 5, 10, 20]
portfolio_returns = {}
turnover_by_horizon = {}

# 18.1 Recalculate on the same common evaluation months
for n in lookback_periods:
    weights = build_positions(factors[n], top_n=50).loc[common_dates]
    next_month = future_returns.loc[common_dates]

    missing_held_returns = ((weights != 0) & next_month.isna()).sum().sum()
    if missing_held_returns:
        raise ValueError(f"{n}M: {missing_held_returns} held returns are missing")

    gross = (weights * next_month.fillna(0)).sum(axis=1)

    turnover = weights.diff().abs().sum(axis=1)
    turnover.iloc[0] = weights.iloc[0].abs().sum()
    turnover_by_horizon[n] = turnover

    for bps in cost_levels:
        portfolio_returns[(n, bps)] = gross - turnover * bps / 10000

    expected = results[n].loc[common_dates, "gross"]
    if not np.allclose(gross.to_numpy(), expected.to_numpy()):
        raise ValueError(f"{n}M gross returns disagree with the earlier backtest")

# 18.2 Final performance and cost tables
performance_rows = []
cost_rows = []

for n in lookback_periods:
    gross = portfolio_returns[(n, 0)]
    metrics = evaluate(gross)
    t_stat, p_value = positive_mean_test(gross)

    performance_rows.append({
        "Momentum": f"{n}M",
        "Months": len(gross),
        "Annual Return": metrics["Annual Return"],
        "Sharpe": metrics["Sharpe"],
        "Max Drawdown": max_drawdown(gross),
        "Return t": t_stat,
        "Return p": p_value,
    })

    for bps in cost_levels:
        net = portfolio_returns[(n, bps)]
        cost_rows.append({
            "Momentum": f"{n}M",
            "Cost (bps)": bps,
            "Annual Return": evaluate(net)["Annual Return"],
            "Sharpe": evaluate(net)["Sharpe"],
            "Avg Turnover": turnover_by_horizon[n].mean(),
        })

performance_df = pd.DataFrame(performance_rows)
fair_cost_df = pd.DataFrame(cost_rows)

performance_df.to_csv(out_dir / "performance.csv", index=False)
fair_cost_df.to_csv(out_dir / "cost_sensitivity.csv", index=False)

print("\n===== Section 18: Final Performance =====")
print(performance_df.round(4).to_string(index=False))
print("\n===== Section 18: Common-Period Cost Sensitivity =====")
print(fair_cost_df.round(4).to_string(index=False))

# 18.3 Cumulative NAV and drawdown
start_date = common_dates.min() - pd.offsets.MonthEnd(1)
nav_df = pd.DataFrame(index=pd.DatetimeIndex([start_date]).append(common_dates))

for n in lookback_periods:
    r = portfolio_returns[(n, 0)]
    nav_df.loc[start_date, f"{n}M"] = 1.0
    nav_df.loc[common_dates, f"{n}M"] = (1 + r).cumprod().to_numpy()

ax = nav_df.plot(figsize=(10, 5), title="Momentum: Cumulative NAV (0 bps)")
ax.axhline(1.0, linestyle="--", linewidth=1)
ax.set(ylabel="Portfolio NAV (start = 1)", xlabel="Date")
plt.tight_layout()
plt.savefig(out_dir / "equity_curve.png", dpi=160)
plt.close()

drawdown_df = nav_df.div(nav_df.cummax()).sub(1)
ax = (drawdown_df * 100).plot(figsize=(10, 5), title="Momentum: Drawdown")
ax.set(ylabel="Drawdown (%)", xlabel="Date")
plt.tight_layout()
plt.savefig(out_dir / "drawdown.png", dpi=160)
plt.close()

# 18.4 Monthly RankIC and 6-month rolling mean RankIC
rankic_df = pd.DataFrame(index=common_dates)

for n in lookback_periods:
    values = []
    for date in common_dates:
        paired = pd.DataFrame({
            "factor": factors[n].loc[date],
            "next_return": future_returns.loc[date],
        }).dropna()

        values.append(
            paired["factor"].corr(paired["next_return"], method="spearman")
            if len(paired) >= 20 else np.nan
        )

    rankic_df[f"{n}M"] = values

rankic_df.to_csv(out_dir / "monthly_rankic.csv", index_label="date")

ax = rankic_df.rolling(6, min_periods=6).mean().plot(
    figsize=(10, 5),
    title="Momentum: 6-Month Rolling RankIC"
)
ax.axhline(0, linestyle="--", linewidth=1)
ax.set(ylabel="Rolling Mean RankIC", xlabel="Date")
plt.tight_layout()
plt.savefig(out_dir / "rolling_rankic.png", dpi=160)
plt.close()

# 18.5 Transaction-cost sensitivity
fig, ax = plt.subplots(figsize=(9, 5))
for n in lookback_periods:
    rows = fair_cost_df.loc[fair_cost_df["Momentum"] == f"{n}M"]
    ax.plot(
        rows["Cost (bps)"],
        100 * rows["Annual Return"],
        marker="o",
        label=f"{n}M",
    )

ax.set(
    title="Annual Return vs Transaction Cost",
    xlabel="Cost (bps per traded notional)",
    ylabel="Annual Return (%)",
)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(out_dir / "cost_sensitivity.png", dpi=160)
plt.close()

print("\nSaved outputs to:", out_dir.resolve())
