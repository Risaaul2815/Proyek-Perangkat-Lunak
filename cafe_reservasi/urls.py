"""
URL configuration for cafe_reservasi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from reservasi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('add_to_order/<int:menu_id>/', views.add_to_order, name='add_to_order'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/add/<int:menu_id>/', views.add_to_order, name='add_to_order'),
    path('order/now/<int:menu_id>/', views.order_now, name='order_now'),
    path('cart/', views.cart_page, name='cart'),
    path('profil/', views.profil, name='profil'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('tentang/', views.tentang, name='tentang'),
    path('reservasi/', views.reservasi, name='reservasi'),
    path('reservasi/riwayat/', views.riwayat_reservasi, name='riwayat_reservasi'),
    path('reservasi/create/', views.create_reservasi, name='create_reservasi'),
    path('detail/<int:booking_id>/', views.detail_reservasi, name='detail_reservasi'),
    path('reservasi/upload_bukti/<int:id>/', views.upload_bukti, name='upload_bukti'),
    path('admin-cafe/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-cafe/menu/', views.admin_menu, name='admin_menu'),
    path('admin-cafe/menu/tambah/', views.admin_add_menu, name='admin_add_menu'),
    path('admin-cafe/menu/edit/<int:id>/', views.admin_edit_menu, name='admin_edit_menu'),
    path('admin-cafe/menu/hapus/<int:id>/', views.admin_delete_menu, name='admin_delete_menu'),
    path('admin-cafe/pesanan/', views.admin_orders, name='admin_orders'),
    path('admin-cafe/pesanan/update/<int:id>/', views.update_order_status, name='update_order_status'),
    path('admin-cafe/reservasi/', views.admin_reservasi, name='admin_reservasi'),
    path('admin-cafe/reservasi/hapus/<int:id>/', views.delete_reservasi, name='delete_reservasi'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('update-item/<int:item_id>/<str:action>/', views.update_item_quantity, name='update_item_quantity'),
    path('reservasi/status/<int:id>/', views.update_reservasi_status, name='update_reservasi_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
