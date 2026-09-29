from datetime import datetime, timezone
import pandas as pd
from utils.supabase_client import get_supabase

MONTHS=["janeiro","fevereiro","marco","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]

def visible_forecast(profile, limit=5000):
    q=get_supabase().table("forecast").select("*").order("grupo_empresarial").limit(limit)
    p=profile["perfil"]
    if p=="DV": q=q.eq("diretor", profile.get("dv") or profile.get("nome"))
    elif p=="GEV": q=q.eq("nome_gev", profile.get("gev") or profile.get("nome"))
    elif p=="GC": q=q.eq("nome_gc", profile.get("gc") or profile.get("nome"))
    return q.execute().data or []

def update_month(record_id, month, value, user_id):
    if month not in MONTHS: raise ValueError("Mês inválido")
    db=get_supabase()
    old=db.table("forecast").select(month).eq("id", record_id).single().execute().data[month]
    db.table("forecast").update({month: float(value), "atualizado_por": str(user_id), "atualizado_em": datetime.now(timezone.utc).isoformat()}).eq("id", record_id).execute()
    db.table("historico").insert({"forecast_id": record_id,"campo":month,"valor_anterior":old,"valor_novo":float(value),"usuario_id":str(user_id)}).execute()

def to_excel_bytes(rows):
    from io import BytesIO
    out=BytesIO(); pd.DataFrame(rows).to_excel(out,index=False,engine="openpyxl"); return out.getvalue()
