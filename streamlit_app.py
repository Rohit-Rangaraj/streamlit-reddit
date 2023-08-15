import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json


def clear_form():
    st.session_state["title_input"] = ""
    st.session_state["url_input"] = ""


key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit")

title = st.text_input("Post title", key="title_input")
url = st.text_input("Post URL", key="url_input")
submit_btn = st.button("Submit!")

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
