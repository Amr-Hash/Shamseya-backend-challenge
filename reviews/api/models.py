from django.db import models

# Create your models here.

class Day(models.Model):
    date = models.DateField(unique=True)

# class AnnotatedManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().annotate(count=Count('reviews'))

class Review(models.Model):
    submitted_at = models.DateTimeField()
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='reviews')

    # objects = AnnotatedManager()

    def __str__(self):
        return self.submitted_at.isoformat()

class Choice(models.Model):
    text = models.CharField(max_length=20)
    
    def __str__(self):
        return self.text

class Question(models.Model):
    text = models.TextField()
    choices = models.ManyToManyField(Choice, related_name='questions')

    def __str__(self):
        return self.text


class Answer(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.review} - {self.question}'