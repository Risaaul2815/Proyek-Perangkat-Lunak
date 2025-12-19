from django.contrib import admin
from .models import Menu, Booking, Meja, Order, OrderItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kategori', 'harga')
    list_filter = ('kategori',)
    search_fields = ('nama',)

@admin.register(Meja)
class MejaAdmin(admin.ModelAdmin):
    list_display = ('nomor', 'kapasitas', 'harga_per_orang')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'meja', 'tanggal_reservasi',
        'jam_reservasi', 'jumlah_orang',
        'status'
    )
    list_filter = ('status', 'tanggal_reservasi')
    search_fields = ('user__username',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('menu', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'order_time')
    list_filter = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('customer', 'total_price', 'order_time')

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
