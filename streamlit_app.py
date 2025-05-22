# streamlit_app.py

import streamlit as st
import psycopg2
import mysql.connector
import pymongo
import pyodbc
import pandas as pd
import google.generativeai as genai
import json
from bson import ObjectId

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🧠 Multi-Database AI Query Tool")

# Step 1: Select Database Type
db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])

# Step 2: Enter Connection Details
st.subheader("Enter Database Connection Details")
host = st.text_input("Host", "")
port = st.text_input("Port", "")
database = st.text_input("Database Name", "")
user = st.text_input("Username", "")
password = st.text_input("Password", type="password")

connected = False

if st.button("Connect"):
    try:
        db_config = {
            "host": host,
            "port": int(port),
            "database": database,
            "user": user,
            "password": password,
        }

        # Test connection
        if db_type == "PostgreSQL":
            conn = psycopg2.connect(**db_config)
        elif db_type == "MySQL":
            conn = mysql.connector.connect(**db_config)
        elif db_type == "MSSQL":
            conn = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={host};DATABASE={database};UID={user};PWD={password}"
            )
        elif db_type == "MongoDB":
            client = pymongo.MongoClient(host, int(port))
            db = client[database]
            db.command("ping")
        else:
            st.error("Invalid database type.")
            st.stop()

        if db_type != "MongoDB":
            conn.close()

        st.session_state["db_type"] = db_type
        st.session_state["db_config"] = db_config
        st.success(f"Connected to {db_type} successfully!")
        connected = True
    except Exception as e:
        st.error(f"Connection failed: {e}")

# Step 3: Ask Query
if "db_type" in st.session_state:
    st.subheader(f"Ask a question for {st.session_state['db_type']}")

    user_query = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        db_type = st.session_state["db_type"]
        db_config = st.session_state["db_config"]

        def generate_sql(nl_query, db_type):
            try:
                model = genai.GenerativeModel(model_name="gemini-2.0-flash")
                prompt = f"""
                Convert this user query into a valid SQL query for {db_type}.
                ❌ Do NOT include database names.
                ✅ Return SQL for a single database only.

                User Query: {nl_query}
                SQL:
                """
                response = model.generate_content(prompt)
                return response.text.strip().replace("```sql", "").replace("```", "").strip()
            except Exception as e:
                return f"Error generating SQL: {str(e)}"

        def execute_sql_query(sql_query, db_type, db_config):
            try:
                if db_type == "PostgreSQL":
                    conn = psycopg2.connect(**db_config)
                elif db_type == "MySQL":
                    conn = mysql.connector.connect(**db_config)
                elif db_type == "MSSQL":
                    conn = pyodbc.connect(
                        f"DRIVER={{SQL Server}};SERVER={db_config['host']};DATABASE={db_config['database']};"
                        f"UID={db_config['user']};PWD={db_config['password']}"
                    )
                else:
                    return {"error": "Unsupported DB"}

                cursor = conn.cursor()
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                cols = [desc[0] for desc in cursor.description]

                cursor.close()
                conn.close()
                return pd.DataFrame(rows, columns=cols)
            except Exception as e:
                return {"error": str(e)}

        def execute_mongo_query(collection_name, db_config):
            try:
                client = pymongo.MongoClient(db_config["host"], int(db_config["port"]))
                db = client[db_config["database"]]
                collection = db[collection_name]
                data = list(collection.find())
                df = pd.json_normalize(json.loads(json.dumps(data, default=str)))
                return df
            except Exception as e:
                return {"error": str(e)}

        if db_type == "MongoDB":
            collection_name = user_query.split()[-1]
            result = execute_mongo_query(collection_name, db_config)
            if isinstance(result, dict) and "error" in result:
                st.error(result["error"])
            else:
                st.dataframe(result)
        else:
            sql_query = generate_sql(user_query, db_type)
            st.subheader("Generated SQL Query:")
            st.code(sql_query, language="sql")

            result = execute_sql_query(sql_query, db_type, db_config)
            if isinstance(result, dict) and "error" in result:
                st.error(result["error"])
            else:
                st.subheader("Query Result:")
                st.dataframe(result)
