# AI Shopping Website

This repository contains the source code for an AI-powered shopping website built with FastAPI, Streamlit, MySQL, Redis, and Docker.

## Project Overview

This website is an e-commerce platform that allows users to buy a wide range of products.

## Key Features

* **User Registration and Login System:** Enables users to easily create accounts and log in.
* **Product Addition to Cart and Favorites:** Users can add products to their shopping carts and save favorite items.
* **Advanced Product Search:** Product search by name and filtering by stock quantity.
* **Gemini-based Chat Assistant:** Intelligent chat assistant tailored to the store's products, assisting users in finding products and providing information.
* **Administrator Management Page:** Restricted access for administrators only. Enables prediction of customer purchase amounts for technology products through data analysis.

## Technologies Used

* **FastAPI:** A modern, high-performance web framework for building APIs.
* **Streamlit:** A Python library for creating interactive web applications.
* **MySQL:** A robust relational database for storing product information, user data, and order history.
* **Redis:** An in-memory data store for caching frequently accessed data and improving application performance.
* **Docker:** A platform for containerizing and orchestrating applications.

## Project Structure

    ai_shopping/
    ├── api/
    │   ├── main.py  # FastAPI application entry point
    │   ├── models.py  # Data models for API endpoints
    │   ├── services.py  # Business logic for API services
    │   ├── routers/
    │   │   ├── products.py  # Product-related API routes
    │   │   ├── users.py  # User-related API routes
    │   │   ├── orders.py  # Order-related API routes
    │   ├── dependencies.py  # Dependency injection for database and caching
    ├── ui/
    │   ├── main.py  # Streamlit UI application entry point
    │   ├── components/  # Reusable UI components
    ├── db/
    │   ├── init.sql  # SQL scripts for database initialization
    ├── docker-compose.yml  # Docker Compose configuration file
    ├── requirements.txt  # Project dependencies
    ├── .env  # Environment variables


## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>


2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate

  
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Configure environment variables:**
  
  Create a .env file in the project root directory.
  (To run docker-compose create also .env.docker) 
  
  Add the following environment variables:
  
  DATABASE_URL: Connection string for the MySQL database.
  
  REDIS_HOST: Hostname or IP address of the Redis server.
  
  REDIS_PORT: Port number of the Redis server.
  
  SECRET_KEY =  String/+Int for Encryption
  
  BASE_URL = "http://web:8000"


  ## API Keys

Before running the application, you need to obtain an OpenAI API key and configure it in your environment.

 

**Set the API Key Environment Variable:**

   - **Option 1: Using Environment Variables:**
      - Create a `.env` file in the root directory of your project.
      - Add the following line to the `.env` file:
        ```
        GEMINI_API_KEY =<your_api_key>
        ```
        - Replace `<your_api_key>` with your actual GEMINI API API key.

   - **Option 2: Setting Environment Variable Directly (Not Recommended for Production):**
      - Set the environment variable directly in your terminal:
        ```bash
        export GEMINI_API_KEY =<your_api_key> 
        ```
      - **Note:** This method is not recommended for production as it exposes your API key directly in your shell history.

  
      
  ## Running the Application
     
  **Start the Docker containers with all at once:**

        docker-compose up -d --build
   
       
  **Run the FastAPI application:**

     uvicorn main:app --reload 
    
  **Run the Streamlit UI:**
    
     streamlit run ui/Home.py
    
  ## Contributing
  Contributions are welcome! Please open an issue or submit a pull request.
