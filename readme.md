# Inventory Management System

## Overview

This project is a Django-based web application designed to manage products, warehouses, and inventory operations. It includes features such as barcode generation and display in the admin interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later
- pip (Python package manager)
- Virtualenv (optional but recommended)
- PostgreSQL (or your preferred database)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**

   Ensure your database server is running and create a database for the project. Update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Apply Migrations**

   Run the following command to apply database migrations:

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**

   Create an admin user to access the Django admin interface:

   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files**

   Collect static files for the project:

   ```bash
   python manage.py collectstatic
   ```

## Running the Project

To start the development server, run:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin` in your web browser and log in using the superuser credentials you created.

## Features

- **Barcode Generation**: The project uses the `python-barcode` library to generate barcodes. Ensure this library is installed and configured correctly.
- **Admin Interface**: The admin interface displays barcodes as images using base64 encoding.

## Additional Information

- **Environment Variables**: You may need to set environment variables for sensitive information such as secret keys and database credentials. Consider using a `.env` file and a library like `python-decouple` or `django-environ`.

- **Testing**: To run tests, use:

  ```bash
  python manage.py test
  ```
