"""Creates reference.csv (normal days) and current.csv (rainy festival week) for Evidently."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
N = 500

#make function
def make(n, time_mu, value_mu, rating_mu, upi_share):
    pay = rng.choice(["UPI", "Card", "Cash"], size=n,
                     p=[upi_share, (1 - upi_share) * 0.45, (1 - upi_share) * 0.55])
    return pd.DataFrame({
        "delivery_time_min": rng.normal(time_mu, 5, n).clip(10, 90).round(1),
        "distance_km": rng.normal(4.0, 1.2, n).clip(0.5, 12).round(1),
        "order_value": rng.normal(value_mu, 90, n).clip(80, 1500).round(0),
        "customer_rating": rng.normal(rating_mu, 0.35, n).clip(1, 5).round(1),
        "items_count": rng.integers(1, 7, n),
        "payment_mode": pay,
    })


# reference = normal days, current = rainy festival week
make(N, 28, 350, 4.4, 0.45).to_csv("reference.csv", index=False)
make(N, 42, 520, 3.7, 0.65).to_csv("current.csv", index=False)
print("Created reference.csv and current.csv (500 rows each)")