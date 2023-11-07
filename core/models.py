from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from autoslug import AutoSlugField
import secrets
User = get_user_model()

class Profile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    id_user = models.IntegerField(null=True)
    phone_number = models.CharField(max_length=300)
    how_did_you_hear_about_us = models.TextField()
    nationality = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    about_me = models.TextField()

    def __str__(self):
        return self.owner
    

class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = AutoSlugField(populate_from="title", editable=False, primary_key=True)
    date_published = models.DateField(auto_now_add=True)
    body = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    about = models.TextField(null=True)
    image = models.FileField(upload_to="poll_images", null=True)

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['title'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res

    def __str__(self):
        return self.title


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.title[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.poll.title[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'


# Create your models here.
