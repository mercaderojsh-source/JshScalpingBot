import time

from config import (
    START_BALANCE,
    RISK_PER_TRADE,
)

from trading.risk_manager import calculate_levels
from trading.position_sizer import calculate_position_size
from trading.paper_state import load_state, save_state, STATE_FILE
from utils.github_backup import upload_file

# Bitget Taker Fee Rate (0.06% per execution = 0.12% roundtrip)
TAKER_FEE_RATE = 0.0006


class PaperTrader:

    def __init__(self):

        state = load_state()

        if state:
            self.balance = state["balance"]
            self.position = state["position"]
            self.trade_count = state["trade_count"]
            self.wins = state["wins"]
            self.losses = state["losses"]
            self.cooldowns = state["cooldowns"]
            print("💾 Paper account restored.")
        else:
            self.balance = START_BALANCE
            self.position = None
            self.trade_count = 0
            self.wins = 0
            self.losses = 0
            self.cooldowns = {}

    def save(self):

        save_state({
            "balance": self.balance,
            "position": self.position,
            "trade_count": self.trade_count,
            "wins": self.wins,
            "losses": self.losses,
            "cooldowns": self.cooldowns
        })

        upload_file(STATE_FILE, "paper_account.json")

    def in_cooldown(self, pair):

        if pair not in self.cooldowns:
            return False

        return time.time() < self.cooldowns[pair]

    def open_trade(
        self,
        pair,
        direction,
        price,
        atr,
        context=None
    ):

        if self.position is not None:
            return False

        levels = calculate_levels(
            entry_price=price,
            atr=atr,
            direction=direction
        )

        position_size = calculate_position_size(
            balance=self.balance,
            risk_percent=RISK_PER_TRADE,
            entry_price=price,
            stop_loss=levels["stop_loss"]
        )

        # Deduct Bitget entry taker fee
        entry_notional = position_size * price
        entry_fee = entry_notional * TAKER_FEE_RATE
        self.balance -= entry_fee

        self.position = {
            "pair": pair,
            "direction": direction,
            "entry": price,
            "opened_at": price,
            "atr": atr,

            "context": {
                "setup": context.get("setup"),
                "market_state": context.get("market_state"),
                "higher_timeframe": context.get("higher_timeframe"),
                "brain_score": context.get("brain_score"),
                "confidence": context.get("confidence"),
                "momentum": context.get("momentum"),
                "quality": context.get("quality"),
                "trend_strength": context.get("trend_strength"),
                "volatility_score": context.get("volatility_score"),
                "rsi": context.get("rsi"),
                "atr_percent": context.get("atr_percent")
            } if context else {},

            "initial_stop": levels["stop_loss"],
            "stop_loss": levels["stop_loss"],
            "take_profit": levels["take_profit"],

            "size": position_size,
            "remaining_size": position_size,

            "break_even": False,
            "partial_taken": False
        }

        print(f"📈 OPEN {direction} {pair} @ {price}")
        print(f"📦 Position Size : {position_size}")
        print(f"🛑 Stop Loss : {levels['stop_loss']}")
        print(f"🎯 Take Profit : {levels['take_profit']}")
        print(f"💸 Entry Fee Deducted: ${entry_fee:.4f}")

        self.save()

        return self.position

    def execute_trade(
        self,
        pair,
        direction,
        entry_price,
        atr,
        context=None
    ):
        return self.open_trade(
            pair=pair,
            direction=direction,
            price=entry_price,
            atr=atr,
            context=context
        )

    def check_exit(self, current_price):

        if self.position is None:
            return None

        direction = self.position["direction"]
        stop_loss = self.position["stop_loss"]
        take_profit = self.position["take_profit"]

        trailing_only = self.position["partial_taken"]

        if direction == "BUY":
            if not trailing_only and current_price >= take_profit:
                return "TP"
            if current_price <= stop_loss:
                return "SL"
        else:
            if not trailing_only and current_price <= take_profit:
                return "TP"
            if current_price >= stop_loss:
                return "SL"

        return None

    def manage_trade(self, current_price):

        if self.position is None:
            return None

        entry = self.position["entry"]
        initial_stop = self.position["initial_stop"]
        direction = self.position["direction"]

        risk = abs(entry - initial_stop)

        if risk == 0:
            return None

        profit = (current_price - entry) if direction == "BUY" else (entry - current_price)
        r_multiple = profit / risk

        # -----------------------------
        # Stage 1: Break-even at 1.2R (with fee buffer)
        # -----------------------------
        if not self.position["break_even"] and r_multiple >= 1.2:

            fee_buffer = entry * (TAKER_FEE_RATE * 2)

            if direction == "BUY":
                self.position["stop_loss"] = entry + fee_buffer
            else:
                self.position["stop_loss"] = entry - fee_buffer

            self.position["break_even"] = True
            self.save()

            print(f"🛡 Break-even (+Fee Buffer) activated for {self.position['pair']}")

            return "BREAK_EVEN"

        # -----------------------------
        # Stage 2: Partial Take Profit at 2.0R
        # -----------------------------
        if (
            self.position["break_even"]
            and not self.position["partial_taken"]
            and r_multiple >= 2.0
        ):

            partial_size = self.position["remaining_size"] / 2

            gross_pnl = (current_price - entry) * partial_size if direction == "BUY" else (entry - current_price) * partial_size
            exit_fee = (partial_size * current_price) * TAKER_FEE_RATE
            net_pnl = gross_pnl - exit_fee

            self.balance += net_pnl
            self.position["remaining_size"] -= partial_size
            self.position["partial_taken"] = True

            self.save()

            print(f"💵 PARTIAL TAKE PROFIT {self.position['pair']}")
            print(f"Net Realized PnL : ${round(net_pnl, 2)}")
            print(f"Remaining Size : {self.position['remaining_size']:.6f}")
            print(f"Balance : ${round(self.balance, 2)}")

            return {
                "event": "PARTIAL_TP",
                "pair": self.position["pair"],
                "pnl": net_pnl,
                "remaining_size": self.position["remaining_size"],
                "balance": self.balance
            }

        # -----------------------------
        # Stage 3: ATR Trailing Stop
        # -----------------------------
        if self.position["partial_taken"]:

            atr = self.position["atr"]

            if direction == "BUY":
                new_stop = current_price - atr
                if new_stop > self.position["stop_loss"]:
                    self.position["stop_loss"] = new_stop
                    self.save()
                    print(f"📈 Trailing Stop Updated: {self.position['pair']} -> {new_stop:.4f}")
                    return {
                        "event": "TRAILING_STOP",
                        "pair": self.position["pair"],
                        "stop_loss": new_stop
                    }
            else:
                new_stop = current_price + atr
                if new_stop < self.position["stop_loss"]:
                    self.position["stop_loss"] = new_stop
                    self.save()
                    print(f"📉 Trailing Stop Updated: {self.position['pair']} -> {new_stop:.4f}")
                    return {
                        "event": "TRAILING_STOP",
                        "pair": self.position["pair"],
                        "stop_loss": new_stop
                    }

        return None

    def close_trade(self, current_price):

        if self.position is None:
            return None

        entry = self.position["entry"]
        direction = self.position["direction"]
        pair = self.position["pair"]
        size = self.position["remaining_size"]

        gross_pnl = (current_price - entry) * size if direction == "BUY" else (entry - current_price) * size
        exit_fee = (size * current_price) * TAKER_FEE_RATE
        net_pnl = gross_pnl - exit_fee

        self.balance += net_pnl
        self.trade_count += 1

        if net_pnl > 0:
            self.wins += 1
        else:
            self.losses += 1

        print(f"💰 CLOSE {pair}")
        print(f"Net PnL : ${round(net_pnl, 2)}")
        print(f"Balance : ${round(self.balance, 2)}")

        # 5-minute cooldown
        self.cooldowns[pair] = time.time() + 300
        print(f"⏳ {pair} cooldown started (5 minutes)")

        trade = {
            "pair": pair,
            "direction": direction,
            "entry": entry,
            "exit": current_price,
            "pnl": net_pnl,
            "balance": self.balance,
            "stop_loss": self.position["stop_loss"],
            "take_profit": self.position["take_profit"],
            "size": self.position["size"],
            "remaining_size": self.position["remaining_size"],
            "context": self.position.get("context", {})
        }

        self.position = None
        self.save()

        return trade

    def stats(self):

        win_rate = 0 if self.trade_count == 0 else round((self.wins / self.trade_count) * 100, 2)
        active_cooldowns = {}
        now = time.time()

        for pair, expiry in self.cooldowns.items():
            remaining = int(expiry - now)
            if remaining > 0:
                active_cooldowns[pair] = remaining

        return {
            "balance": round(self.balance, 2),
            "trades": self.trade_count,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate": win_rate,
            "cooldowns": active_cooldowns
        }
