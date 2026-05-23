import pandas as pd
import numpy as np
from quant_backtest.engine import BacktestEngine
from quant_backtest.strategy import MovingAverageCrossStrategy
from quant_backtest.analysis import PerformanceAnalyzer


def test_ma_strategy_profits_in_uptrend():
    """上涨趋势中，双均线策略应该赚钱"""
    dates = pd.date_range("2024-01-01", periods=150, freq="B")
    # 先跌后涨：前50天从12跌到10，后100天从10涨到15
    prices = np.concatenate([
        np.linspace(12, 10, 50),
        np.linspace(10, 15, 100),
    ])

    df = pd.DataFrame({
        "open": prices, "high": prices + 0.1,
        "low": prices - 0.1, "close": prices,
        "volume": 1000000,
    }, index=pd.MultiIndex.from_product(
        [["TEST"], dates], names=["order_book_id", "date"]
    ))
    ...


def test_max_drawdown_never_positive():
    """最大回撤应 ≤ 0（没有负数的回撤）"""
    dates = pd.date_range("2024-01-01", periods=100, freq="B")
    prices = 10 + np.arange(len(dates)) * 0.05

    df = pd.DataFrame({
        "open": prices, "high": prices + 0.1,
        "low": prices - 0.1, "close": prices,
        "volume": 1000000,
    }, index=pd.MultiIndex.from_product(
        [["TEST"], dates], names=["order_book_id", "date"]
    ))

    strategy = MovingAverageCrossStrategy()
    engine = BacktestEngine()
    analyzer = PerformanceAnalyzer()

    df_signal = strategy.generate_signals(df)
    result = engine.run(df_signal)
    max_dd = analyzer.max_drawdown(result["total"])

    assert max_dd <= 0, f"最大回撤应 <= 0，实际为 {max_dd}"
