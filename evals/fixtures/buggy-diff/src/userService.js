const db = require('./db');

// GET /api/users — returns all users with their profile names.
// BUG: N+1 query — fetches users in a loop, querying profiles one-by-one
// instead of a single batched query.
async function listUsers(req, res) {
  const users = await db.query('SELECT id, email FROM users');
  const result = [];
  for (const user of users) {
    // N+1: one query per user inside the loop
    const profile = await db.query('SELECT display_name FROM profiles WHERE user_id = $1', [user.id]);
    result.push({
      id: user.id,
      email: user.email,
      displayName: profile.display_name,
    });
  }
  // BUG: no handling for empty users — result is [] but no 404 / message
  res.json(result);
}

module.exports = { listUsers };
