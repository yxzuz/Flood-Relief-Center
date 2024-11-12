# Flood-Relief-Center

| Username | Password  |
| -------- | --------- |
| admin    | admin1234 |

## Installation guides

1. Clone the project from Github
    ```
    git clone https://github.com/yxzuz/Flood-Relief-Center.git
    ```
2. Open the project file in your IDE
3. Go to Flood-Relief-Center directory
    ```
    cd Flood-Relief-Center
    ```
4. Create your virtual environment
    ```
    python3 -m venv env
    ```
5. Activate virtual environment
   ```
   # On Mac/Linux
   source env/bin/activate
   
   # On Window
   env\Scripts\activate
   ```
6. Install requirements.txt
    ```
    pip install -r requirements.txt
    ```

7. Run Migrations
    ```
    python manage.py migrate
    ```
8. Load fixture data
    ```
    python manage.py loaddata data/data-v1.json
    ```
9. Run server
    ```
    python manage.py runserver
    ```
10. Access the server on your browser http://127.0.0.1:8000/