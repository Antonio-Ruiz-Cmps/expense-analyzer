import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Load data ──────────────────────────────────────────────
df = pd.read_csv("gastos.csv", parse_dates=["date"])

# ── Basic stats ────────────────────────────────────────────
total     = df["amount"].sum()
avg_month = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().mean()
top_cat   = df.groupby("category")["amount"].sum().idxmax()

print(f"Total spent   : ${total:,.2f}")
print(f"Monthly avg   : ${avg_month:,.2f}")
print(f"Top category  : {top_cat}")

# ── Monthly summary ────────────────────────────────────────
monthly = (
    df.groupby([df["date"].dt.to_period("M"), "category"])["amount"]
    .sum()
    .unstack(fill_value=0)
)

# ── Plot 1: spending by category (pie) ─────────────────────
cat_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Personal Expense Analyzer", fontsize=14, fontweight="bold")

axes[0].pie(
    cat_totals,
    labels=cat_totals.index,
    autopct="%1.1f%%",
    startangle=140,
)
axes[0].set_title("Spending by Category")

# ── Plot 2: monthly trend (bar) ────────────────────────────
monthly_total = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
monthly_total.index = monthly_total.index.astype(str)

axes[1].bar(monthly_total.index, monthly_total.values, color="#378ADD")
axes[1].set_title("Monthly Total")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Amount (USD)")
axes[1].yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("expense_report.png", dpi=150)
plt.show()
print("Chart saved as expense_report.png")
