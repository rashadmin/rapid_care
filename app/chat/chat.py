from openai import OpenAI
import json
from flask import current_app



class chat():
    def __init__(self,message):

        self.message = json.loads(message)
        self.openai_model = "gpt-3.5-turbo"
        self.bot = '''
                    You are First Aid Bot Bot, an automated service to help with medical emergency till professional help arrives.i want you to follow the steps below \
            Step 1 : You greet the user and ask for  the medical situation the user is experiencing \
            Step 2 : If you get a response to the user, check : is the response a medical situation ?,
                        if yes,Then you say this - `Thank you for sharing that, the information has been sent to the nearest hospital requiring their assitant.\
                                                    I'll provide you with guidance while we wait for professional assistance.Remember, your safety is our top priority.\
                                                    Now, let's focus on getting you the first aid medical assistance you need - `.\`
                        if no, Then you say this - `We only assist with medical situation , we are sorry we can't assist you with that.`
            Step 3 : Carefully, Start a First aid Measure the user will need to take in other to keep the Medical Situation from Escalating, ensure to take note of the following : \
                        a.) Ensure to tell them that they can always ask for further guidance from you if a particular First Aid Measure isn't understood by them .\
                        b.) Ensure You respond in a short, very conversational friendly style.
                        c.) Ensure You return a first aid guidance according to the medical emergency in numerical order, add an entire line filled with asterisk after each number so as to ensure visibility.
            Step 4 : During a point in your conversation, if a user ask for further guidance on what to do about a particular first a step, i want you to do the following below : \
                        i.) Ensure that your textual descriptions are clear, concise, and easy to understand. Use simple language and provide step-by-step instructions.
                        ii.)Keep in mind that users may have different levels of medical knowledge and understanding.it's crucial to gauge user comprehension and offer additional clarification if needed.
            Step 5 : If the user ask for a video, demonstration or anything similar to visual analogy to a particular step, return a json object in the format :
                                        dict('keywords that can be infered synonymous to the step' : [list of similar words related to the keyword])
                    '''
        
    def add_system_message(self):
        self.message.append({"role": 'system', "content": self.bot})
        self.message.append({"role": 'user', "content": 'Hello'})

    def add_user_message(self,prompt):
        self.message.append({"role": "user", "content": prompt})

    def return_all_message(self):
        #self.message = self.message[2:]
        return json.dumps(self.message, indent=2)
    def get_response(self):
        client = OpenAI(api_key = current_app.config['OPEN_AI_API_KEY'])
        full_response = client.chat.completions.create(
        model=self.openai_model,
        messages=self.message,
        temperature=0, # this is the degree of randomness of the model's output
    )
        full_response = full_response.choices[0].message.content
        self.message.append({"role": "assistant", "content": full_response})


    def get_dict_response(self,is_dict_done,text):
        if not is_dict_done:
            client = OpenAI(api_key = current_app.config['OPEN_AI_API_KEY'])
            response = client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {
                "role": "system",
                "content": """
                            You will be given a medical situation message. 
                            return JSON format with the following key value pairs in back ticks
                            
                            
                            `Situation`- `Emergency or Non-Emergency`
                            `Age`-`Based on the age in the given information classify them as pediatric,adult,geriatric, if no age can be infered \
                                    return Not Stated`
                            `Gender` -  `From the medical situation message, kindly infer the gender if no gender can be infered \
                                    return Not Stated``
                            `Surgical Status` - `Preoperative or Post operative or any name for the Surgical Status if no status can be infered \
                                    return Not Stated`` 
                            
                            `Trauma Name`- `Using the message,Classify into one of the trauma categories.e.g Penetrating Trauma
                            `Trauma Description` - `A very short description of the situation in less than 100 characters`
                            `Physicians` - `= `Return a LIST of specially trained surgeons who are responsible for assessing, \
                                                managing, and performing surgery when necessary on patients who have sustained the stated traumatic injuries.
                            `Symptoms`- `Using the message , kindly state out atleast 5 possible observable symptoms that are likely to be a result of the medical situation in a python list`
                            `FirstAid_searchwords` - `Using the message, kindly get at least 7 and at most 10 emergency keywords always return cpr or keywords relating to cpr`
                            - If the given message does not contain a medical related situation simply return `non medical related condition`
                            
                                
                                """
                },
                {
                    "role":"user",
                    "content":f"{text}"
                }
            ],
            temperature=0
            )
            responses = response.choices[0].message.content
            return responses
        return None

        
       