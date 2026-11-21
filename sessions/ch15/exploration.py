"""Descriptive exploration only: overlapping labels, no models or rule fitting."""
import pandas as pd
from sessions.ch15.drilling_data import SUBGROUPS,TARGETS
NUMERIC=["Cutting speed vc [m/min]","Spindle speed n [1/min]","Feed f [mm/rev]","Feed rate vf [mm/min]","Power Pc [kW]","Cooling [%]","Process Time [sec]"]
CATEGORICAL=["Material","Drill Bit Type"]

def summarize(data):
    numeric=[];categories=[];bounds=[];identifiers=[]
    for flag in SUBGROUPS:
        for value in [0,1]:
            part=data.loc[data[flag].eq(value)]
            identifiers.append({"Fehlertyp":flag,"Flag":value,"Zeilen":len(part),"ID eindeutig":part.ID.nunique(),"ID min":part.ID.min(),"ID max":part.ID.max()})
            for feature in NUMERIC:
                row={"Fehlertyp":flag,"Flag":value,"Merkmal":feature,**part[feature].describe().to_dict()}
                numeric.append(row)
                if value==1:bounds.append({"Fehlertyp":flag,"Merkmal":feature,"n":len(part),"Minimum markiert":part[feature].min(),"Maximum markiert":part[feature].max()})
            for feature in CATEGORICAL:
                for level in sorted(data[feature].unique()):
                    n=int(part[feature].eq(level).sum())
                    categories.append({"Fehlertyp":flag,"Flag":value,"Merkmal":feature,"Kategorie":level,"Anzahl":n,"Anteil [%]":100*n/len(part) if len(part) else float("nan")})
    material=[]
    for mat in sorted(data.Material.unique()):
        for value in [0,1]:
            part=data.loc[data.Material.eq(mat)&data.FWF.eq(value)]
            for feature in [NUMERIC[0],NUMERIC[3]]:
                material.append({"Material":mat,"FWF":value,"Merkmal":feature,"n":len(part),"min":part[feature].min(),"Median":part[feature].median(),"max":part[feature].max()})
    pairs=data.groupby(CATEGORICAL,observed=True).WDF.agg(Zeilen="size",WDF="sum").reset_index()
    pairs["WDF-Anteil [%]"]=100*pairs.WDF/pairs.Zeilen
    return {"numeric_summary":pd.DataFrame(numeric),"categorical_summary":pd.DataFrame(categories),"positive_bounds":pd.DataFrame(bounds),"identifier_check":pd.DataFrame(identifiers),"fwf_material_summary":pd.DataFrame(material),"wdf_pairs":pairs}
