<<<<<<< HEAD
import streamlit as st
import requests

st.title("Multi-Database AI Query Tool")

# Step 1: Select Database Type
db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])

# Step 2: Enter Connection Details
st.subheader("Enter Database Connection Details")
host = st.text_input("Host", "")
port = st.text_input("Port", "")
database = st.text_input("Database Name", "")
user = st.text_input("Username", "")
password = st.text_input("Password", type="password")

if st.button("Connect"):
    db_config = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }
    response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})

    if response.status_code == 200:
        st.success(f"Connected to {db_type} successfully!")
        st.session_state["db_type"] = db_type
        st.session_state["db_config"] = db_config
    else:
        st.error(response.json().get("error", "Unknown error"))

# Step 3: Ask Query
if "db_type" in st.session_state:
    st.subheader(f"Ask a question for {st.session_state['db_type']}")

    user_query = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        response = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"query": user_query, "db_type": st.session_state["db_type"], "db_config": st.session_state["db_config"]},
        )

        if response.status_code == 200:
            result = response.json()
            st.subheader("Generated SQL Query:")
            st.code(result["sql"], language="sql")

            st.subheader("Query Result:")
            if result["result"].get("data"):
                import pandas as pd
                df = pd.DataFrame(result["result"]["data"], columns=result["result"]["columns"])
                st.dataframe(df)
            else:
                st.write("No results found.")
        else:
=======
import streamlit as st
import requests

st.title("Multi-Database AI Query Tool")

# Step 1: Select Database Type
db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])

# Step 2: Enter Connection Details
st.subheader("Enter Database Connection Details")
host = st.text_input("Host", "")
port = st.text_input("Port", "")
database = st.text_input("Database Name", "")
user = st.text_input("Username", "")
password = st.text_input("Password", type="password")

if st.button("Connect"):
    db_config = {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
    }
    response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})

    if response.status_code == 200:
        st.success(f"Connected to {db_type} successfully!")
        st.session_state["db_type"] = db_type
        st.session_state["db_config"] = db_config
    else:
        st.error(response.json().get("error", "Unknown error"))

# Step 3: Ask Query
if "db_type" in st.session_state:
    st.subheader(f"Ask a question for {st.session_state['db_type']}")

    user_query = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        response = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"query": user_query, "db_type": st.session_state["db_type"], "db_config": st.session_state["db_config"]},
        )

        if response.status_code == 200:
            result = response.json()
            st.subheader("Generated SQL Query:")
            st.code(result["sql"], language="sql")

            st.subheader("Query Result:")
            if result["result"].get("data"):
                import pandas as pd
                df = pd.DataFrame(result["result"]["data"], columns=result["result"]["columns"])
                st.dataframe(df)
            else:
                st.write("No results found.")
        else:
>>>>>>> e9340ba3d8bdde2efb90e68c0ff68ffd7529c477
            st.error(response.json().get("error", "Unknown error"))