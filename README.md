# Pricing Configuration App

This is a Django-based application to configure and manage pricing for a taxi booking service. The app includes APIs to estimate prices and generate invoices for rides, as well as admin views to manage pricing configurations.

## Features

- CRUD operations for pricing configurations and day-specific pricing.
- API endpoints for estimating ride prices and generating invoices.
- Email notifications for generated invoices.
- Integration with PostgreSQL via pgAdmin.
- Connection pooling using PgBouncer.

## Requirements

- Python 3.11
- Django 4.x
- PostgreSQL
- PgBouncer
- Django REST Framework

## Installation


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
    Set Up Environment Variables
        Create a .env file in the project root and add your environment variables:

        env
        Copy code
        DEBUG=True
        SECRET_KEY=your_secret_key
        EMAIL_HOST_USER=your_email@gmail.com
        EMAIL_HOST_PASSWORD=your_app_password
        DATABASE_URL=postgres://username:password@localhost:5432/pricing_config_db


        Set Up PostgreSQL and PgBouncer
        PostgreSQL: Ensure PostgreSQL is installed and running.
        PgBouncer: Install and configure PgBouncer for connection pooling.

5. **Run the migrations:**
    
    python manage.py migrate

6. **python manage.py createsuperuser**

    python manage.py createsuperuser

7. **Start the development server:**

    python manage.py runserver

8. Access the application at http://127.0.0.1:8000/.


Email Configuration
The application uses Gmail for sending emails. Make sure to:

Enable "Less Secure Apps" in your Google account settings or use an App Password if you have 2FA enabled.
Update the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file.


## API Usage

Endpoint
POST [/pricing/api/estimate-price/]

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



## Testing with Postman

    Start the Django server:

    python manage.py runserver

    Open Postman and create a new POST request to http://127.0.0.1:8000/pricing/api/estimate-price.

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


    Generate Invoice: POST /pricing/api/generate-invoice/

    {
        "pricing_config_id": 1,
        "distance": 10,
        "travel_time": 2,
        "waiting_time": 5,
        "day": "monday",
        "user_email":"email@gmail.com",
        "total_tax_percentage":"18"
}
