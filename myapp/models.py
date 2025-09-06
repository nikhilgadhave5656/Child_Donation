from django.db import models
from django.contrib.auth.models import User

class Contact (models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=150)
    phone=models.CharField(max_length=15,blank=True)
    message=models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Child(models.Model):
    name=models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='child_images/')
    def __str__(self):
        return self.name

class Payment (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)#who user
    child=models.ForeignKey(Child,on_delete=models.CASCADE)# child specific
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    payment_id=models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending','Pending'), ('Completed','Completed'), ('Failed','Failed')],
        default='Pending'
    )

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.child.name} - {self.status}"
    



