<<<<<<< HEAD
# # import streamlit as st
# # import requests

# # st.title("AI-Powered Database Query Generator 🚀")

# # # Step 1: Select Database
# # db_type = st.selectbox("Select a Database", ["PostgreSQL", "MySQL", "MSSQL", "MongoDB"])

# # # Step 2: Enter Connection Details
# # st.subheader(f"Enter {db_type} Connection Details:")
# # config = {
# #     "host": st.text_input("Host", value="localhost"),
# #     "port": st.text_input("Port", value="5433" if db_type == "PostgreSQL" else "3306"),
# #     "user": st.text_input("Username"),
# #     "password": st.text_input("Password", type="password"),
# # }

# # if db_type != "MongoDB":
# #     config["dbname"] = st.text_input("Database Name")
# # else:
# #     config["database"] = st.text_input("MongoDB Database")
# #     config["collection"] = st.text_input("MongoDB Collection")

# # if st.button("Connect"):
# #     response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type.lower(), "config": config})
# #     if response.status_code == 200:
# #         st.success("Connected successfully! Now ask a question.")
# #     else:
# #         st.error("Connection failed!")

# # # Step 3: Ask a Question
# # st.subheader("Ask Your Question:")
# # user_query = st.text_input("Enter your question:")

# # if st.button("Get Answer"):
# #     response = requests.post("http://127.0.0.1:5000/ask", json={"query": user_query})

# #     if response.status_code == 200:
# #         result = response.json()
# #         st.subheader("Generated Query:")
# #         st.code(result["sql"], language="sql" if db_type != "MongoDB" else "json")

# #         st.subheader("Query Result:")
# #         if result["result"].get("data"):
# #             import pandas as pd
# #             df = pd.DataFrame(result["result"]["data"], columns=result["result"].get("columns", []))
# #             st.dataframe(df)
# #         else:
# #             st.write("No results found.")
# #     else:
# #         st.error("Error processing request.")





# import streamlit as st
# import requests

# st.title("Multi-Database AI Query Tool")

# # Step 1: Select Database Type
# db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])

# # Step 2: Enter Connection Details
# st.subheader("Enter Database Connection Details")
# host = st.text_input("Host", "")
# port = st.text_input("Port", "")
# database = st.text_input("Database Name", "")
# user = st.text_input("Username", "")
# password = st.text_input("Password", type="password")

# if st.button("Connect"):
#     db_config = {
#         "host": host,
#         "port": port,
#         "database": database,
#         "user": user,
#         "password": password,
#     }
#     response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})

#     if response.status_code == 200:
#         st.success(f"Connected to {db_type} successfully!")
#         st.session_state["db_type"] = db_type
#         st.session_state["db_config"] = db_config
#     else:
#         st.error(response.json().get("error", "Unknown error"))

# # Step 3: Ask Query
# if "db_type" in st.session_state:
#     st.subheader(f"Ask a question for {st.session_state['db_type']}")

#     user_query = st.text_input("Enter your question:")

#     if st.button("Get Answer"):
#         response = requests.post(
#             "http://127.0.0.1:5000/ask",
#             json={"query": user_query, "db_type": st.session_state["db_type"], "db_config": st.session_state["db_config"]},
#         )

#         if response.status_code == 200:
#             result = response.json()
#             st.subheader("Generated SQL Query:")
#             st.code(result["sql"], language="sql")

#             st.subheader("Query Result:")
#             if result["result"].get("data"):
#                 import pandas as pd
#                 df = pd.DataFrame(result["result"]["data"], columns=result["result"]["columns"])
#                 st.dataframe(df)
#             else:
#                 st.write("No results found.")
#         else:
#             st.error(response.json().get("error", "Unknown error"))




import streamlit as st
import requests

# Define session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "connect"  # Start on the connect page

st.title("Multi-Database AI Query Tool 🚀")

