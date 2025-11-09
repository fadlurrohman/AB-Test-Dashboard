import numpy as np
import pandas as pd

def generate_marketing_data(n_rows: int = 10000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    countries = np.array(['TH', 'TW', 'KR', 'JP', 'SG'])
    channels = np.array(['Google', 'Facebook', 'Twitter', 'Baidu', 'Naver'])
    campaigns = np.array(['Hotel', 'Flight', 'Vacation'])
    devices = np.array(['mobile', 'desktop'])

    dates = pd.date_range('2025-01-01', periods=90, freq='D')
    date_choices = rng.choice(dates, size=n_rows)

    rows = []
    for i in range(n_rows):
        date = date_choices[i]
        country = rng.choice(countries)
        channel = rng.choice(channels)
        campaign = rng.choice(campaigns)
        device = rng.choice(devices)
        group = rng.choice(['A', 'B'])

        base_impr = rng.integers(200, 15000)
        # Make performance slightly different by group and channel
        ctr_base = 0.03 + (0.01 if group == 'B' else 0.0)
        if channel == 'Google':
            ctr_base += 0.01
        elif channel == 'Facebook':
            ctr_base += 0.005

        clicks = rng.binomial(base_impr, min(max(ctr_base, 0.001), 0.3))
        clicks = max(clicks, 1)

        cvr_base = 0.04 + (0.01 if group == 'B' else 0.0)
        conversions = rng.binomial(clicks, min(max(cvr_base, 0.001), 0.4))

        avg_cpc = rng.uniform(0.1, 1.5)
        spend = clicks * avg_cpc

        rows.append({
            "date": date,
            "country": country,
            "channel": channel,
            "campaign": campaign,
            "device": device,
            "group": group,
            "impressions": int(base_impr),
            "clicks": int(clicks),
            "conversions": int(conversions),
            "spend_usd": float(round(spend, 2)),
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv("marketing_data.csv", index=False)
    print(f"Generated marketing_data.csv with {len(df)} rows")
    return df

if __name__ == "__main__":
    generate_marketing_data()
