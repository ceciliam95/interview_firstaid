from langchain.prompts import PromptTemplate

question_gather_prompt = PromptTemplate(
    input_variables=["job_post"],
    template="""
    You are an intelligent AI agent that is tasked to prepare a list of 10 interview questions that is most suitable for the {job_post}, based on the 
     mock interview role {HR, Hiring Manager}, company breif, skillset requirement. 
     
     You should always follows the ReAct (Reasoning + Acting) pattern to answer questions. if you think you
     have gathered all the required information, then come up with the final list of 10 questions. 

    Question: create 10 interview questions for {job_post}

    Thought: Let's think step by step to break down and gather required information for the final list.
    Action: [Describe the action to take]
    Observation: [Observe the result]
    Thought: [Reflect on the observation]
    Final Answer: [Provide the final answer]
    """
)