if st.session_state.page == "connect":
    # Page 1: Database Connection
    st.subheader("Enter Database Connection Details")

    # Select Database Type
    db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])
    
    # Empty fields for connection details
    host = st.text_input("Host", "")
    port = st.text_input("Port", "")
    user = st.text_input("Username", "")
    password = st.text_input("Password", type="password")

    if st.button("Connect"):
        if not host or not port or not user or not password:
            st.error("Please fill in all fields before connecting.")
        else:
            db_config = {"host": host, "port": port, "user": user, "password": password}

            response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})

            if response.status_code == 200:
                st.success(f"Connected to {db_type} successfully!")
                st.session_state.db_type = db_type
                st.session_state.db_config = db_config
                st.session_state.page = "query"  # Move to next page
                st.rerun()
            else:
                st.error(response.json().get("error", "Unknown error"))

elif st.session_state.page == "query":
    # Page 2: Query the database
    st.subheader(f"Ask a question for {st.session_state.db_type}")

    database = st.text_input("Enter Database Name", "")  # Allow user to enter DB name
    user_query = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        if not database or not user_query:
            st.error("Please enter both database name and question.")
        else:
            db_config = st.session_state.db_config
            db_config["database"] = database  # Include the database name

            response = requests.post(
                "http://127.0.0.1:5000/ask",
                json={"query": user_query, "db_type": st.session_state.db_type, "db_config": db_config},
            )

            if response.status_code == 200:
                result = response.json()
                st.subheader("Generated SQL Query:")
                st.code(result["sql"], language="sql" if st.session_state.db_type != "MongoDB" else "json")

                st.subheader("Query Result:")
                if result["result"].get("data"):
                    import pandas as pd
                    df = pd.DataFrame(result["result"]["data"], columns=result["result"].get("columns", []))
                    st.dataframe(df)
                else:
                    st.write("No results found.")
            else:
                st.error(response.json().get("error", "Unknown error"))

    if st.button("Back"):
        st.session_state.page = "connect"  # Go back to connection page
        st.rerun()
=======
# # import streamlit as st
# # import requests

# # st.title("AI-Powered Database Query Generator 🚀")

# # # Step 1: Select Database
# # db_type = st.selectbox("Select a Database", ["PostgreSQL", "MySQL", "MSSQL", "MongoDB"])

# # # Step 2: Enter Connection Details
# # st.subheader(f"Enter {db_type} Connection Details:")
# # config = {
# #     "host": st.text_input("Host", value="localhost"),
# #     "port": st.text_input("Port", value="5433" if db_type == "PostgreSQL" else "3306"),
# #     "user": st.text_input("Username"),
# #     "password": st.text_input("Password", type="password"),
# # }

# # if db_type != "MongoDB":
# #     config["dbname"] = st.text_input("Database Name")
# # else:
# #     config["database"] = st.text_input("MongoDB Database")
# #     config["collection"] = st.text_input("MongoDB Collection")

# # if st.button("Connect"):
# #     response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type.lower(), "config": config})
# #     if response.status_code == 200:
# #         st.success("Connected successfully! Now ask a question.")
# #     else:
# #         st.error("Connection failed!")

# # # Step 3: Ask a Question
# # st.subheader("Ask Your Question:")
# # user_query = st.text_input("Enter your question:")

# # if st.button("Get Answer"):
# #     response = requests.post("http://127.0.0.1:5000/ask", json={"query": user_query})

# #     if response.status_code == 200:
# #         result = response.json()
# #         st.subheader("Generated Query:")
# #         st.code(result["sql"], language="sql" if db_type != "MongoDB" else "json")

# #         st.subheader("Query Result:")
# #         if result["result"].get("data"):
# #             import pandas as pd
# #             df = pd.DataFrame(result["result"]["data"], columns=result["result"].get("columns", []))
# #             st.dataframe(df)
# #         else:
# #             st.write("No results found.")
# #     else:
# #         st.error("Error processing request.")





# import streamlit as st
# import requests

# st.title("Multi-Database AI Query Tool")

# # Step 1: Select Database Type
# db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])

