from openai import OpenAI
import tempfile
import os
import pygame
from backend.secret import  OPENAI_API_KEY
import time
os.environ["OpenAI_API_KEY"] = OPENAI_API_KEY

# test inputs:
interviewer_role = 'hiring manager'
industry_sector = 'energy'
role_description = 'commercial manager'
time_length = 300
question_list = ['Can you explain your experience with the National Electricity Market and how it has prepared you for this role?'
,'Describe a specific market trend in electricity that you forecasted accurately. What data did you analyze to make your prediction?'
,'How do you approach evaluating market data from various energy markets? Can you give an example of a model you built for market analysis?'
,'Discuss a time when your analysis of risk positions across a portfolio led to a significant business decision. What was the outcome?'
,'What techniques do you employ when assessing the potential value of new revenue contracts?'
,'Can you describe a complex negotiation you led with a counterparty? What strategies did you use to achieve a successful outcome?'
,'How do you balance the interests of your company with those of external stakeholders during a negotiation?'
,'Describe a situation where you had to manage conflicts arising during negotiations. What was your approach?'
,'How do you ensure that your presentations effectively communicate market conditions and portfolio insights to both internal teams and external clients?'
, 'Can you provide an example of how you have built and maintained a strong working relationship with a client or counterparty? What was the key to that relationship?'
, 'What is your approach to identifying and mitigating risks in energy contracts? Can you provide an example?'
, 'Discuss a situation where your risk assessment prevented a potential loss for your organization. What actions did you take?'
, 'How do you incorporate the principles of safety and compliance into your day-to-day operations?'
, 'Describe how you have fostered collaboration within a cross-functional team or across different regions in your past roles.'
, 'What steps do you take to stay updated with changes in the energy market? How do you see yourself growing within EnergyAustralia?']

# prompt:
interviewer_prompt = f'''
You are a professional {interviewer_role}, with deep knowledge of {industry_sector}, and now you are an interviewer for the role {role_description}.
You are expected to have a {time_length}s interview with the candidate, with prepared list of questions {question_list}. 

Please note no need to cover all questions in the preset order, you should be really natural and go with the flow. 

You should always start with thanking the candidate taking the interview, a little bit of the company, and the role.

You should always be very professional and polite, no inappropriate words allowed during the process.

You should aim for natural transition between questions.

You should use diversed style in your words, avoding repetiting patterns. 

You should be mindful about not asking repetitive questions. 
'''


start_time = time.time()
client = OpenAI()
conversation = [{"role": "system", "content": interviewer_prompt}]

while True:
    elapsed_time = time.time() - start_time

    # Check if 300 seconds have passed (5 minutes)
    if elapsed_time >= time_length:
        print("Time's up! Thank you for attending the interview!")
        break



    # start the conversation

    if (elapsed_time < 5) and len(conversation) <= 1:
        instruction = 'Now greet the interviewee and say hello. introduction in less than 20 words'
        conversation[0]["content"] = interviewer_prompt + instruction # update system instruction

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4 model
            messages=conversation,
            # functions=functions,
            # function_call="auto"  # Let the model automatically determine if a function should be called
        )

    else:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye bye']:
            print("Ending conversation.")
            break

        # Add user input to the conversation history
        instruction = 'Now continue the conversation based on user input'

        conversation[0]["content"] = interviewer_prompt + instruction # update system instruction
        conversation.append({"role": "user", "content": user_input})

        # Response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4 model
            messages=conversation,
            # functions=functions,
            # function_call="auto"  # Let the model automatically determine if a function should be called
        )

    # Extract model response
    message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": message})

    print(f"Interviewer: {message}")