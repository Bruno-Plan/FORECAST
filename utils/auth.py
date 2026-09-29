import streamlit as st
from utils.supabase_client import get_supabase

def login(email, password):
    result = get_supabase().auth.sign_in_with_password({"email": email.strip().lower(), "password": password})
    st.session_state["session"] = result.session
    st.session_state["user"] = result.user
    return result

def logout():
    try: get_supabase().auth.sign_out()
    except Exception: pass
    st.session_state.clear()

def require_login():
    if not st.session_state.get("user"):
        st.warning("Faça login para continuar.")
        st.stop()
    return st.session_state["user"]

def get_profile():
    user=require_login()
    data=(get_supabase().table("usuarios").select("*").eq("auth_user_id", str(user.id)).eq("ativo", True).maybe_single().execute().data)
    if not data:
        st.error("Usuário sem perfil ativo na tabela usuarios.")
        st.stop()
    return data
