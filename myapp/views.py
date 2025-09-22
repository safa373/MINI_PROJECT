from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

from myapp.models import *

def adminhome(request):
    return render(request, "admin/Admin_index.html")
def logout(request):
    request.session['lid']=''
    return redirect('/myapp/login/')



def login(request):
    return render(request, "loginindex.html")

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    log=Login.objects.filter(username=username,password=password)
    if log.exists():
        log1=Login.objects.get(username=username,password=password)
        request.session['lid']=log1.id
        if log1.type=='admin':
            return HttpResponse('''<script>alert('welcome');window.location='/myapp/adminhome/'</script>''')
        elif log1.type=='authority':
            return HttpResponse('''<script>alert('welcome');window.location='/myapp/authorityhome/'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid');window.location='/myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/myapp/login/'</script>''')

def changepassword(request):
    return render(request,'admin/changepassword.html')

def changepassword_post(request):
    oldpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']
    log=Login.objects.filter(password=oldpassword)
    if log.exists():
        log1=Login.objects.get(password=oldpassword,id=request.session['lid'])
        if newpassword==confirmpassword:
            log1 = Login.objects.filter(password=oldpassword, id=request.session['lid']).update(password=newpassword)
            return HttpResponse('''<script>alert('successfully changed');window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert('invalid');window.location='/myapp/changepassword/'</script>''')
    else:
        return HttpResponse('''<script>alert('invalid');window.location='/myapp/changepassword/'</script>''')


def adddepartment(request):
    return render(request,'admin/department.html')

def adddepartment_post(request):
    department=request.POST['textfield']

    obj=Department()
    obj.departmentname=department
    obj.save()
    return HttpResponse('''<script>alert('Succesfully Added');window.location='/myapp/adddepartment/#mu-features'</script>''')

def viewdepartment(request):
    res=Department.objects.all()
    return render(request,'admin/view department.html',{'data':res})

def viewdepartment_post(request):
    search=request.POST['textfield']
    res=Department.objects.filter(departmentname__icontains=search)
    return render(request,'admin/view department.html',{'data':res})

def deletedepartment(request,id):
    res=Department.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert('Succesfully Deleted');window.location='/myapp/viewdepartment/#mu-features'</script>''')

def editdepartment(request,id):
    res=Department.objects.get(id=id)
    return render(request,'admin/editdepartment.html',{'data':res})

def editdepartment_post(request):
    department = request.POST['textfield']
    id=request.POST['id']

    obj = Department.objects.get(id=id)
    obj.departmentname = department
    obj.save()
    return HttpResponse('''<script>alert('Succesfully Edited');window.location='/myapp/viewdepartment/#mu-features'</script>''')


def addcourse(request):
    res=Department.objects.all()
    return render(request,'admin/course.html',{'data':res})

def addcoursepost(request):
    department=request.POST['select']
    semester=request.POST['select2']
    course=request.POST['textfield3']

    obj=Course()
    obj.DEPARTMENT_id=department
    obj.semester=semester
    obj.coursename=course
    obj.save()
    return HttpResponse('''<script>alert('Succesfully Added');window.location='/myapp/addcourse/#mu-features'</script>''')


def viewcourse(request):
    res=Course.objects.all()
    return render(request,'admin/view course.html',{'data':res})

def viewcoursepost(request):
    search=request.POST['textfield']
    res=Course.objects.filter(coursename__icontains=search)
    return render(request,'admin/view course.html',{'data':res})

def deletecourse(request,id):
    res=Course.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert('Succesfully Deleted');window.location='/myapp/viewcourse/#mu-features'</script>''')

def editcourse(request,id):
    res=Department.objects.all()
    res1=Course.objects.get(id=id)
    return render(request,'admin/editcourse.html',{'data':res,'data1':res1})

def editcoursepost(request):
    department=request.POST['select']
    semester=request.POST['select2']
    course=request.POST['textfield3']
    id=request.POST['id']

    obj=Course.objects.get(id=id)
    obj.DEPARTMENT_id=department
    obj.semester=semester
    obj.coursename=course
    obj.save()
    return HttpResponse('''<script>alert('Succesfully Updated');window.location='/myapp/viewcourse/#mu-features'</script>''')




def addstudent(request):
    res=Course.objects.all()
    date=datetime.now().today()
    return render(request,'admin/student.html',{'data':res,'date':date})

