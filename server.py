import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for, request, jsonify
import requests


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
       
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
UNSPLASH_ACCESS_KEY = "pMgW6_xKiPodZXmzU2ZYwGTaL1rQf3vbalMdA21tMAI"

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/dashboard")
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/")
def home():
    return render_template("title.html")
    
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html") 


@app.route("/img-url", methods = ["POST"])
def imgGen():
    data = request.get_json()
    destination = data.get("destination")
    response = requests.get(
        "https://api.unsplash.com/photos/random",
        params = {
          "query": destination,
          "client_id": UNSPLASH_ACCESS_KEY,
          "orientation": "landscape"      
   })
    data = response.json()
    url = data.get("urls").get("regular")
    return jsonify({"image":url})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))