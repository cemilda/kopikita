// Server etalase KopiKita: menyajikan halaman statis dan meneruskan API ke backend Flask.
const express = require("express");
const path = require("path");

const app = express();
const API_URL = process.env.API_URL || "http://localhost:5000";

app.use(express.static(path.join(__dirname, "public")));

app.get("/config.js", (_req, res) => {
  res.type("application/javascript").send(`window.KOPIKITA_API = ${JSON.stringify(API_URL)};`);
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Etalase KopiKita di http://localhost:${port}`));
