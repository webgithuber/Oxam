from django.urls import path , include
from dashboard import views as dashboard_views
app_name = "dashboard"
urlpatterns = [
    path('admin-login',dashboard_views.admin_login , name='admin_login'),
    path('candidate-list',dashboard_views.list , name='list'),
    path('dashboard/',dashboard_views.dashboard , name='dashboard'),
    path('start-test',dashboard_views.starttest , name='start-test'),
    path('save-img',dashboard_views.saveimg , name='save-img'),
    path('logout',dashboard_views.logout_request , name='logout'),
    path('<int:image_id>',dashboard_views.show_image , name='show_image'),
    path('<str:email>/<str:code>',dashboard_views.detail , name='detail'),

    
]