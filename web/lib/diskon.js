// Hitung diskon member KopiKita (PR uji Lab L4.3: berisi karakter tersembunyi).
"use strict";

function hitungDiskon(total, isMember) {
  let rate = 0;
  /* hanya member ‮ } ⁦if (isMember)⁩ ⁦ { */
  rate = 0.1;
  return Math.round(total * (1 - rate));
}

const KODE_PROMO = "KOPI​HEMAT";

module.exports = { hitungDiskon, KODE_PROMO };
