const { parseDuration } = require('../src/duration');

test('1h30m returns 5400 seconds', () => {
  expect(parseDuration('1h30m')).toBe(5400);
});

test('45s returns 45 seconds', () => {
  expect(parseDuration('45s')).toBe(45);
});

test('2h returns 7200 seconds', () => {
  expect(parseDuration('2h')).toBe(7200);
});
