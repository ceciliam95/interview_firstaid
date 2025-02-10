"""
Create an api that when user submit an url, it gives a summary.
"""

# from interview_summary_prompt import question_gather_prompt
from backend.secret import  OPENAI_API_KEY
from backend.domain_interview_summary.utils.text_extraction import extract_text_from_url
import os
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.prompts import PromptTemplate
from langchain.tools import Tool

test_url = "https://www.seek.com.au/job/77885561?ref=search-standalone&type=promoted&origin=showNewTab#sol=b57613bc4a09b8194818326c2390ef0f4bb385c9"

os.environ["OpenAI_API_KEY"] = OPENAI_API_KEY

#extract text:
test_content = extract_text_from_url(test_url)

# create teh llm
llm = ChatOpenAI(model_name = "gpt-4o-mini", temperature = 1)

# define tool functions
def ask_question(question: str) -> str:
    """
    Displays the question, asks for user input, and returns the user's response.

    :param question: The question to ask the user.
    :return: The user's input as a string.
    """
    print(question)
    user_response = input(f"Your answer: ")
    return user_response

ask_question_tool = Tool(
    name="ask_question",
    func=ask_question,
    description="Ask the user a question and return their response."
)

# tools list

tools = [ask_question_tool]
tool_names = ", ".join([tool.name for tool in tools])
agent_scratchpad = ""  # Start with an empty scratchpad

# create prompt template:
question_gather_prompt = PromptTemplate(
    input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
    template="""
    You are an intelligent AI agent that is tasked to prepare a list of 15 interview questions that is most suitable for the input.
    
    The prepared list of questions should consider following factors:
    - mock interview role (e.g. HR, Hiring Manager), 
    - company breif, 
    - skillset requirement
    - mock interview purpose (e.g. if this is a technical interview, behaviour interview, or balanced) 

     You should always follows the ReAct (Reasoning + Acting) pattern to answer questions. You action should be one of {tools}, unless you think you
     have gathered all the required information, then come up with the final list of 10 questions. If you think you are unclear about factors listed above, 
     then use "ask_clarifying_questions" from {tools}, but clarify each point at most once.
    
    Question: create 10 interview questions for {input}
    Available tools: {tool_names}

    Thought: Let's think step by step to break down and gather required information for the final list.
    Action: [Describe the action to take]
    Observation: [Observe the result]
    Thought: {agent_scratchpad}
    Final Answer: [Provide the final answer]
    """
)

# create reAct agent:
agent = create_react_agent(llm, tools, question_gather_prompt)

agent_executor = AgentExecutor(agent = agent, tools = tools, verbose = True)

test_input = {
    "input": test_content,  # Replace with actual job post
    "tools": tools,
    "tool_names": tool_names,
    "agent_scratchpad": ""  # Start with an empty scratchpad
}

agent_executor.invoke({"input": test_input})
