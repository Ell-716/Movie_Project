# 🎬 Movie_Project

## Overview

**Movie_Project** is a simple yet powerful movie database application that allows users to manage their favorite movies. With this app, users can add, view, and store information about movies, including their titles, release years, ratings, poster images and country flags. 

> *This project was developed as part of an assignment in the Software Engineer Bootcamp.* 🎓

## Purpose

The primary purpose of Movie_Project is to provide a user-friendly interface for movie management. Whether you are a movie enthusiast wanting to keep track of your watched films or someone looking for a simple way to catalog your favorite movies, this app serves as an efficient solution. 

## Features

- 📜 **List Movies**: View all movies in your collection.
- ➕ **Add Movie**: Easily add new movies to your database.
- ❌ **Delete Movie**: Remove movies from your collection.
- ✏️ **Update Movie**: Add or remove a note.
- 📊 **Stats**: View statistics about your movie collection.
- 🎲 **Random Movie**: Get a random movie suggestion from your collection.
- 🔍 **Search Movie**: Quickly search for a movie by title or other criteria.
- ⭐ **Movies Sorted by Rating**: View movies sorted based on their ratings.
- 📅 **Movies Sorted by Year**: View movies sorted based on their release years.
- 🎞️ **Filter Movies**: Filter your movie collection based on different criteria.
- 🌐 **Generate Website**: Create a static website to showcase your movie collection.
- 🎬 **IMDb Links**: Click on the movie poster to be redirected to the movie's page on IMDb for more details.
## Technologies Used

- **Python**: The main programming language used for development.
- **External Libraries**: 
  - `colorama`: For colored terminal output.
  - `fuzzywuzzy`: For fuzzy string matching.
  - `python-dotenv`: For loading environment variables.
  - `requests`: For making HTTP requests.
  - `statistics`: For statistical calculations.

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/movie_project.git
   
2. **Navigate to the project directory**:

   ```bash
   cd movie_project
   
3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   
4. **Set up environment variables (if needed)**:
Create a .env file in the project root directory. Get your own api on [OMDb API website](https://www.omdbapi.com/), set it up in your '.env' file.

   ```bash
   API_KEY=your_secret_key

## Usage

To run the application, follow these steps:

1. **Run**:

   ```bash
   main.py
   
2. **Or start the application**:

   ```bash
   python3 main.py data/denis.csv
   
3. **Follow the on-screen instructions**: to add and manage movies.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, please create an issue or submit a pull request. 🤝


