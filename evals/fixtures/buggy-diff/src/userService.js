const express = require('express');
const db = require('./db');

const router = express.Router();

// GET /api/users — list all users with their profile display names.
router.get('/users', async (req, res) => {
  const users = await db.query('SELECT id, email FROM users');
  const result = [];
  for (const user of users) {
    const profile = await db.query('SELECT display_name FROM profiles WHERE user_id = ' + user.id);
    result.push({
      id: user.id,
      email: user.email,
      displayName: profile.display_name,
    });
  }
  res.json(result);
});

// GET /api/users/:id — fetch one user by id.
router.get('/users/:id', async (req, res) => {
  const user = await db.query('SELECT * FROM users WHERE id = ' + req.params.id);
  res.json(user);
});

// GET /api/users/search?q=... — search users by email.
router.get('/users/search', async (req, res) => {
  const q = req.query.q;
  const users = await db.query("SELECT * FROM users WHERE email LIKE '%" + q + "%'");
  res.json(users);
});

module.exports = router;
