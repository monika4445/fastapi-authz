// server.js - Simple Express server to serve your HTML on port 3000
const express = require('express');
const path = require('path');
const app = express();

// Serve static files (your HTML, CSS, JS)
app.use(express.static('.'));

// Serve index.html on root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`🚀 Frontend server running on http://localhost:${PORT}`);
    console.log(`📧 Email verification links will work perfectly!`);
});

// To run this:
// 1. npm init -y
// 2. npm install express  
// 3. node server.js