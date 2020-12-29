import json, random, os, sys
from datetime import datetime, timedelta, timezone

cur_path = os.path.dirname(__file__)

if len(sys.argv) > 1:
    try:
        number_of_reviews = int(sys.argv[1])
        if number_of_reviews <= 0:
            print('number of reviews must be postive int greater than 0 - set to default (4000)')
            number_of_reviews = 4000    
    except:
        print('number of reviews must be int - set to default (4000)')
        number_of_reviews = 4000    
else:
    number_of_reviews = 4000

with open(f'{cur_path}\\questions.json', 'r') as f_q:
    questions = json.loads(f_q.read())

first_date = datetime(year=2018, month=1, day=1).astimezone(timezone.utc)
last_date = datetime(year=2020, month=12, day=31).astimezone(timezone.utc)
number_of_days = (last_date - first_date).days

with open(f'{cur_path}\\reviews.json', 'w') as f_rev:
    with open(f'{cur_path}\\answers.json', 'w') as f_ans:
        f_rev.write('[')
        f_ans.write('[')
        for review_pk in range(number_of_reviews):
            random_days = random.randint(0, number_of_days)
            date = (first_date + timedelta(days=random_days)).isoformat()
            review = {
                "model": "api.review",
                "pk": review_pk,
                "fields": {
                    "submitted_at": date
                }
            }
            f_rev.write(json.dumps(review))
            if review_pk != (number_of_reviews-1):
                f_rev.write(',')

            review_questions = random.sample(questions, 4)
            for count, question in enumerate(review_questions):
                choice = random.choice(question['fields']['choices'])
                answer = {
                    "model": "api.answer",
                    "pk": ((review_pk * 4) + count),
                    "fields": {
                        "review": review_pk,
                        "question": question['pk'],
                        "choice": choice
                    }
                }
                f_ans.write(json.dumps(answer))
                if review_pk != (number_of_reviews-1) or count != 3:
                    f_ans.write(',')

        f_rev.write(']')
        f_ans.write(']')

print(f'{number_of_reviews} reviews has created.')