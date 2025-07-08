// server.js
const express = require('express');
const path = require('path');
const fetch = (...args) =>
  import('node-fetch').then(({default: fetch}) => fetch(...args));

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname)));

app.post('/price', async (req, res) => {
  try {
    const resp = await fetch('http://127.0.0.1:8000/price', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body),
    });
    const data = await resp.json();
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.listen(3000, () => console.log('Frontend running at http://localhost:3000'));
