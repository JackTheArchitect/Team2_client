from flask import Flask, render_template
import requests
import json

# import pickle
import pandas as pd
import os


# # load the model from disk
# filename = 'finalized_model.sav'
# loaded_model = pickle.load(open(filename, 'rb'))

# Load X_test, y_test
X_test = pd.read_pickle('X_test.pkl')
y_test = pd.read_pickle('y_test.pkl')


print(X_test.head(2))

# Merge the X_test, y_test again so we can make one json obect
df = X_test.assign(Status=y_test)

# Convert df into one json object
df_json = df.to_json(orient='records')

# backend api url
url = "http://localhost:5000"





app = Flask(__name__)

# def display_score():
#     r = requests.post(url = (url + "/run"), json= df_json )
#     return r.content

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_score")
def get_score():
    r = requests.post(url = (url + "/run"), json= df_json )
    return r.content




# @app.route("/data")
# def displayData():

#     out = X_test.head(1).to_json(orient='records', lines=True)
#     return out



# @app.route("/forward/", methods=['POST'])
# def move_forward():
#     #Moving forward code
#     forward_message = "Moving Forward..."
#     return render_template('index.html', forward_message=forward_message);


if __name__ ==  "__main__":
     app.run(host="localhost", port=3000, debug=True)

