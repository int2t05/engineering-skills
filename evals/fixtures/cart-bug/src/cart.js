// Cart module — discount preview and total calculation.

function applyDiscount(items, percent) {
  return items.map(item => {
    item.price = item.price * (1 - percent / 100);
    return item;
  });
}

function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

module.exports = { applyDiscount, calculateTotal };
