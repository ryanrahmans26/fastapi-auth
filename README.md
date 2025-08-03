# FastAPI Auth

A simple authentication system built with FastAPI, MySQL, and JWT.

## How to run
1. Clone the repository
2. Create a `.env` file based on the `.env.example` file
- Set MySQL credentials
- Set JWT secret
3. Import the `users.sql` table
4. Install the dependencies using `pip install -r requirements.txt`
5. Run the application using `uvicorn main:app --reload`

Swagger documentation is available at `http://localhost:8000/docs`
