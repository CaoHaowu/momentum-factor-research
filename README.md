# Cross-Sectional Momentum Factor Research

[中文说明](README_CN.md)

## Overview

This project reproduces and extends a course-style cross-sectional momentum backtest into a small factor-research study. The objective is not to claim a profitable strategy, but to test whether past stock returns predict next-month cross-sectional returns and whether the result survives basic robustness and transaction-cost checks.

### Research question
Do 1-, 3-, and 6-month momentum signals predict next-month stock returns?

## Data

The baseline dataset is a locally obtained `eod-quotemedia.csv` associated with the Udacity AI for Trading momentum exercise.

Observed coverage in the local copy:
- 2013-07-01 to 2017-06-30
- 495 tickers
- 490,737 ticker-date rows
- 1,009 daily dates
- 48 monthly observations after month-end resampling

The historical point-in-time index membership of the 495 tickers has not been independently verified, so survivorship/selection bias may remain. The raw vendor-derived CSV is not committed to this repository.

## Method

1. Resample adjusted daily prices to month-end.
2. Construct 1M, 3M and 6M simple-return momentum factors.
3. At each month-end, long the top 50 stocks and short the bottom 50.
4. Use information available at month-end t to form positions and evaluate them using t+1 returns.
5. Compare all three horizons over the same 41-month evaluation period.
6. Evaluate annualized return, Sharpe ratio, maximum drawdown, one-sided return t-test, Pearson IC and Spearman RankIC.
7. Test transaction costs of 0, 5, 10 and 20 bps per traded notional.

The portfolio is dollar-neutral at rebalance (50% long / 50% short, 100% gross exposure), but it is not explicitly beta-, sector-, or risk-neutral.

## Main results

Common evaluation period: 2014-01-31 to 2017-05-31, 41 months, before transaction costs.

| Lookback | Annualized Return | Sharpe | Max Drawdown | Return p-value | Mean RankIC |
|---|---:|---:|---:|---:|---:|
| 1M | -2.67% | -0.4199 | -11.16% | 0.7789 | -0.0308 |
| 3M | -0.14% | 0.0151 | -10.63% | 0.4889 | -0.0234 |
| 6M | +0.28% | 0.0737 | -9.24% | 0.4462 | -0.0070 |

Key observations:
- None of the three strategies shows statistically significant positive mean returns at the 5% level under the ordinary one-sided t-test.
- Mean RankIC is close to zero and slightly negative across all three horizons.
- The 6M version is relatively better in this sample, but its absolute risk-adjusted performance is weak.
- Shorter lookbacks generate higher turnover and are more sensitive to transaction costs.
- Rolling RankIC changes sign through time, indicating unstable predictive relationships.

An earlier course-style baseline produced approximately 4.16% annualized return with a one-sided p-value around 0.0734, but it used a different signal lag and log-return aggregation. It is therefore not directly comparable to the revised multi-horizon backtest.

## Transaction-cost sensitivity

On the common evaluation period:

| Strategy | 0 bps | 10 bps | 20 bps |
|---|---:|---:|---:|
| 1M | -2.67% | -4.67% | -6.63% |
| 3M | -0.14% | -1.38% | -2.61% |
| 6M | +0.28% | -0.61% | -1.48% |

Average monthly turnover under the project definition is approximately 1.72 for 1M, 1.04 for 3M and 0.74 for 6M.

## Reporting

`section_18_reporting.py` contains the final reporting section used to generate:
- cumulative NAV
- drawdown
- rolling 6-month mean RankIC
- transaction-cost sensitivity
- CSV summary tables

It is designed to run after the earlier analysis sections in the same Python namespace.

## Environment

Tested locally with:
- Python 3.12.15
- pandas 3.0.6

Install the main dependencies with:

```bash
pip install -r requirements.txt
```

## Limitations

- Only 41 common monthly evaluation observations.
- Ordinary t-tests do not correct for autocorrelation or multiple testing.
- Historical point-in-time universe membership has not been independently verified.
- No beta/sector neutralization, liquidity filters, borrow costs, slippage or market-impact model.
- Turnover is based on target-weight changes and does not model intramonth weight drift.
- Repeatedly searching additional horizons after seeing these results would introduce data-snooping risk.

## Next step

Run the same research pipeline on an independently sourced later-period dataset, then freeze this project before moving to a multi-factor / machine-learning study.

## Acknowledgment

Inspired by the Udacity *AI for Trading — Trading with Momentum* exercise. The multi-horizon comparison, common-period evaluation, transaction-cost sensitivity, IC/RankIC analysis and final reporting are research extensions. This project is for educational/research purposes only and is not investment advice.
