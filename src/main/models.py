from django.db import models


class CV(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    skills = models.TextField()
    projects = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    contacts = models.TextField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
