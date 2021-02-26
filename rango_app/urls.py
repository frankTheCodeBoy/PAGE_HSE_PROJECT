"""Defines urls for rango_app"""
from django.urls import path
from . import views

app_name = "rango_app"
urlpatterns = [
    path(
        "", 
        views.index, 
        name='index',
    ),
    path(
        'about/', 
        views.about, 
        name='about',
    ),
    path(
        'category/<slug:category_name_slug>/', 
        views.show_category, 
        name='show_category',
    ),
    path(
        'add_category/', 
        views.add_category, 
        name='add_category',
    ),
    path(
        'category/<slug:category_name_slug>/add_page/', 
        views.add_page, 
        name='add_page',
    ),
    path(
        'restricted',
        views.restricted,
        name='restricted'
    ),
    path(
        'goto/', 
        views.track_url, 
        name='goto'
    ),
    path(
        'search/',
        views.search_page,
        name='search_page'
    ),
    path(
        'profile/<username>/', 
        views.ProfileView.as_view(), 
        name='profile'),
    path(
        'profile/', 
        views.ListProfilesView.as_view(), 
        name='list_profiles'
    ),
    path(
        'like/',
        views.like_category,
        name='like_category'
    ),
    path(
        'suggest/',
        views.suggest_category,
        name='suggest_category'
    ),
    
]