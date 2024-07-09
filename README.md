# Django Pricing Module

This project is a web application with a configurable pricing module that supports differential pricing. It is built using Django and allows for flexible pricing configurations.

## Features

- Configurable pricing based on ride distance, time, waiting time, and day of the week.
- Custom Django Admin interface for managing pricing configurations.
- API endpoint to calculate the price based on the provided details.

## Prerequisites

- Python 3.x
- Django 3.x

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/devid-koch/assignment-django-v2.git
   cd assignment-django-v2

2. **Create and activate a virtual environment:**

    python -m venv venv
    source venv/bin/activate

3. **Install the dependencies:**
    pip install -r requirements.txt

4. **Set up the database:**
    Here I am using sqlite
    Create a database for the project.
    Update the DATABASES setting in settings.py with your database configuration.

5. **Run the migrations:**
    
    python manage.py migrate

6. **python manage.py createsuperuser**

    python manage.py createsuperuser

7. **Start the development server:**

    python manage.py runserver

8. Access the application at http://127.0.0.1:8000/.


## Admin Interface

Access the Django Admin at http://127.0.0.1:8000/admin/.
Log in with the superuser credentials created earlier.
        **username: hp**
        **password: 123**
Manage pricing configurations via the Django Admin interface.


## API Usage

Endpoint
POST [/pricing/api/calculate-price/]

**Request Body**
{
  "pricing_config_id": 7, // id of the pricing configuration
  "distance": 10,
  "travel_time": 2,
  "waiting_time": 5,
  "day": "monday"
}


**Response**

{
    "price": "80.83"
}

## How to get the pricing config id

ENDPOINT to fetch all configurations

GET [/pricing/api/pricing-configs/]

here you will get all the pricing configurations including id's for each price configuration


## Testing with Postman

    Start the Django server:

    python manage.py runserver

    Open Postman and create a new POST request to http://127.0.0.1:8000/pricing/api/calculate-price/.

    Set the request body to JSON and add the following content:

    {
        "pricing_config_id": 7, // id of the pricing configuration
        "distance": 10,
        "travel_time": 2,
        "waiting_time": 5,
        "day": "monday"
    }

    Send the request and you should get a response like:

    {
        "price": "80.83"
    }



