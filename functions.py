import subprocess
import streamlit as st

import pandas as pd
import openai
import json

from TrustpilotReviews.TrustpilotReviews.pipelines import DataBase

db_url = "sqlite:///TrustpilotReviews/TrustpilotReviews/trustpilot.db"
openai.api_key = st.secrets["openai_key"]

def sidebar():
    st.write(
        "With this app, you can scrape reviews from the following websites : "
        "Netatmo, Shein, Amazon, Ikea, Darty and Boulanger. on Trustpilot."
    )
    st.write(
        "Armand Thomas")
    st.image("https://www.facilitoo.fr/wp-content/uploads/2019/04/trustpilot-new-.png", width=200)

def execute_scrapy_spider(brand):
    p = subprocess.Popen(
        ["scrapy", "crawl", "allocine", "-a", f"brand={brand}", "-o", f"./exports/{brand.replace('.', '')}.csv"],
        cwd="TrustpilotReviews/TrustpilotReviews"
    )
    p.wait()
    return p.returncode


def brands():
    return [
        "netatmo.com",
        "www.shein.com",
        "www.amazon.com",
        "www.ikea.com",
        "www.darty.com",
        "boulanger.com",
    ]


def get_all_export_from_brand(brand):
    db = DataBase(db_url)
    tables = db.get_all_tables()
    tables_for_brand = [table for table in tables if brand in table]
    return tables_for_brand


def get_data_from_table(table_name):
    db = DataBase(db_url)
    df = pd.read_sql_table(table_name, db.engine)
    df["select"] = False
    df = df[['select','name', 'rating', 'title', 'review', 'locale', 'published_date', 'id_review']]
    df["published_date"] = pd.to_datetime(df["published_date"])
    df["rating"] = df["rating"].astype(str)
    df["rating"] = df["rating"].apply(lambda x: x + "✨")

    return df

def get_rows_with_selected(df):
    return df[df["select"] == True]

def translate_rows(df, table_name):

    db = DataBase(db_url)

    for index, row in df.iterrows():
        try:
            new_data = openai_translate(row["title"], row["review"])
            title = new_data.get('title', row['title']) if new_data.get('title', row['title']) != '' else row['title']
            review = new_data.get('content', row['review']) if new_data.get('content', row['review']) != '' else row['review']
            df.loc[index, "title"] = title
            df.loc[index, "review"] = review
            db.update_row_by_id(table_name, row["id_review"], title=title, review=review)
        except Exception as e:
            print(e)
            st.error(e)
            pass

    return df

def openai_translate(title, content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
             "role" : "system",
             "content" :
                 "Ton ojectif est de traduire un titre et un contenu séparément. tu vas voire comme entrée un titre et un contenu qui proviennent d'avis trustpilot."
                 "Tu dois déterminer la langue du titre et du contenu et le traduire en français. et me renvoyer uniquement le contenu traduit sous format json tel que {'title' : '', 'content' : ''}"
            },
            {
                "role" : "user",
                "content" : "Voici le titre à traduire : %s, et le contenu %s" % (title, content)
            },
        ]
    )
    msg_text = response['choices'][0]['message']['content']

    return json.loads(msg_text)
