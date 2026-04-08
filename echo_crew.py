from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.tools import DuckDuckGoSearchRun
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

search_tool = DuckDuckGoSearchRun()

# Agents
researcher = Agent(
    role="Senior AI Research Analyst",
    goal="Identify recent breakthroughs in self-improving agents and recursive systems",
    backstory="Expert at finding and summarizing the latest relevant research.",
    llm=llm,
    tools=[search_tool],
    verbose=True
)

coder = Agent(
    role="Senior Python Engineer",
    goal="Propose clean, safe code improvements to the system",
    backstory="Focuses on creating maintainable and effective modifications.",
    llm=llm,
    verbose=True
)

evaluator = Agent(
    role="System Evaluator",
    goal="Provide honest assessment of proposed changes",
    backstory="Evaluates practicality, safety, and potential impact.",
    llm=llm,
    verbose=True
)

improver = Agent(
    role="Improvement Director",
    goal="Make final decisions on changes and define next steps",
    backstory="Coordinates the overall improvement process.",
    llm=llm,
    verbose=True
)

hyperreflector = Agent(
    role="HyperReflector",
    goal="Analyze conversation trajectory and extract meta-lessons for future improvement",
    backstory="Specialized in learning from the improvement process itself.",
    llm=llm,
    verbose=True
)

# Tasks
research_task = Task(
    description="Find and summarize the 3 most recent relevant papers or breakthroughs on self-improving agents from the last 60 days.",
    expected_output="3 bullet points with brief explanations and sources.",
    agent=researcher
)

code_task = Task(
    description="Based on research, propose specific improvements to echo_crew.py as a unified diff.",
    expected_output="Code block containing a valid unified diff.",
    agent=coder
)

eval_task = Task(
    description="Score the proposed changes from 1-100 and explain the reasoning.",
    expected_output="Overall score with detailed justification.",
    agent=evaluator
)

improve_task = Task(
    description="Give final recommendation on changes and define the next loop goal.",
    expected_output="Clear decision and next iteration goal.",
    agent=improver
)

reflect_task = Task(
    description="Review the full trajectory of this loop and extract 3-5 actionable meta-lessons.",
    expected_output="Bullet list of meta-lessons with specific recommendations.",
    agent=hyperreflector
)

# Crew
echo_crew = Crew(
    agents=[researcher, coder, evaluator, improver, hyperreflector],
    tasks=[research_task, code_task, eval_task, improve_task, reflect_task],
    process=Process.sequential,
    memory=True,
    verbose=2
)

def run_echo():
    print("Starting Echo Swarm v0.2 - Self-Improvement Loop\n")
    result = echo_crew.kickoff()
    print("\n" + "="*80)
    print("LOOP RESULT:")
    print(result)
    print("="*80)

if __name__ == "__main__":
    run_echo()
