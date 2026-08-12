import os
import streamlit as st
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import scrape_webpage, duckduckgo_search

load_dotenv()

# Get key from st.secrets if using Streamlit secrets, or fallback to environment variable
api_key = st.secrets.get("GOOGLE_API_KEY") if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets else os.getenv("GOOGLE_API_KEY")

# Initialize Gemini 1.5 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=api_key
)

def build_research_agent():
    return create_react_agent(
        model=llm,
        tools=[duckduckgo_search],
        prompt="You are a research agent. Search the web for relevant information using DuckDuckGo. Find useful and reliable sources."
    )

# 2nd agent
def build_reader_agent():
    return create_react_agent(
        model=llm,
        tools=[scrape_webpage],
        prompt="You are a web page reader agent. Your job is to read and analyze web pages using the scrape_webpage tool. Extract important information. Ignore irrelevant content. Do not invent information."
    )

writer_prompt = ChatPromptTemplate.from_template("""
You are a professional research report writer.

Based on the research below:

{research}

Structure the report as:

- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.
""")

writer_chain = writer_prompt | llm | StrOutputParser()

# Critic Chain
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Be honest and specific."
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Accuracy Issues:
- ...

Missing Information:
- ...

Final Recommendation:
- APPROVE
- REVISE
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()
