from django.contrib import admin
from django.urls import path, include, re_path
from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drfarequipamarket.product import views
from drfarequipamarket.chat.views import ChatGroupViewSet, ChatNotificationViewSet

# Changed imports
from django.urls import re_path as url

from django.views.generic import RedirectView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'districts', views.DistrictViewSet)
router.register(r'chats', ChatGroupViewSet, basename='chat')
router.register(r'notifications', ChatNotificationViewSet, basename='notification')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")
    ),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")
    ),
    re_path(r"^account/", include("allauth.urls")),
    re_path(
        r"^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    path("", RedirectView.as_view(url="/api/schema/docs/", permanent=False)),
    path('api/auth/', include('drfarequipamarket.users.urls')),
]

# Agregar configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
