const test = require("node:test");
const assert = require("node:assert");
const { formatRupiah } = require("../lib/format");

test("format ribuan dengan titik", () => {
  assert.strictEqual(formatRupiah(46000), "Rp46.000");
  assert.strictEqual(formatRupiah(1250000), "Rp1.250.000");
});

test("menolak nilai negatif", () => {
  assert.throws(() => formatRupiah(-1), TypeError);
});
