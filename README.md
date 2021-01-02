# ![Shamseya Backend Challenge](project-logo.jpg)

## Installation

1. Clone this repository: `git clone https://github.com/Amr-Hash/Shamseya-backend-challenge.git`.
2. cd into project directory: `cd Shamseya-backend-challenge/`.
3. Create a new virtualenv : `python3 -m venv venv` for windows may use `python -m venv venv`.
4. Activate virtualenv `Mac OS / Linux`: `source venv/bin/activate` , `Windows`: `venv\Scripts\activate`.
5. Install requiremnts: `pip install -r requirements.txt`.
6. Create `.env` file using `.env.example`.
7. Make migrations: `python reviews/manage.py makemigrations`.
8. Migrate Database: `python reviews/manage.py migrate`.
9. Seed Data into Database: `python reviews/manage.py initdata <number_of_reviews:optional(default:4000)>`.

## Testing

* Run all tests: `python reviews/manage.py test api`.
* Run Endpoint test: `python reviews/manage.py test api.tests.GetReviewsTest`.
* Run Benchmark test: `python reviews/manage.py test api.tests.BenchmarkReviewsTest`.

## Running
1. Run server using: `python reviews/manage.py runserver`.

## Usage
* Using postman: send GET request to `http://127.0.0.1:8000/api/days?from=2018-01-01&to=2020-12-13`.
> :Note: **from & to**: are totally optional you could use them both or just one of them or neither.

> :Note: **You could use saved postman collection**: `Shamseya Backend Challenge.postman_collection.json`.
* Use basic authintication for superuser or staff user to be able to get results.
* Results
    ```
    {
        "detail": "Invalid username/password."
    }
    ``` 
    * with status code `401` for Unauthenticated users.
    ```
    {
        "detail": "You do not have permission to perform this action."
    }
    ```
    * with status code `403` for Unauthorized users.
    ```
    [
        {
            "submitted_at": "2018-08-05",
            "count": 4,
            "answers": [
                {
                    "choice": "21-30",
                    "count": 2
                },
                ...
            ]
        },
        ...
    ]
    ```
    * with status code `200` for authenticated and authorized users.

## Debugging
* For every succesful request on the runnig server command this lines would expalin how man query was made for this request and the time it takes to handle the request
```
Function : list
Number of Queries : 3
Finished in : 2.12s
[02/Jan/2021 23:03:34] "GET /api/days/?from=2018-01-01&to=2018-03-31 HTTP/1.1" 200 379616
```
