from openai import OpenAI
from config import Config
client = OpenAI(api_key = Config['OPEN_AI_API_KEY'])
def generate_other_names(name):
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": 'system', "content":f"""
                            You will be given a name for a particular first aid emergency video
                            return a python list object with the at least 50 similar words or phrases that can be used to search for the videos. 
                            """ },
                {
                "role": "user",
                "content": f'{name}'
                }
            ],
            temperature=0
            )
    responses = response.choices[0].message.content.strip()
    responses = [item.strip() for item in  responses.split('\n') if item.strip()]
    return responses