def addstudentpost(request):
    name=request.POST['textfield']
    phno=request.POST['textfield2']
    email=request.POST['textfield3']
    dob=request.POST['textfield4']
    gender=request.POST['RadioGroup1']
    photo=request.FILES['textfield5']
    housename=request.POST['textfield6']
    place=request.POST['textfield7']
    city=request.POST['textfield8']
    post=request.POST['textfield9']
    pin=request.POST['textfield10']
    state=request.POST['textfield11']
    guardianname=request.POST['textfield12']
    guardianemail=request.POST['textfield13']
    guardianphno=request.POST['textfield14']
    course=request.POST['select']


    if Login.objects.filter(username=email).exists():
        return HttpResponse('''<script>alert('Student mail already exists');history.back()</script>''')


    if not Login.objects.filter(username=guardianemail).exists():
        lobj2 = Login()
        lobj2.username = guardianemail
        lobj2.password = guardianphno
        lobj2.type = 'parent'
        lobj2.save()


    from datetime import datetime
    date=datetime.now().strftime('%y%m%d-%H%M%S')+'.jpg'
    fs=FileSystemStorage()
    fs.save(date,photo)
    path=fs.url(date)

    lobj=Login()
    lobj.username=email
    lobj.password=phno
    lobj.type='student'
    lobj.save()


    obj=Student()
    obj.name=name
    obj.phonenumber=phno
    obj.emailid=email
    obj.dob=dob
    obj.gender=gender
    obj.photo=path
    obj.housename=housename
    obj.place=place
    obj.city=city
    obj.post=post
    obj.pin=pin
    obj.state=state
    obj.guardianname=guardianname
    obj.guardianemail=guardianemail
    obj.guardianphonenumber=guardianphno
    obj.COURSE_id=course
    obj.LOGIN=lobj
    obj.save()
    return HttpResponse('''<script>alert('Succesfully Added');window.location='/myapp/addstudent/#mu-features'</script>''')


def viewstudent(request):
    res=Student.objects.all()
    return render(request,'admin/view student.html',{'data':res})

def viewstudentpost(request):
    search=request.POST['textfield']
    res = Student.objects.filter(name__icontains=search)
    return render(request,'admin/view student.html',{'data':res})

def deletestudent(request,id):
    res=Student.objects.get(id=id)
    res.delete()
    return HttpResponse('''<script>alert('Succesfully Deleted');window.location='/myapp/viewstudent/#mu-features'</script>''')

def editstudent(request,id):
    res=Course.objects.all()
    res1=Student.objects.get(id=id)
    date=datetime.now().today()
    return render(request,'admin/editstudent.html',{'data':res,'data1':res1,'date':date})

def editstudentpost(request):
    name=request.POST['textfield']
    phno=request.POST['textfield2']
    email=request.POST['textfield3']
    dob=request.POST['textfield4']
    gender=request.POST['RadioGroup1']
    housename=request.POST['textfield6']
    place=request.POST['textfield7']
    city=request.POST['textfield8']
    post=request.POST['textfield9']
    pin=request.POST['textfield10']
    state=request.POST['textfield11']
    guardianname=request.POST['textfield12']
    guardianemail=request.POST['textfield13']
    guardianphno=request.POST['textfield14']
    course=request.POST['select']
    id=request.POST['id']


    obj=Student.objects.get(id=id)
    if 'textfield5' in request.FILES:
        photo = request.FILES['textfield5']
        from datetime import datetime
        date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, photo)
        path = fs.url(date)
        obj.photo = path
        obj.save()

    obj.name=name
    obj.phonenumber=phno
    obj.emailid=email
    obj.dob=dob
    obj.gender=gender
    obj.housename=housename
    obj.place=place
    obj.city=city
    obj.post=post
    obj.pin=pin
    obj.state=state
    obj.guardianname=guardianname
    obj.guardianemail=guardianemail
    obj.guardianphonenumber=guardianphno
    obj.COURSE_id=course
    obj.save()
    return HttpResponse('''<script>alert('Succesfully Updated');window.location='/myapp/viewstudent/#mu-features'</script>''')



def adm_takeaction(request,id):
    return render(request,'admin/takeaction.html',{'id':id})

def adm_takeaction_post(request):
    action=request.POST['action']
    id=request.POST['id']
    # Violencehub.?objects.filter(id=id).update(action=action)

    Violencehub.objects.filter(VIOLENCE_id=id).update(action=action)



    d=Violence.objects.get(id=id)
    d.action=action
    d.save()



    return HttpResponse('''<script>alert('Action Submitted succesfully');window.location='/myapp/viewincident/'</script>''')
def viewincident(request):
    res=Violence.objects.all()
    return render(request,'admin/view incident.html',{'data':res})

