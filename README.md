# Forecast 2027

Aplicação Streamlit com Supabase para consulta, edição, auditoria e acesso hierárquico.

## Perfis
- PLANEJAMENTO: todos os registros.
- DV: registros do seu diretor.
- GEV: registros do seu GEV.
- GC: registros do seu GC.

## Implantação
1. Crie um projeto no Supabase.
2. No SQL Editor execute `supabase/schema.sql`.
3. Em Authentication > Users crie o primeiro usuário.
4. Copie o UUID e execute uma versão ajustada de `supabase/exemplo_primeiro_usuario.sql`.
5. No GitHub, envie todos os arquivos, exceto `.streamlit/secrets.toml`.
6. No Streamlit Community Cloud escolha o repositório e `app.py`.
7. Em Advanced settings > Secrets informe:
```toml
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
SUPABASE_ANON_KEY = "SUA_CHAVE_PUBLICAVEL_ANON"
```
8. Faça o deploy.

## Segurança
Nunca envie `secrets.toml`, senha, service_role key ou credenciais corporativas ao GitHub. Use apenas a chave pública/anon no app e mantenha RLS ativa. Para uso corporativo real, obtenha aprovação de Segurança da Informação e Privacidade antes de inserir dados empresariais em serviço externo.

## Carga inicial
Importe CSV no Table Editor da tabela `forecast`. Use os nomes de coluna definidos em `supabase/schema.sql`; `marco` é usado sem cedilha.
