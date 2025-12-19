from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Menu(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.CharField(max_length=50, choices=[
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
    ])
    gambar = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama

class Meja(models.Model):
    nomor = models.IntegerField(unique=True)
    kapasitas = models.IntegerField()
    harga_per_orang = models.DecimalField(max_digits=10, decimal_places=2)
    gambar = models.ImageField(upload_to='meja_images/', blank=True, null=True) 

    def __str__(self):
        return f"Meja {self.nomor} - {self.kapasitas} orang"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu DP'),
        ('confirmed', 'Sudah DP'),
        ('cancelled', 'Dibatalkan'),
        ('completed', 'Selesai')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    meja = models.ForeignKey(Meja, on_delete=models.CASCADE, null=True)
    tanggal_reservasi = models.DateField()
    jam_reservasi = models.TimeField()
    jumlah_orang = models.IntegerField()
    harga_tempat_per_orang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dp_nominal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sudah_bayar_dp = models.BooleanField(default=False)
    bukti_pembayaran = models.ImageField(upload_to='bukti_dp/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    waktu_dibuat = models.DateTimeField(auto_now_add=True)

    def hitung_total(self):
        self.harga_tempat_per_orang = self.meja.harga_per_orang
        self.total_harga = self.jumlah_orang * self.harga_tempat_per_orang
        self.save()

    def hitung_dp(self, persentase=30):
        self.dp_nominal = (self.total_harga * persentase) / 100
        self.save()

    def batal_otomatis(self):
        batas_waktu = self.waktu_dibuat + timedelta(hours=2)
        if self.status == 'pending' and timezone.now() > batas_waktu:
            self.status = 'cancelled'
            self.save()

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest'} (Meja {self.meja.nomor})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Menunggu Konfirmasi'),
        ('process', 'Sedang Diproses'),
        ('done', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_time = models.DateTimeField(auto_now_add=True)

    def hitung_total(self):
        total_menu = sum(item.subtotal for item in self.items.all())
        self.total_price = total_menu

        if self.booking:
            self.final_price = max(total_menu - self.booking.dp_nominal, 0)
        else:
            self.final_price = total_menu

        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username if self.customer else 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.menu.harga * self.quantity
        super().save(*args, **kwargs)

        self.order.hitung_total()

    def __str__(self):
        return f"{self.menu.nama} x {self.quantity}"