def viewincidentpost(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    res=Violence.objects.filter(daterange=[fromdate,todate])
    return render(request, 'admin/view incident.html', {'data': res})

def view_violence(request,id):
    # res=Violencehub.objects.all()
    res=Violencehub.objects.filter(VIOLENCE_id=id)
    return render(request,'admin/view violence.html',{'data':res})

def view_violence_post(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    res=Violence.objects.filter(VIOLENCEdate__range=[fromdate,todate])
    return render(request,'admin/view violence.html',{'data':res})

def addstaff(request):
    return render(request,'admin/staff.html')

def addstaffpost(request):
    name=request.POST['name']
    gender=request.POST['RadioGroup1']
    photo=request.FILES['filefield']
    date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
    fs = FileSystemStorage()
    fs.save(date, photo)
    path = fs.url(date)
    place=request.POST['textfield']
    post=request.POST['textfield2']
    pin=request.POST['textfield3']
    district=request.POST['textfield4']
    state=request.POST['textfield5']
    emailid=request.POST['textfield6']
    phonenumber=request.POST['textfield7']
    dob=request.POST['textfield8']

    obj=Staff()
    obj.name=name
    obj.gender=gender
    obj.photo=path

    obj.place=place
    obj.post=post
    obj.pin=pin
    obj.district=district
    obj.state=state
    obj.emailid=emailid
    obj.phonenumber=phonenumber
    obj.dob=dob
    obj.save()

    return HttpResponse('''<script>alert('succesfully added');window.location='/myapp/adminhome/'</script>''')


def viewstaff(request):
    res=Staff.objects.all()
    return render(request,'admin/view staff.html',{'data':res})

def viewstaffpost(request):
    search=request.POST['textfield']
    res=Staff.objects.filter(name__icontains=search)
    return render(request, 'admin/view staff.html', {'data': res})

def deletestaff(request,id):
    res=Staff.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('succesfully deleted');window.location='/myapp/viewstaff/'</script>''')

def editstaff(request,id):
    res=Staff.objects.get(id=id)
    return render(request, 'admin/editstaff.html', {'data': res})

def editstaffpost(request):
    name=request.POST['name']
    gender=request.POST['RadioGroup1']


    place=request.POST['textfield']
    post=request.POST['textfield2']
    pin=request.POST['textfield3']
    district=request.POST['textfield4']
    state=request.POST['textfield5']
    emailid=request.POST['textfield6']
    phonenumber=request.POST['textfield7']
    dob=request.POST['textfield8']
    did=request.POST['id1']
    if'filefield'in request.FILES:
        photo = request.FILES['filefield']
        if photo !='':
            date = datetime.now().strftime('%y%m%d-%H%M%S') + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, photo)
            path = fs.url(date)
            obj = Staff.objects.get(id=did)
            obj.name = name
            obj.gender = gender
            obj.photo = path

            obj.place = place
            obj.post = post
            obj.pin = pin
            obj.district = district
            obj.state = state
            obj.emailid = emailid
            obj.phonenumber = phonenumber
            obj.dob = dob
            obj.save()

            return HttpResponse('''<script>alert('succesfully updated');window.location='/myapp/viewstaff/'</script>''')
    else:




        obj=Staff.objects.get(id=did)
        obj.name=name
        obj.gender=gender

        obj.place=place
        obj.post=post
        obj.pin=pin
        obj.district=district
        obj.state=state
        obj.emailid=emailid
        obj.phonenumber=phonenumber
        obj.dob=dob
        obj.save()

        return HttpResponse('''<script>alert('succesfully updated');window.location='/myapp/viewstaff/'</script>''')






def addauthority(request):
    return render(request,'admin/authority.html')

def addauthoritypost(request):
    name=request.POST['textfield']
    photo=request.FILES['textfield2']
    # housename=request.POST['textfield3']
    place=request.POST['textfield4']
    post=request.POST['textfield5']
    pin=request.POST['textfield6']
    district=request.POST['textfield7']
    state=request.POST['textfield8']
    password=request.POST['textfield9']
    email=request.POST['email']
    phone=request.POST['phone']
    lobj=Login()
    lobj.username=email
    lobj.password=password
    lobj.type='authority'
    lobj.save()
    fs=FileSystemStorage()
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    fn=fs.save(date,photo)
    obj=Authority()
    obj.name=name
    # obj.housename=housename
    obj.place=place
    obj.post=post
    obj.email=email
    obj.phone=phone
    obj.pin=pin
    obj.district=district
    obj.state=state
    obj.photo=fs.url(date)
    obj.LOGIN=lobj
    obj.save()


    return HttpResponse('''<script>alert('Succesfully Added');window.location='/myapp/addauthority/#mu-features'</script>''')


def viewauthority(request):
    res=Authority.objects.all()
    return render(request,'admin/view authority.html',{'data':res})

def viewauthoritypost(request):
    search=request.POST['textfield']
    res=Authority.objects.filter(name__icontains=search)
    return render(request,'admin/view authority.html',{'data':res})

def deleteauthority(request,id):
    res=Authority.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('succesfully deleted');window.location='/myapp/viewauthority/#mu-features'</script>''')

def editauthority(request,id):
    res=Authority.objects.get(id=id)
    return render(request, 'admin/editauthority.html', {'data': res})

def editauthoritypost(request):
    name = request.POST['textfield']

    # housename = request.POST['textfield3']
    place = request.POST['textfield4']
    post = request.POST['textfield5']
    pin = request.POST['textfield6']
    district = request.POST['textfield7']
    state = request.POST['textfield8']
    email = request.POST['email']
    phone = request.POST['phone']
    did=request.POST['id1']
    if'textfield2'in request.FILES:
        photo = request.FILES['textfield2']
        if photo!="":
            fs = FileSystemStorage()
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fn = fs.save(date, photo)
            obj = Authority.objects.get(id=did)
            obj.name = name
            # obj.housename = housename
            obj.place = place
            obj.post = post
            obj.pin = pin
            obj.district = district
            obj.state = state
            obj.email=email
            obj.phone=phone
            obj.photo = fs.url(date)
            obj.save()

            return HttpResponse('''<script>alert('Succesfully Updated');window.location='/myapp/viewauthority/#mu-features'</script>''')
    else:
        obj = Authority.objects.get(id=did)
        obj.name = name
        # obj.housename = housename
        obj.place = place
        obj.post = post
        obj.pin = pin
        obj.district = district
        obj.state = state
        obj.save()
        return HttpResponse('''<script>alert('Succesfully Updated');window.location='/myapp/viewauthority/#mu-features'</script>''')



def addincident(request):
    return render(request,'admin/incident.html')

def addincidentpost(request):
    description=request.POST['textarea']
    obj=Incident()
    obj.description=description
    from datetime import datetime
    obj.date=datetime.now().strftime('%Y%m%d')
    obj.save()
    return HttpResponse('''<script>alert('succesfully added');window.location='/myapp/adminhome/'</script>''')


# def viewincident(request):
#     res=Incident.objects.all()
#     return render(request,'admin/view incident.html',{'data':res})
#
# def viewincidentpost(request):
#     fromdate=request.POST['textfield']
#     todate=request.POST['textfield2']
#     res=Incident.objects.filter(date__range=[fromdate,todate])
#     return render(request, 'admin/view incident.html', {'data': res})

def deleteincident(request,id):
    res=Incident.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('succesfully deleted');window.location='/myapp/viewincident/'</script>''')

def editincident(request,id):
    res=Incident.objects.get(id=id)
    return render(request,'admin/editincident.html',{"data":res})

def editincidentpost(request):
    description=request.POST['textarea']
    id=request.POST['id']
    obj=Incident.objects.get(id=id)
    obj.description=description
    from datetime import datetime
    obj.date=datetime.now().strftime('%Y%m%d')
    obj.save()
    return HttpResponse('''<script>alert('succesfully updated');window.location='/myapp/viewincident/'</script>''')

def attendance(request):
    res=Attendance.objects.all()
    return render(request,'admin/view attendance.html',{'data':res})

def attendancepost(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    res = Attendance.objects.filter(date__range=[fromdate,todate])
    return render(request, 'admin/view attendance.html', {'data': res})


def viewfeedback(request):
    res=Feedback.objects.all()
    return render(request,'admin/view feedback.html',{'data':res})

def viewfeedbackpost(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    res = Feedback.objects.filter(date__range=[fromdate,todate])
    return render(request, 'admin/view feedback.html', {'data': res})


def viewcomplaint(request):
    res=Complaint.objects.all()
    return render(request,'admin/view complaint.html',{'data':res})

def viewcomplaintpost(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    res = Complaint.objects.filter(date__range=[fromdate,todate])
    return render(request, 'admin/view complaint.html', {'data': res})

def sendreply(request,id):
    return render(request, 'admin/send replay.html',{'id':id})

def sendreplypost(request):
    reply=request.POST['textarea']
    id=request.POST['id']
    Complaint.objects.filter(id=id).update(reply=reply,status='replied')
    return HttpResponse('''<script>alert('succesfully updated');window.location='/myapp/viewcomplaint/#mu-features'</script>''')




#################STUDEND



def student_login(request):
    username=request.POST['username']
    password=request.POST['password']
    print(request.POST)
    log=Login.objects.filter(username=username,password=password)
    if log.exists():
        log1=Login.objects.get(username=username,password=password)
        lid=log1.id

        if log1.type=='student':
            return JsonResponse({'status':'ok','lid':lid,'type':log1.type})
        if log1.type=='parent':
            return JsonResponse({'status':'ok','lid':lid,'type':log1.type})
        if log1.type=='security':
            return JsonResponse({'status':'ok','lid':lid,'type':log1.type})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status': 'no'})


def student_Register(request):
    name=request.POST['name']
    phonenumber=request.POST['phonenumber']
    emailid=request.POST['email']
    dob =request.POST['dob']
    gender=request.POST['gender']
    photo=request.POST['photo']
    housename=request.POST['housename']
    place=request.POST['place']
    city=request.POST['city']
    post=request.POST['post']
    pin=request.POST['pin']
    state=request.POST['state']
    guardianname=request.POST['guardianname']
    guardianemail=request.POST['guardianemail']
    guardianphonenumber=request.POST['guardianphonenumber']
    password=request.POST['password']
    confirmpassword=request.POST['confirmpassword']
    cid=request.POST['cid']

    lobj=Login()
    lobj.username=emailid
    lobj.password=confirmpassword
    lobj.type='student'
    lobj.save()

    if password==confirmpassword:
        obj=Student()
        obj.name=name
        obj.phonenumber=phonenumber
        obj.emailid=emailid
        obj.dob=dob
        obj.gender=gender
        obj.photo=photo
        obj.housename=housename
        obj.place=place
        obj.city=city
        obj.post=post
        obj.pin=pin
        obj.state=state
        obj.guardianname=guardianname
        obj.guardianemail=guardianemail
        obj.guardianphonenumber=guardianphonenumber
        obj.COURSE_id=cid
        obj.LOGIN_id=lobj.id
        obj.save()

    return JsonResponse({'status':'ok'})

def student_Viewattendence(request):
    lid=request.POST['lid']
    obj=Attendance.objects.get(STUDENT__LOGIN_id=lid)
    l=[]
    for i in obj:
        l.append({'id':i.id,'date':i.date,'time':i.time,'STUDENT':i.STUDENT.name,'attendance':i.attendance})
    return JsonResponse({'status':'ok','data':l})


def student_Viewissuelist(request):
    obj=Issuelist.objects.all()
    l=[]
    for i in obj:
        l.append({'id':i.id,'date':i.date,'issue':i.issue})
    return JsonResponse({'status':'ok','data':1})

def student_writefeedback(request):
    feedback=request.POST['feedback']
    lid=request.POST['lid']

    obj=Feedback()
    obj.feedback=feedback
    from datetime import datetime
    obj.date=datetime.now().today()
    obj.LOGIN_id=lid
    obj.save()
    return JsonResponse({'status':'ok'})


def and_viewprofile(request):
    lid=request.POST['lid']
    var=Student.objects.get(LOGIN_id=lid)
    print(var)
    return  JsonResponse({'status':'ok',
                          'name':var.name,
                          'email':var.emailid,
                          'phone_number':var.phonenumber,
                          'image':var.photo,
                          'gender':var.gender,
                          'housename':var.housename,
                          'place':var.place,
                          "city":var.city,
                          "post":var.post,
                          'district':var.city,
                          'state':var.state,
                          'pincode':var.pin,
                          'parentname':var.guardianname,
                          'parentnumber':var.guardianphonenumber,
                          'parentemail':var.guardianemail,
                          'dob':var.dob,
                          'course':var.COURSE.coursename})

def user_changepassword(request):
    lid = request.POST['lid']
    old = request.POST['old']
    newpass = request.POST['new']
    confirm = request.POST['confirm']

    var = Login.objects.filter(id=lid, password=old)
    if var.exists():
        if newpass == confirm:
            var2 = Login.objects.filter(id=lid).update(password=confirm)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'Not ok'})
    else:
        return JsonResponse({'status': 'NoT Ok'})
#################parent



def parent_Register(request):
    name=request.POST['name']
    emailid=request.POST['email']
    phonenumber=request.POST['phonenumber']
    place=request.POST['place']
    post=request.POST['post']
    pin=request.POST['pin']
    district=request.POST['district']
    state=request.POST['state']
    password=request.POST['password']
    confirmpassword=request.POST['confirmpassword']

    lobj=Login()
    lobj.username=emailid
    lobj.password=password
    lobj.type='parent'
    lobj.save()

    if password==confirmpassword:
        obj=Parent()
        obj.name=name
        obj.email=emailid
        obj.phonenumber=phonenumber
        obj.place=place
        obj.pin=pin
        obj.post=post
        obj.district=district
        obj.state=state
        obj.LOGIN=lobj
        obj.save()

    return JsonResponse({'status':'ok'})

def parent_Viewattendence(request):
    lid=request.POST['lid']
    obj=Attendance.objects.filter(STUDENT__LOGIN_id=lid)
    l=[]
    for i in obj:
        l.append({'id':id,'date':i.date,'time':i.time,'attendance':i.attendance})

    return JsonResponse({'status':'ok','data':l})

def parent_Viewissuelist(request):
    obj = Issuelist.objects.all()
    l = []
    for i in obj:
        l.append({'id': i.id, 'date': i.date, 'issue': i.issue})
    return JsonResponse({'status': 'ok', 'data': 1})


def parent_Rightfeedback(request):
    feedback = request.POST['feedback']
    lid = request.POST['lid']

    obj = Feedback()
    obj.feedback = feedback
    from datetime import datetime
    obj.date = datetime.now().today()
    obj.LOGIN_id = lid
    obj.save()
    return JsonResponse({'status':'ok'})

def parent_Viewstudents(request):
    lid=request.POST['lid']
    res=Student.objects.filter(guardianemail=Login.objects.get(id=lid).username)
    l = []
    for var in res:
        l.append({'id': var.id,
                  'name':var.name,
                          'email':var.emailid,
                          'phone_number':var.phonenumber,
                          'image':var.photo,
                          'gender':var.gender,
                          'housename':var.housename,
                          'place':var.place,
                          "city":var.city,
                          "post":var.post,
                          'district':var.city,
                          'state':var.state,
                          'pincode':var.pin,
                          'parentname':var.guardianname,
                          'parentnumber':var.guardianphonenumber,
                          'parentemail':var.guardianemail,
                          'dob':var.dob,
                          'course':var.COURSE.coursename})
        print(l,'lllll')
    return JsonResponse({'status': 'ok', 'data': l})

def parent_Viewnotification(request):
    obj = Violence.objects.all()
    l = []
    for i in obj:
        l.append({'id': i.id, 'date': i.date,'time': i.time, 'notification': i.action, 'authority':i.STUDENT.name})
    return JsonResponse({'status':'ok','data':l})

def parent_Requestforoutpass(request):
    obj = Outpass.objects.all()
    l = []
    for i in obj:
        l.append({'student': i.STUDENT, 'date': i.date, 'fromtime': i.fromtime, 'totime': i.totime, 'appstatus':i.appstatus, 'chstatus':i.chstatus})
    return JsonResponse({'status':'ok'})

def parent_complaintsend(request):
    lid=request.POST['lid']
    complaint=request.POST['complaint']
    from datetime import datetime
    date=datetime.now()
    obj=Complaint()
    obj.date=date
    obj.complaint=complaint
    obj.reply='pending'
    obj.status='pending'

    obj.LOGIN_id=lid
    obj.save()
    return JsonResponse({'status':'ok'})

def parent_viewreplay(request):
    lid=request.POST['lid']
    obj=Complaint.objects.filter(LOGIN_id=lid)
    l=[]
    for i in obj:
        l.append({'id':i.id,'complaint':i.complaint,'date':i.date,'status':i.status,'reply':i.reply})
    return JsonResponse({'status':'ok','data':l})

def parent_Viewauthority(request):
    lid=request.POST['lid']
    obj=Authority.objects.all()
    l = []
    for i in obj:
              l.append({
                  'id':i.id,
                  'LOGIN_id':i.LOGIN.id,
                  'name':i.name,
                        'photo':i.photo,

                        'place':i.place,
                  'email':i.email,
                        'phone':i.phone

                        })
    return JsonResponse({'status':'ok','data':l})

def au_view_student(request):
    data=Student.objects.all()
    return render(request,'authority/viewstudent.html',{'data':data})

def parent_chatwithauthority(request):
    lid=request.POST['lid']
    obj=Authority.objects.all()
    l = []
    for i in obj:
        l.append({})
    return JsonResponse({'status':'ok'})

def parent_viewoutpassstatus(request):
    lid=request.POST['lid']
    obj=Outpass.objects.all()
    l = []
    for i in obj:
        l.append({'STUDENT':i.STUDENT,
                  'date':i.date,'fromtime':i.fromtime,'totime':i.totime,'appstatus':i.appstatus,'chstatus':i.chstatus})
    return JsonResponse({'status':'ok'})


def and_parent_view_outpass_status(request):
    lid=request.POST['lid']
    # res = Outpass.objects.filter(STUDENT__LOGIN_id=lid)

    res=Student.objects.get(guardianemail=Login.objects.get(id=lid).username)

    res = Outpass.objects.filter(STUDENT_id=res)
    cat = []
    for i in res:
        cat.append({

            'id': i.id,
            'date': i.date,
            'fromtime': i.fromtime,
            'totime': i.totime,
            'app_status': i.appstatus,
            'ch_status': i.chstatus,
            # 'lid': i.LOGIN_id

        })
    return JsonResponse({"status": "ok", "data": cat})

def student_send_request(request):
    lid = request.POST['lid']
    sid = request.POST['sid']
    date = request.POST['date']
    fromtime = request.POST['fromtime']
    totime = request.POST['totime']
    cobj = Outpass()
    cobj.date = date
    cobj.fromtime=fromtime
    cobj.totime=totime
    cobj.appstatus='pending'
    cobj.chstatus='requested'

    # res=Student.objects.filter(guardianemail=Login.objects.get(id=lid).username)
    cobj.STUDENT_id=sid

    cobj.STUDENT = Student.objects.get(id=sid)
    cobj.save()
    return JsonResponse({'status': 'ok'})

def and_parent_view_checkincheckout(request):
    lid=request.POST['lid']

    res = Student.objects.get(guardianemail=Login.objects.get(id=lid).username)

    res = Checkincheckout.objects.filter(STUDENT_id=res)
    cat = []
    for i in res:
        cat.append({

            'id': i.id,
            'date': i.date,
            'time': i.time,
            'type': i.type,
            # 'lid': i.LOGIN_id

        })
    print(cat,'hiiiiiiii')
    return JsonResponse({"status": "ok", "data": cat})

def parent_view_violence(request):
    sid = request.POST['sid']
    res = Violencehub.objects.filter(VIOLENCE__STUDENT_id=sid)
    cat=[]
    # print()
    for i in res:
        cat.append({

            'id': i.id,
            'date': i.VIOLENCE.date,
            'photo': i.photo,

            # 'name': i.type,
            # 'lid': i.LOGIN_id

        })
    print(cat)
    return JsonResponse({"status": "ok", "data": cat})
#################securityguard



def securityguard_viewprofile(request):
    lid=request.POST['lid']
    obj=security.objects.get(LOGIN_id=lid)
    return JsonResponse({'status':'ok',
                         'name':obj.name,
                         'gender':obj.gender,
                         'photo':obj.photo,
                         'place':obj.place,
                         'post':obj.post,
                         'pin':obj.pin,
                         'district':obj.district,
                         'state':obj.state,
                         'email':obj.emailid,
                         'phone':obj.phonenumber,
                         'dob':obj.dob,
                         'idproof':obj.idproof,'AUTHORITY':obj.AUTHORITY.name})

def securityguard_viewgatepassrequest(request):
    obj=security.objects.all()
    l = []
    for i in obj:
        l.append(
            {'STUDENT': i.STUDENT, 'date': i.date, 'fromtime': i.fromtime, 'totime': i.totime, 'appstatus': i.appstatus,
             'chstatus': i.chstatus})
    return JsonResponse({'status':'ok'})

def securityguard_allow(request):
    return JsonResponse({'status':'ok'})

def securityguard_viewviolencenotification(request):
    obj=Violencehub.objects.getall
    l = []
    for i in obj:
        l.append({'VIOLENCE':i.VIOLENCE,'STUDENT':i.STUDENT,'action':i.action,'date':i.date,'photo':i.photo})
    return JsonResponse({'status':'ok'})

def securityguard_changepassword(request):
    lid=request.POST['lid']
    oldpassword = request.POST['oldpassword']
    newpassword = request.POST['newpassword']
    confirmpassword = request.POST['confirmpassword']
    log = Login.objects.filter(password=oldpassword)
    if log.exists():
        log1 = Login.objects.get(password=oldpassword, id=lid)
        if newpassword == confirmpassword:
            log1 = Login.objects.filter(password=oldpassword, id=lid).update(password=newpassword)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no'})

    else:
        return JsonResponse({'status':'no'})







def security_profile(request):
    lid=request.POST['lid']
    ress=security.objects.get(LOGIN_id=lid)
    return JsonResponse({"status": "ok",
                         'name': ress.name,
                         'email': ress.emailid,
                         'phone':ress.phonenumber,
                         'place':ress.place,
                         'post':ress.post,
                         'pin':ress.pin,
                         'city':ress.district,
                         'state':ress.state,
                         'photo':ress.photo,
                         })

def security_view_notification(request):
    var=Violencehub.objects.all()
    l = []
    for i in var:
        l.append({
            'id': i.id,
            'date':i.VIOLENCE.date,
            'photo':i.VIOLENCE.photo,
            'time':i.VIOLENCE.time,
            'name':i.STUDENT.name})
    return JsonResponse({'status': 'ok', 'data': l})

def and_guard_view_outpass_status(request):
    res = Outpass.objects.filter(appstatus='approved')
    # res = Outpass.objects.all()
    cat = []
    for i in res:
        cat.append({

            'id': i.id,
            'date': i.date,
            'fromtime': i.fromtime,
            'totime': i.totime,
            'app_status': i.appstatus,
            'ch_status': i.chstatus,
            'name':i.STUDENT.name,
            'photo':i.STUDENT.photo,
            'dept':i.STUDENT.COURSE.DEPARTMENT.departmentname,
            # 'lid': i.LOGIN_id

        })
    return JsonResponse({"status": "ok", "data": cat})

def markin_gatepass(request):
    sid=request.POST['sid']
    res=Outpass.objects.filter(id=sid).update(chstatus='CheckIn')
    return JsonResponse({"status": "ok", "data": res})


def markout_gatepass(request):
    sid=request.POST['sid']
    res=Outpass.objects.filter(id=sid).update(chstatus='CheckOut')
    return JsonResponse({"status": "ok", "data": res})




def chat1(request, id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid


    student= Student.objects.get(LOGIN_id=id)

    lid= Login.objects.get(username= student.guardianemail)
    cid=lid.id
    request.session["userid"] = cid

    return render(request, "authority/Chat.html", {'photo': "/static/bg2.jpg", 'name': "parent", 'toid': cid})

def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]
    # qry = Student.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q
    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid)).order_by('id')
    l = []
    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TOID_id, "date": i.date, "from": i.FROMID_id})
    return JsonResponse({'photo':'/static/bg2.jpg', "data": l, 'name': "parent", 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]



    print(toid,lid,"===================")
    message = msg
    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.message = message
    chatobt.TOID_id = toid
    chatobt.FROMID_id = lid
    chatobt.date = d
    chatobt.save()
    return JsonResponse({"status": "ok"})

# flutter

def user_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    msg=request.POST['message']
    from  datetime import datetime


    print(FROM_id,TOID_id)

    c=Chat()
    c.FROMID_id=FROM_id
    c.TOID_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()

    return JsonResponse({'status':"ok"})

def user_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]

    from django.db.models import Q
    res = Chat.objects.filter(Q(FROMID_id=fromid, TOID_id=toid) | Q(FROMID_id=toid, TOID_id=fromid))
    l = []
    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROMID_id, "date": i.date, "to": i.TOID_id})


    return JsonResponse({"status":"ok",'data':l})





#cam
# def test(request):
#     import cv2
#     import face_recognition
#     res=Student.objects.all()
#     knownimage = []
#     knownids = []
#     for i in res:
#         s = i.photo
#         s = s.replace("/", "\\")
#         pth = "C:\\Users\\user\\PycharmProjects\\violencedetection" + s
#         picture_of_me = face_recognition.load_image_file(pth)
#         # print(pth)
#         my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
#         knownimage.append(my_face_encoding)
#         knownids.append(i.id)
#     vid = cv2.VideoCapture(0)
#     while (True):
#         ret, frame = vid.read()
#         cv2.imwrite(r"C:\\Users\\user\\PycharmProjects\\violencedetection\\media\\tests\\a.jpg", frame)
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         picture_of_others = face_recognition.load_image_file(r"C:\\Users\\user\\PycharmProjects\\violencedetection\\media\\tests\\b..jpg")
#         others_face_encoding = face_recognition.face_encodings(picture_of_others)
#         totface = len(others_face_encoding)
#         for i in range(0, totface):
#             res = face_recognition.compare_faces(knownimage, others_face_encoding[i], tolerance=0.5)
#             print(res)
#             l = 0
#             for j in res:
#                 if j == True:
#
#                     import datetime
#                     if not Checkincheckout.objects.filter(STUDENT_id=knownids[l], date=datetime.date.today(), type='CheckIn').exists():
#                         cv2.imwrite(r"C:\\Users\\user\\PycharmProjects\\violencedetection\\media\\"+str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))+".jpg", frame)
#                         qry = Checkincheckout()
#                         qry.STUDENT_id = knownids[l]
#                         qry.date = datetime.date.today()
#                         # if period == 1:
#                         qry.type = 'CheckIn'
#                         # if period == 5:
#                         #     qry.checkin_checkout = 'Check Out'
#                         qry.time = datetime.datetime.now().strftime('%H:%M:%S')
#                         # qry.photo='/media/'+str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))+".jpg"
#                         qry.save()
#                     elif Checkincheckout.objects.filter(STUDENT_id=knownids[l], date=datetime.date.today(), type='CheckIn').exists():
#                         att = Checkincheckout.objects.filter(STUDENT_id=knownids[l], date=datetime.date.today())
#                         if len(att)==2:
#                             break
#                         # if att.checkin_checkout=='Check In':
#                         # att = Attendance.objects.get(STUDENT_id=knownids[l], date=datetime.date.today())
#                         dt = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
#                         cv2.imwrite(r"C:\\Users\\user\\PycharmProjects\\violencedetection\\media\\"+dt+".jpg", frame)
#                         qry = Checkincheckout()
#                         qry.STUDENT_id = knownids[l]
#                         qry.date = datetime.date.today()
#                         # if period == 1:
#                         # qry.checkin_checkout = 'Check In'
#                         # if period == 5:
#                         qry.type = 'CheckOut'
#                         # qry.photo='/media/'+dt+".jpg"
#                         qry.time = datetime.datetime.now().strftime('%H:%M:%S')
#                         qry.save()
#
#                 l = l + 1
#     vid.release()
#     # Destroy all the windows
#     cv2.destroyAllWindows()
#     return redirect('/myapp/login/')




