from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('HospitalLogin.html', views.HospitalLogin, name="HospitalLogin"), 
	       path('EducationLogin.html', views.EducationLogin, name="EducationLogin"), 
	       path('UserLogin.html', views.UserLogin, name="UserLogin"), 
	       path('AddHospitals.html', views.AddHospitals, name="AddHospitals"),
	       path('AddHospitalsAction', views.AddHospitalsAction, name="AddHospitalsAction"),	
	       path('AddEducation', views.AddEducation, name="AddEducation"),
	       path('AddEducationAction', views.AddEducationAction, name="AddEducationAction"),
	       path('ViewHospitals', views.ViewHospitals, name="ViewHospitals"),
	       path('ViewEducation', views.ViewEducation, name="ViewEducation"),
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"), 
	       path('HospitalLoginAction', views.HospitalLoginAction, name="HospitalLoginAction"), 	
	       path('EducationLoginAction', views.EducationLoginAction, name="EducationLoginAction"),	
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	
	       path('AddStudent', views.AddStudent, name="AddStudent"),
	       path('AddStudentAction', views.AddStudentAction, name="AddStudentAction"),
	       path('ViewStudent', views.ViewStudent, name="ViewStudent"),
	       path('AddPatients', views.AddPatients, name="AddPatients"),
	       path('AddPatientsAction', views.AddPatientsAction, name="AddPatientsAction"),
	       path('ViewPatients', views.ViewPatients, name="ViewPatients"),
]
