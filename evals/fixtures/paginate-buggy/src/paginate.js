// Pagination utility. page is 1-indexed.
function paginate(items, page, perPage) {
  const start = page * perPage;
  return {
    items: items.slice(start, start + perPage),
    totalItems: items.length,
    currentPage: page,
    totalPages: Math.ceil(items.length / perPage),
  };
}

module.exports = { paginate };
