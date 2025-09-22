from django.db import models


# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=120)
    type = models.CharField(max_length=20)


class Department(models.Model):
    departmentname = models.CharField(max_length=100)


class Course(models.Model):
    coursename = models.CharField(max_length=100)
    DEPARTMENT = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=100)


class Student(models.Model):
    name = models.CharField(max_length=100)
    phonenumber = models.BigIntegerField()
    emailid = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=100)
    photo = models.CharField(max_length=250)
    housename = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    state = models.CharField(max_length=100)
    guardianname = models.CharField(max_length=100)
    guardianemail = models.CharField(max_length=100)
    guardianphonenumber = models.BigIntegerField()
    COURSE = models.ForeignKey(Course, on_delete=models.CASCADE)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)


class Authority(models.Model):
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=250)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)


class Staff(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    photo = models.CharField(max_length=250)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100)
    phonenumber = models.BigIntegerField()
    dob = models.DateField()


class Incident(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=100)


class Attendance(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=100)
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance=models.CharField(max_length=100)


class Feedback(models.Model):
    date = models.DateField()
    feedback = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)


class Notification(models.Model):
    date = models.DateField()
    notification = models.CharField(max_length=100)
    AUTHORITY=models.ForeignKey(Authority, on_delete=models.CASCADE)


class Outpass(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    fromtime = models.CharField(max_length=100)
    totime = models.CharField(max_length=100)
    appstatus = models.CharField(max_length=100)
    chstatus = models.CharField(max_length=100)


class Checkincheckout(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)


class Violence(models.Model):
    STUDENT = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    action=models.CharField(max_length=100, default='pending')
    time = models.CharField(max_length=100)


class Violencehub(models.Model):
    VIOLENCE = models.ForeignKey(Violence, on_delete=models.CASCADE)
    action=models.CharField(max_length=100, default='pending')
    photo = models.CharField(max_length=300)

class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phonenumber = models.BigIntegerField()
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)


class Complaint(models.Model):
    date = models.DateField()
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)


class Issuelist(models.Model):
    date = models.DateField()
    issue = models.CharField(max_length=100)


class Chat(models.Model):
    date = models.DateField()
    message = models.CharField(max_length=100)
    FROMID = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='frmid')
    TOID = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='toid')

class security(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    photo = models.CharField(max_length=250)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.IntegerField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    emailid = models.CharField(max_length=100)
    phonenumber = models.BigIntegerField()
    dob = models.DateField()
    idproof=models.CharField(max_length=250)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    AUTHORITY=models.ForeignKey(Authority,on_delete=models.CASCADE)





