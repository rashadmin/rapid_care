import numpy as np
import pandas as pd
import random
import json
import time 
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of Earth in kilometers
    return distance

class get_top():
    def __init__(self):
        self.number = 0
        self.initial_displayed_list = None
        json_file_path = "app/google_places.json"
        with open(json_file_path, 'r') as j:
            self.contents = json.loads(j.read())
    def get_top_5(self):
        print(1)
        time.sleep(4)
        data = pd.DataFrame().from_dict(self.contents['places'])
        data = data[~data['currentOpeningHours'].isna()].reset_index(drop=True)
        lat1, lon1 = 52.6749, -1.14194
        #if data['currentOpeningHours']:
        data['dist_km'] = data['location'].apply(lambda x: haversine(lat1, lon1,x['latitude'],x['longitude']))
        data = data[data['dist_km']<=5].reset_index(drop=True)
        lists = data['displayName'].apply(lambda x : x['text']).to_dict()
        #print(self.contents)
        if self.number == 0:
            self.initial_displayed_list = np.array(random.sample(sorted(lists),k=3))
            self.number+=1
        else:
            accept = random.randint(1,3)
            reject = random.randint(-2,-1)
            selection = {'accept':accept,'reject':reject}
            selected = random.choices(['accept','reject'])
            if selected[0] == 'accept':
                self.initial_displayed_list = np.array(random.sample(sorted(lists),k=min(len(self.initial_displayed_list)+selection[selected[0]],len(lists))))
            elif selected[0] == 'reject':
                if len(self.initial_displayed_list) > 1:
                    if selection[selected[0]]+len(self.initial_displayed_list) > 1:
                        index_to_remove = random.choices(range(0,len(self.initial_displayed_list)),k=abs(selection[selected[0]]))
                        self.initial_displayed_list = np.delete(self.initial_displayed_list,index_to_remove)

        # we create a variable with accept and reject that randomly selects a number
        # we also make random.choice select which variable to use
        # then it is added before showing the sampled data
        return data.iloc[self.initial_displayed_list].sort_values('dist_km')['displayName'].apply(lambda x: x['text']).to_dict()
    