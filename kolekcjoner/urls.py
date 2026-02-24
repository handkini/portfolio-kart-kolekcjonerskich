from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portfolio import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('portfolio/', views.portfolio_view, name='portfolio_view'),
    path('portfolio/add/', views.card_add, name='card_add'),
    path('portfolio/<int:pk>/edit/', views.card_edit, name='card_edit'),
    path('portfolio/<int:pk>/delete/', views.card_delete, name='card_delete'),
    path('u/<str:username>/', views.user_portfolio, name='user_portfolio'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

