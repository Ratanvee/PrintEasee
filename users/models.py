from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings
from PyPDF2 import PdfReader
from django.db import models
from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     unique_url = models.SlugField(unique=True, blank=True, null=True)
#     total_orders = models.PositiveIntegerField(default=0)  # Add this line
#     total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add total revenue
#     total_customers = models.PositiveIntegerField(default=0)  # New field

#     def save(self, *args, **kwargs):
#         if not self.unique_url:  # Generate only if empty
#             base_url = self.username.lower().replace(" ", "-")
#             unique_part = str(uuid.uuid4())[:8]
#             self.unique_url = f"{base_url}-{unique_part}"

#             # Ensure uniqueness in case of a rare conflict
#             while CustomUser.objects.filter(unique_url=self.unique_url).exists():
#                 unique_part = str(uuid.uuid4())[:8]
#                 self.unique_url = f"{base_url}-{unique_part}"

#         super().save(*args, **kwargs)

import uuid
from django.contrib.auth.models import AbstractUser
from djongo import models  # Use djongo's models for MongoDB compatibility

class CustomUser(AbstractUser):
    unique_url = models.CharField(max_length=255, unique=True, blank=True, null=True)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_customers = models.IntegerField(default=0)
    id = models.AutoField(primary_key=True)  # Ensure it's an integer, not an ObjectId

    def save(self, *args, **kwargs):
        if not self.unique_url:  # Generate only if empty
            base_url = self.username.lower().replace(" ", "-")
            unique_part = str(uuid.uuid4())[:8]
            self.unique_url = f"{base_url}-{unique_part}"

            # Ensure uniqueness in MongoDB (rare conflicts possible)
            while CustomUser.objects.filter(unique_url=self.unique_url).exists():
                unique_part = str(uuid.uuid4())[:8]
                self.unique_url = f"{base_url}-{unique_part}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username




from django.db import models
from django.conf import settings
from PyPDF2 import PdfReader

# class Document(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('in_process', 'In Process'),
#         ('completed', 'Completed'),
#     ]

#     PAPER_SIZE_CHOICES = [
#         ('A4', 'A4'),
#         ('A3', 'A3'),
#         ('Letter', 'Letter'),
#         ('Legal', 'Legal'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The customer who uploaded the file
#     file = models.FileField(upload_to='documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     num_copies = models.PositiveIntegerField(default=1)
#     color_type = models.CharField(
#         max_length=11,
#         choices=[('black_white', 'Black & White'), ('color', 'Color'), ('both', 'Both')],
#         default='black_white'
#     )
#     double_sided = models.BooleanField(default=False)
#     paper_size = models.CharField(max_length=10, choices=PAPER_SIZE_CHOICES, default='A4')
#     # price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     num_pages = models.PositiveIntegerField(default=1)

#     def save(self, *args, **kwargs):
#         """Automatically count pages in the PDF before saving."""
#         if self.file and self.file.name.endswith(".pdf"):
#             try:
#                 pdf = PdfReader(self.file)
#                 self.num_pages = len(pdf.pages)
#             except Exception as e:
#                 print(f"Error reading PDF: {e}")
#                 self.num_pages = 1  # Default to 1 if an error occurs

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.username} - {self.file.name} ({self.num_pages} pages)"




from decimal import Decimal
from PyPDF2 import PdfReader
from django.db import models
from django.conf import settings

class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
    ]

    PAPER_SIZE_CHOICES = [
        ('A4', 'A4'),
        ('A3', 'A3'),
        ('Letter', 'Letter'),
        ('Legal', 'Legal'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    num_copies = models.PositiveIntegerField(default=1)
    color_type = models.CharField(
        max_length=11,
        choices=[('black_white', 'Black & White'), ('color', 'Color'), ('both', 'Both')],
        default='black_white'
    )
    double_sided = models.BooleanField(default=False)
    paper_size = models.CharField(max_length=10, choices=PAPER_SIZE_CHOICES, default='A4')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    num_pages = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        """Automatically count pages in the PDF before saving and ensure price is stored correctly."""
        if self.file and self.file.name.endswith(".pdf"):
            try:
                pdf = PdfReader(self.file)
                self.num_pages = len(pdf.pages)
            except Exception as e:
                print(f"Error reading PDF: {e}")
                self.num_pages = 1  # Default to 1 if an error occurs

        # Ensure price is always a valid decimal
        if self.price is not None:
            try:
                self.price = Decimal(str(self.price).replace("“", "").replace("”", "").strip())
            except:
                self.price = None  # Set to None if conversion fails

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.file.name} ({self.num_pages} pages)"

    
    # def save(self, *args, **kwargs):
    #     """Calculate the number of pages in the uploaded PDF before saving."""
    #     if self.file:
    #         try:
    #             pdf = PdfReader(self.file)
    #             self.num_pages = len(pdf.pages)  # Count total pages
    #             print('NO. of pages : ', self.num_pages)
    #         except:
    #             self.num_pages = 1  # Default to 1 if there's an error
    #             print('This is default value ')




from django.db import models

class Order(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"


from django.db import models

class PrintOrder(models.Model):
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('printing', 'Printing'),
        ('completed', 'Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
