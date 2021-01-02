# ![Shamseya Backend Challenge](project-logo.png)

## Installation

1. Clone this repository: `git clone https://github.com/Amr-Hash/Shamseya-backend-challenge.git`.
2. Create a new virtualenv : `python -m venv venv`.
3. Activate virtualenv `Mac OS / Linux`: `source venv/bin/activate` , `Windows`: `venv\Scripts\activate`.
4. Install requiremnts: `pip install -r requirements.txt`.
5. Create .env file using .env.example or add to Environment variables for Windows users.
6. Make migrations: `python review\manage.py makemigrations`.
7. Migrate Database: `python review\manage.py migrate`.
8. Seed Data into Database: `python review\manage.py initdata <number_of_reviews:optional(default:4000)>`.

## Testing

1. Run all tests: `python review\manage.py test api`.
2. Run Endpoint test: `python review\manage.py test api.tests.GetReviewsTest`.
3. Run Benchmark test: `python review\manage.py test api.test.BenchmarkReviewsTest`.
