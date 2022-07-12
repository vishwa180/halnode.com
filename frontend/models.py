from django.db import models


class ContactMessage(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    done = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.email


class Lead(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    done = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.email
