let selectedMenu = null;

function openOrderModal(nama, harga, gambar, id) {
    selectedMenu = {
        name: nama,
        price: harga,
        id: id,
        image: gambar,
        quantity: 1,
    };

    document.getElementById("menuName").innerText = nama;
    document.getElementById("menuPrice").innerText = "Rp " + harga;
    document.getElementById("modalItemImage").src = gambar;
    document.getElementById("menuId").value = id;
    document.getElementById("menuQuantity").value = 1;

    document.getElementById("orderModal").style.display = "block";
}


document.querySelector(".close").onclick = function () {
    document.getElementById("orderModal").style.display = "none";
};

window.onclick = function (event) {
    if (event.target === document.getElementById("orderModal")) {
        document.getElementById("orderModal").style.display = "none";
    }
};


document.getElementById("minusBtn").addEventListener("click", function () {
    let qty = document.getElementById("menuQuantity");
    if (qty.value > 1) qty.value--;
});

document.getElementById("plusBtn").addEventListener("click", function () {
    let qty = document.getElementById("menuQuantity");
    qty.value++;
});


document.getElementById("addToCartBtn").onclick = function () {
    const id = document.getElementById("menuId").value;
    const qty = document.getElementById("menuQuantity").value;

    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/order/add/${id}/`;
    
    const csrf = document.getElementById("csrf-token").cloneNode(true);
    form.appendChild(csrf);

    const quantityField = document.createElement("input");
    quantityField.type = "hidden";
    quantityField.name = "quantity";
    quantityField.value = qty;
    form.appendChild(quantityField);

    document.body.appendChild(form);
    form.submit();
};


document.getElementById("orderNowBtn").onclick = function () {
    const id = document.getElementById("menuId").value;
    const qty = document.getElementById("menuQuantity").value;

    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/order/now/${id}/`;
    
    const csrf = document.querySelector("[name=csrfmiddlewaretoken]").cloneNode(true);
    form.appendChild(csrf);

    const quantityField = document.createElement("input");
    quantityField.type = "hidden";
    quantityField.name = "quantity";
    quantityField.value = qty;
    form.appendChild(quantityField);

    document.body.appendChild(form);
    form.submit();
};

document.getElementById("orderNowBtn").addEventListener("click", function() {
    const menuId = document.getElementById("menuId").value;
    const quantity = document.getElementById("menuQuantity").value;

    window.location.href = `/order/now/${menuId}/?quantity=${quantity}`;
});