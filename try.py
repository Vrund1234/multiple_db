from openai import OpenAI
import pyodbc
import pandas as pd

# Set your OpenAI API key here
# openai.api_key = "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"
client = OpenAI(api_key="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")
# MS SQL connection string (edit this)
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-IIUF7SB;"
    "Database=EuroCouponApp;"
    "Trusted_Connection=yes;"
)

def get_db_schema():
    """Fetch table and column info from SQL Server schema."""
    with pyodbc.connect(conn_str) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE='BASE TABLE'
        """)
        tables = [row[0] for row in cursor.fetchall()]

        schema = ""
        for table in tables:
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = '{table}'
            """)
            columns = cursor.fetchall()
            schema += f"Table {table} columns:\n"
            for col in columns:
                schema += f" - {col[0]} ({col[1]})\n"
            schema += "\n"
        return schema

def generate_sql_from_nl(natural_language_question, schema_info):
    prompt = f"""
You are an AI assistant that translates natural language questions into Microsoft SQL queries.
Use the following database schema information:
{schema_info}

Write a single valid SQL query to answer this question:
{natural_language_question}

Only return the SQL query, no explanation.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    sql_query = response.choices[0].message.content.strip()
    return sql_query



def clean_sql_query(query: str) -> str:
    # Remove triple backticks and language hints if present
    if query.startswith("```"):
        lines = query.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        query = "\n".join(lines)
    return query.strip()

def run_sql_query(sql_query):
    with pyodbc.connect(conn_str) as conn:
        df = pd.read_sql(sql_query, conn)
    return df

def main():
    schema = get_db_schema()
    print("Database schema loaded.\n")

    while True:
        question = input("Ask a question about your database (or type 'exit'): ")
        if question.lower() == "exit":
            break

        try:
            print("\nGenerating SQL query from your question...")
            sql = generate_sql_from_nl(question, schema)
            sql = clean_sql_query(sql)
            print(f"Generated SQL:\n{sql}\n")

            print("Running query on database...")
            results_df = run_sql_query(sql)
            print("\nQuery Results:")
            print(results_df)
            print("\n" + "-"*50 + "\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()