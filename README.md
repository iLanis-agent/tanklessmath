# Tankless Math

The tankless water heater honesty tool. The GPM sticker was measured
against a 35 F rise from water that was already warm. Tankless Math
shrinks the sticker to your inlet temperature, holds it against the
morning's showers, and counts the BTU the burner actually owes.

- Live app: https://ilanis-agent.github.io/tanklessmath/app.html
- Landing: https://ilanis-agent.github.io/tanklessmath/

## What it does

1. **The GPM truth** - honest flow = sticker GPM x 35 / your real rise
   (120 F setpoint minus your inlet temperature).
2. **The morning truth** - honest flow minus 2 GPM per simultaneous
   shower; the verdict reads the unrounded margin.
3. **The burner truth** - BTU per hour = GPM x 60 x 8.34 x rise.

## Files

- `engine.js` - pure functions (`gpmPlan`, `morningPlan`, `gasPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 33 oracle cases, `node test.js` runs green

The norms are labeled; your inlet thermometer keeps the honest ledger.
