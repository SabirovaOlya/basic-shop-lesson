from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from apps.schemas import schema

from rest_framework.routers import DefaultRouter
from apps.views import (
    CategoryListCreateAPIView,
    ProductListCreateAPIView,
    RegisterCreateAPIView,
    UserListAPIView,
)
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()

urlpatterns = [
    # graphQL
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    path('users', UserListAPIView.as_view(), name='users'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('products-postgres', ProductListCreateAPIView.as_view(), name='product-list'),
    path('auth/register', RegisterCreateAPIView.as_view(), name='register'),
    path('token', obtain_auth_token, name='token_obtain_pair'),
]
