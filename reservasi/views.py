import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Booking, Meja, Menu, Order, OrderItem
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

def landing_page(request):
    return render(request, "landing_page.html")


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")  

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "Username atau password salah.")

    return render(request, "login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Password tidak cocok!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan!")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Akun berhasil dibuat, silakan login.")
        return redirect("login")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("landing_page")


def menu(request):
    menu_makanan = Menu.objects.filter(kategori='makanan')
    menu_minuman = Menu.objects.filter(kategori='minuman')

    return render(request, 'menu.html', {
        'menu_makanan': menu_makanan,
        'menu_minuman': menu_minuman,
    })


def tentang(request):
    return render(request, 'tentang.html')


@login_required
def profil(request):
    reservasi_user = Booking.objects.filter(user=request.user).order_by('-waktu_dibuat')
    orders_user = Order.objects.filter(customer=request.user).order_by('-order_time')

    return render(request, 'profil.html', {
        'reservasi_user': reservasi_user,
        'orders_user': orders_user,
    })

def reservasi(request):
    meja_list = Meja.objects.all()
    return render(request, 'reservasi.html', {"meja_list": meja_list})


from datetime import datetime

@login_required
def create_reservasi(request):
    if request.method == "POST":
        tanggal = request.POST.get('tanggal')
        jam = request.POST.get('waktu_mulai')
        jumlah_orang = int(request.POST.get('jumlah_orang'))
        meja_id = request.POST.get('meja')

        tanggal_reservasi = datetime.strptime(tanggal, "%Y-%m-%d").date()
        jam_reservasi = datetime.strptime(jam, "%H:%M").time()
        sekarang = timezone.localtime()

        if tanggal_reservasi < sekarang.date():
            messages.error(request, "Tanggal reservasi tidak boleh sebelum hari ini.")
            return redirect("reservasi")

        if tanggal_reservasi == sekarang.date() and jam_reservasi <= sekarang.time():
            messages.error(request, "Jam reservasi sudah lewat.")
            return redirect("reservasi")

        if not meja_id:
            messages.error(request, "Silakan pilih meja terlebih dahulu.")
            return redirect('reservasi')

        try:
            meja = Meja.objects.get(id=meja_id)
        except Meja.DoesNotExist:
            messages.error(request, "Meja tidak ditemukan.")
            return redirect('reservasi')

        if jumlah_orang > meja.kapasitas:
            messages.error(
                request,
                f"Kapasitas meja hanya {meja.kapasitas} orang."
            )
            return redirect('detail_reservasi')

        booking = Booking.objects.create(
            user=request.user,
            meja=meja,
            tanggal_reservasi=tanggal_reservasi,
            jam_reservasi=jam_reservasi,
            jumlah_orang=jumlah_orang
        )

        booking.hitung_total()
        booking.hitung_dp()

    return redirect('riwayat_reservasi')


