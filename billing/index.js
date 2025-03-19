const data = {
  shirts: {
    sizes: ["Small (S)", "Medium (M)", "Large (L)"],
    prices: [500, 600, 700],
  },
  pants: {
    sizes: ["28", "30", "32", "34", "36", "38"],
    prices: [1000, 1100, 1200, 1300, 1400, 1500],
  },
};

let selectedCategory = null;
let selectedSizeIndex = null;
let quantity = 0;
let totalPrice = 0;
let bill = [];
let grandTotal = 0;

function updateSizes() {
  selectedCategory = document.getElementById("category").value;
  const sizeDropdown = document.getElementById("size");
  sizeDropdown.innerHTML = `<option value="default">Select Size</option>`;

  if (selectedCategory !== "default") {
    const sizes = data[selectedCategory].sizes;
    sizes.forEach((size, index) => {
      const option = document.createElement("option");
      option.value = index;
      option.textContent = size;
      sizeDropdown.appendChild(option);
    });
  }
  resetSelection();
}

function resetSelection() {
  selectedSizeIndex = null;
  quantity = 0;
  document.getElementById("quantity").textContent = "Quantity: 0";
  document.getElementById("price").textContent = "Price: --";
  updateTotalPrice();
}

function updatePrice() {
  selectedSizeIndex = document.getElementById("size").value;

  if (selectedCategory !== "default" && selectedSizeIndex !== "default") {
    const price = data[selectedCategory].prices[selectedSizeIndex];
    document.getElementById("price").textContent = `Price: ₹${price}`;
  } else {
    document.getElementById("price").textContent = "Price: --";
  }
}

function increaseQuantity() {
  if (
    selectedCategory &&
    selectedSizeIndex !== null &&
    selectedSizeIndex !== "default"
  ) {
    quantity++;
    document.getElementById("quantity").textContent = `Quantity: ${quantity}`;
    updateTotalPrice();
  } else {
    alert("Please select a category and size first.");
  }
}

function decreaseQuantity() {
  if (quantity > 0) {
    quantity--;
    document.getElementById("quantity").textContent = `Quantity: ${quantity}`;
    updateTotalPrice();
  }
}

function updateTotalPrice() {
  if (
    selectedCategory &&
    selectedSizeIndex !== null &&
    selectedSizeIndex !== "default"
  ) {
    const pricePerItem = data[selectedCategory].prices[selectedSizeIndex];
    totalPrice = pricePerItem * quantity;
    document.getElementById(
      "totalPrice"
    ).textContent = `Total Price: ₹${totalPrice}`;
  } else {
    document.getElementById("totalPrice").textContent = "Total Price: ₹0";
  }
}

function addToBill() {
  if (quantity > 0 && selectedCategory && selectedSizeIndex !== "default") {
    const item = {
      category: selectedCategory,
      size: data[selectedCategory].sizes[selectedSizeIndex],
      quantity: quantity,
      subtotal: totalPrice,
    };
    bill.push(item);
    updateBillTable();
    resetSelection();
  } else {
    alert(
      "Please select a category, size, and quantity before adding to the bill."
    );
  }
}

function updateBillTable() {
  const billTableBody = document.getElementById("billTableBody");
  billTableBody.innerHTML = ""; // Clear existing rows
  grandTotal = 0;

  bill.forEach((item) => {
    const row = document.createElement("tr");
    row.innerHTML = `
                    <td>${item.category}</td>
                    <td>${item.size}</td>
                    <td>${item.quantity}</td>
                    <td>₹${item.subtotal}</td>
                `;
    billTableBody.appendChild(row);
    grandTotal += item.subtotal;
  });

  document.getElementById("grandTotal").textContent = `₹${grandTotal}`;
}
