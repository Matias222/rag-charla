import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt(prompt: str, model="gpt-4o", max_tokens=1000):

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Provide the best possible response."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling GPT-4o: {e}")
        return None

response = ask_gpt("Does transformers need rnn layers?")
