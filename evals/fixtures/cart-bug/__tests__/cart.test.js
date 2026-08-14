const { applyDiscount, calculateTotal } = require('../src/cart');

test('discounted preview has reduced prices', () => {
  const cart = [
    { name: 'Book', price: 20 },
    { name: 'Pen', price: 5 },
  ];
  const preview = applyDiscount(cart, 10);
  expect(preview[0].price).toBe(18);
  expect(preview[1].price).toBe(4.5);
});

test('original cart is unchanged after a discount preview', () => {
  const cart = [
    { name: 'Book', price: 20 },
    { name: 'Pen', price: 5 },
  ];
  applyDiscount(cart, 10);
  // A discount is a PREVIEW — the original cart must stay at full price
  // so a customer who declines the discount is charged correctly.
  expect(cart[0].price).toBe(20);
  expect(cart[1].price).toBe(5);
});

test('total of original cart after a declined discount', () => {
  const cart = [
    { name: 'Book', price: 20 },
    { name: 'Pen', price: 5 },
  ];
  applyDiscount(cart, 10);   // customer previews, then declines
  const total = calculateTotal(cart);
  expect(total).toBe(25);
});
