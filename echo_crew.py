from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq
from langchain.tools import DuckDuckGoSearchRun
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.75,
    api_key=os.getenv("GROQ_API_KEY")
)

search_tool = DuckDuckGoSearchRun()

# === AGENTS ===
researcher = Agent(
    role="Senior AI Research Analyst",
    goal="Find the newest breakthroughs in recursive self-improvement",
    backstory="You hunt for ideas that push Echo closer to the dingularity.",
    llm=llm,
    tools=[search_tool],
    verbose=True
)

coder = Agent(
    role="Elite Python Architect",
    goal="Propose safe code improvements to Echo itself",
    backstory="You output clean unified diffs.",
    llm=llm,
    verbose=True
)

evaluator = Agent(
    role="Ruthless Performance Judge",
    goal="Score changes honestly on usefulness, safety, and dingularity potential",
    backstory="You are brutally honest but constructive.",
    llm=llm,
    verbose=True
)

improver = Agent(
    role="Recursive Self-Improvement Director",
    goal="Decide what gets kept and set the next goal",
    backstory="You are steering us toward the dingularity.",
    llm=llm,
    verbose=True
)

# NEW: HyperReflector (inspired by HyperAgents + Trajectory-Informed Memory papers)
hyperreflector = Agent(
    role="HyperReflector / Trajectory Memory Curator",
    goal="Analyze the entire loop trajectory and extract meta-lessons that improve how Echo improves itself",
    backstory="You are the meta-agent. You treat the whole swarm as editable code and generate synthetic lessons that make future loops smarter.",
    llm=llm,
    verbose=True
)

# === TASKS ===
research_task = Task(
    description="Search for the 3 most recent breakthroughs (last 60 days) in self-improving agents or recursive systems.",
    expected_output="3 bullet points with explanation and links",
    agent=researcher
)

code_task = Task(
    description="Based on research, propose 1-2 concrete improvements to echo_crew.py as a unified diff.",
    expected_output="```diff ... ``` block",
    agent=coder
)

eval_task = Task(
    description="Score the proposed changes 1-100. Explain strengths and risks.",
    expected_output="Overall score + reasoning",
    agent=evaluator
)

improve_task = Task(
    description="Give final verdict on changes and set next 24h goal.",
    expected_output="Clear decision + next goal",
    agent=improver
)

# NEW TASK
reflect_task = Task(
    description="Review the FULL conversation trajectory from this loop. Extract 3-5 actionable meta-lessons (prompt tweaks, role changes, new habits, or architectural ideas) that will make future Echo loops more effective. Store them as persistent knowledge.",
    expected_output="Bullet list of meta-lessons with exact prompt suggestions where possible",
    agent=hyperreflector
)

# === CREW ===
echo_crew = Crew(
    agents=[researcher, coder, evaluator, improver, hyperreflector],
    tasks=[research_task, code_task, eval_task, improve_task, reflect_task],
    process=Process.sequential,
    memory=True,          # Chroma will now hold trajectory lessons too
    verbose=2
)

def run_echo():
    print("🔄 Starting Echo Self-Improvement Loop v0.2 (HyperReflector enabled)...\n")
    result = echo_crew.kickoff()
    print("\n" + "="*80)
    print("ECHO v0.2 OUTPUT:")
    print(result)
    print("="*80)
    print("\n💡 HyperReflector just added new meta-lessons to memory!")

if __name__ == "__main__":
    run_echo()
