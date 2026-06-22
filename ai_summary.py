from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

business_data = """
Total Revenue: $1,065,000
Average Revenue: $133,125
Best Month: Aug ($165,000)
Worst Month: Jan ($100,000)

Revenue increased in 5 months and declined in 2 months.
"""

prompt = f"""
You are a business analyst.

Based on the following metrics, write a professional executive summary.

{business_data}
"""

response = client.responses.create(
    model="gpt-5-mini",
    input=prompt
)

print(response.output_text)