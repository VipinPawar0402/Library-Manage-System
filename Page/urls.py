from django.urls import path
from Page import views


urlpatterns = [
    path("signin/", views.person, name='person'),
    path("send_data/", views.send_data, name='send_data'),
    path("persondata/", views.persondata, name='persondata'),
    path("delete/<int:person_id>/", views.delete_data,name="delete_data"),
    path('edit-person/<int:person_id>/', views.edit_data,name="edit_data"),
    path("update-person/", views.update_data, name="update_data"),
    path('show-date/', views.show_date, name='show_date'),
    path('show-time/', views.show_time, name='show_time'),
    path('login/', views.login_view, name='login'),
    path('person-detail/<int:pid>/', views.person_view, name='persons'),
    path('logout/', views.logout_view, name='logout'),
    path("header/", views.HeaderView.as_view(), name='header'),
    path("sidebar/", views.SidebarView.as_view(), name='sidebar'),
    path("", views.BaseView.as_view(), name='base'),
    path("person-table/", views.person_table,name='person-table'),
    path("login-page/", views.login_page,name='login-page'),
    path("forget-page/", views.forget_page, name='forget-page'),
    path('reset/',views.send_otp,name= 'reset'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('set-pass/', views.set_pass, name='set_pass')
]
