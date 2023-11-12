import requests
from flask import Flask, render_template, url_for
from flask import request as req

app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarization",methods=["GET","POST"])
def Summarize():
    if req.method=="POST":
        
        API_URL = "https://api-inference.huggingface.co/models/HuyHNG/autotrain-1_flan-99948147515"
        headers = {"Authorization": "Bearer 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"}

        # API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        # headers = {"Authorization": "Bearer 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"}
        data=req.form["data"]

        percentage = req.form["maxL"]
        maxL = int(len(data) * int(req.form["maxL"]) / 100)
        minL= int(maxL / 2)
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        output = query(
            {
                "inputs": data,
                "parameters": {"do_sample": False, "min_length":minL,"max_length":maxL},
            }
        )[0]

        return render_template("index.html", result= output["summary_text"], previous=data, data_size= len(data), output_size = len(output["summary_text"]), percent=percentage)
    else:
        return render_template("index.html")
if __name__ == '__main__':
        app.debug = True
        app.run()