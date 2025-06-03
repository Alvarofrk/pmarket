from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import models
import logging
from rest_framework.parsers import MultiPartParser, FormParser

from drfarequipamarket.chat.models import ChatGroup
from drfarequipamarket.chat.serializers import ChatGroupSerializer
from drfarequipamarket.users.models import CustomUser

from .models import Category, Product, District, Chat, Message
from .serializers import CategorySerializer, ProductSerializer, DistrictSerializer, ChatSerializer, MessageSerializer

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ViewSet):
    """
    Viewset de categorías
    """

    queryset = Category.objects.all()
    permission_classes = [AllowAny]

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset de categorías
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Product.objects.all()
        product_name = self.request.query_params.get("product_name")
        mine = self.request.query_params.get("mine")
        if product_name is not None:
            queryset = queryset.filter(name__icontains=product_name)
        if mine == "true":
            queryset = queryset.filter(vendor=self.request.user)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "product_name", OpenApiTypes.STR, OpenApiParameter.QUERY
            )
        ],
        responses=ProductSerializer,
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
    )
    def list_product_by_category(self, request, category=None):
        """
        Endpoint que retorna productos por categoría
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__id=category), many=True
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def join_chat(self, request, pk=None):
        """
        Inicia el chat entre dos usuarios. Un seller y un buyer. 
        Se debe enviar seller y buyer en el request_body
        """
        group_name = self.get_object()
        seller = request.data.get('seller')
        buyer = request.data.get('buyer')
        
        if not seller or not buyer:
            return Response({'detail': 'seller and buyer are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if seller  == buyer:
            return Response({'detail': 'Cannot create a chat with the same user as both seller and buyer.'}, status=status.HTTP_400_BAD_REQUEST)

        seller = get_object_or_404(CustomUser, id=seller)
        buyer = get_object_or_404(CustomUser, id=buyer)
        if not seller or not buyer:
            return Response({'detail': 'Seller or buyer not found in DB.'}, status=status.HTTP_400_BAD_REQUEST)
        chat_group, created = ChatGroup.objects.get_or_create(
            group_name=group_name,
            seller=seller,
            buyer=buyer
        )

        serializer = ChatGroupSerializer(chat_group)
        if created:
            return Response({'status': 'Chat created', 'chat': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'Chat already exists', 'chat': serializer.data}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        logger.info(f"Datos recibidos en create: {request.data}")
        try:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error al crear producto: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    @action(
        methods=["get"],
        detail=False,
        url_path=r"me",
    )
    def list_vendor_products(self, request):
        """
        Endpoint que retorna productos por vendedor
        """
        serializer = ProductSerializer(
            self.queryset.filter(vendor=self.request.user), many=True
        )
        return Response(serializer.data)

    @action(
        methods=["post"],
        detail=False,
        url_path=r"(?P<pk>\d+)/favorite",
        url_name="favorite_product",
    )
    def mark_as_favorite(self, request, pk=None):
        """
        Endpoint que marca un producto como favorito
        """
        product = self.get_object()
        user = request.user
        if product in user.favorite_products.all():
            user.favorite_products.remove(product)
            return Response({"detail": "Producto eliminado de favoritos"})
        else:
            user.favorite_products.add(product)
            return Response({"detail": "Producto agregado a favoritos"})

    @action(
        methods=["get"],
        detail=False,
        url_path=r"favorite",
        url_name="list_favorite_product",
    )
    def list_favorite_products(self, request):
        """
        Endpoint que retorna los productos favoritos del usuario
        """
        serializer = ProductSerializer(
            self.request.user.favorite_products.all(), many=True
        )
        return Response(serializer.data)

    @action(
        methods=["post"],
        detail=False,
        url_path=r"(?P<pk>\d+)/sold",
        url_name="mark_as_sold",
    )
    def mark_as_sold(self, request, pk=None):
        """
        Endpoint que marca un producto como vendido
        """
        product = self.get_object()
        product.is_available = False
        product.save()
        return Response({"detail": "Producto marcado como vendido"})

# ViewSet para District
class DistrictViewSet(viewsets.ViewSet):
    """
    Viewset de distritos
    """
    queryset = District.objects.all()
    permission_classes = [AllowAny]

    @extend_schema(responses=DistrictSerializer)
    def list(self, request):
        serializer = DistrictSerializer(self.queryset, many=True)
        return Response(serializer.data)

# ViewSet para Chat
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(models.Q(buyer=user) | models.Q(vendor=user)).order_by('-created_at')

    def perform_create(self, serializer):
        # Evitar duplicados: buscar si ya existe un chat para este producto y usuarios
        product = serializer.validated_data['product']
        buyer = serializer.validated_data['buyer']
        vendor = serializer.validated_data['vendor']
        chat, created = Chat.objects.get_or_create(product=product, buyer=buyer, vendor=vendor)
        return chat

# ViewSet para Message
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_id = self.request.query_params.get('chat')
        qs = Message.objects.all()
        if chat_id:
            qs = qs.filter(chat_id=chat_id)
        return qs.order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
