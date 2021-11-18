from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
	# path('list', vie/ws.profile_list, name='profile-list'),
	path('', views.ProfileListView.as_view(), name='profile-list'),
	path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
	path('search/', views.search, name='search'),
	path('follow/', views.follow_and_unfollow , name="follow_unfollow"),
	path('myprofile/', views.my_profile, name='myprofile'),
] 