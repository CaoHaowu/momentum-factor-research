# Stooq Independent Replication — Final Summary

## Dataset

- Daily date range: 2018-01-02 to 2026-09-30
- 2,198 daily observations
- 502 matched current S&P 500 securities out of 503
- 105 month-end observations
- minimum valid stocks per month: 464
- common evaluation period: 2018-07-31 to 2026-08-31
- common-period observations: 98 months

## Common-period performance

| Momentum | Annual Return | Sharpe | Max Drawdown | Return t | Return p |
|---|---:|---:|---:|---:|---:|
| 1M | 2.25% | 0.2601 | -22.25% | 0.7432 | 0.2296 |
| 3M | -0.21% | 0.0393 | -19.91% | 0.1123 | 0.4554 |
| 6M | 5.19% | 0.4939 | -13.68% | 1.4115 | 0.0806 |

## IC / RankIC

| Momentum | Mean IC | Mean RankIC | RankIC p |
|---|---:|---:|---:|
| 1M | 0.0172 | 0.0064 | 0.3589 |
| 3M | 0.0127 | -0.0025 | 0.5509 |
| 6M | 0.0337 | 0.0122 | 0.2684 |

## Transaction-cost sensitivity

| Momentum | Cost | Annual Return | Sharpe | Avg Turnover |
|---|---:|---:|---:|---:|
| 1M | 0 bps | 2.25% | 0.2601 | 1.7073 |
| 1M | 5 bps | 1.21% | 0.1650 | 1.7073 |
| 1M | 10 bps | 0.18% | 0.0699 | 1.7073 |
| 1M | 20 bps | -1.86% | -0.1203 | 1.7073 |
| 3M | 0 bps | -0.21% | 0.0393 | 1.0378 |
| 3M | 5 bps | -0.83% | -0.0153 | 1.0378 |
| 3M | 10 bps | -1.44% | -0.0698 | 1.0378 |
| 3M | 20 bps | -2.67% | -0.1790 | 1.0378 |
| 6M | 0 bps | 5.19% | 0.4939 | 0.7335 |
| 6M | 5 bps | 4.73% | 0.4561 | 0.7335 |
| 6M | 10 bps | 4.27% | 0.4182 | 0.7335 |
| 6M | 20 bps | 3.36% | 0.3425 | 0.7335 |

## Interpretation

The 6M specification was the strongest of the three on economic metrics and remained positive under the simplified transaction-cost scenarios. However, its one-sided return p-value was 0.0806 and mean RankIC was only 0.0122, so the evidence is suggestive rather than conventionally strong.

The result should not be interpreted as proof of stable alpha. Train/later-period performance differed materially, rolling RankIC changed sign through time, and the universe uses current constituents rather than point-in-time historical membership.

Project 1 is frozen after this replication to avoid post-hoc parameter tuning.
