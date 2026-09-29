-- Execute no SQL Editor do Supabase.
create extension if not exists pgcrypto;
create table if not exists public.usuarios (
 id uuid primary key default gen_random_uuid(), auth_user_id uuid unique references auth.users(id) on delete cascade,
 nome text not null, email text unique not null, perfil text not null check (perfil in ('PLANEJAMENTO','DV','GEV','GC')),
 dv text, gev text, gc text, ativo boolean not null default true, ultimo_acesso timestamptz
);
create table if not exists public.forecast (
 id bigint generated always as identity primary key, dir text, diretor text, nome_gev text, nome_gc text,
 conta_principal text, grupo_empresarial text, vertical text, internacional boolean default false, iot boolean default false,
 broker boolean default false, novo boolean default false, so_ge boolean default false, plataforma text, familia text, tipo text,
 janeiro numeric default 0, fevereiro numeric default 0, marco numeric default 0, abril numeric default 0, maio numeric default 0, junho numeric default 0,
 julho numeric default 0, agosto numeric default 0, setembro numeric default 0, outubro numeric default 0, novembro numeric default 0, dezembro numeric default 0,
 atualizado_em timestamptz default now(), atualizado_por uuid references auth.users(id)
);
create table if not exists public.historico (
 id bigint generated always as identity primary key, forecast_id bigint references public.forecast(id) on delete cascade,
 campo text not null, valor_anterior numeric, valor_novo numeric, usuario_id uuid references auth.users(id), criado_em timestamptz default now()
);
create index if not exists forecast_diretor_idx on public.forecast(diretor);
create index if not exists forecast_gev_idx on public.forecast(nome_gev);
create index if not exists forecast_gc_idx on public.forecast(nome_gc);
alter table public.usuarios enable row level security;
alter table public.forecast enable row level security;
alter table public.historico enable row level security;

create or replace function public.meu_perfil() returns public.usuarios language sql stable security definer set search_path=public as $$
 select * from public.usuarios where auth_user_id=auth.uid() and ativo=true limit 1; $$;
revoke all on function public.meu_perfil() from public; grant execute on function public.meu_perfil() to authenticated;

create policy "usuario le proprio perfil" on public.usuarios for select to authenticated using (auth_user_id=auth.uid() or (select perfil from public.meu_perfil())='PLANEJAMENTO');
create policy "forecast leitura hierarquica" on public.forecast for select to authenticated using (
 (select perfil from public.meu_perfil())='PLANEJAMENTO' or
 ((select perfil from public.meu_perfil())='DV' and diretor=coalesce((select dv from public.meu_perfil()),(select nome from public.meu_perfil()))) or
 ((select perfil from public.meu_perfil())='GEV' and nome_gev=coalesce((select gev from public.meu_perfil()),(select nome from public.meu_perfil()))) or
 ((select perfil from public.meu_perfil())='GC' and nome_gc=coalesce((select gc from public.meu_perfil()),(select nome from public.meu_perfil()))) );
create policy "forecast atualizacao hierarquica" on public.forecast for update to authenticated using (
 (select perfil from public.meu_perfil())='PLANEJAMENTO' or
 ((select perfil from public.meu_perfil())='DV' and diretor=coalesce((select dv from public.meu_perfil()),(select nome from public.meu_perfil()))) or
 ((select perfil from public.meu_perfil())='GEV' and nome_gev=coalesce((select gev from public.meu_perfil()),(select nome from public.meu_perfil()))) or
 ((select perfil from public.meu_perfil())='GC' and nome_gc=coalesce((select gc from public.meu_perfil()),(select nome from public.meu_perfil()))) ) with check (true);
create policy "historico inserir proprio" on public.historico for insert to authenticated with check (usuario_id=auth.uid());
create policy "historico ler planejamento" on public.historico for select to authenticated using ((select perfil from public.meu_perfil())='PLANEJAMENTO' or usuario_id=auth.uid());
