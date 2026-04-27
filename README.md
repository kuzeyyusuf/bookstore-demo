# Bookstore Inventory & Sales Demo

## Project Description

This project is a local web-based bookstore system developed using Flask and SQLite.

The main goal is to demonstrate a system that can:

- Handle corrupted (junk) data  
- Restore the system to a clean, reusable "Golden State"  
- Provide a simple admin and user interface  
- Simulate a basic e-commerce workflow  

## Features

User:
- Login system  
- View books  
- Add books to cart  
- Checkout simulation  

Admin:
- Login system  
- View and manage inventory  
- Add and delete books  
- Generate junk (corrupted) data  
- Reset system to Golden State  
- View sales chart  

## Technologies Used

- Python (Flask)  
- SQLite  
- HTML / CSS  
- JavaScript (Chart.js)  

## Setup and Run Instructions

1. Create virtual environment:
python -m venv venv

Activate:
venv\Scripts\activate

2. Install Flask:
pip install flask

3. Initialize database:
python init_db.py

4. Run project:
python app.py

Open:
http://127.0.0.1:5000

## Login Credentials

Admin:
Email: admin@bookstore.com  
Password: admin123  

User:
Email: user@bookstore.com  
Password: user123  

## Demo Scenario

1. Login as Admin  
2. Generate Junk Data  
3. Observe broken system  
4. Reset Golden State  
5. System becomes clean again  
