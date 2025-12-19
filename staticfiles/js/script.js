let selectedTableNumber = null;

function selectTable(id) {
    selectedTableNumber = id; // update variabel JS
    document.getElementById("meja").value = id; // update hidden input di form

    document.getElementById("selected-table").innerText = `Meja ${id} telah dipilih.`;

    // Highlight meja terpilih
    document.querySelectorAll(".table-item").forEach(item => item.classList.remove("selected"));
    document.getElementById(`table-${id}`).classList.add("selected");

    // Aktifkan tombol submit
    document.getElementById("btn-submit-reservasi").disabled = false;
}

/* ==========================
   1. CAROUSEL
========================== */
const carousel = document.querySelector(".carousel");
const cards = document.querySelectorAll(".menu-card");

if (carousel && cards.length > 0) {
    let index = 0;
    const total = cards.length;

    function moveCarousel() {
        index = (index + 1) % total;
        carousel.style.transform = `translateX(-${index * 100}%)`;
    }

    setInterval(moveCarousel, 4000);
}

/* ==========================
   3. Fungsi CSRF
========================== */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/* ==========================
   4. FORM RESERVASI
========================== */
const reservationForm = document.getElementById('reservation-form');

if (reservationForm) {
    reservationForm.addEventListener('submit', function (event) {
        if (!selectedTableNumber) {
            alert("Mohon pilih meja terlebih dahulu.");
            event.preventDefault(); // hentikan submit
            return;
        }

        // opsional: validasi waktu atau jumlah orang di sini
        // jika semua valid, biarkan form submit ke Django
    });
}
