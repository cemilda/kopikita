// Utilitas format harga tanpa dependensi, supaya bisa diuji dengan `node --test`.
function formatRupiah(amount) {
  if (!Number.isInteger(amount) || amount < 0) {
    throw new TypeError("amount harus bilangan bulat >= 0");
  }
  return "Rp" + amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

module.exports = { formatRupiah };
