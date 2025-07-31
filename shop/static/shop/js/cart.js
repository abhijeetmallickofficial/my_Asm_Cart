document.addEventListener("DOMContentLoaded", function () {
    console.log("🟢 JS Loaded from cart.js");
    //Function for Stop carosel scrolling
    var carousels = document.querySelectorAll('.carousel');
        carousels.forEach(function (carousel) {
            var bsCarousel = bootstrap.Carousel.getInstance(carousel);
            if (bsCarousel) {
                bsCarousel.pause();  // Pause auto-slide if already started
            }
        });
    //loads cart fro the local storage
    let cart = localStorage.getItem("cart") ? JSON.parse(localStorage.getItem("cart")) : {};
    updateCartCount();
    //Prevent Event Bubbling on Buttons
    document.querySelectorAll(".cart, .add, .remove, .quickview").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    });
    //Add Product to Cart
    document.querySelectorAll(".cart").forEach(btn => {
        btn.addEventListener("click", function () {
            let prodId = this.id.slice(2);
            let name = this.dataset.name || "Product " + prodId;
            let price = parseFloat(this.dataset.price) || 0;
            cart[prodId] = {
                qty: (cart[prodId]?.qty || 0) + 1,
                name: name,
                price: price
            };
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCartCount();
            alert(`${name} added to cart!`);
        });
    });
    //Increase Quantity
    document.querySelectorAll(".add").forEach(btn => {
        btn.addEventListener("click", function () {
            let prodId = this.dataset.id;
            let name = this.dataset.name || "Product " + prodId;
            let price = parseFloat(this.dataset.price) || 0;
            cart[prodId] = {
                qty: (cart[prodId]?.qty || 0) + 1,
                name: name,
                price: price
            };
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCartCount();
        });
    });
    //Decrease Quantity
    document.querySelectorAll(".remove").forEach(btn => {
        btn.addEventListener("click", function () {
            let prodId = this.dataset.id;
            let name = this.dataset.name || "Product " + prodId;
            if (cart[prodId]) {
                cart[prodId].qty--;
                if (cart[prodId].qty <= 0) {
                    delete cart[prodId];
                }
                localStorage.setItem("cart", JSON.stringify(cart));
                updateCartCount();
            }
        });
    });
    //Clear Entire Cart
    document.getElementById("clear-cart")?.addEventListener("click", () => {
        if (confirm("Clear cart?")) {
            cart = {};
            localStorage.removeItem("cart");
            updateCartCount();
        }
    });
    //Cart Count & UI Updates
    function updateCartCount() {
        let count = 0;
        //Loops through cart items to calculate total count and update quantity indicators.
        document.querySelectorAll("[id^='qtyControls']").forEach(el => {
            const prodId = el.id.replace("qtyControls", "");
            const quantity = cart[prodId]?.qty || 0;
            count += quantity;

            const qtyElem = document.getElementById("qty" + prodId);
            const qtyWrap = document.getElementById("qtyControls" + prodId);
            const addBtn = document.getElementById("pr" + prodId);

            if (qtyElem) qtyElem.innerText = quantity;
            if (qtyWrap) qtyWrap.style.display = quantity > 0 ? "flex" : "none";
            if (addBtn) addBtn.style.display = quantity > 0 ? "none" : "inline-block";
        });
        //Updates the number displayed in the cart badge.
        document.getElementById("cart-count").innerText = count;
        const navCart = document.getElementById("cart");
        if (navCart) navCart.innerText = count;

        updatePopover();
    }
    //Popover Content (Cart Preview)
    function generateCartContent() {
        //Checks if the cart object is empty.
        if (Object.keys(cart).length === 0) {
            return '<strong>🛒 Cart is empty!</strong>';
        }
        //Initializes a string variable content that starts building the HTML.
        let content = `
        <div>
            <h5 class="mb-2">🛒 My Cart Items</h5>
            <ul class="list-unstyled mb-0">
    `;
        ///index is used to number the items (1, 2, 3).
        let index = 1;
        let total = 0;

        for (let pid in cart) {  //Iterates over each product ID (pid) in the cart object.
            let item = cart[pid];
            let price = parseFloat(item.price) || 0;
            let itemTotal = item.qty * price;
            total += itemTotal;
            content += `<li><h6>${index}. ${item.name} → ${item.qty} pcs × ₹${price} = ₹${itemTotal}</h6></li>`;
            index++;
        }

        content += `
            </ul>
        </div>
    `;
        return content; //Returns the final HTML content as a string, ready to be inserted into a popover or modal.
    }

    //Popover Setup
    const popcart = document.getElementById("popcart");
    let popover;
    if (popcart) {
        popover = new bootstrap.Popover(popcart, {
            html: true,
            trigger: 'focus',
            placement: 'bottom',
            content: generateCartContent()
        });
        //When the user clicks the cart icon, it refreshes and displays the latest cart content.
        popcart.addEventListener('click', () => {
            popcart.setAttribute('data-bs-content', generateCartContent());
            popover.show();
        });
    }
    //Update Popover Dynamically
    //Dynamically refreshes the popover content if quantities change without reopening it.
    function updatePopover() {
        const popcart = document.getElementById("popcart");

        if (popcart && bootstrap?.Popover?.getInstance(popcart)) {
            const instance = bootstrap.Popover.getInstance(popcart);
            const newContent = generateCartContent();
            popcart.setAttribute('data-bs-content', newContent);
            instance.setContent({'.popover-body': newContent});
        }
    }

    //search

});
