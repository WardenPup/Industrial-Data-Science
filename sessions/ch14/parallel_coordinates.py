"""Categorical AI4I parallel coordinates, notebook widget and standalone offline view."""
import html
import json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import get_plotlyjs
from sessions.ch14.tool_wear import load_data, FLAGS
from sessions.ch14.overstrain import prepare as add_features

CONTINUOUS = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]", "Tool wear [min]", "temp_diff", "power", "wearadjTorque"]
LABELS = ["Luft [K]", "Prozess [K]", "Drehzahl [rpm]", "Drehmoment [Nm]", "Verschleiß [min]", "ΔT [K]", "Leistung [W]", "w·τ [min·Nm]"]
TYPE_CODES = {"L": 0, "M": 1, "H": 2}

def prepare():
    data = add_features(load_data())
    data["Type"] = pd.Categorical(data.Type, categories=["L", "M", "H"])
    for flag in FLAGS:
        data[flag] = pd.Categorical(data[flag], categories=[0, 1])
    return data

def figure(data, target="HDF"):
    if target not in FLAGS:
        raise ValueError("Unknown failure flag")
    dimensions = [dict(name=column, label=label, values=data[column].tolist()) for column, label in zip(CONTINUOUS, LABELS)]
    dimensions += [dict(name="Type", label="Type", values=data.Type.map(TYPE_CODES).astype(int).tolist(), range=[-.15,2.15], tickvals=[0,1,2], ticktext=["L","M","H"]),
                   dict(name="failure", label=target, values=data[target].astype(int).tolist(), range=[-.08,1.08], tickvals=[0,1], ticktext=["0: nicht markiert","1: markiert"])]
    colors = [[0,"#0072b2"],[1/3,"#0072b2"],[1/3,"#d55e00"],[2/3,"#d55e00"],[2/3,"#009e73"],[1,"#009e73"]]
    fig = go.Figure(go.Parcoords(dimensions=dimensions, line=dict(color=data.Type.map(TYPE_CODES).astype(int).tolist(), colorscale=colors, cmin=-.5, cmax=2.5, colorbar=dict(title="Type",tickvals=[0,1,2],ticktext=["L","M","H"])), labelfont=dict(size=12), tickfont=dict(size=11)))
    fig.update_layout(width=1400,height=610,margin=dict(l=65,r=160,t=90,b=45),paper_bgcolor="white",font=dict(family="Arial"))
    return fig

def offline_html(data, target="HDF"):
    payload = figure(data,target).to_json()
    flags = json.dumps({name:data[name].astype(int).tolist() for name in FLAGS})
    options = "".join(f'<option value="{name}"'+(' selected' if name==target else '')+f'>{name}</option>' for name in FLAGS)
    template = Path(__file__).with_name("parallel_coordinates.html").read_text(encoding="utf-8")
    return template.replace("__PLOTLY_JS__",get_plotlyjs()).replace("__FIGURE__",payload).replace("__FLAGS__",flags).replace("__OPTIONS__",options)

def notebook_widget(data):
    import ipywidgets as widgets
    dropdown = widgets.Dropdown(options=FLAGS, value="HDF", description="Fehlerflag:")
    panel = widgets.HTML()
    def update(change=None):
        panel.value = '<iframe title="Interaktive Parallelkoordinaten" style="width:100%;height:790px;border:0" srcdoc="'+html.escape(offline_html(data,dropdown.value),quote=True)+'"></iframe>'
    dropdown.observe(update,names="value")
    update()
    return widgets.VBox([dropdown,panel]), dropdown
