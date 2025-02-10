"""brickheroes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static, serve
from allauth.account.views import EmailVerificationSentView
from django.conf.urls import handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('notifications/', include('notifications.urls')),
    path(
        "accounts/confirm-email/",
        EmailVerificationSentView.as_view(template_name="account/verification_sent.html"),
        name="account_email_verification_sent",
    ),
    path('subscriptions/', include('subscriptions.urls')),
    path('sitemap.xml', serve, {'document_root': settings.BASE_DIR, 'path': 'sitemap.xml'}, name='sitemap'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'home.views.custom_404'


# Serve media files during development
if settings.DEBUG:  # Only serve media in development
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
