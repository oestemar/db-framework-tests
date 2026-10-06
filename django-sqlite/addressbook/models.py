from django.db import models

class AddressBook(models.Model):
    name = models.CharField(max_length=100)
    kana = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('男', '男'), ('女', '女'), ('不明', '不明')], blank=True, null=True)
    blood_type = models.CharField(max_length=3, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name