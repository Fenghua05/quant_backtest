import pandas as pd
import math
class PerformanceAnalyzer:
    def __init__(self,risk_free_rate=0.02):
        self.risk_free_rate=risk_free_rate

    def annual_return(self,total_return,days):#年化
        annual=(1+total_return)**(250/days)-1
        return annual

    def max_drawdown(self,equity_curve):#最大回撤
        rolling_max = equity_curve.cummax()
        drawdown=(equity_curve-rolling_max)/rolling_max
        max_dd=drawdown.min()
        return max_dd

    def sharpe_ratio(self, daily_returns):#夏普比率
        annual_ret = daily_returns.mean() * 250
        annual_vol = daily_returns.std() * math.sqrt(250)
        return (annual_ret - self.risk_free_rate) / annual_vol
    
    def win_rate(self,trades_df):
        buy_cost=None
        win_count=0
        total_count=0
        for _,row in trades_df.iterrows():
            trade_val = row["trade"]
            if trade_val < 0:
                buy_cost = abs(trade_val)
            elif trade_val > 0 and buy_cost is not None:
                sell_income = trade_val
                profit = sell_income-buy_cost
                total_count += 1

                if profit > 0:
                    win_count += 1
                buy_cost = None
        if total_count == 0:
            wr = 0.0
        else:
            wr = win_count/total_count
        return wr


    def generate_report(self,result_df):#完整报告
        equity_curve=result_df["total"]
        initial_cash=result_df["total"].iloc[0]
        final_equity=result_df["total"].iloc[-1]
        total_return=(final_equity-initial_cash)/initial_cash
        days=len(result_df)
        daily_return = result_df["total"].pct_change()
        trades_df=result_df[result_df["trade"]!=0].copy()
        ar = self.annual_return(total_return,days)
        md = self.max_drawdown(equity_curve)
        sr = self.sharpe_ratio(daily_return)
        wr = self.win_rate(trades_df)
        print("年化收益率为：",ar)
        print("最大回撤为：",md)
        print("夏普比率为：",sr)
        print("胜率为：",wr)
        