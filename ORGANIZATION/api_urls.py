from django.urls import path
from ORGANIZATION import api_views

urlpatterns = [
    path('', api_views.organization),
    path('products/', api_views.get_all_product_for_organization),
    path('products/<str:product_id>/', api_views.get_a_product_by_id_for_organization),
]
