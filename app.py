import requests
from flask import Flask, render_template, url_for


from flask import request as req
from collections import defaultdict

app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarization",methods=["GET","POST"])

def Summarize():
    if req.method=="POST":
      
        API_URL = "https://api-inference.huggingface.co/models/marianna13/flan-t5-base-summarization"
        headers = {"Authorization": "Bearer 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"}
        
        data=req.form["data"]
        
        percentage = req.form["maxL"]
        summarySize = int(req.form["maxL"])
        maxL = int(len(data) * int(req.form["maxL"]) / 100)
        minL= int(maxL / 2)
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        output = query(
            {
                "inputs": data,
                "parameters": {"min_length":minL,"max_length":maxL},
            }
        )[0]
        

        return render_template("index.html", maxSize=summarySize,result= output['summary_text'], previous=data)
    else:
        return 'OK'
if __name__ == '__main__':
        app.debug = True
        app.run()