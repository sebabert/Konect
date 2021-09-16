from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views


app_name = 'konekt'
urlpatterns = [
    path('', views.search_index, name='search_view'),
    path('download/', views.format_cv),
    path('cvs/', views.listing_cv),
    path('cv/<int:candidate_id>/', views.detail_candidate),
    path('search/', views.search_candidate),
    path('add_candidate/', views.add_candidate, name='add_candidate'),
    path('edit_candidate/<int:candidate_id>/', views.edit_candidate, name='edit_candidate'),
    path('delete_candidate/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),
    # path('add_fullcandidate/', views.add_fullcandidate, name='add_fullcandidate'),
    path('candidates/', views.CandidateListView.as_view(), name='candidate_list'),
    path('candidates/<int:pk>/', views.CandidateDetailView.as_view(), name='candidate_detail'),
    path('candidates/add/', views.CandidateCreateView.as_view(), name='candidate_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
