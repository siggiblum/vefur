import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

data = [
    ["RIKB 24 0415", 98.625000, 98.710000, 10.121832, 1, 0.174775, 69, "2024-04-15"],
    ["RIKB 25 0612", 98.950000, 99.070000, 8.797499, 1, 1.272446, 127, "2025-06-12"],
    ["RIKB 26 1015", 97.000000, 97.190000, 8.010518, 1, 2.499648, 252, "2026-10-15"],
    ["RIKB 28 1115", 91.350000, 91.585000, 7.197403, 1, 4.294504, 283, "2028-11-15"],
    ["RIKB 31 0124", 98.225000, 98.600000, 6.827343, 1, 5.794940, 353, "2031-01-24"],
    ["RIKB 42 0217", 79.700000, 80.450000, 6.434300, 1, 11.404116, 11, "2042-02-17"],
    ["RIKS 26 0216", 95.950000, 96.185000, 3.606995, 1, 1.968860, 10, "2026-02-16"],
    ["RIKS 30 0701", 102.485000, 102.900000, 2.818276, 1, 5.560478, 146, "2030-07-01"],
    ["RIKS 33 0321", 102.775000, 103.305000, 2.652919, 1, 7.530562, 44, "2033-03-21"],
    ["RIKS 37 0115", 85.200000, 85.770000, 2.338693, 1, 12.024966, 344, "2037-01-15"],
    ["RVKN 35 1", 92.665000, 93.350000, 7.860138, 2, 7.686296, 49, "2035-03-26"],
    ["RVK 32 1", 93.100000, 93.935000, 3.419470, 4, 7.806886, 75, "2032-10-21"],
    ["RVK 53 1", 111.800000, 113.350000, 3.775122, 2, 13.796831, 125, "2053-12-10"],
    ["RVKG 48 1", 87.000000, 88.070000, 3.145621, 2, 18.182083, 75, "2048-10-21"],
    ["OR180255 GB", 92.200000, 92.990000, 2.989111, 1, 20.692547, 12, "2055-02-18"],
    ["OR020934 GB", 89.600000, 90.350000, 2.852709, 1, 9.636367, 129, "2034-09-02"],
    ["OR180242 GB", 82.200000, 83.400000, 6.146622, 2, 6.369581, 12, "2042-02-18"],
    ["RVKN24 1", np.nan, np.nan, 10.271807, 2, 0.270120, 95, "2024-05-11"],
    ["RVKNG 40 1", np.nan, np.nan, 7.228395, 1, 10.892690, 197, "2040-08-21"],
    ["OR090546", np.nan, np.nan, 3.618318, 2, 15.819347, 93, "2046-05-09"]
]

columns = ["Nafn", "BID", "ASK", "YLD_YTM_BID", "CPN_FREQ", "DUR_MID", "DAYS_TO_NEXT_COUPON", "FINAL_MATURITY"]


# Create the DataFrame
df = pd.DataFrame(data, columns=columns)

riks_bonds = df[df['Nafn'].str.contains('RIKS')]
rikb_bonds = df[df['Nafn'].str.contains('RIKB')]
riks_bonds = riks_bonds.sort_values(by=["DUR_MID"])
rikb_bonds = rikb_bonds.sort_values(by=["DUR_MID"])

# Fyrir CubicSpline, sameina rikb_bonds og riks_bonds ef þörf er á
# Notum hér rikb_bonds sem dæmi. Gakktu úr skugga um að gögnin innihaldi ekki NaN gildi í viðkomandi dálkum
x = rikb_bonds["DUR_MID"].dropna()
y = rikb_bonds["YLD_YTM_BID"].dropna()

# Ef þú vilt nota gögn úr bæði riks_bonds og rikb_bonds, þarftu að sameina þau gögn áður.
# Passaðu að gögnin séu í réttri röð og án NaN gilda

if len(x) > 0 and len(x) == len(y):  # Gakktu úr skugga um að lengdir séu eins og ekki tómar
    cs = CubicSpline(x, y)
    # Til að sýna Cubic Spline ávöxtunarkúrvu
    xs = np.linspace(x.min(), x.max(), 200)
    ys = cs(xs)
    plt.figure(figsize=(10, 6))
    plt.plot(xs, ys, label="Cubic Spline Interpolated Curve")
    plt.scatter(x, y, color='red', label="Original Data")
    plt.title("Cubic Spline Interpolation of Yield Curve")
    plt.xlabel("Duration (MID)")
    plt.ylabel("Yield (YTM_BID)")
    plt.legend()
    plt.show()
else:
    print("Data for Cubic Spline interpolation is not valid.")

new_durations = np.array([3, 7, 12])  # Example durations

# Use the CubicSpline object to estimate yields for these new durations
estimated_yields = cs(new_durations)

# Print the estimated yields
for duration, yield_ in zip(new_durations, estimated_yields):
    print(f"Estimated yield for duration {duration}: {yield_:.4f}")