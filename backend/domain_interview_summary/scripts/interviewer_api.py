from openai import OpenAI
import tempfile
import os
import pygame
from backend.secret import  OPENAI_API_KEY
import time
import openai
import uuid
import json

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
# interviewer_prompt = f'''
# Context:
# You are a highly professional {interviewer_role} with deep expertise in {industry_sector}. You have been assigned as the interviewer for the {role_description} position at our company.
#
# Objective:
# Your goal is to conduct a structured yet natural {time_length}-second interview, evaluating the candidate’s suitability for the role. You have access to a prepared list of questions: {question_list}, but you are expected to engage in a fluid conversation rather than following the list rigidly.
#
# Audience:
# Your primary audience is candidates interviewing for the role. Maintain a professional, respectful, and welcoming demeanor to create a positive interview experience while effectively assessing their skills, experience, and cultural fit.
#
# Scope:
#
# Opening:
# Begin by thanking the candidate for their time.
# Provide a brief introduction to the company and the role.
#
# Questioning Approach:
# Avoid a rigid question order; instead, adapt dynamically based on the candidate’s responses.
# Use smooth transitions between topics for a natural conversational flow.
# Avoid repetitive or redundant questions.
#
# Communication Style:
# Maintain a professional and polite tone throughout the interview.
# Use diverse phrasing to avoid predictable or robotic speech patterns.
# Ensure clarity in your questions and responses.
# Tone:
#
# Professional yet warm – Engage in a way that encourages the candidate to open up while maintaining professionalism.
# Conversational, not scripted – Avoid sounding robotic or overly rehearsed.
# Neutral and unbiased – Ensure fairness and inclusivity in your questioning.
# '''

interviewer_prompt = f'''
Context:
You are a highly professional {interviewer_role} with deep expertise in {industry_sector}. You are conducting an interview for the {role_description} position at our company.

This is a structured yet dynamic interview, lasting approximately {time_length} seconds. You have access to a prepared list of questions: {question_list}, but instead of following them in a strict order, you will adapt based on the conversation flow.

You are capable of calling functions when necessary to retrieve additional data, generate follow-up questions, or evaluate candidate responses.

Objective (ReAct Thinking Pattern):
You will engage in an interactive, reasoning-based interview by:

Observing: Analyzing the candidate’s responses.
Reasoning: Determining the most relevant next question based on context.
Acting: Either asking a new question,  or calling a function when needed to provide relevant insights,
Interview Flow (Scope & Function Calls):
Opening:

Begin by thanking the candidate for their time.
Provide a brief, engaging introduction to the company and the role.
Ensure the candidate feels comfortable and welcomed.
Questioning Approach (Dynamic & Context-Aware):

Use a structured yet flexible interview approach.
Avoid rigid order – instead, select questions based on the candidate’s responses.
Ensure natural conversation flow, with smooth transitions between topics.
Prevent repetitive or redundant questions.
If a candidate's response is unclear or incomplete, probe further with follow-ups.

Function Calling Capability:

Call get_candidate_profile() if additional background details are needed. -- IGNORE FOR NOW
Call generate_followup_question(previous_answer) to create personalized follow-up questions.  -- IGNORE FOR NOW
Call get_company_info() if the candidate asks for more details about the company, or you want to breifly introduce the company.

'''

# sample function calls
def get_company_info(company_name: str):
    """
    Simulated function to retrieve company details.
    """
    company_data = {
        "EnergyAustralia": "EnergyAustralia is one of the largest energy retailers in Australia, providing electricity and gas services.",
        "Tesla": "Tesla is an American electric vehicle and clean energy company known for its innovations in battery technology and autonomous driving.",
    }
    return company_data.get(company_name, "Company information not found.")


# Define the function schema
functions = [
    {
        "name": "get_company_info",
        "description": "Retrieve details about a company",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "The name of the company to retrieve details for."
                }
            },
            "required": ["company_name"]
        }
    }
]

def convert_to_audio(text_response: str, output_path = "") -> str:
    """
    This function is to convert response from text into audio
    :param text_response: the text input to be converted
    :param output_path: the save path
    :return: the file path for the mp3 file
    """

    audio_response = openai.audio.speech.create(
        model="tts-1",  # Choose the TTS model (e.g., "alloy", "echo", "fable")
        voice="fable",  # Available voices: "alloy", "echo", "fable", etc.
        input= text_response
    )

    # Save the audio to a temporary file
    if output_path == "":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_filename = temp_audio.name  # Get the temporary file path
            temp_audio.write(audio_response.content)  # Write the speech audio to the file

            return temp_filename

    else:

        # Ensure the directory exists
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)

        # If output_path is a folder, generate a random filename
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, f"{uuid.uuid4().hex}.mp3")

        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_response.content)  # Save the speech audio to the specified path

        return output_path


def play_audio(input_file: str):
    """
    This function is just to play the audio
    :param input_file:
    :return:
    """

    # Validate that the file exists and is an .mp3 file
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Error: The file '{input_file}' does not exist.")

    if not input_file.lower().endswith(".mp3"):
        raise ValueError(f"Error: The file '{input_file}' is not an MP3 file.")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the temporary audio file and play it
    pygame.mixer.music.load(input_file)
    pygame.mixer.music.play()

    # Keep the script running until the audio is finished
    while pygame.mixer.music.get_busy():
        pass

    return None


def get_interviewer_response(client, conversation):
    """
    This function is to generate and play in audio of the response from the interviewer
    :return:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using GPT-4 model
        messages=conversation,
        functions=functions,
        function_call="auto"  # Let the model automatically determine if a function should be called
    )

    print(response)


    # firstly check if function calls
    if_function_called = response.choices[0].message.function_call

    if if_function_called is not None:
        function_name = if_function_called.name
        function_args = json.loads(if_function_called.arguments)

        if function_name:
            # Dynamically call the function based on its name
            # function_response = getattr(module_name, function_name)(**function_args)
            function_response = globals()[function_name](**function_args)
            print(function_response)

            # update the memoery
            conversation.append({"role": "assistant", "content": function_response + "now ask a question"})

            # call to get the question
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4 model
                messages=conversation,
                functions=functions,
                function_call="auto"  # Let the model automatically determine if a function should be called
            )

    text_response = response.choices[0].message.content

    # print out the message too
    print(text_response)

    # update the conversation memory
    conversation.append({"role": "assistant", "content": text_response})

    # convert, save and output the audio
    audio_saved_path = convert_to_audio(text_response)

    play_audio(audio_saved_path)

    return None

###################################################### SESSION START
print('Interview start')
start_time = time.time()
client = OpenAI()
conversation = [{"role": "system", "content": interviewer_prompt}]

# start the conversation
start_instruction = ''''Now greet the interviewee and say hello. introduce yourself, the company in less than 20 words
                            and invite the interviewee to introduce him/herself. '''

conversation[0]["content"] = interviewer_prompt + start_instruction # update system instruction

get_interviewer_response(client, conversation)

# continue the conversation
while True:
    elapsed_time = time.time() - start_time

    # Check if 300 seconds have passed (5 minutes)
    if elapsed_time >= time_length:
        print("Time's up! Thank you for attending the interview!")
        break

    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye bye']:
        print("Ending conversation.")
        break

    # Add user input to the conversation history
    instruction = 'Now continue the conversation based on user input'

    conversation[0]["content"] = interviewer_prompt + instruction  # update system instruction
    conversation.append({"role": "user", "content": user_input})

    get_interviewer_response(client, conversation)


    # wrap up the conversation


