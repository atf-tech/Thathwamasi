from django.db import models

class ContactMessage(models.Model):
    PAGE_CHOICES = [
        ('index', 'Index Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
    ]

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)   
    email = models.EmailField()
    message = models.TextField()
    source_page = models.CharField(max_length=20, choices=PAGE_CHOICES)  
    submitted_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - {self.source_page}"
