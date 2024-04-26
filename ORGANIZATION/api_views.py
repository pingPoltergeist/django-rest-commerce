from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User as AuthUser
from DRC.core.exceptions import ErrorResponse
from PRODUCT.models import Product
from SELLER.models import Seller
from SELLER.serializers import SellerSerializer
from rest_framework.permissions import IsAuthenticated
from DRC.core.permissions import SellerOnly, VerifiedSeller
from .order_permissions import OrderViewPermission
from .permissions import StaffOfTheOrganization
from PRODUCT.serializers import ProductListSerializer, SingleProductSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, SellerOnly, VerifiedSeller])
def organization(request, org_id: str):
    if request.method == 'GET':
        return Response(SellerSerializer(request.user.seller, many=False).data)


@api_view(['GET'])
@permission_classes([StaffOfTheOrganization, OrderViewPermission])
def get_all_product_for_organization(request, org_id: str):
    product_qs = Product.objects.filter(seller__id=org_id)
    return Response(ProductListSerializer(product_qs, many=True).data)


@api_view(['GET'])
@permission_classes([StaffOfTheOrganization, OrderViewPermission])
def get_a_product_by_id_for_organization(request, org_id: str, product_id):
    if request.method == 'GET':
        product: Product = Product.objects.get(seller__id=org_id, product_id=str(product_id).strip())
        return Response(SingleProductSerializer(product).data)
