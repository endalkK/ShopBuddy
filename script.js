// Items in the store
const storeItems = [
  { id: 1, name: "Item 1", price: 10 },
  { id: 2, name: "Item 2", price: 20 },
  { id: 3, name: "Item 3", price: 15 },
  { id: 4, name: "Item 4", price: 25 },
];

// Shopping bag
let shoppingBag = [];

// DOM elements
const itemsList = document.getElementById("items-list");
const bagList = document.getElementById("bag-list");
const checkoutBtn = document.getElementById("checkout-btn");

// Populate the store items
function displayStoreItems() {
  storeItems.forEach((item) => {
    const li = document.createElement("li");
    li.innerHTML = `
      ${item.name} - $${item.price}
      <button onclick="addToBag(${item.id})">Add to Bag</button>
    `;
    itemsList.appendChild(li);
  });
}

// Update shopping bag UI
function updateBag() {
  bagList.innerHTML = ""; // Clear the current bag
  shoppingBag.forEach((item) => {
    const li = document.createElement("li");
    li.innerHTML = `
      ${item.name} - $${item.price}
      <button onclick="removeFromBag(${item.id})">Remove</button>
    `;
    bagList.appendChild(li);
  });

  // Enable or disable checkout button
  checkoutBtn.disabled = shoppingBag.length === 0;
}

// Add item to the shopping bag
function addToBag(itemId) {
  const item = storeItems.find((i) => i.id === itemId);
  if (item) {
    shoppingBag.push(item);
    updateBag();
  }
}

// Remove item from the shopping bag
function removeFromBag(itemId) {
  shoppingBag = shoppingBag.filter((item) => item.id !== itemId);
  updateBag();
}

// Proceed to checkout
checkoutBtn.addEventListener("click", () => {
  const total = shoppingBag.reduce((sum, item) => sum + item.price, 0);
  alert(`Checkout successful! Total: $${total}`);
  shoppingBag = []; // Clear the bag after checkout
  updateBag();
});

// Initialize the store
displayStoreItems();
