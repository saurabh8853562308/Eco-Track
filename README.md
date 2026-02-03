# Carbon Footprint Calculator

A generic carbon footprint calculator application for Ghaziabad Climate Awareness, built with Django. This application allows users to track their carbon footprint based on food consumption, energy usage, and transportation.

## Features

- **Dual Dashboard System**:
  - **Customer Role**: Calculate and track personal carbon footprints.
  - **Company Member Role**: View platform data and analytics.
- **Carbon Calculator**: easy-to-use form to input usage data.
- **Analytics**: Visual breakdown of carbon emissions (Food, Energy, Transportation).
- **Responsive Design**: Clean and modern interface.

## Project Structure

The project code is located in the `carbon_footprint/` directory.

- `carbon_footprint/`: Main Django project folder.
- `carbon_footprint/calculator/`: Main application with models, views, and templates.
- `setup_test_users.py`: Script to generate demo data (users and carbon footprint entries).
- `carbon_footprint/run.bat`: Windows batch script to easily setup and run the app.

## Prerequisites

- **Python 3.8+** must be installed and added to your system PATH.

## Installation & Setup

1.  **Navigate to the project directory** (if not already there):
    ```bash
    cd "path/to/project2 - Copy"
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    cd carbon_footprint
    pip install -r requirements.txt
    ```

3.  **Database Migration**:
    Initialize the database schema.
    ```bash
    python manage.py migrate
    ```

4.  **Create Test Users & Data**:
    You can populate the database with test users (`customer_demo` and `company_admin`) using the provided script.
    Note: You may need to move `setup_test_users.py` into the `carbon_footprint` directory or run it via shell referencing the path.
    
    *Easier method:* Copy `setup_test_users.py` into `carbon_footprint/` and run:
    ```bash
    python manage.py shell < setup_test_users.py
    ```

## Running the Application

### Option 1: Using the Batch Script (Windows)

Navigate to the `carbon_footprint` folder and double-click `run.bat` or run it from command line:
```cmd
cd carbon_footprint
run.bat
```
This script acts as a helper to install dependencies, migrate DB, collect static files, and start the server.

### Option 2: Manual Start

From the `carbon_footprint` directory:

```bash
python manage.py runserver
```

The application will be accessible at: **http://127.0.0.1:8000/**

## Usage Credentials

The system comes with pre-configured test accounts (if you ran the setup script):

### 📱 Customer Account
*For tracking personal carbon footprint*
- **Username**: `customer_demo`
- **Password**: `customer123`

### 🏢 Company Admin Account
*For viewing analytics and user data*
- **Username**: `company_admin`
- **Password**: `company123`

## URLs

- **Home/Login**: `http://127.0.0.1:8000/calculator/login/` (or root `/`)
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
