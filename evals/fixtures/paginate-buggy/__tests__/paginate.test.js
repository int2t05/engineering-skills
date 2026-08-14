const { paginate } = require('../src/paginate');

// Existing tests — these pass. They cover metadata only, not the slice logic,
// so the page-slice bug is hidden until a reproduction test is written.

test('reports total items and pages', () => {
  const result = paginate([1, 2, 3, 4, 5], 1, 2);
  expect(result.totalItems).toBe(5);
  expect(result.totalPages).toBe(3);
});

test('currentPage is echoed back', () => {
  expect(paginate([1, 2, 3, 4, 5], 3, 2).currentPage).toBe(3);
});
