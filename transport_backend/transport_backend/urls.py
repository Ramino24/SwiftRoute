from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
    openapi.Info(
        title="SwiftRoute API",
        default_version='v1',
        description="API documentation for SwiftRoute Backend System",
        terms_of_service="https://www.SwiftRoute.com/terms/",
        contact=openapi.Contact(email="ezekieleyitayo2020@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# SwiftRoute Admin Dashboard Customization
admin.site.site_header = "SwiftRoute Admin"
admin.site.site_title = "SwiftRoute Admin Portal"
admin.site.index_title = "Welcome to the SwiftRoute Dashboard"

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('core.urls')),
    
     # Swagger & Redoc URLs
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
