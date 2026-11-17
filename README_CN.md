# 横截面动量因子研究

[English README](README.md)

## 项目简介

本项目从课程式 Momentum Trading 练习出发，扩展为一个小型量化因子研究，核心问题是：过去收益能否预测下一月股票的横截面收益，以及这种表现能否通过统一样本期、统计检验、换手率和交易成本检验。

项目分为两阶段：

1. **QuoteMedia baseline**：2013-2017 教学数据复现与修正。
2. **Stooq 独立复测**：2018-2026 更晚时期、第二数据源上的独立检验。

目标不是证明“发现了可盈利策略”，而是形成一个能够解释研究设计、结果、失败点和局限性的完整因子研究项目。

## 研究方法

- 日频 Close 重采样到月末。
- 构造 1M、3M、6M 简单收益 Momentum 因子。
- 每月做多因子排名前 50、做空后 50。
- 月末 t 只使用当时已知信息构建仓位，用 t+1 收益评价。
- 调仓时 50% 多头 + 50% 空头，总名义敞口 100%，净美元敞口约为 0。
- 三个窗口统一到共同可评价区间。
- 评价年化收益、Sharpe、最大回撤、单侧收益 t-test、Pearson IC、Spearman RankIC。
- 测试 0 / 5 / 10 / 20 bps 的简化交易成本。

组合是 **dollar-neutral**，但没有显式做到 beta-neutral、sector-neutral 或其他风险中性化。

## 数据集 1：QuoteMedia baseline

本地教学数据：

- 2013-07-01 至 2017-06-30
- 495 个 ticker
- 490,737 条 ticker-date 记录
- 1,009 个日频日期
- 月末采样后 48 个月

共同评价期：**2014-01-31 至 2017-05-31，共 41 个月**。

| 窗口 | 年化收益 | Sharpe | 最大回撤 | Return p-value | Mean RankIC |
|---|---:|---:|---:|---:|---:|
| 1M | -2.67% | -0.4199 | -11.16% | 0.7789 | -0.0308 |
| 3M | -0.14% | 0.0151 | -10.63% | 0.4889 | -0.0234 |
| 6M | +0.28% | 0.0737 | -9.24% | 0.4462 | -0.0070 |

该样本中三个策略都较弱。6M 相对最好，但其绝对收益、Sharpe 和 RankIC 都很低。

## 数据集 2：Stooq 独立复测

本地处理 Stooq U.S. daily bulk data，并与当前 S&P 500 成分列表匹配。

最终数据：

- 2018-01-02 至 2026-09-30
- 2,198 个交易日
- 503 只目标股票中成功匹配 502 只
- 105 个月度观察
- 任一月份最少有效股票数 464
- 共同评价期：**2018-07-31 至 2026-08-31，共 98 个月**

### 最终共同样本表现

| 窗口 | 年化收益 | Sharpe | 最大回撤 | Return t | Return p | Mean IC | Mean RankIC |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1M | +2.25% | 0.2601 | -22.25% | 0.7432 | 0.2296 | 0.0172 | 0.0064 |
| 3M | -0.21% | 0.0393 | -19.91% | 0.1123 | 0.4554 | 0.0127 | -0.0025 |
| 6M | **+5.19%** | **0.4939** | **-13.68%** | **1.4115** | **0.0806** | **0.0337** | **0.0122** |

### 交易成本敏感性

| 策略 | 0 bps | 5 bps | 10 bps | 20 bps | 平均月度 Turnover |
|---|---:|---:|---:|---:|---:|
| 1M | +2.25% | +1.21% | +0.18% | -1.86% | 1.7073 |
| 3M | -0.21% | -0.83% | -1.44% | -2.67% | 1.0378 |
| 6M | **+5.19%** | **+4.73%** | **+4.27%** | **+3.36%** | **0.7335** |

### Earlier / Later split

在查看最终结果前固定：

```
split_date = 2023-01-01
```

| 窗口 | Earlier Sharpe | Later Sharpe | Later 年化收益 |
|---|---:|---:|---:|
| 1M | -0.4092 | 1.0156 | 11.20% |
| 3M | -0.0369 | 0.1403 | 0.97% |
| 6M | 0.2141 | 0.8029 | 9.53% |

Earlier / Later 差异很大，说明因子具有明显 **regime dependence**，不能把后段表现直接解释成稳定 alpha。

## 核心结论

1. **两个样本中 6M 都是三种定义里相对最好的一种。**  
   但 QuoteMedia 样本中 6M 绝对表现仍很弱；Stooq 更晚时期明显改善。

2. **经济表现比统计证据更强。**  
   Stooq 样本的 6M 年化约 5.2%、Sharpe 约 0.49、单侧收益 p-value = 0.0806。它具有一定 suggestive evidence，但没有达到传统 5% 显著性标准。

3. **Turnover 是非常明确的实施约束。**  
   1M 换手约 1.71/月，在交易成本下收益迅速消失；6M 换手约 0.73/月，在简化 20 bps 成本情景下年化仍约 3.36%。

4. **RankIC 并不强。**  
   即使 6M 的组合表现较好，Mean RankIC 也只有 0.0122，而且 rolling RankIC 随时间多次正负切换。这说明预测能力较弱且具有时间变化。

因此更合适的表述不是“发现了稳定可盈利 Momentum”，而是：

> Across both samples, the 6M specification ranked relatively better than 1M and 3M, but its absolute effectiveness was strongly sample-dependent.

## Repo 中的代码

- `P1-002_prepare_stooq.py`：把本地 Stooq U.S. daily bulk files 处理成研究用价格矩阵。
- `section_18_reporting.py`：输出最终 performance、transaction cost、NAV、drawdown 与 rolling RankIC。
- 原始 Stooq / QuoteMedia 行情数据不上传到公开仓库。

## 局限

- 使用当前 S&P 500 成分股回看历史，而不是 point-in-time historical membership，存在 survivorship / selection bias。
- 普通 t-test 尚未使用 HAC / Newey-West 标准误，也没有进行 multiple-testing adjustment。
- 未做 Beta / 行业中性化。
- 没有显式模拟流动性、融券成本、滑点、market impact。
- Turnover 基于目标权重变化，没有模拟月内持仓权重漂移。
- 6M 的 RankIC 仍然较弱。
- 看到结果后继续大量搜索其他 Momentum horizon 会引入 data snooping。

## 项目状态

**Project 1 到此冻结。**

point-in-time universe、beta/sector neutralization、HAC、更多 horizon 等均列入 Future Work，而不在当前样本上继续事后调参。

下一项目：**Multi-Factor + Machine Learning**。

## 致谢

项目起点来自 Udacity *AI for Trading — Trading with Momentum*。多窗口比较、统一样本期、独立数据源复测、交易成本敏感性、IC/RankIC 和最终报告属于后续扩展。

仅用于学习与研究，不构成投资建议。
