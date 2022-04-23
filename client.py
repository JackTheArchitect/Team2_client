from flask import Flask, render_template, request
import requests
import pandas as pd
import random
import json
import numpy as np


# Load X_test, y_test
X_test = pd.read_pickle('./static/X_test.pkl')
y_test = pd.read_pickle('./static/y_test.pkl')
features_df = pd.read_pickle('./static/features_df.pkl')
# X_test = pd.read_pickle('/home/jackim2/mysite/static/X_test.pkl')
# y_test = pd.read_pickle('/home/jackim2/mysite/static/y_test.pkl')
# features_df = pd.read_pickle('/home/jackim2/mysite/static/features_df.pkl')


# Merge the X_test, y_test again so we can make one json obect
df = X_test.assign(Status=y_test)

# Convert df into one json object
df_json = df.to_json(orient='records')

# backend api url
# url = "http://jackim.pythonanywhere.com"
url ="http://localhost:5000"



app = Flask(__name__)
# app = Flask(__name__, template_folder='/home/jackim2/mysite/templates/')

@app.route("/", methods=['GET', 'POST'])
def home():
    Primary_Offence = features_df['Primary_Offence'].unique().tolist()
    diff = np.arange(-364, 256, 1).tolist()
    Premises_Type = features_df['Premises_Type'].unique().tolist()
    # Cost_of_Bike = features_df['Cost_of_Bike'].unique().tolist()
    Occurrence_DayOfWeek = features_df['Occurrence_DayOfWeek'].unique().tolist()
    # Occurrence_Year = features_df['Occurrence_Year'].unique().tolist()
    Report_Hour = np.arange(1, 24, 1).tolist()
    Occurrence_Month = features_df['Occurrence_Month'].unique().tolist()
    Location_Type = features_df['Location_Type'].unique().tolist()
    NeighbourhoodName = features_df['NeighbourhoodName'].unique().tolist()
    Longitude = np.arange(-79.99, -78.00, 0.001).tolist()
    Latitude = np.arange(43.50, 43.99, 0.001).tolist()
    return render_template('index.html', Primary_Offence = Primary_Offence, diff = diff, Premises_Type = Premises_Type, 
    Occurrence_DayOfWeek = Occurrence_DayOfWeek, Report_Hour=Report_Hour, Occurrence_Month=Occurrence_Month, 
    Location_Type = Location_Type,NeighbourhoodName = NeighbourhoodName, Longitude = Longitude ,Latitude = Latitude)# render_template only takes the name of the file itself. NO path
    



@app.route("/get_score")
def get_score():
    r = requests.post(url = (url + "/run"), json= df_json )
    json_string = r.content
    data = json.loads(json_string)
    score = data['Model Score']
    return render_template("score.html", score = score)



@app.route("/get_prediction1", methods=['GET', 'POST'])
def get_prediction1():
    
    rnd_index = random.randrange(0, df.shape[0]-1, 1)
    X_instance = X_test.iloc[rnd_index : rnd_index+1, :] # [rnd_index : rnd_index+1, :] is to keep X_instance as a dataframe, not series
    y_instance = y_test.iloc[rnd_index]

    x_dict = {}

    for each in X_instance.columns:
        x_dict[each] = X_instance[each].values[0]

    X_instance.insert(12, "Status", [y_instance]) # 12 is the last of the x asis. last column
    instance = X_instance
    instance_json = instance.to_json(orient='records')
    

    r = requests.post(url = (url + "/prediction1"), json= instance_json )
    json_string = r.content
    data = json.loads(json_string) # json.loads(json_object_string) to convert a json_object_string to a dictionary

    # prediction = data['prediction']
    # actual_value = data['actual_value']

    prediction = 'Recovered' if data['prediction'] == 1 else "Stolen"
    actual_value = 'Recovered' if data['actual_value'] == 1 else "Stolen"

    return render_template('result1.html', prediction=prediction, actual_value=actual_value, x_dict = x_dict)



@app.route("/get_prediction2", methods=['GET', 'POST'])
def get_prediction2():    
    
    Primary_Offence = request.form.get('Primary_Offence')
    diff = request.form.get('diff')
    Premises_Type = request.form.get('Premises_Type')
    Cost_of_Bike = request.form.get('Cost_of_Bike')
    Occurrence_DayOfWeek = request.form.get('Occurrence_DayOfWeek')
    Occurrence_Year = request.form.get('Occurrence_Year')
    Report_Hour = request.form.get('Report_Hour')
    Occurrence_Month = request.form.get('Occurrence_Month')
    Location_Type = request.form.get('Location_Type')
    NeighbourhoodName = request.form.get('NeighbourhoodName')
    Longitude = request.form.get('Longitude')
    Latitude = request.form.get('Latitude')

    form_dict = {
        "Primary_Offence" : [str(Primary_Offence)],
        "diff" : [int(diff)],
        "Premises_Type" : [str(Premises_Type)],
        "Cost_of_Bike" : [Cost_of_Bike],
        "Occurrence_DayOfWeek" : [str(Occurrence_DayOfWeek)],
        "Occurrence_Year" : [Occurrence_Year],
        "Report_Hour" : [int(Report_Hour)],
        "Occurrence_Month" : [Occurrence_Month],
        "Location_Type" : [str(Location_Type)],
        "NeighbourhoodName" : [str(NeighbourhoodName)],
        "Longitude" : [float(Longitude)],
        "Latitude" : [float(Latitude)]
    }


    for each in form_dict.values():
        print(type(each[0]), each)


    df_instance = pd.DataFrame(form_dict)
    
    instance_json = df_instance.to_json(orient='records')

    r = requests.post(url = (url + "/prediction2"), json= instance_json )
    
    json_string = r.content    

    data = json.loads(json_string) # json.loads(json_object_string) to convert a json_object_string to a dictionary

    prediction = 'Recovered' if data['prediction'] == 1 else "Stolen"    
    
    return render_template('result2.html', prediction = prediction)


if __name__ ==  "__main__":
     app.run(host="localhost", port=3000, debug=True)

