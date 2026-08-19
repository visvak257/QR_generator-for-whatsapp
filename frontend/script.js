async function generateQR() {

    const productId =
        document
        .getElementById("productId")
        .value
        .trim()
        .toUpperCase();


    if (!productId) {

        alert("Please enter Product ID");

        return;
    }


    const response = await fetch(
        `http://localhost:8000/generate-qr/${productId}`
    );


    const data = await response.json();


    if (data.error) {

        alert(data.error);

        return;
    }


    document.getElementById("product").innerHTML = `
        <h2>${data.product.name}</h2>

        <p>
            ${data.product.description}
        </p>

        <p>
            Price: ₹${data.product.price}
        </p>
    `;


    const qrImage =
        document.getElementById("qrImage");


    qrImage.src =
        `http://localhost:8000/view-qr/${productId}`;


    qrImage.style.display = "block";
}