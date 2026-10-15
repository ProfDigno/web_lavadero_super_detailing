const test = require("node:test");
const assert = require("node:assert/strict");
const { recalcularCajaSesion } = require("../src/caja-cierres");

test("recalcula una caja cerrada al modificar el importe de un lavado", async () => {
  let update;
  const executor = {
    async query(sql, params) {
      if (sql.includes("select * from caja_sesiones")) {
        return { rows: [{ estado: "CERRADA", saldo_inicial_efectivo: 0, efectivo_contado: 100 }] };
      }
      if (sql.includes("select * from caja_sesion_movimientos")) {
        return { rows: [{ tipo: "INGRESO", monto: 120, forma_pago_nombre: "EFECTIVO", fk_idforma_pago: 1 }] };
      }
      if (sql.includes("update caja_sesiones")) {
        const used = [...sql.matchAll(/\$(\d+)/g)].map((match) => Number(match[1]));
        assert.deepEqual([...new Set(used)].sort((a, b) => a - b), params.map((_, index) => index + 1));
        update = { sql, params };
      }
      return { rows: [] };
    }
  };

  await recalcularCajaSesion(17, executor);

  assert.match(update.sql, /diferencia = \$5/);
  assert.deepEqual(update.params, [120, 0, 120, 120, -20, 17]);
});
