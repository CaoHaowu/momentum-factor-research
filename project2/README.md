# Project 2 — Multi-Factor Stock Return Prediction

**Status:** Model research completed; final deterministic tie-breaking replay and source-code publication pending. The results below document the original run, not a new independently validated run.

## Research question

Does combining price-derived signals with linear or nonlinear machine learning improve monthly cross-sectional stock return prediction and long-short portfolio performance relative to a six-month momentum baseline?

## Data and method

- Reuses the Stooq daily price matrix from Project 1 (502 matched current S&P 500 securities, January 2018–September 2026).
- Complete monthly panel: 47,694 stock-month observations, 500 securities, 98 signal months.
- Features: 3M momentum, 6M momentum, 1M reversal (negative previous monthly return), 3M volatility (standard deviation of three monthly returns).
- Cross-sectional 1st/99th percentile winsorization and z-score normalization.
- Target: next-month simple return.
- Ridge: alpha = 1.0; 25,880 pre-2023 signal observations.
- LightGBM: development signal months July 2018–December 2020, validation January 2021–December 2022; early stopping on validation RMSE selected three boosting iterations. Refit on all pre-2023 signal observations.
- Common evaluation: 21,814 stock-month observations, 44 signal months from January 2023 through August 2026 (realized return months February 2023 through September 2026).
- Models use information available by the corresponding month-end; the December 2022 training label is realized in January 2023, before the first January month-end prediction. Development/validation boundaries also require this label-availability convention; a stricter embargo is future work.
- Portfolio: monthly top 50 long and bottom 50 short, 1% absolute weight per position, 100% gross and zero net dollar exposure at rebalance.
- Turnover is the sum of absolute target-weight changes, including initial establishment from cash. Costs are 0/5/10/20 bps per traded notional. Sharpe assumes zero risk-free rate.

## Prediction results

| Model | Mean RankIC | RankIC std | Positive months | One-sided RankIC p |
|---|---:|---:|---:|---:|
| 6M Momentum | 0.023046 | 0.164956 | 56.82% | 0.179622 |
| Ridge | 0.002288 | 0.146724 | 52.27% | 0.459046 |
| LightGBM | -0.005245 | 0.096770 | 45.45% | 0.639509 |

Neither ML model improved mean RankIC relative to the simple baseline. Ridge test R² was 0.001726; LightGBM test R² was 0.000256. These are pooled return regression metrics, not direct ranking objectives.

## Original portfolio results (0 bps)

| Strategy | Annualized compound return | Sharpe | Max drawdown | Monthly turnover | One-sided mean-return p |
|---|---:|---:|---:|---:|---:|
| 6M Momentum | 9.53% | 0.8029 | -13.68% | 0.7268 | 0.0658 |
| Ridge | 9.76% | 1.1012 | -7.72% | 1.3914 | 0.0204 |
| LightGBM* | 2.58% | 0.3737 | -11.91% | 1.4359 | 0.2391 |

*LightGBM portfolio figures are implementation-sensitive: the original selection did not explicitly resolve score ties. Treat them as illustrative until replayed with a fixed tie-break.

## Cost sensitivity (annualized compound return)

| Cost | 6M Momentum | Ridge | LightGBM* |
|---|---:|---:|---:|
| 0 bps | 9.53% | 9.76% | 2.58% |
| 5 bps | 9.06% | 8.86% | 1.70% |
| 10 bps | 8.59% | 7.96% | 0.83% |
| 20 bps | 7.65% | 6.18% | -0.90% |

At 10 bps, Ridge retained a higher realized Sharpe (0.9124 versus 0.7321), while momentum had higher net annualized return. This is a descriptive sample comparison, not proof of superior risk-adjusted performance in future data.

## Tail analysis and paired return test

| Strategy | Monthly D10−D1 mean | Monthly spread std |
|---|---:|---:|
| 6M Momentum | 1.6355% | 7.1082% |
| Ridge | 1.6245% | 5.1078% |
| LightGBM* | 0.5402% | 4.2327% |

The decile spread is the full difference between equal-weight stock groups, not the return of a 100%-gross, 50/50 long-short portfolio. The Ridge and momentum spreads are similar in mean, but Ridge has lower realized spread volatility. The original LightGBM decile analysis also depends on tie-breaking.

Paired monthly gross returns (Ridge minus momentum): mean -0.000129, annualized arithmetic mean difference -0.1545 percentage points, t = -0.0286, one-sided p = 0.511339. No significant evidence of a mean-return improvement. The higher Ridge compound return is consistent with lower volatility; its standalone p-value is not a test of superiority over momentum.

## Final audit (user-run, read-only)

- Non-positive observed prices: 0.
- Feature-eligible historical rows: 47,694; missing future labels: 0, including evaluation rows. The final month without any future observations is excluded.
- Reconstructed panel versus saved panel: 47,694 matched, 0 unmatched; maximum absolute numeric discrepancy about 1.78e-15. Panel audit passed.
- Prediction keys match across the three methods.
- Portfolio boundary ties: momentum and Ridge 0/44 on both sides; LightGBM 44/44 short and 43/44 long.
- Comparing alphabetical versus reverse-alphabetical tie resolution gives a mean absolute monthly gross-return difference of 52.7916 bps for LightGBM, zero for momentum and Ridge.

The audit found no realized effect from conditioning the original panel preprocessing on label availability in this historical sample. It does not eliminate broader universe-selection bias. LightGBM's three-tree model has coarse score granularity, and tied stocks cannot be distinguished by score alone.

**Final implementation rule:** sort ascending by (score, ticker); select first 50 for shorts and last 50 for longs. Use the same ordering before assigning score deciles. This deterministic convention is chosen for reproducibility, not based on which tie rule is more profitable. Replay the portfolio and reporting scripts only; no model retraining or test-set tuning. Preserve the original-run values as an audit trail.

## Conclusion

Adding model complexity did not improve average cross-sectional ranking in the observed evaluation period. Ridge produced comparable gross portfolio returns with lower realized volatility and drawdown, but no statistically significant paired mean-return improvement and materially higher turnover. Momentum retained stronger cost-adjusted absolute returns in the tested positive-cost scenarios. LightGBM did not improve RankIC and its portfolio implementation was highly sensitive to tied scores.

## Limitations

Current constituents rather than point-in-time membership; possible survivorship/selection bias; no explicit sector or beta neutralization; simplified turnover, borrow, execution and cost assumptions; month-end signal versus execution timing; only 44 evaluation months; conventional t-tests without serial-dependence or multiple-testing adjustments; previously inspected evaluation period (including Project 1), not an untouched holdout. Results do not establish robust alpha.

## Source files and reproducibility

Local scripts to publish: P2-001_build_features.py, P2-002_ridge.py, P2-002b_feature_diagnostics.py, P2-003_lightgbm.py, P2-004_backtest.py, P2-005_reporting.py, P2-006_final_audit.py. Add environment requirements, aggregate results and regenerated figures. Do not publish vendor raw prices, derived row-level target data or predictions without checking redistribution permissions. The source scripts and figures have not yet been uploaded to this folder.

Research/education only.
