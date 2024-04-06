from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User as AuthUser
from DRC.core.exceptions import ErrorResponse
from PRODUCT.models import Product
from SELLER.models import Seller
from SELLER.serializers import SellerSerializer
from rest_framework.permissions import IsAuthenticated
from DRC.core.permissions import SellerOnly, VerifiedSeller
from PRODUCT.serializers import ProductListSerializer, SingleProductSerializer


@api_view(['POST'])
def seller_signup(request):
    if request.method == "POST":
        first_name = request.data.get('first_name').strip() if request.data.get('first_name') else None
        last_name = request.data.get('last_name').strip() if request.data.get('last_name') else None
        email = request.data.get('email').strip() if request.data.get('email') else None
        phone_no = request.data.get('phone_no').strip() if request.data.get('phone_no') else None
        alt_phone_no = request.data.get('alt_phone_no').strip() if request.data.get('alt_phone_no') else None
        gstin = request.data.get('gstin').strip() if request.data.get('gstin') else None
        password = request.data.get('password')
        try:
            user = AuthUser.objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password(password)
            user.save()

            seller_profile = Seller.objects.create(
                user_id=user.id,
                ph_no=phone_no,
                alt_ph_no=alt_phone_no,
                gstin=gstin,
            )
            seller_profile.save()
            return Response(SellerSerializer(seller_profile, many=False).data)
        except Exception as ex:
            return ErrorResponse(code=500, msg=ex.__str__(), details=ex.__str__()).response


@api_view(['GET'])
@permission_classes([IsAuthenticated, SellerOnly, VerifiedSeller])
def seller(request):
    if request.method == 'GET':
        return Response(SellerSerializer(request.user.seller, many=False).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, SellerOnly, VerifiedSeller])
def get_all_product_for_seller(request):
    if request.method == 'GET':
        product_qs = Product.objects.filter(seller__user=request.user)
        return Response(ProductListSerializer(product_qs, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, SellerOnly, VerifiedSeller])
def get_a_product_by_id_for_seller(request, product_id):
    if request.method == 'GET':
        product: Product = Product.objects.get(seller__user=request.user, product_id=str(product_id).strip())
        return Response(SingleProductSerializer(product).data)

