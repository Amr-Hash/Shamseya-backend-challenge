from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIClient
from django.urls import reverse
from django.conf import settings
from .models import Review, Answer, Day
from django.db.models import Count, F
import json, os
from rest_framework import status

# Create your tests here.

client = APIClient()

class GetReviewsTest(TestCase):
    """ Test module for GET Reviews API """
    
    def setUp(self):
        call_command('initdata','50')
        with open(os.path.join(settings.BASE_DIR, 'api', 'fixtures', 'users.json'), 'r') as users_file:
            self.users = json.loads(users_file.read())
        
    def test_superuser_get_all_reviews(self):
        # get API response
        for user in self.users:
            if user['is_superuser'] and user['is_active']:
                superuser = user
                break
        client.login(username=superuser['username'], password=superuser['password'])
        response = client.get(reverse('day-list'))
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_staff_get_all_reviews(self):
        # get API response
        for user in self.users:
            if user['is_staff'] and user['is_active']:
                staff = user
                break
        client.login(username=staff['username'], password=staff['password'])
        response = client.get(reverse('day-list'))
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_non_staff_or_super_user_get_all_reviews(self):
        # get API response
        for user in self.users:
            if user['is_active'] and not(user['is_staff'] or user['is_superuser']):
                active = user
                break
        client.login(username=active['username'], password=active['password'])
        response = client.get(reverse('day-list'))
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_superuser_get_from_to_reviews(self):
        # get API response
        for user in self.users:
            if user['is_superuser'] and user['is_active']:
                superuser = user
                break
        client.login(username=superuser['username'], password=superuser['password'])
        response = client.get(reverse('day-list'), {'from': '2018-02-03','to':'2019-01-17'})
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_superuser_get_from_only_reviews(self):
        # get API response
        for user in self.users:
            if user['is_superuser'] and user['is_active']:
                superuser = user
                break
        client.login(username=superuser['username'], password=superuser['password'])
        response = client.get(reverse('day-list'), {'from': '2018-02-03'})
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_superuser_get_from_to_only_reviews(self):
        # get API response
        for user in self.users:
            if user['is_superuser'] and user['is_active']:
                superuser = user
                break
        client.login(username=superuser['username'], password=superuser['password'])
        response = client.get(reverse('day-list'), {'to': '2018-02-03'})
        client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BenchmarkReviewsTest(TestCase):
    """ Benchmark Test module for GET Reviews API """
    
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'api', 'fixtures', 'users.json'), 'r') as users_file:
            self.users = json.loads(users_file.read())
        self.sequance = [4000, 8000, 12000, 16000, 20000]
        
    def test_sequance(self):
        for user in self.users:
            if user['is_superuser'] and user['is_active']:
                superuser = user
                break
        client.login(username=superuser['username'], password=superuser['password'])
        for number in self.sequance:
            # get API response
            call_command('initdata',number)
            for user in self.users:
                if user['is_superuser'] and user['is_active']:
                    superuser = user
                    break
            client.login(username=superuser['username'], password=superuser['password']) 
            response = client.get(reverse('day-list'))
            client.logout()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
