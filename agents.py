from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import scrape_webpage,duckduckgo_search
import os
from dotenv import load_dotenv
load_dotenv()

load_dotenv()
ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def build_research_agent():
    return create_agent(
        model=llm,
        tools=[duckduckgo_search],
        system_prompt="""You are a research agent.Search the web for relevant information using DuckDuckGo.Find useful and reliable sources.""")

# 2nd agent

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_webpage],
        system_prompt="""You are a web page reader agent.Your job is to read and analyze web pages using the scrape_webpage tool.Extract the important information from the page.Ignore irrelevant content.Do not invent information.""")

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
        "You are a sharp and constructive research critic. "
        "Be honest and specific."
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
