def volatility_score(atr, price):
    if price <= 0:
        return 0

    return round((atr / price) * 10000, 2)


def rank_pairs(results):
    return sorted(
        results,
        key=lambda x: x["volatility_score"],
        reverse=True
    )