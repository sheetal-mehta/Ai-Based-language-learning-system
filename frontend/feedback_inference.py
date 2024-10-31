import os
import together
from together import Together
from dotenv import load_dotenv
import time
import logging

load_dotenv()

API_KEY = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=API_KEY)

def ensemble_approach(data,correction):
    attempt= 0
    retries = 5
    backoff_factor=1.5
    while attempt < retries:
        try:
            response = together.Completion.create(
                        #model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                        model= "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                        prompt=f"data- {data} Correction - {correction} correct grammar if required in the correction. only give the coreected sentence in response, do not add any other information. Just give corrected sentence",
                        max_tokens=1000,
                        temperature=0.7,
                        top_k=50,
                        repetition_penalty=1
                    )
            return response.choices[0].text
        except (together.error.APIError, together.error.APIConnectionError, together.error.InvalidRequestError) as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(backoff_factor ** attempt)

        # If all retries fail, raise exception
        raise Exception(f"Failed to complete after {retries} retries")
     
     # getting feedback from llm by passing data and correction pair.
def get_feedback_llm(data,correction):
    attempt= 0
    retries = 5
    backoff_factor=1.5
    while attempt < retries:
        try:
            response = together.Completion.create(
                        #model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                        model= "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                        prompt=f"data- {data} Correction - {correction} from the give data and correction pair, point out and explain the grammatical error in short. do not repeat same thing in the response.",
                        max_tokens=500,
                        temperature=0.7,
                        top_k=50,
                        repetition_penalty=1
                    )
            return response.choices[0].text
        except (together.error.APIError, together.error.APIConnectionError, together.error.InvalidRequestError) as e:
                logging.warning(f"Attempt {attempt + 1} failed: {e}")
                attempt += 1
                time.sleep(backoff_factor ** attempt)

        # If all retries fail, raise an exception
        raise Exception(f"Failed to complete after {retries} retries")
