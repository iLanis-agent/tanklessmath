import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def r2(x): return jround(x*100)/100
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def comma(x):
    if isinstance(x,float) and x==int(x): x=int(x)
    return f"{x:,}"

SETPOINT=120
RATED_RISE=35

def gpm_plan(sticker,inlet):
    if not pos(sticker): return {"error":"the sticker GPM must be above zero"}
    if not num(inlet): return {"error":"the inlet temperature must be a number"}
    if inlet>=SETPOINT: return {"error":"the inlet is already at the 120 F setpoint"}
    rise=SETPOINT-inlet
    return {"real":r1(sticker*RATED_RISE/rise),"rise":rise}

def render_gpm(r,sticker,inlet):
    return ("The "+jsnum(sticker)+" GPM sticker assumed a 35 F rise; your "+jsnum(inlet)
            +" F inlet water is "+jsnum(r["rise"])+" F short of the 120 F setpoint, so the heater honestly gives "+jsnum(r["real"])+" GPM.")

def morning_plan(gpm,showers):
    if not pos(gpm): return {"error":"the honest GPM must be above zero"}
    if not num(showers): return {"error":"the shower count must be a number"}
    if showers<1: return {"error":"the shower count must be at least one"}
    demand=showers*2
    margin=gpm-demand
    verdict="with a sink to spare" if margin>=1 else ("honest, but nothing else runs" if margin>=0 else "someone gets the cold surprise")
    return {"demand":r1(demand),"margin":r2(margin),"verdict":verdict}

def render_morning(r,gpm,showers):
    return (jsnum(showers)+(" shower asks " if showers==1 else " showers ask ")+jsnum(r["demand"])+" GPM; your honest "+jsnum(gpm)
            +" GPM leaves a margin of "+jsnum(r["margin"])+" - "+r["verdict"]+".")

def gas_plan(gpm,rise):
    if not pos(gpm): return {"error":"the flow must be above zero"}
    if not pos(rise): return {"error":"the rise must be above zero"}
    return {"btu":jround(gpm*60*8.34*rise)}

def render_gas(r,gpm,rise):
    return ("Heating "+jsnum(gpm)+" GPM across a rise of "+jsnum(rise)+" F asks "+comma(r["btu"])
            +" BTU an hour - check that against the burner sticker, because the GPM number and the BTU number were never in the same room.")

cases=[]
def add(tool,args):
    if tool=="gpm": r=gpm_plan(*args); fn=render_gpm
    elif tool=="morning": r=morning_plan(*args); fn=render_morning
    else: r=gas_plan(*args); fn=render_gas
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(9,40),(11,55),(7,50),(10,45),(8.5,60),(6,70),(9,35),(11.2,42)]:
    add("gpm",a)
for a in [(3.9,2),(6.5,2),(4,2),(5,1),(4.5,3),(2.5,2),(8,3),(3.95,2)]:
    add("morning",a)
for a in [(4,80),(2.5,60),(3.9,80),(5,65),(1.5,90),(6,50)]:
    add("gas",a)
add("gpm",[0,40]); add("gpm",[9,120]); add("gpm",[9,125]); add("gpm",["nine",40]); add("gpm",[9,"cold"])
add("morning",[0,2]); add("morning",[4,0]); add("morning",["some",2])
add("gas",[0,80]); add("gas",[4,0]); add("gas",["lots",80])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
