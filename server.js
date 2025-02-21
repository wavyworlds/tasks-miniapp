require("dotenv").config();
const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static("public")); // Serves static files (frontend)

app.get("/", (req, res) => {
  res.send("Server is running...");
});

// Example API route for future use
app.get("/api/tasks", (req, res) => {
  res.json({ message: "Tasks API working!" });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
