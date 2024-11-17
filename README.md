
# Video Streaming Service

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Project Finality](#project-finality)
- [Design Patterns](#design-patterns)
- [How it Works](#how-it-works)
- [Installation](#installation)
- [Documentation](#documentation)
- [Author](#author)

---

## Introduction

This project is a **Video Streaming Service**, developed as a platform for streaming videos, including movies and series, with features such as user profiles, recommendations, bookmarks, and watch history. It is designed to handle video content efficiently and deliver a user-friendly interface.

---

## Technologies Used

### Backend
- **Django**: Used as the primary backend framework.
- **Django Rest Framework (DRF)**: For building APIs to serve video content and manage user interactions.

### Frontend
- **HTML, CSS**: For creating static web pages.
- **JavaScript**: To enhance interactivity and handle API requests.
- **Axios**: Used for making HTTP requests.

### Database
- **SQLite**: Database for storing video content, user data, and system configurations.

### Media
- **Embed Video**: For embedding and managing video content.

---

## Project Finality

This project was developed as part of my **Computer Engineering** coursework at the **Federal University of Alagoas (UFAL)**. The main objective is to create a scalable and user-friendly video streaming platform while applying concepts learned throughout the course.

The system includes:
- **User Management**: Authentication and custom user models with premium and parental control settings.
- **Content Streaming**: Support for movies and series with categorization by genre.
- **Recommendation System**: Personalized recommendations based on user preferences and viewing history.
- **Parental Controls**: Content filtering based on user settings.
- **Interactive Reviews**: Users can rate and review movies and series.

---

## Design Patterns

This project leverages several **GoF (Gang of Four)** design patterns to ensure modularity, scalability, and maintainability:

### Strategy Pattern
The Strategy pattern was used to handle dynamic content filtering based on parental control settings. It encapsulates different filtering logic into separate strategies.

This allows the system to select the appropriate filtering strategy based on the user's preferences. The use of the Strategy pattern makes it easier to extend the system with new filtering strategies in the future without changing the core logic.

The Strategy pattern was also applied to handle user interactions with different types of content (movies, series, episodes). The specific logic for movies and series was encapsulated into dedicated classes, and the application dynamically selects the appropriate class to execute actions, such as managing bookmarks or watch history.

### Factory Pattern
The Factory pattern was applied to the creation of video content objects (such as movies and episodes). A Factory Class was introduced to encapsulate the creation logic of these objects, simplifying their instantiation and reducing repetitive code.

In the context of the project, the Factory allows for the centralized and controlled creation of objects which makes the system more maintainable. Additionally, this approach facilitates future expansion of the codebase, allowing for easier addition of new content types

### Facade Pattern
The Facade pattern was applied in the get_content function to simplify the generation of context for rendering content details. Instead of handling multiple models and logic within the view, the Facade abstracts the complexity, providing a unified interface to retrieve necessary data, such as reviews, related content, and user interaction details.

By encapsulating this logic, the view becomes cleaner and focuses solely on rendering the template with the provided context

---

## How it Works

### Backend
- Built with Django and Django Rest Framework to manage the database, authentication, and API endpoints.
- Provides endpoints for managing content, user profiles, and recommendations.

### Frontend
- Developed with HTML, CSS, and JavaScript to create a responsive user interface.
- **Axios** is used to handle API communication for user interactions and video streaming.

---

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- pip (Python package manager)

### Step 1: Clone the Repository
Clone the project repository to your local machine:
```bash
git clone https://github.com/lucasbeelen/Video-streming-service
cd Video-streming-service
```

### Step 2: Configure the Django Environment

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Run the Project

1. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

3. **Access the Web Application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## Author

**Lucas Beelen**

Connect with me:
- [GitHub Profile](https://github.com/lucasbeelen)
