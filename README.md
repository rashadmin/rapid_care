# RapidCare Hub

> An AI-powered first aid assistant providing immediate guidance, structured medical information, and local healthcare resources.

## 🧠 Overview

RapidCare Hub is a Flask-based web application designed to be a comprehensive first aid resource. It integrates a conversational AI chatbot to offer immediate first aid advice, extracts structured information from user-provided medical scenarios, and provides details on nearby hospitals and relevant instructional videos. The project aims to make essential first aid knowledge and access to healthcare resources readily available to users.

## 🔨 What I Built

RapidCare Hub features a multi-faceted approach to emergency first aid assistance:

-   **Conversational AI Chatbot:** An intelligent chatbot powered by OpenAI API that delivers first aid guidance in response to user-described medical situations.
-   **Structured Data Extraction:** The AI can process medical queries to extract key information, facilitating better understanding and response.
-   **User Management:** Secure user registration, login, and profile management using Flask-Login and custom forms.
-   **Anonymous User Support:** Allows users to interact with the chatbot without needing to register, maintaining privacy.

-   **Dynamic Chat History:** Stores and displays conversation history, with pagination for easy navigation.
-   **Hospital Locator:** Provides information on nearby hospitals, including filtering and simulated distance calculations.
-   **Video Resources:** Integrates with the YouTube Data API to find and display relevant first aid instructional videos.
-   **Full-text Search:** Utilizes Elasticsearch for robust search capabilities across application models.
-   **Modular API:** A well-structured RESTful API for programmatic interaction with user, conversation, video, and hospital data.
-   **Command-Line Interface (CLI):** Custom Flask CLI commands for streamlined database management.

## 💭 Thought Process

I approached the development of RapidCare Hub with a focus on modularity and extensibility, which led to the adoption of Flask Blueprints for organizing distinct features like authentication, chat, API, and mapping. This structure makes the application easier to maintain and scale.

A key decision was to implement a factory pattern for the Flask application (`create_app`), allowing for flexible configuration across different environments (development, testing, production). For data persistence, I chose SQLAlchemy with Flask-SQLAlchemy, as it provides a robust ORM and integrates well with Flask. I also decided to implement `SeachableMixin` and `PaginatedAPIMixin` to ensure reusable search and pagination functionality across various models, which significantly reduced boilerplate code.

Integrating external AI (OpenAI) and video (YouTube Data API) services was crucial for the project's core functionality. I focused on designing clear interfaces for these integrations, including detailed system prompts for the AI to ensure accurate and contextually appropriate first aid advice. For real-time map simulations, Flask-SocketIO was chosen, although the current distance and duration calculations are simulated, highlighting a potential area for future enhancement with real-time data.

Throughout the process, I prioritized user experience with features like consistent error handling through custom error pages and the "next" parameter redirection after login. While building, I identified areas like potential security risks with `eval()` in specific model fields and the need for more robust error handling around external API calls, which are important considerations for future improvements.

## 🛠️ Tools & Tech Stack

| Layer            | Technology                  |
| :--------------- | :-------------------------- |
| Language         | Python 3.x                  |
| Web Framework    | Flask                       |
| ORM              | Flask-SQLAlchemy, SQLAlchemy |
| Database         | PostgreSQL, SQLite          |
| Authentication   | Flask-Login, Flask-WTF, WTForms |
| AI / LLM         | OpenAI API                  |
| Video            | YouTube Data API v3         |
| Search           | Elasticsearch (client)      |
| Real-time        | Flask-SocketIO              |
| Data Manipulation| pandas, numpy               |
| Configuration    | python-dotenv               |
| Utilities        | `requests`, `urllib.parse`, `datetime`, `uuid`, `enum`, `werkzeug`, `logging` |

## 🚀 Getting Started

### Prerequisites
-   Python 3.x
-   An OpenAI API Key
-   A YouTube Data API v3 Key
-   An Elasticsearch instance (optional, but recommended for full search functionality)
-   A Mail Server (optional, for email features)

### Installation

```bash
git clone https://github.com/rashadmin/rapid_care.git
cd rapid_care
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root and populate it with the following:

```env
SECRET_KEY=your_secret_key_for_flask_sessions
DATABASE_URL=postgresql://user:password@host:port/database_name (or sqlite:///app.db)
MAIL_SERVER=your_mail_server
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_mail_username
MAIL_PASSWORD=your_mail_password
ELASTICSEARCH_URL=http://localhost:9200 (or your Elasticsearch instance URL)
OPEN_AI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
CHAT_PER_PAGE=10
```

### Run

Initialize the database:

```bash
flask cli initialize_database
```

Run the Flask application:

```bash
flask run
```

## 📖 Usage

### Chatbot Interaction

Navigate to the chatbot interface in your browser. Type your medical first aid query, and the AI will provide guidance.

### API Usage (Example: Get User Details)

You can interact with the API endpoints programmatically. For example, to get details of a user (assuming an API key or authentication token is handled):

```bash
curl -X GET http://127.0.0.1:5000/api/users/<user_id>
```

### CLI for Database Initialization

The `flask cli initialize_database` command can be used to set up your database schema. This is useful for initial setup or after schema changes.

## 📚 Resources

-   [Flask Documentation](https://flask.palletsprojects.com/) — Web framework
-   [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/) — SQLAlchemy integration for Flask
-   [Flask-Login Documentation](https://flask-login.readthedocs.io/) — User session management
-   [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/) — WTForms integration for Flask
-   [WTForms Documentation](https://wtforms.readthedocs.io/) — Flexible form rendering and validation library
-   [OpenAI API Documentation](https://platform.openai.com/docs/api-reference) — LLM API reference
-   [YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3/docs) — Video search API
-   [Elasticsearch Python Client](https://elasticsearch-py.readthedocs.io/) — Python client for Elasticsearch
-   [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/) — Socket.IO integration for Flask
-   [Pandas Documentation](https://pandas.pydata.org/docs/) — Data manipulation and analysis library
-   [NumPy Documentation](https://numpy.org/doc/) — Numerical computing library
-   [python-dotenv Documentation](https://github.com/theskumar/python-dotenv) — Loads environment variables from `.env` files
-   [requests Documentation](https://requests.readthedocs.io/) — HTTP library for Python
-   [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/latest/orm/) — SQL toolkit and Object Relational Mapper
-   [Werkzeug Documentation](https://werkzeug.palletsprojects.com/) — WSGI utility library (used for password hashing)

## 📄 License

MIT © [rashadmin](https://github.com/rashadmin)