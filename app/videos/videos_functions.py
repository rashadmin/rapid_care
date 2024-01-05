from openai import OpenAI
from flask import current_app
import requests

def generate_other_names(name):
    client = OpenAI(api_key = current_app.config['OPEN_AI_API_KEY'])
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



def return_url(query):
    api_key = current_app.config["YOUTUBE_API_KEY"]
    url = ('https://youtube.googleapis.com/youtube/v3/search?'\
                        'part=snippet&'\
                        'maxResults=1&'\
                        'order=relevance&'\
                        f'q=medical first aid for {query}&'\
                        'type=video&'\
                        'videoDuration=short&'\
                        'videoEmbeddable=true&'\
                        f'key={api_key}')
    response = requests.get(url)
    if response.status_code == 200:
        data =  response.json()['items']
        url_links = {data[i]['snippet']['title']:f"https://youtu.be/{data[i]['id']['videoId']}" for i in range(len(data))}
        return url_links
    return False




