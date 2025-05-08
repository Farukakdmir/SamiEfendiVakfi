const { Pool } = require("pg");

const pool = new Pool({
  user: "postgres",
  host: "localhost",
  database: "vakif_db",
  password: "159753f!!",
  port: 5432,
});

module.exports = {
  query: (text, params) => pool.query(text, params),
};
