import streamlit as st
from utils.auth import login, logout

st.set_page_config(page_title="Forecast 2027", page_icon="📊", layout="wide")
st.title("Forecast 2027")
st.caption("Planejamento Comercial SP")

if st.session_state.get("user"):
    st.success(f"Acesso ativo: {st.session_state.user.email}")
    st.write("Use o menu lateral para abrir Dashboard, Forecast ou Administração.")
    if st.button("Sair"):
        logout(); st.rerun()
else:
    with st.form("login"):
        email=st.text_input("E-mail corporativo")
        password=st.text_input("Senha", type="password")
        submit=st.form_submit_button("Entrar", use_container_width=True)
    if submit:
        try:
            login(email,password); st.success("Login realizado."); st.rerun()
        except Exception:
            st.error("E-mail ou senha inválidos, ou acesso ainda não liberado.")
