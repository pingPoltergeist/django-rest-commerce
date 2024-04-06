from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.seller),
    path('signup/', api_views.seller_signup),
    path('products/', api_views.get_all_product_for_seller),
    path('products/<str:product_id>/', api_views.get_a_product_by_id_for_seller),
]
