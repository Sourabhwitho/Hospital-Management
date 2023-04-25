from django.db import models
from django.contrib.auth.models import User
    
class Doctor(models.Model):
    name=models.CharField(max_length=200,null=True)
    speciality=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)

    # tags=models.ManyToManyField(Tag)
    def __str__(self):
        return self.name
    
class Patient(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    DAYS=(
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
    )
    TIME_SLOT=(
        ('09:00 AM','09:00 : 09:30'),
        ('10:00 AM','10:00 : 10:30'),
        ('11:00 AM','11:00 : 11:30'),
        ('12:00 PM','12:00 : 12:30'),
        ('1:00 PM','13:00 : 13:30'),
        ('2:00 PM','14:00 : 14:30'),
        ('3:00 PM','15:00 : 15:30'),
        ('4:00 PM','16:00 : 16:30'),
        ('15:00 PM','17:00 : 17:30'),
    )
    patient=models.ForeignKey(Patient,null=True,on_delete=models.SET_NULL)
    Doctor=models.ForeignKey(Doctor,null=True,on_delete=models.SET_NULL)
    day=models.CharField(max_length=200,null=True,choices=DAYS)
    time_slot=models.CharField(max_length=200,choices=TIME_SLOT)

    def __str__(self):
        return '{} {} {}. Patient: {}'.format(self.day, self.time_slot, self.Doctor, self.patient)

    
