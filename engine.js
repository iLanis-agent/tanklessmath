var TanklessMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  function comma(x) { return String(x).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  var SETPOINT = 120;
  var RATED_RISE = 35;
  function gpmPlan(sticker, inletF) {
    if (!pos(sticker)) return { error: "the sticker GPM must be above zero" };
    if (!num(inletF)) return { error: "the inlet temperature must be a number" };
    if (inletF >= SETPOINT) return { error: "the inlet is already at the 120 F setpoint" };
    var rise = SETPOINT - inletF;
    return { real: r1(sticker * RATED_RISE / rise), rise: rise };
  }
  function renderGpm(r, sticker, inletF) {
    return "The " + jsnum(sticker) + " GPM sticker assumed a 35 F rise; your " + jsnum(inletF)
      + " F inlet water is " + jsnum(r.rise) + " F short of the 120 F setpoint, so the heater honestly gives " + jsnum(r.real) + " GPM.";
  }
  function morningPlan(gpm, showers) {
    if (!pos(gpm)) return { error: "the honest GPM must be above zero" };
    if (!num(showers)) return { error: "the shower count must be a number" };
    if (showers < 1) return { error: "the shower count must be at least one" };
    var demand = showers * 2;
    var margin = gpm - demand;
    var verdict = margin >= 1 ? "with a sink to spare" : margin >= 0 ? "honest, but nothing else runs" : "someone gets the cold surprise";
    return { demand: r1(demand), margin: r2(margin), verdict: verdict };
  }
  function renderMorning(r, gpm, showers) {
    return jsnum(showers) + (showers === 1 ? " shower asks " : " showers ask ") + jsnum(r.demand) + " GPM; your honest " + jsnum(gpm)
      + " GPM leaves a margin of " + jsnum(r.margin) + " - " + r.verdict + ".";
  }
  function gasPlan(gpm, rise) {
    if (!pos(gpm)) return { error: "the flow must be above zero" };
    if (!pos(rise)) return { error: "the rise must be above zero" };
    return { btu: Math.round(gpm * 60 * 8.34 * rise) };
  }
  function renderGas(r, gpm, rise) {
    return "Heating " + jsnum(gpm) + " GPM across a rise of " + jsnum(rise) + " F asks " + comma(r.btu)
      + " BTU an hour - check that against the burner sticker, because the GPM number and the BTU number were never in the same room.";
  }
  return { gpmPlan: gpmPlan, renderGpm: renderGpm, morningPlan: morningPlan, renderMorning: renderMorning, gasPlan: gasPlan, renderGas: renderGas };
})();
if (typeof module !== "undefined" && module.exports) module.exports = TanklessMath;