def detail_reservasi(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    order = Order.objects.filter(
        customer=request.user,
        booking=booking
    ).first()

    context = {
        'booking': booking,  
        'order': order
    }

    return render(request, 'detail_reservasi.html', context)



def upload_bukti(request, id):
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        file = request.FILES.get("bukti")

        if file:
            booking.bukti_pembayaran = file
            booking.sudah_bayar_dp = True
            booking.status = "Menunggu konfirmasi"
            booking.save()

            messages.success(request, "Bukti pembayaran berhasil diupload!")
            return redirect("detail_reservasi", booking_id=booking.id)

        messages.error(request, "Harap upload bukti pembayaran.")
    
    return redirect("detail_reservasi", booking_id=id)


def admin_dashboard(request):
    today = timezone.now().date()

    total_menu = Menu.objects.count()
    total_orders_today = Order.objects.filter(order_time__date=today).count()
    total_reservasi = Booking.objects.count()

    recent_menu = Menu.objects.all().order_by('-created_at')[:5]

    recent_orders = Order.objects.select_related('customer').all().order_by('-order_time')[:5]

    recent_reservasi = Booking.objects.select_related('user', 'meja').all().order_by('-waktu_dibuat')[:5]

    context = {
        'total_menu': total_menu,
        'total_orders_today': total_orders_today,
        'total_reservasi': total_reservasi,
        'recent_menu': recent_menu,
        'recent_orders': recent_orders,
        'recent_reservasi': recent_reservasi,
    }

    return render(request, 'admin/admin_dashboard.html', context)


def admin_menu(request):
    menu = Menu.objects.all()
    return render(request, "admin/admin_menu.html", {"menu": menu})


def admin_add_menu(request):
    if request.method == "POST":
        nama = request.POST["name"]
        kategori = request.POST["category"]
        harga = request.POST["price"]
        deskripsi = request.POST.get("deskripsi")
        gambar = request.FILES.get("image")

        Menu.objects.create(
            nama=nama,
            kategori=kategori,
            harga=harga,
            deskripsi=deskripsi,
            gambar=gambar,
        )
        return redirect("admin_menu")

    return render(request, "admin/admin_add_menu.html")


def admin_edit_menu(request, id):
    menu = get_object_or_404(Menu, id=id)

    if request.method == "POST":
        menu.nama = request.POST["name"]
        menu.kategori = request.POST["category"]
        menu.harga = request.POST["price"]
        menu.deskripsi = request.POST.get("deskripsi")

        if "image" in request.FILES:
            menu.gambar = request.FILES["image"]

        menu.save()
        return redirect("admin_menu")

    return render(request, "admin/admin_edit_menu.html", {"menu": menu})


def admin_delete_menu(request, id):
    menu = get_object_or_404(Menu, id=id)
    menu.delete()
    return redirect("admin_menu")


def admin_orders(request):
    orders = Order.objects.all().order_by('-order_time')
    return render(request, "admin/admin_orders.html", {"orders": orders})


def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    new_status = request.GET.get("status")

    if new_status in ["pending", "process", "done"]:
        order.status = new_status
        order.save()

    return redirect("admin_orders")


def admin_reservasi(request):
    reservations = Booking.objects.all().order_by("-waktu_dibuat")
    return render(request, "admin/admin_reservasi.html", {"reservations": reservations})


def delete_reservasi(request, id):
    res = get_object_or_404(Booking, id=id)
    res.delete()
    return redirect("admin_reservasi")


@staff_member_required
def update_reservasi_status(request, id):
    reservasi = get_object_or_404(Booking, id=id)
    status = request.GET.get('status')

    if status in ['pending', 'confirmed', 'completed', 'cancelled']:
        reservasi.status = status
        reservasi.save()

    return redirect('admin_reservasi')


def add_to_order(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    quantity = int(request.POST.get("quantity", 1))

    order_id = request.session.get("order_id")

    if order_id:
        order = Order.objects.filter(id=order_id, status="pending").first()
    else:
        order = None

    if not order:
        order = Order.objects.create(customer=request.user)  
        request.session["order_id"] = order.id

    booking_id = request.session.get("booking_id")

    booking = None
    if booking_id:
        booking = Booking.objects.filter(
            id=booking_id,
            user=request.user,
            status="confirmed"
        ).first()

    for item in order:
        OrderItem.objects.create(
            order=order,
            menu=item.menu,
            quantity=item.quantity
        )

    order.hitung_total()

    item, created = OrderItem.objects.get_or_create(
        order=order,
        menu=menu,
        defaults={"quantity": quantity}
    )

    if not created:
        item.quantity += quantity
        item.save()

    order.hitung_total()

    return redirect("menu")


def checkout(request):
    order_id = request.session.get("order_id")
    if not order_id:
        messages.error(request, "Keranjang masih kosong.")
        return redirect("cart")

    order = Order.objects.get(id=order_id)
    order.status = "process"
    order.save()

    request.session["order_id"] = None

    messages.success(request, "Pesanan berhasil diproses!")
    return redirect("order_detail", order_id=order.id)


def create_order(request):
    if request.method == "POST":
        data = json.loads(request.body)

        menu_name = data["name"]
        quantity = int(data["quantity"])

        try:
            menu = Menu.objects.get(nama=menu_name)
        except Menu.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Menu tidak ditemukan"})

        order = Order.objects.create(customer=request.user)

        OrderItem.objects.create(
            order=order,
            menu=menu,
            quantity=quantity
        )

        order.hitung_total()

        return JsonResponse({"status": "success", "order_id": order.id})

    return JsonResponse({"status": "error", "message": "Metode tidak didukung"})


def cart_page(request):
    order_id = request.session.get("order_id")

    if not order_id:
        return render(request, "cart.html", {"order": None})

    order = Order.objects.filter(id=order_id, status="pending").first()

    return render(request, "cart.html", {"order": order})


def order_now(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    quantity = int(request.GET.get("quantity", 1)) 

    order = Order.objects.create(customer=request.user)

    OrderItem.objects.create(
        order=order,
        menu=menu,
        quantity=quantity
    )

    order.hitung_total()
    order.status = "process"
    order.save()

    messages.success(request, f"Pesanan {menu.nama} berhasil dibuat!")

    return redirect("order_detail", order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})


@login_required
def riwayat_reservasi(request):
    user = request.user
    reservations = Booking.objects.filter(user=user).order_by('-waktu_dibuat')

    return render(request, 'riwayat_reservasi.html', {'reservations': reservations})


def remove_item(request, item_id):
    order_id = request.session.get("order_id")

    if not order_id:
        messages.error(request, "Keranjang tidak ditemukan.")
        return redirect("cart")

    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order_id=order_id
    )

    order = item.order
    item.delete()

    order.hitung_total()

    if order.items.count() == 0:
        order.delete()
        request.session["order_id"] = None
        messages.info(request, "Keranjang kosong.")
    else:
        messages.success(request, "Item berhasil dihapus dari keranjang.")

    return redirect("cart")


def update_item_quantity(request, item_id, action):
    order_id = request.session.get("order_id")

    if not order_id:
        return redirect("cart")

    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order_id=order_id
    )

    if action == "plus":
        item.quantity += 1
        item.save()

    elif action == "minus":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    item.order.hitung_total()

    messages.success(request, "Jumlah item diperbarui.")
    return redirect("cart")
