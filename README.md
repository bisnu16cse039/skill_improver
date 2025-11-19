# Skill Improver

Skill Improver is a web application built with Python and Flask that allows users to manage and share knowledge through categories/articles. It features user authentication, a dashboard for content management, and a rich text editor for creating content.

## Features

*   **User Authentication**: Secure registration and login system using password hashing.
*   **Dashboard**: Personalized dashboard for users to manage their created content.
*   **CRUD Operations**: Create, Read, Update, and Delete categories/articles.
*   **Rich Text Editor**: Integrated CKEditor for formatting content.
*   **Responsive Design**: Built with Bootstrap for a mobile-friendly interface.

## Tech Stack

*   **Backend**: Python, Flask
*   **Database**: MySQL
*   **Frontend**: HTML, CSS, Bootstrap, CKEditor
*   **Libraries**:
    *   `flask-mysqldb`: For MySQL database integration.
    *   `wtforms`: For form handling and validation.
    *   `passlib`: For password hashing.

## Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.x
*   MySQL Server

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd skill_improver
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    You can install the required packages using pip:
    ```bash
    pip install flask flask-mysqldb wtforms passlib
    ```

4.  **Database Setup:**
    
    1.  Open your MySQL client (e.g., phpMyAdmin, MySQL Workbench, or command line).
    2.  Create a database named `skill_improver_db`.
    3.  Run the following SQL commands to create the necessary tables:

    ```sql
    USE skill_improver_db;

    CREATE TABLE users (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        user_name VARCHAR(30),
        password VARCHAR(100),
        register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE catagories (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(100),
        body TEXT,
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ```

5.  **Configure Database Connection:**
    Open `app.py` and ensure the MySQL configuration matches your local setup (update the password if necessary):
    ```python
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '' # Add your MySQL password here
    app.config['MYSQL_DB'] = 'skill_improver_db'
    ```

## Usage

1.  **Run the application:**
    ```bash
    python app.py
    ```

2.  **Access the app:**
    Open your web browser and go to `http://localhost:5000`.

3.  **Register and Login:**
    Create a new account and log in to access the dashboard and start creating categories.

## Project Structure

*   `app.py`: The main Flask application file containing routes and logic.
*   `data.py`: Contains dummy data (initially used, now replaced by DB).
*   `templates/`: Contains HTML templates for the application.
    *   `layout.html`: The base template with navbar and scripts.
    *   `home.html`, `about.html`: Static pages.
    *   `register.html`, `login.html`: Authentication pages.
    *   `dashboard.html`: User dashboard.
    *   `catagories.html`, `catagory.html`: Views for listing and showing categories.
    *   `add_catagories.html`, `edit_catagory.html`: Forms for creating/editing.

## License

This project is open source.
