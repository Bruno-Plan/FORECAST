import streamlit as st
import pandas as pd
from utils.auth import get_profile, require_login
from utils.data import visible_forecast, update_month, to_excel_bytes, MONTHS

st.set_page_config(page_title="Forecast | Forecast 2027",layout="wide")
user=require_login(); p=get_profile(); rows=visible_forecast(p); df=pd.DataFrame(rows)
st.title("Consulta e atualização")
st.caption("A visibilidade é aplicada pelo perfil e também deve ser protegida pelas políticas RLS do Supabase.")
if df.empty: st.info("Nenhum registro disponível."); st.stop()
search=st.text_input("Pesquisar grupo, conta ou responsável")
if search:
    mask=df.astype(str).apply(lambda c:c.str.contains(search,case=False,na=False)).any(axis=1); df=df[mask]
show=[c for c in ["id","diretor","nome_gev","nome_gc","conta_principal","grupo_empresarial","vertical","plataforma","familia","tipo"]+MONTHS if c in df.columns]
st.dataframe(df[show],use_container_width=True,hide_index=True)
st.download_button("Exportar visão para Excel",to_excel_bytes(df[show].to_dict("records")),"forecast_visivel.xlsx")
st.subheader("Alterar valor mensal")
ids=df["id"].tolist(); rid=st.selectbox("ID do registro",ids); month=st.selectbox("Mês",MONTHS); value=st.number_input("Novo valor",min_value=0.0,step=100.0)
if st.button("Salvar alteração",type="primary"):
    try: update_month(rid,month,value,user.id); st.success("Alteração salva e auditada."); st.rerun()
    except Exception as e: st.error(f"Não foi possível salvar: {e}")
