<<<<<<< HEAD
import streamlit as st
import requests
import pandas as pd
import base64

# Custom CSS for Glassmorphism UI
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928DAB);
            font-family: 'Poppins', sans-serif;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            width: 60%;
            margin-bottom: 20px;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #ffcc00;
            text-align: center;
            animation: fadeIn 2s;
        }
        .sub-text {
            text-align: center;
            font-size: 18px;
            color: #f0f0f0;
        }
        .custom-button {
            background: #ffcc00;
            color: #000;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .custom-button:hover {
            background: #e6b800;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

st.markdown("""
    <div class='main-container'>
        <h1 class='main-title'>🚀 AI-Powered Database Query Tool</h1>
        <p class='sub-text'>Query PostgreSQL, MongoDB, MySQL, MSSQL effortlessly with AI-generated SQL.</p>
    </div>
    """, unsafe_allow_html=True)

# Step 1: Select Database Type
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"], index=0)
st.markdown("</div>", unsafe_allow_html=True)

# Step 2: Enter Connection Details
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("Enter Database Connection Details")
host = st.text_input("Host", "")
port = st.text_input("Port", "")
database = st.text_input("Database Name", "")
user = st.text_input("Username", "")
password = st.text_input("Password", type="password")

if st.button("Connect", key="connect_button", help="Click to connect to database"):
    db_config = {"host": host, "port": port, "database": database, "user": user, "password": password}
    response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})
    if response.status_code == 200:
        st.success(f"✅ Connected to {db_type} successfully!")
        st.session_state["db_type"] = db_type
        st.session_state["db_config"] = db_config
    else:
        st.error(response.json().get("error", "Unknown error"))
st.markdown("</div>", unsafe_allow_html=True)

# Step 3: Ask Query
if "db_type" in st.session_state:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader(f"💬 Ask a question for {st.session_state['db_type']}")
    user_query = st.text_input("Enter your question:")
    
    if st.button("Get Answer", key="get_answer", help="Click to generate SQL and fetch results"):
        response = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"query": user_query, "db_type": st.session_state["db_type"], "db_config": st.session_state["db_config"]},
        )
        if response.status_code == 200:
            result = response.json()
            st.subheader("📝 Generated SQL Query:")
            st.code(result["sql"], language="sql")
            st.subheader("📊 Query Result:")
            if result["result"].get("data"):
                df = pd.DataFrame(result["result"]["data"], columns=result["result"]["columns"])
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                b64 = base64.b64encode(csv).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="query_results.csv">📥 Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.write("No results found.")
        else:
            st.error(response.json().get("error", "Unknown error"))
=======
import streamlit as st
import requests
import pandas as pd
import base64

# Custom CSS for Glassmorphism UI
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928DAB);
            font-family: 'Poppins', sans-serif;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            width: 60%;
            margin-bottom: 20px;
        }
        .main-title {
            font-size: 36px;
            font-weight: bold;
            color: #ffcc00;
            text-align: center;
            animation: fadeIn 2s;
        }
        .sub-text {
            text-align: center;
            font-size: 18px;
            color: #f0f0f0;
        }
        .custom-button {
            background: #ffcc00;
            color: #000;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .custom-button:hover {
            background: #e6b800;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

st.markdown("""
    <div class='main-container'>
        <h1 class='main-title'>🚀 AI-Powered Database Query Tool</h1>
        <p class='sub-text'>Query PostgreSQL, MongoDB, MySQL, MSSQL effortlessly with AI-generated SQL.</p>
    </div>
    """, unsafe_allow_html=True)

# Step 1: Select Database Type
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"], index=0)
st.markdown("</div>", unsafe_allow_html=True)

# Step 2: Enter Connection Details
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("Enter Database Connection Details")
host = st.text_input("Host", "")
port = st.text_input("Port", "")
database = st.text_input("Database Name", "")
user = st.text_input("Username", "")
password = st.text_input("Password", type="password")

if st.button("Connect", key="connect_button", help="Click to connect to database"):
    db_config = {"host": host, "port": port, "database": database, "user": user, "password": password}
    response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})
    if response.status_code == 200:
        st.success(f"✅ Connected to {db_type} successfully!")
        st.session_state["db_type"] = db_type
        st.session_state["db_config"] = db_config
    else:
        st.error(response.json().get("error", "Unknown error"))
st.markdown("</div>", unsafe_allow_html=True)

# Step 3: Ask Query
if "db_type" in st.session_state:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader(f"💬 Ask a question for {st.session_state['db_type']}")
    user_query = st.text_input("Enter your question:")
    
    if st.button("Get Answer", key="get_answer", help="Click to generate SQL and fetch results"):
        response = requests.post(
            "http://127.0.0.1:5000/ask",
            json={"query": user_query, "db_type": st.session_state["db_type"], "db_config": st.session_state["db_config"]},
        )
        if response.status_code == 200:
            result = response.json()
            st.subheader("📝 Generated SQL Query:")
            st.code(result["sql"], language="sql")
            st.subheader("📊 Query Result:")
            if result["result"].get("data"):
                df = pd.DataFrame(result["result"]["data"], columns=result["result"]["columns"])
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                b64 = base64.b64encode(csv).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="query_results.csv">📥 Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.write("No results found.")
        else:
            st.error(response.json().get("error", "Unknown error"))
>>>>>>> e9340ba3d8bdde2efb90e68c0ff68ffd7529c477
    st.markdown("</div>", unsafe_allow_html=True)