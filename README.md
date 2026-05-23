# quant_backtest

基于 Python 的 A 股量化回测框架，支持多只股票、自定义策略、绩效分析和可视化。

## 快速开始

```python
from quant_backtest.data import DataFetcher
from quant_backtest.strategy import MovingAverageCrossStrategy
from quant_backtest.engine import BacktestEngine
from quant_backtest.analysis import PerformanceAnalyzer
from quant_backtest.visualization import BacktestChart
import rqdatac

rqdatac.init()

# 1. 获取数据
fetcher = DataFetcher()
df = fetcher.fetch_one("600000", "20240101", "20260501")

# 2. 生成策略信号
strategy = MovingAverageCrossStrategy(short_window=5, long_window=20)
df = strategy.generate_signals(df)

# 3. 运行回测
engine = BacktestEngine(initial_cash=1000000)
result = engine.run(df)

# 4. 分析绩效
analyzer = PerformanceAnalyzer()
analyzer.generate_report(result)

# 5. 可视化
chart = BacktestChart()
chart.plot_equity_curve(result)
chart.plot_drawdown(result)
```

## 项目结构

```
quant_backtest/
├── data/             # 数据模块
│   ├── data_fetcher.py   # 获取行情数据（rqdatac）
│   ├── data_cache.py     # CSV 缓存管理
│   └── data_cleaner.py   # 数据质量检查
├── strategy/         # 策略模块
│   ├── base_strategy.py         # 抽象策略基类
│   └── moving_average_cross.py  # 双均线交叉策略
├── engine/           # 回测引擎
│   └── backtest_engine.py       # 向量化回测执行
├── analysis/         # 绩效分析
│   └── performance.py           # 夏普比率、最大回撤等指标
├── visualization/    # 可视化
│   └── charts.py               # 权益曲线、回撤图、月度收益
└── tests/            # 单元测试
    └── test_backtest.py
```

## 核心功能

- **数据获取** — 通过 rqdatac 获取 A 股日线行情，自动识别沪市/深市代码格式
- **数据缓存** — 本地 CSV 缓存，避免重复请求，日期类型正确保留
- **策略框架** — 基于抽象基类的策略设计，新增策略只需实现 `generate_signals` 方法
- **回测引擎** — 向量化计算，支持 A 股 T+1 制度、佣金不免五、印花税
- **绩效分析** — 年化收益率、最大回撤、夏普比率、胜率
- **可视化** — 权益曲线、回撤曲线、月度收益率柱状图

## 安装

```bash
pip install rqdatac pandas numpy matplotlib
```

## 数据源

本框架使用 [Ricequant RQData](https://www.ricequant.com/) 作为数据源，需申请账号并配置 token。

```python
import rqdatac
rqdatac.init("your_token")
```

## 依赖

- Python >= 3.10
- pandas
- numpy
- matplotlib
- rqdatac

## 待改进的方向

1.用数据库替代CSV
2.增加滑点
3.多因子选股
4.事件驱动
5.参数优化（网格搜索）