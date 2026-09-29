import streamlit as st
import pandas as pd
from utils.auth import get_profile
from utils.supabase_client import get_supabase

st.set_page_config(page_title="Administração | Forecast 2027",layout="wide")
p=get_profile(); st.title("Administração")
if p["perfil"]!="PLANEJAMENTO": st.error("Acesso exclusivo do Planejamento."); st.stop()
db=get_supabase(); users=db.table("usuarios").select("id,nome,email,perfil,dv,gev,gc,ativo").order("nome").execute().data or []
st.dataframe(pd.DataFrame(users),use_container_width=True,hide_index=True)
st.info("Cadastre contas primeiro em Authentication > Users e depois vincule o UUID em usuarios.auth_user_id.")
