import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

df = pd.read_excel("data/sales_data.xlsx")

total_revenue = df["Revenue"].sum()
average_revenue = df["Revenue"].mean()

best_month = df.loc[df["Revenue"].idxmax()]
worst_month = df.loc[df["Revenue"].idxmin()]

print("Business Summary")
print(f"Total Revenue: ${total_revenue:,.0f}")
print(f"Average Revenue: ${average_revenue:,.0f}")
print(f"Best Month: {best_month['Month']} (${best_month['Revenue']:,.0f})")
print(f"Worst Month: {worst_month['Month']} (${worst_month['Revenue']:,.0f})")

df["MoM Growth %"] = df["Revenue"].pct_change() * 100

print("\nRevenue Trend")
print(df)
latest_month = df.iloc[-1]

summary = f"""
Revenue Summary

Latest Month: {latest_month['Month']}
Revenue: ${latest_month['Revenue']:,.0f}

Total Revenue: ${total_revenue:,.0f}
Average Revenue: ${average_revenue:,.0f}

Best Month: {best_month['Month']}
Worst Month: {worst_month['Month']}
"""

print(summary)
print("\nManagement Summary")

for i in range(1, len(df)):
    
    current_month = df.iloc[i]["Month"]
    growth = df.iloc[i]["MoM Growth %"]
    
    if growth > 10:
        print(
            f"Revenue increased significantly in {current_month} (+{growth:.1f}%)."
        )
        
    elif growth > 0:
        print(
            f"Revenue increased in {current_month} (+{growth:.1f}%)."
        )
        
    else:
        print(
            f"Revenue declined in {current_month} ({growth:.1f}%)."
        )

positive_months = (df["MoM Growth %"] > 0).sum()
negative_months = (df["MoM Growth %"] < 0).sum()

print("\nExecutive Summary")

print(
    f"Revenue reached ${total_revenue:,.0f} across the reporting period, "
    f"with an average monthly revenue of ${average_revenue:,.0f}."
)

print(
    f"The strongest month was {best_month['Month']} "
    f"with revenue of ${best_month['Revenue']:,.0f}, "
    f"while the weakest month was {worst_month['Month']} "
    f"at ${worst_month['Revenue']:,.0f}."
)

print(
    f"Revenue increased in {positive_months} months and declined in {negative_months} months."
)

if positive_months > negative_months:
    print("Overall, revenue showed a generally positive trend.")
elif positive_months < negative_months:
    print("Overall, revenue showed a generally negative trend.")
else:
    print("Overall, revenue showed a mixed trend.")

report = f"""
Executive Summary

Revenue reached ${total_revenue:,.0f} across the reporting period, with an average monthly revenue of ${average_revenue:,.0f}.

The strongest month was {best_month['Month']} with revenue of ${best_month['Revenue']:,.0f}, while the weakest month was {worst_month['Month']} at ${worst_month['Revenue']:,.0f}.

Revenue increased in {positive_months} months and declined in {negative_months} months.
"""

with open(
    "output/executive_summary.txt",
    "w"
) as file:
    file.write(report)

print("Report exported successfully.")
business_data = f"""
Total Revenue: ${total_revenue:,.0f}
Average Revenue: ${average_revenue:,.0f}

Best Month: {best_month['Month']} (${best_month['Revenue']:,.0f})
Worst Month: {worst_month['Month']} (${worst_month['Revenue']:,.0f})

Revenue increased in {positive_months} months and declined in {negative_months} months.
"""

prompt = f"""
You are a senior business analyst.

Based on the following business metrics, write a professional executive summary with:
- Period overview
- Key highlights
- Interpretation
- Recommended next steps
- Conclusion

{business_data}
"""

response = client.responses.create(
    model="gpt-5-mini",
    input=prompt
)

ai_summary = response.output_text

with open(
    "output/ai_executive_summary.txt", "w", encoding="utf-8") as file:
    file.write(ai_summary)

print("\nAI Executive Summary")
print(ai_summary)

print("\nAI report generated successfully.")
plt.figure(figsize=(8, 5))

plt.plot(
    df["Month"],
    df["Revenue"],
    marker="o"
)

plt.title("Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.grid(True)

plt.savefig(
    "output/revenue_trend.png",
    bbox_inches="tight"
)

plt.close()

print("Revenue chart generated successfully.")