from django.urls import path
from .views import EmployeeViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('employees/', EmployeeViewset.as_view(), name='employee-list'),
    # path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('token/', TokenObtainPairView.as_view(), name='login'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]

