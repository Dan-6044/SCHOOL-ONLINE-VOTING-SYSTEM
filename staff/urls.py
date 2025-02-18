from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'), #Include user_id in URL
    path('panel/', views.panel, name='panel'),
    path('add-voter/', views.add_voter, name='add_voter'),
    path('add-candidate/', views.add_candidate, name='add_candidate'),
    path('tables/', views.tables, name='tables'),
    path('reports/', views.reports, name='reports'),
     path('update-profile/', views.update_profile, name='update_profile'),
     path('logout/', views.logout_view, name='logout'),

   
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
