from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, products_by_category, register_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/<int:pk>/products/', products_by_category),
    path('users/register/', register_user),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
