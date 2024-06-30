# EasyLaw-Backend

EasyLaw is an intelligent platform for legal monitoring. The back-end is developed using Flask with a PostgreSQL database.

## Setup Instructions

1. Create a database named easyLawDb in PostgreSQL with the user 'postgres' and an empty password.

2. Run `flask shell` to launch an interactive Flask shell with the loaded application.

3. Use `db.create_all()` to create all tables defined in SQLAlchemy database models.

4. For initial data insertion, execute the following scripts :
   - `python insertionDomains.py`
   - `python insertionBDD_mahkama.py`
   - `python insertionBDD_majliss_test.py`
   - `python insertionLaws.py`
   - `python insertionPlanTarification.py`
     
5. Use `flask run --port 8000` to start the Flask application on port 8000.

## Chatbot Requirements

Install the following Python packages for the chatbot:
- cohere
- pinecone-client
- configparser
- langchain-community

Run `pip install cohere pinecone-client configparser langchain-community` to install these packages.
