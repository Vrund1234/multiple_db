# # Use an official Python image
# FROM python:3.10

# # Set the working directory
# WORKDIR /app

# # Copy files
# COPY requirements.txt .
# COPY backend.py .
# COPY frontend.py .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose the Streamlit and Flask ports
# EXPOSE 8501 5000

# # Start the backend first, then the frontend
# CMD ["sh", "-c", "python backend.py & streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0"]


# # Use an official Python base image
# FROM python:3.9

# # Install required system packages for ODBC
# RUN apt-get update && apt-get install -y \
#     unixodbc \
#     unixodbc-dev \
#     odbcinst \
#     libpq-dev \
#     libssl-dev \
#     libffi-dev \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

# # Install Microsoft ODBC Driver 17 for SQL Server
# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
#     && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
#     && apt-get update \
#     && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY . .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose ports
# EXPOSE 8501 5000

# # Run Streamlit and Flask backend
# CMD ["bash", "-c", "streamlit run frontend.py & python backend.py"]









# Use the official Python image as the base
#main file content


# FROM python:3.9

# # Set the working directory
# WORKDIR /app

# # Copy the requirements file and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Install Gunicorn
# RUN pip install gunicorn

# # Copy the rest of the application
# COPY . .

# # Expose the Flask API port
# EXPOSE 5000

# # Use Gunicorn to serve Flask app in production
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend:app"]















#new content

FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY . .

# Expose ports for both backend and frontend
EXPOSE 5000 8501

# Use a simple script to start both backend and frontend together
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:5000 backend:app & streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0"]




