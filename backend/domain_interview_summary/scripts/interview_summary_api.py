"""
Create an api that when user submit an url, it gives a summary.
"""

from interview_summary_prompt import interview_summary_prompt
from backend.secret import  interview_first_aid_api
from openai import OpenAI
from backend.domain_interview_summary.utils.text_extraction import extract_text_from_url
import os

test_url = "https://www.seek.com.au/job/77885561?ref=search-standalone&type=promoted&origin=showNewTab#sol=b57613bc4a09b8194818326c2390ef0f4bb385c9"

#extract text:
test_content = extract_text_from_url(test_url)

client = OpenAI(api_key= interview_first_aid_api)
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": interview_summary_prompt},
    {"role": "user", "content": f'/job_link: {test_content}'}
  ]
)

output = completion.choices[0].message.content

# output as text for testing
file_path = './test_files/tset_output.txt'
os.makedirs(os.path.dirname(file_path), exist_ok=True)
# Open the file in write mode and write the message
with open(file_path, 'w') as file:
    file.write(output)
