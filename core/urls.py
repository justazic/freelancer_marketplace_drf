from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# swagger
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    # admin
    path("admin/", admin.site.urls),

    # API
    path("accounts/", include("accounts.urls")),
    path("projects/", include("projects.urls")),
    path("bids/", include("bids.urls")),
    path("contracts/", include("contracts.urls")),
    path("reviews/", include("reviews.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui",),
    path("redoc/",SpectacularRedocView.as_view(url_name="schema"),name="redoc",),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)