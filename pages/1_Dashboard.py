import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auth import get_profile
from utils.data import visible_forecast, MONTHS

st.set_page_config(page_title="Dashboard | Forecast 2027",layout="wide")
p=get_profile(); rows=visible_forecast(p); df=pd.DataFrame(rows)
st.title("Dashboard")
st.caption(f"{p['nome']} | Perfil {p['perfil']}")
if df.empty: st.info("Nenhum registro disponível para o seu perfil."); st.stop()
for m in MONTHS:
    if m not in df: df[m]=0
    df[m]=pd.to_numeric(df[m],errors="coerce").fillna(0)
monthly=df[MONTHS].sum()
c1,c2,c3=st.columns(3)
c1.metric("Forecast anual",f"R$ {monthly.sum():,.2f}")
c2.metric("Registros",len(df))
c3.metric("Grupos empresariais",df.get("grupo_empresarial",pd.Series(dtype=str)).nunique())
fig=px.bar(x=[m.title() for m in MONTHS],y=monthly.values,labels={"x":"Mês","y":"Valor"},title="Forecast mensal")
st.plotly_chart(fig,use_container_width=True)
