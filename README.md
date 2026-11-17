# Cross-Sectional Momentum Factor Research

[中文说明](README_CN.md)

## Overview

This project reproduces and extends a course-style cross-sectional momentum backtest into a small factor-research study. It tests whether past stock returns predict next-month cross-sectional returns, and whether any apparent performance survives common-period comparison, statistical checks, turnover analysis and transaction costs.

The project contains two stages:

1. **Baseline study** using a QuoteMedia-derived educational dataset (2013-2017).
2. **Independent later-period replication** using Stooq U.S. daily data (2018-2026) for 502 current S&P 500 constituents successfully matched to the downloaded files.

The objective is not to claim a profitable strategy, but to document what works, what does not, and how sensitive the conclusions are to sample period and implementation choices.

## Research question

Do 1-, 3-, and 6-month cross-sectional momentum signals predict next-month stock returns?

## Method

- Resample daily close prices to month-end.
- Construct 1M, 3M and 6M simple-return momentum factors.
- At each month-end, long the top 50 stocks and short the bottom 50.
- Use only information available at month-end t to form positions; evaluate with t+1 returns.
- Portfolio is 50% long / 50% short at rebalance, so net dollar exposure is approximately zero and gross exposure is 100%.
- Compare all horizons over a common evaluation period.
- Evaluate annualized return, Sharpe ratio, maximum drawdown, one-sided mean-return t-test, Pearson IC and Spearman RankIC.
- Test transaction costs of 0, 5, 10 and 20 bps per traded notional.

The portfolio is dollar-neutral but is **not** explicitly beta-, sector-, liquidity- or risk-neutral.

## Dataset 1: QuoteMedia baseline

Local educational dataset coverage:

- 2013-07-01 to 2017-06-30
- 495 tickers
- 490,737 ticker-date rows
- 1,009 daily dates
- 48 monthly observations after month-end resampling

Common evaluation period: **2014-01-31 to 2017-05-31 (41 months)**.

| Lookback | Annualized Return | Sharpe | Max Drawdown | Return p-value | Mean RankIC |
|---|---:|---:|---:|---:|---:|
| 1M | -2.67% | -0.4199 | -11.16% | 0.7789 | -0.0308 |
| 3M | -0.14% | 0.0151 | -10.63% | 0.4889 | -0.0234 |
| 6M | +0.28% | 0.0737 | -9.24% | 0.4462 | -0.0070 |

In this sample, all three specifications were weak. The 6M version ranked relatively best, but its absolute performance and cross-sectional predictive power were small.

## Dataset 2: Stooq independent replication

Stooq U.S. daily bulk files were processed locally and matched against the current S&P 500 constituent list.

Prepared dataset:

- 2018-01-02 to 2026-09-30
- 2,198 daily observations
- 502 successfully matched securities out of 503
- 105 month-end observations
- minimum valid stocks in any month: 464
- common evaluation period: **2018-07-31 to 2026-08-31 (98 months)**

### Final common-period performance

| Lookback | Annualized Return | Sharpe | Max Drawdown | Return t | Return p | Mean IC | Mean RankIC |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1M | +2.25% | 0.2601 | -22.25% | 0.7432 | 0.2296 | 0.0172 | 0.0064 |
| 3M | -0.21% | 0.0393 | -19.91% | 0.1123 | 0.4554 | 0.0127 | -0.0025 |
| 6M | **+5.19%** | **0.4939** | **-13.68%** | **1.4115** | **0.0806** | **0.0337** | **0.0122** |

### Transaction-cost sensitivity

| Strategy | 0 bps | 5 bps | 10 bps | 20 bps | Avg. monthly turnover |
|---|---:|---:|---:|---:|---:|
| 1M | +2.25% | +1.21% | +0.18% | -1.86% | 1.7073 |
| 3M | -0.21% | -0.83% | -1.44% | -2.67% | 1.0378 |
| 6M | **+5.19%** | **+4.73%** | **+4.27%** | **+3.36%** | **0.7335** |

### Train / later-period split

A split date of **2023-01-01** was fixed before reviewing the final results.

| Lookback | Earlier-period Sharpe | Later-period Sharpe | Later-period annual return |
|---|---:|---:|---:|
| 1M | -0.4092 | 1.0156 | 11.20% |
| 3M | -0.0369 | 0.1403 | 0.97% |
| 6M | 0.2141 | 0.8029 | 9.53% |

This large change between earlier and later periods is evidence of **regime dependence**, not proof of stable alpha.

## Interpretation

Three findings matter most:

1. **6M momentum was relatively strongest in both datasets.**  
   The first sample still showed weak absolute performance, while the later Stooq sample improved materially.

2. **The evidence is economically more interesting than statistically decisive.**  
   In the Stooq replication, 6M momentum earned about 5.2% annualized before costs with a Sharpe near 0.49 and a one-sided return p-value of 0.0806. This is suggestive, but it does not meet the conventional 5% significance threshold.

3. **Turnover strongly affects implementability.**  
   The shorter 1M signal turns over far more often and loses most of its gross return after moderate trading-cost assumptions. The 6M signal combines higher gross return with lower turnover and remains positive under the simplified 20 bps cost scenario.

Rolling RankIC changes sign through time, further suggesting that momentum effectiveness is time-varying rather than structurally stable.

## Reproducibility

- `P1-002_prepare_stooq.py`: converts locally downloaded Stooq U.S. daily bulk files into a research-ready close-price matrix.
- `section_18_reporting.py`: generates final performance tables, transaction-cost sensitivity, cumulative NAV, drawdown and rolling RankIC outputs.
- Raw Stooq / QuoteMedia price files are intentionally excluded from the repository.

## Environment

Tested locally with:

- Python 3.12
- pandas 3.x
- NumPy
- SciPy
- Matplotlib

Install:

```bash
pip install -r requirements.txt
```

## Limitations

- The historical universe is based on current S&P 500 constituents rather than point-in-time membership, so survivorship / selection bias may remain.
- Ordinary t-tests do not correct for serial correlation or multiple testing.
- The portfolio is not beta- or sector-neutral.
- No explicit liquidity filter, borrow cost, slippage or market-impact model is included.
- Turnover is estimated from target-weight changes and does not simulate intramonth weight drift.
- RankIC is weak even in the stronger 6M replication.
- Further tuning of lookback horizons after observing these results would introduce data-snooping risk.

## Conclusion

Across two samples, 6M momentum ranked relatively better than 1M and 3M, but its absolute effectiveness was strongly sample-dependent. The later Stooq replication produced economically positive and more cost-robust results, while conventional statistical evidence remained weak.

The project is therefore **frozen at this point**. Further enhancements such as point-in-time universes, beta/sector neutralization, HAC standard errors or additional momentum horizons are treated as future work rather than post-hoc optimization.

## Acknowledgment

Inspired by the Udacity *AI for Trading — Trading with Momentum* exercise. The multi-horizon comparison, independent replication, common-period evaluation, transaction-cost sensitivity, IC/RankIC analysis and final reporting are research extensions.

Educational/research use only; not investment advice.
