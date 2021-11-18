from django.urls import path

from . import views

urlpatterns= [
	path('', views.index, name='home-view'),
	path('posts', views.post_of_friends_profiles, name='posts-profile' ),
	path('create_post', views.create_post, name='create-post'),
	path('update/<id>', views.update_post, name='update-post'),
	path('detail/<pk>', views.detail_post, name='detail-post'),
	path('delete/<pk>', views.delete_post, name='delete-post')
]