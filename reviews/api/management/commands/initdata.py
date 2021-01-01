from django.core.management import BaseCommand, call_command
from django.contrib.auth.models import User
from api.models import Day
from django.conf import settings
import os, json, sys, random
from datetime import datetime, timedelta, timezone

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of users for testing purposes"
    
    def add_arguments(self, parser):
        parser.add_argument('number_of_reviews', type=int, nargs='?', default=4000)
    
    def handle(self, *args, **options):
        with open(os.path.join(settings.BASE_DIR, 'api', 'fixtures', 'users.json'), 'r') as users_file:
            users = json.loads(users_file.read())
            for user in users:
                get_fields = {key:value for key,value in user.items() if key in ['username','email']}
                update_fields = {key:value for key,value in user.items() if key not in ['username','email','password']}
                user_object, created = User.objects.update_or_create(**get_fields, defaults=update_fields)
                user_object.set_password(user['password'])
                user_object.save()
        print('Users has created-or-updated')

        # init reviews and answers
        with open(os.path.join(settings.BASE_DIR, 'api', 'fixtures', 'questions.json'), 'r') as questions_file:
            questions = json.loads(questions_file.read())
    
        first_date = datetime(year=2018, month=1, day=1).astimezone(timezone.utc)
        last_date = datetime(year=2020, month=12, day=31).astimezone(timezone.utc)
        number_of_days = (last_date - first_date).days

        with open(os.path.join(settings.BASE_DIR, 'api', 'fixtures','reviews.json'), 'w') as reviews_file:
            with open(os.path.join(settings.BASE_DIR, 'api', 'fixtures', 'answers.json'), 'w') as answers_file:
                reviews_list = []
                answers_list = []
                for review_pk in range(options['number_of_reviews']):
                    random_days = random.randint(0, number_of_days)
                    date = first_date + timedelta(days=random_days)
                    day, created = Day.objects.get_or_create(date=date.date())
                    date = date.isoformat()
                    review = {
                        "model": "api.review",
                        "pk": review_pk,
                        "fields": {
                            "submitted_at": date,
                            "day": day.pk
                        }
                    }
                    reviews_list.append(review)
                    
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
                        answers_list.append(answer)
                answers_file.write(json.dumps(answers_list))
                reviews_file.write(json.dumps(reviews_list))
        print(f'{options["number_of_reviews"]} reviews has created.')
        
        # load data to database
        call_command('loaddata','choices','questions','reviews','answers')
