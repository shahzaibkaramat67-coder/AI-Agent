from langchain.agents import create_agent
from dotenv import load_dotenv
from research_tool import duckduckgo_search
from web_reader import read_webpage
from calculator import calculator
from model import resultModel

load_dotenv()

# -----------------------------
# INIT MODELS
# -----------------------------
agent_model = resultModel()
formatter_model = resultModel()





# thiiudbiuw ui1whiuew1 iue1wiud wqiud wudb w dywd w uy w duywbduyqwbduyqyu
# -----------------------------
# AGENT (STAGE 1)
# -----------------------------
agent = create_agent(
    model=agent_model,
    tools=[duckduckgo_search, calculator, read_webpage],
    system_prompt="You are a tool-based research agent. Always use tools and return raw factual results only.",
)

# -----------------------------
# LOOP
# -----------------------------
while True:
    user_input = input("Ask Question: ")

    if user_input.lower() == "exit":
        break

    # -------------------------
    # STAGE 1: TOOL AGENT
    # -------------------------
    raw_result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

    raw_text = raw_result["messages"][-1].content

    # -------------------------
    # STAGE 2: FORMATTER LLM
    # -------------------------
    final_output = formatter_model.stream(
        [
            {
                "role": "system",
                "content": "Convert raw tool output into clean structured report.",
            },
            {
                "role": "user",
                "content": f"""
User Question:
{user_input}

Raw Tool Output:
{raw_text}

Now convert into a clean structured answer with:
- headings
- bullet points
- short summary
""",
            },
        ]
    )

    print("\nFINAL ANSWER:\n")

    for chunk in final_output:
        if chunk.content:
            print(chunk.content, end="", flush=True)
# thi sis laast one 
