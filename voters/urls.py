from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('voting/', views.voting, name='voting'),
    path('auth/', views.authenticate_voter, name='auth'),
    path('voter_page/', views.voter_page, name='voter_page'),
      path("vote/<int:candidate_id>/", views.vote, name="vote"),
    path("unvote/<int:candidate_id>/", views.unvote, name="unvote"),
     path('logout_voter/', views.logout_voter, name='logout_voter'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