# # Step 2: Enter Connection Details
# st.subheader("Enter Database Connection Details")
# host = st.text_input("Host", "")
# port = st.text_input("Port", "")
# database = st.text_input("Database Name", "")
# user = st.text_input("Username", "")
# password = st.text_input("Password", type="password")

# if st.button("Connect"):
#     db_config = {
#         "host": host,
#         "port": port,
#         "database": database,
#         "user": user,
#         "password": password,
#     }
#     response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})

#     if response.status_code == 200:
#         st.success(f"Connected to {db_type} successfully!")
#         st.session_state["db_type"] = db_type
#         st.session_state["db_config"] = db_config
#     else:
#         st.error(response.json().get("error", "Unknown error"))

# # Step 3: Ask Query
# if "db_type" in st.session_state:
#     st.subheader(f"Ask a question for {st.session_state['db_type']}")

#     user_query = st.text_input("Enter your question:")

#     if st.button("Get Answer"):
#         response = requests.post(
#             "http://127.0.0.1:5000/ask",
#             json={"query": user_query, "db_type": st.session_state["db_type"], "db_config": st.session_state["db_config"]},
#         )

#         if response.status_code == 200:
#             result = response.json()
#             st.subheader("Generated SQL Query:")
#             st.code(result["sql"], language="sql")

#             st.subheader("Query Result:")
#             if result["result"].get("data"):
#                 import pandas as pd
#                 df = pd.DataFrame(result["result"]["data"], columns=result["result"]["columns"])
#                 st.dataframe(df)
#             else:
#                 st.write("No results found.")
#         else:
#             st.error(response.json().get("error", "Unknown error"))




import streamlit as st
import requests

# Define session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "connect"  # Start on the connect page

st.title("Multi-Database AI Query Tool 🚀")

if st.session_state.page == "connect":
    # Page 1: Database Connection
    st.subheader("Enter Database Connection Details")

    # Select Database Type
    db_type = st.selectbox("Select Database Type", ["PostgreSQL", "MongoDB", "MySQL", "MSSQL"])
    
    # Empty fields for connection details
    host = st.text_input("Host", "")
    port = st.text_input("Port", "")
    user = st.text_input("Username", "")
    password = st.text_input("Password", type="password")

    if st.button("Connect"):
        if not host or not port or not user or not password:
            st.error("Please fill in all fields before connecting.")
        else:
            db_config = {"host": host, "port": port, "user": user, "password": password}

            response = requests.post("http://127.0.0.1:5000/connect", json={"db_type": db_type, "db_config": db_config})

            if response.status_code == 200:
                st.success(f"Connected to {db_type} successfully!")
                st.session_state.db_type = db_type
                st.session_state.db_config = db_config
                st.session_state.page = "query"  # Move to next page
                st.rerun()
            else:
                st.error(response.json().get("error", "Unknown error"))

elif st.session_state.page == "query":
    # Page 2: Query the database
    st.subheader(f"Ask a question for {st.session_state.db_type}")

    database = st.text_input("Enter Database Name", "")  # Allow user to enter DB name
    user_query = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        if not database or not user_query:
            st.error("Please enter both database name and question.")
        else:
            db_config = st.session_state.db_config
            db_config["database"] = database  # Include the database name

            response = requests.post(
                "http://127.0.0.1:5000/ask",
                json={"query": user_query, "db_type": st.session_state.db_type, "db_config": db_config},
            )

            if response.status_code == 200:
                result = response.json()
                st.subheader("Generated SQL Query:")
                st.code(result["sql"], language="sql" if st.session_state.db_type != "MongoDB" else "json")

                st.subheader("Query Result:")
                if result["result"].get("data"):
                    import pandas as pd
                    df = pd.DataFrame(result["result"]["data"], columns=result["result"].get("columns", []))
                    st.dataframe(df)
                else:
                    st.write("No results found.")
            else:
                st.error(response.json().get("error", "Unknown error"))

    if st.button("Back"):
        st.session_state.page = "connect"  # Go back to connection page
        st.rerun()
>>>>>>> e9340ba3d8bdde2efb90e68c0ff68ffd7529c477
