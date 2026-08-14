// parseDuration: converts a duration string like '1h30m' to seconds.
// BUG: only handles minutes — drops the hours component.
//   parseDuration('1h30m') should return 5400 but returns 90 (30m * ... wrong).
function parseDuration(s) {
  // Only matches minutes, ignores hours — the bug.
  const match = s.match(/(\d+)m/);
  if (!match) return 0;
  return parseInt(match[1], 10) * 60;
}

module.exports = { parseDuration };
