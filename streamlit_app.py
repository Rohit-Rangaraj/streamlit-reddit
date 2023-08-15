import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json


def clear_form():
    st.session_state["title_input"] = ""
    st.session_state["url_input"] = ""


st.set_page_config("Reddit Clone", layout="centered",
                   page_icon="https://www.redditstatic.com/shreddit/assets/favicon/120x120.png")

st.header("Reddit Clone")

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit-7290e")

title = st.text_input("Post title", key="title_input")
url = st.text_input("Post URL", key="url_input")
submit_btn = st.button("Submit!")
clear_btn = st.button("Clear form", on_click=clear_form)

if title and url and submit_btn:
    doc_ref = db.collection("posts").document(title)
    doc_ref.set({
        "title": title,
        "url": url
    })

posts_ref = db.collection("posts")

for doc in posts_ref.stream():
    post = doc.to_dict()
    title = post["title"]
    url = post["url"]

    st.subheader(f"Post: {title}")
    st.write(f":link: [{url}]({url})")
