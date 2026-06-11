-- ============================================================
--  ORL FLASH — Schema Supabase
--  Execute este arquivo no SQL Editor do Supabase
--  (painel do projeto → SQL Editor → colar e executar)
-- ============================================================

-- ── TABELA PRINCIPAL DE FLASHCARDS ──────────────────────────
create table if not exists flashcards (
  id              bigint        primary key,
  grande_area     text          not null,
  capitulo        text          not null,
  subtema         text          default '',
  tipo            text          not null,
  pergunta        text          not null,
  resposta        text          not null,
  observacao      text          default '',
  imagem_pergunta text          default '',
  imagem_resposta text          default '',
  fonte           text          default '',
  pagina          text          default '',
  created_at      timestamptz   default now()
);

-- ── SEGURANÇA: LEITURA PÚBLICA, SEM LOGIN ───────────────────
alter table flashcards enable row level security;

create policy "Leitura pública de flashcards"
  on flashcards
  for select
  using (true);

-- ── ÍNDICES PARA FILTROS RÁPIDOS ────────────────────────────
create index if not exists idx_flashcards_area     on flashcards (grande_area);
create index if not exists idx_flashcards_capitulo on flashcards (capitulo);
create index if not exists idx_flashcards_tipo     on flashcards (tipo);

-- ── PROGRESSO DO USUÁRIO (preparado para quando tiver login) ─
create table if not exists progresso (
  id          uuid          primary key default gen_random_uuid(),
  user_id     uuid          references auth.users(id) on delete cascade,
  card_id     bigint        references flashcards(id) on delete cascade,
  resultado   text          check (resultado in ('acertei', 'duvida', 'errei')),
  revisado_em timestamptz   default now(),
  unico       text          generated always as (user_id::text || '_' || card_id::text) stored,
  constraint progresso_unico unique (unico)
);

alter table progresso enable row level security;

create policy "Usuário vê só o próprio progresso"
  on progresso for all
  using (auth.uid() = user_id);
