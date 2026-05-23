import matplotlib.pyplot as plt
import pandas as pd


class BacktestChart:
    def __init__(self):
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False

    def plot_equity_curve(self, result_df, benchmark_df=None):
        plt.figure(figsize=(12, 6))
        plt.plot(
            result_df.index.get_level_values("date"),
            result_df["total"],
            label="策略权益",
            color="blue")
        if benchmark_df is not None:
            bench = benchmark_df / benchmark_df.iloc[0] * result_df["total"].iloc[0]
            plt.plot(
                benchmark_df.index,
                bench,
                label="沪深300",
                color="gray",
                alpha=0.7)
        plt.legend()
        plt.title("权益曲线")
        plt.xlabel("日期")
        plt.ylabel("权益")
        plt.grid(True, alpha=0.3)
        plt.show()

    def plot_drawdown(self, result_df):
        equity = result_df["total"]
        rolling_max = equity.cummax()
        drawdown = (equity - rolling_max) / rolling_max

        plt.figure(figsize=(12, 4))
        plt.fill_between(
            result_df.index.get_level_values("date"),
            drawdown,
            0,
            color="red",
            alpha=0.3,
            label="回撤")
        plt.title("回撤曲线")
        plt.ylabel("回撤")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def plot_monthly_returns(self, result_df):
        daily_ret = result_df["total"].pct_change()
        dates = result_df.index.get_level_values("date")
        monthly = daily_ret.groupby([dates.year, dates.month]).sum() * 100

        plt.figure(figsize=(12, 4))
        monthly.plot(kind="bar")
        plt.title("月度收益率")
        plt.ylabel("收益率(%)")
        plt.axhline(y=0, color="black", linewidth=0.5)
        plt.show()
