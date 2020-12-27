import json
import os
from datetime import date, timedelta
import random

cur_path = os.path.dirname(__file__)

with open(f'{cur_path}\\questions.json', 'r') as f_q:
    questions = json.loads(f_q.read())

number_of_reviews = 1000
first_date = date(year=2018, month=1, day=1)
last_date = date(year=2020, month=12, day=31)
number_of_days = (last_date - first_date).days

with open(f'{cur_path}\\reviews.json', 'w') as f_rev:
    with open(f'{cur_path}\\answers.json', 'w') as f_ans:
        f_rev.write('[')
        f_ans.write('[')
        for _ in range(number_of_reviews):
            random_days = random.randint(0, number_of_days)
            date = (first_date + timedelta(days=random_days)).isoformat()
            review = {
                "model": "review.review",
                "pk": _,
                "fields": {
                    "submitted_at": date
                }
            }
            f_rev.write(json.dumps(review))
            f_rev.write(',')
        f_rev.write(']')
        f_ans.write(']')