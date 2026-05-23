import pandas as pd


class BacktestEngine:
    def __init__(
            self, initial_cash=1000000,
            trade_percent=0.95,
            commission_rate=0.00025,
            stamp_tax_rate=0.001,
            min_commission=5.0
            ):
        self.initial_cash = initial_cash
        self.trade_percent = trade_percent
        self.commission_rate = commission_rate
        self.stamp_tax_rate = stamp_tax_rate
        self.min_commission = min_commission

    def _calc_commission(self, amount):
        """计算佣金，不免5：不足5元按5元收"""
        fee = amount * self.commission_rate
        return max(fee, self.min_commission)

    def run(self, df):
        data = df.sort_index(level="date").copy()

        data["position_signal"] = data["signal"].shift(1)

        data["holdings"] = 0.0
        data["cash"] = self.initial_cash
        data["total"] = 0.0
        data["trade"] = 0.0
        data["commission"] = 0.0
        data["stamp_tax"] = 0.0

        cash = self.initial_cash
        holdings = 0
        prev_signal = 0

        for idx, row in data.iterrows():
            signal = row["position_signal"]
            if pd.isna(signal):
                signal = 0

            if signal != prev_signal:
                if signal == 1 and cash > 0:  # 买入
                    buy_amount = cash * self.trade_percent
                    shares = int(buy_amount / (row["open"] * 100)) * 100
                    if shares > 0:
                        cost = shares * row["open"]
                        commission = self._calc_commission(cost)
                        total_cost = cost + commission
                        if total_cost <= cash:
                            cash -= total_cost
                            holdings += shares
                            data.loc[idx, "trade"] = -total_cost
                            data.loc[idx, "commission"] = commission

                elif signal == -1 and holdings > 0:  # 卖出
                    revenue = holdings * row["open"]
                    commission = self._calc_commission(revenue)
                    stamp_tax = revenue * self.stamp_tax_rate
                    total_revenue = revenue - commission - stamp_tax
                    cash += total_revenue
                    data.loc[idx, "trade"] = total_revenue
                    data.loc[idx, "commission"] = commission
                    data.loc[idx, "stamp_tax"] = stamp_tax
                    holdings = 0

            total_value = cash + holdings * row["close"]
            data.loc[idx, "holdings"] = holdings
            data.loc[idx, "cash"] = cash
            data.loc[idx, "total"] = total_value

            prev_signal = signal

        return data