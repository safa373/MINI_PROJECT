from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('logout/',views.logout),
    path('login/',views.login),
    path('login_post/',views.login_post),
    path('adminhome/',views.adminhome),
    path('changepassword/',views.changepassword),
    path('changepassword_post/',views.changepassword_post),
    path('adddepartment/',views.adddepartment),
    path('adddepartment_post/',views.adddepartment_post),
    path('viewdepartment/',views.viewdepartment),
    path('viewdepartment_post/',views.viewdepartment_post),
    path('deletedepartment/<id>',views.deletedepartment),
    path('editdepartment/<id>',views.editdepartment),
    path('editdepartment_post/',views.editdepartment_post),
    path('addcourse/',views.addcourse),
    path('addcoursepost/',views.addcoursepost),
    path('viewcourse/',views.viewcourse),
    path('viewcoursepost/',views.viewcoursepost),
    path('deletecourse/<id>',views.deletecourse),
    path('editcourse/<id>',views.editcourse),
    path('editcoursepost/',views.editcoursepost),
    path('addstudent/',views.addstudent),
    path('addstudentpost/',views.addstudentpost),
    path('viewstudent/',views.viewstudent),
    path('viewstudentpost/',views.viewstudentpost),
    path('deletestudent/<id>',views.deletestudent),
    path('editstudent/<id>',views.editstudent),
    path('editstudentpost/',views.editstudentpost),
    path('addstaff/',views.addstaff),
    path('addstaffpost/',views.addstaffpost),
    path('viewstaff/',views.viewstaff),
    path('deletestaff/<id>',views.deletestaff),
    path('viewstaffpost/',views.viewstaffpost),
    path('editstaff/<id>',views.editstaff),
    path('editstaffpost/',views.editstaffpost),
    path('addauthority/',views.addauthority),
    path('addauthoritypost/',views.addauthoritypost),
    path('viewauthority/',views.viewauthority),
    path('viewauthoritypost/',views.viewauthoritypost),
    path('deleteauthority/<id>',views.deleteauthority),
    path('editauthority/<id>',views.editauthority),
    path('editauthoritypost/',views.editauthoritypost),
    path('addincident/',views.addincident),
    path('addincidentpost/',views.addincidentpost),
    path('viewincident/',views.viewincident),
    path('viewincidentpost/',views.viewincidentpost),
    path('deleteincident/<id>',views.deleteincident),
    path('editincident/<id>',views.editincident),
    path('editincidentpost/',views.editincidentpost),
    path('attendance/',views.attendance),
    path('attendancepost/',views.attendancepost),
    path('viewfeedback/',views.viewfeedback),
    path('viewfeedbackpost/',views.viewfeedbackpost),
    path('viewcomplaint/',views.viewcomplaint),
    path('viewcomplaintpost/',views.viewcomplaintpost),
    path('sendreply/<id>',views.sendreply),
    path('adm_takeaction/<id>',views.adm_takeaction),
    path('sendreplypost/',views.sendreplypost),
    path('adm_takeaction_post/',views.adm_takeaction_post),







    path('student_login/',views.student_login),
    path('student_Register/', views.student_Register),
    path('student_Viewattendence/', views.student_Viewattendence),
    path('student_Viewissuelist/', views.student_Viewissuelist),
    path('student_writefeedback/', views.student_writefeedback),
    path('and_viewprofile/', views.and_viewprofile),
    path('user_changepassword/', views.user_changepassword),






    path('parent_Register/',views. parent_Register),
    path('parent_Viewattendence/', views.parent_Viewattendence),
    path('parent_Viewissuelist/', views.parent_Viewissuelist),
    path('and_par_sendfeedback/', views.parent_Rightfeedback),
    path('parent_view_student/', views.parent_Viewstudents),
    path('parent_view_notification/',views.parent_Viewnotification),
    path('parent_Requestforoutpass/', views.parent_Requestforoutpass),
    path('and_sendcomplaint/', views.parent_complaintsend),
    path('parent_view_replay/', views.parent_viewreplay),
    path('parent_view_authority/', views.parent_Viewauthority),
    path('parent_chatwithauthority/', views.parent_chatwithauthority),
    path('parent_viewoutpassstatus/',views.parent_viewoutpassstatus),
    path('and_parent_view_outpass_status/',views.and_parent_view_outpass_status),
    path('student_send_request/',views.student_send_request),
    path('and_parent_view_checkincheckout/',views.and_parent_view_checkincheckout),
    path('parent_view_violence/',views.parent_view_violence),

    path('securityguard_viewprofile/', views.securityguard_viewprofile),
    path('securityguard_viewgatepassrequest/', views.securityguard_viewgatepassrequest),
    path('securityguard_allow/', views.securityguard_allow),
    path('securityguard_viewviolencenotification/', views.securityguard_viewviolencenotification),
    path('securityguard_changepassword/', views.securityguard_changepassword),
    path('security_profile/', views.security_profile),
    path('security_view_notification/', views.security_view_notification),
    path('and_guard_view_outpass_status/', views.and_guard_view_outpass_status),
    path('markin_gatepass/', views.markin_gatepass),
    path('markout_gatepass/', views.markout_gatepass),

    # path('chat/<toid>', views.chat),
    # path('chat_view/<tid>', views.chat_view),
    # path('chat_send/<msg>/<tid>', views.chat_send),

    path('chat/<id>', views.chat1),
    path('chat_view/', views.chat_view),
    path('chat_send/<msg>', views.chat_send),

    path('user_sendchat/', views.user_sendchat),
    path('user_viewchat/', views.user_viewchat),
    # path('test/', views.test),




]