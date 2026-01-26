# Suggesting 10 top stocks for 2026
# Multi Agent System for Stock Recommendation
from crewai import Agent, Task, Crew
import os
from utils import get_openai_api_key, get_serper_api_key

from crewai_tools import ScrapeWebsiteTool, SerperDevTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Market Sentiment Evaluator

market_sentiment_agent = Agent(
    role="Market Sentiment Evaluator",
    goal="Analyze and interpret financial news articles",
    tools = [scrape_tool, search_tool],
    backstory="You are a experience indian stock market analyzer."
        "You have proven track record of analyzing indian stock by looking at relevant news articles for each company and assess their sentiment critically."
        "You have experience in managing portfolio stocks while managing risk and rewards, with successful profit of 25% every year"
        "You have suggest 10 stocks for a new user entering stock market with a capital of 1 lakhs"
        "Suggested stocks will be analyzed by financial insights agent.",
    verbose=True
)


# Financial Insights Agent

financial_data_agent = Agent(
    role="Financial Insights Agent",
    goal="Extract and analyze essential company financial data of the stocks suggested by market sentiment agent",
    tools = [scrape_tool, search_tool],    
    backstory="You have experince in gathering stock prices, analyst ratings, and key financial metrics."
        "Gather key financial ratios, income statements, balance sheets, cash flow reports, and historical price data."
        "Highlight company fundamentals and trends, structuring the data in tables with meaningful insights."
        "Your goal is emphasize company fundamentals and trends, structuring the data in tables with meaningful insights."
        "Please financially analyze the stocks suggested by the market sentiment agent",
     verbose=True
)

# Task for market_sentiment_agent

market_sentiment_task = Task(
    description=("Suggest 10 stocks sorted based on the analysis."),
    expected_output="10 stocks for buying"
                    "Reason for suggesting the stocks"
                    "Expected profit for the stocks"
                    "Rate the stocks out of 10 considering market, company and financial trends",
    agent=market_sentiment_agent,                  
)

# Task for financial_data_agent

financial_data_task = Task(
    description=("Critically analyze the stocks provided by the market_sentiment_agent"),
    expected_output="Show the financial strength of each stock"
                    "Suggest the reason for buying the stock"
                    "How long should I hold this stock",
    agent=financial_data_agent,                  
)
crewaman = Crew(
    agents=[market_sentiment_agent, financial_data_agent],       
    tasks=[market_sentiment_task, financial_data_task],
    verbose=2
)

result = crewaman.kickoff()
