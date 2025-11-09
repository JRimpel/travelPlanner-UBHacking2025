import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from openai import OpenAI


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
client = OpenAI(api_key=env.get("OPENAI_API_KEY"))


        
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

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
    session.permanent = True
    return redirect("/dashboard")
@app.route("/logout")
def logout():
    session.pop("user")
    print(session)
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
    return render_template("dashboard.html", session = session) 



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))