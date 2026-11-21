"""Drilling parallel coordinates using the established offline/widget approach."""
import html
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs
from sessions.ch15.drilling_data import load_data,SUBGROUPS
from sessions.ch15.exploration import NUMERIC

MATERIAL={"P":0,"K":1,"N":2}
DRILL={"N":0,"H":1,"W":2}
LABELS=["vc [m/min]","n [1/min]","f [mm/rev]","vf [mm/min]","Pc [kW]","Kühlung [%]","Zeit [s]"]

def prepare():
    data=load_data().copy()
    for column,levels in [("Material",list(MATERIAL)),("Drill Bit Type",list(DRILL))]:data[column]=pd.Categorical(data[column],categories=levels)
    for flag in SUBGROUPS:data[flag]=pd.Categorical(data[flag],categories=[0,1])
    return data

def figure(data,target="BEF"):
    if target not in SUBGROUPS:raise ValueError("Unknown drilling failure")
    dims=[dict(name=c,label=label,values=data[c].tolist()) for c,label in zip(NUMERIC,LABELS)]
    dims += [dict(name="Material",label="Material",values=data.Material.map(MATERIAL).astype(int).tolist(),range=[-.15,2.15],tickvals=[0,1,2],ticktext=["P – Stahl","K – Gusseisen","N – Nichteisen"]),dict(name="Drill Bit Type",label="Bohrertyp",values=data["Drill Bit Type"].map(DRILL).astype(int).tolist(),range=[-.15,2.15],tickvals=[0,1,2],ticktext=["N","H","W"]),dict(name="failure",label=target,values=data[target].astype(int).tolist(),range=[-.08,1.08],tickvals=[0,1],ticktext=["0: nicht markiert","1: markiert"])]
    scale=[[0,"#0072b2"],[1/3,"#0072b2"],[1/3,"#d55e00"],[2/3,"#d55e00"],[2/3,"#009e73"],[1,"#009e73"]]
    fig=go.Figure(go.Parcoords(dimensions=dims,line=dict(color=data.Material.map(MATERIAL).astype(int).tolist(),colorscale=scale,cmin=-.5,cmax=2.5,colorbar=dict(title="Material",tickvals=[0,1,2],ticktext=["P","K","N"])),labelfont=dict(size=12),tickfont=dict(size=11)))
    fig.update_layout(width=1400,height=610,margin=dict(l=65,r=160,t=90,b=45),paper_bgcolor="white",font=dict(family="Arial"))
    return fig

def offline_html(data,target="BEF"):
    template=Path(__file__).with_name("interactive_patterns.html").read_text(encoding="utf-8")
    options="".join(f'<option value="{f}"'+(' selected' if f==target else '')+f'>{f}</option>' for f in SUBGROUPS)
    return template.replace("__PLOTLY_JS__",get_plotlyjs()).replace("__FIGURE__",figure(data,target).to_json()).replace("__FLAGS__",json.dumps({f:data[f].astype(int).tolist() for f in SUBGROUPS})).replace("__OPTIONS__",options)

def notebook_widget(data):
    import ipywidgets as widgets
    dropdown=widgets.Dropdown(options=SUBGROUPS,value="BEF",description="Fehlertyp:")
    panel=widgets.HTML()
    def update(change=None):panel.value='<iframe title="Drilling-Parallelkoordinaten" style="width:100%;height:820px;border:0" srcdoc="'+html.escape(offline_html(data,dropdown.value),quote=True)+'"></iframe>'
    dropdown.observe(update,names="value");update()
    return widgets.VBox([dropdown,panel]),dropdown
