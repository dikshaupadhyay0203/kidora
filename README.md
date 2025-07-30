# Kidora

Kidora is a web application designed for kids to learn and have fun with AI-powered stories and activities.

## Features

*   **AI Story Generation**: Creates engaging and educational stories for kids.
*   **Interactive Quizzes**: Tests knowledge with fun quizzes related to the stories.
*   **Personalized Learning**: Tracks progress and adapts to the user's learning pace.
*   **Homework Assistance**: Provides help with homework assignments.

## Directory Structure

Here's a breakdown of the key files and directories in the project:

*   `manage.py`: The command-line utility for interacting with the Django project.
*   `requirements.txt`: A list of the Python packages required to run the project.
*   `db.sqlite3`: The SQLite database file.
*   `kidora/`: The main project directory.
    *   `settings.py`: The settings for the Django project.
    *   `urls.py`: The URL declarations for the project.
*   `accounts/`: The Django app for managing user accounts.
*   `dashboard/`: The Django app for the user's dashboard, including AI story generation.
*   `homework/`: The Django app for the homework assistance feature.
*   `static/`: The directory for static files like images, CSS, and JavaScript.
*   `templates/`: The directory for the HTML templates.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.12 or higher
*   pip (Python package installer)

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/kidora.git
    ```

2.  Navigate to the project directory:

    ```bash
    cd kidora
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Create a `.env` file in the root of the project and add the following environment variables:

```
GOOGLE_API_KEY=your_google_api_key
TOGETHER_API_KEY=your_together_api_key
```

**Note:** You need to replace `your_google_api_key` and `your_together_api_key` with your actual API keys.

### Running the Application

1.  Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

2.  Start the development server:

    ```bash
    python manage.py runserver
    ```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

*   **Register and Login**: Create a new account or log in with an existing account.
*   **Explore the Dashboard**: Access the AI story generator and other features from the dashboard.
*   **Generate Stories**: Enter a topic or a prompt to generate a new story.
*   **Take Quizzes**: Test your understanding of the stories by taking quizzes.
*   **Get Homework Help**: Use the homework assistance feature to get help with your assignments.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss your ideas.
