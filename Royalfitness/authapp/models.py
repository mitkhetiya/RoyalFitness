from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=12)
    description=models.TextField()
    def __str__(self):
        return self.name
    
class Enrollment(models.Model):
    FullName=models.CharField(max_length=25)
    Email=models.EmailField()
    Gender=models.CharField(max_length=12)
    PhoneNumber=models.CharField(max_length=12)
    DOB=models.DateField()    
    SelectTrainer=models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True)
    Reference=models.CharField(max_length=25)
    Address=models.TextField()
    paymentStatus=models.CharField(max_length=25)
    Duedate=models.DateField(blank=True, null=True)
    Price=models.IntegerField(blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.FullName

class Trainer(models.Model):
    name=models.CharField(max_length=25)
    gender=models.CharField(max_length=12)
    phone=models.CharField(max_length=15)
    salary=models.IntegerField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.name
    
class MembershipPlan(models.Model):
    plan=models.CharField(max_length=25)
    price=models.IntegerField()
    def __str__(self):
        return self.plan  

class Gallery(models.Model):
    title=models.CharField(max_length=100)
    img=models.ImageField(upload_to='gallery')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.title      
    
class Attendance(models.Model):
    Selectdate=models.DateTimeField(auto_now_add=True)
    phonenumber=models.CharField(max_length=15)
    Login=models.CharField(max_length=200)
    Logout=models.CharField(max_length=200)
    SelectWorkout=models.CharField(max_length=200)
    TrainedBy=models.CharField(max_length=200)
    def __str__(self): 
        return f"Attendance {self.id}"

class about(models.Model):
     title=models.CharField(max_length=100)
     description=models.TextField()
     img=models.ImageField(upload_to='about')
     timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
     def __str__(self):
         return self.title     

class services(models.Model):
     title=models.CharField(max_length=100)
     description=models.TextField()
     img=models.ImageField(upload_to='services')
     timeStamp=models.DateTimeField(auto_now_add=True,blank=True)
     def __int__(self):
         return self.id     

class free_trial(models.Model):    
    fullname=models.CharField(max_length=25)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=12)      
    goals=models.TextField()
    def __str__(self):
        return self.fullname   
    
class Payment(models.Model):
    enrollment=models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    amount=models.IntegerField()
    payment_date=models.DateTimeField(auto_now_add=True)
    stripe_payment_intent=models.CharField(max_length=255)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.enrollment.FullName}"