from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static, serve
from allauth.account.views import EmailVerificationSentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('products/', include('products.urls')),
    path('notifications/', include('notifications.urls')),

    # Email Verification URL
    path(
        "accounts/confirm-email/",
        EmailVerificationSentView.as_view(
            template_name="account/verification_sent.html"
        ),
        name="account_email_verification_sent",
    ),
    path('subscriptions/', include('subscriptions.urls')),
    path(
        'sitemap.xml', serve, {'document_root': settings.BASE_DIR, 'path': 'sitemap.xml'},
        name='sitemap'
    )

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 Page
handler404 = 'home.views.custom_404'

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
