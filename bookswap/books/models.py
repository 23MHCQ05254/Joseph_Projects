from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Good', 'Good'),
        ('Acceptable', 'Acceptable'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    campus = models.CharField(max_length=100, default="Unknown Campus")
    department = models.CharField(max_length=100)
    semester = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    image = models.ImageField(upload_to='book_images/', default='placeholder.jpg')
    contact_number = models.CharField(
        max_length=20,
        help_text="WhatsApp or mobile number",
        blank=True,
        null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver} at {self.timestamp}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.book.title}"
