# ORL Flash — Guia de Setup Completo

Você vai conectar 3 plataformas gratuitas em ~45 minutos.
Cada etapa tem um "✅ como saber que funcionou".

---

## VISÃO GERAL DO FLUXO

```
Você → faz um card no CSV
  ↓
Python script → envia para o Supabase (banco de dados)
  ↓
index.html → busca cards do Supabase e exibe
  ↓
GitHub → guarda o código
  ↓
Vercel → publica automaticamente (URL pública)
```

---

## ETAPA 1 — SUPABASE (banco de dados)

### 1.1 Criar conta e projeto
1. Acesse **https://supabase.com** → "Start your project" → conta Google
2. "New project" → nome: **orl-flash** → escolha uma senha → região: **South America (São Paulo)**
3. Aguarde ~2 minutos (barra de progresso no painel)

### 1.2 Criar as tabelas
1. No painel do projeto → menu esquerdo → **SQL Editor**
2. Clique em "New query"
3. Abra o arquivo `supabase/schema.sql` desta pasta e **copie todo o conteúdo**
4. Cole no editor e clique **Run** (▶)
5. Deve aparecer "Success. No rows returned"

✅ **Verificação:** Menu esquerdo → "Table Editor" → você verá as tabelas `flashcards` e `progresso`

### 1.3 Pegar as credenciais
1. Menu esquerdo → **Settings** → **API**
2. Copie os dois valores:
   - **Project URL** → algo como `https://abcxyz.supabase.co`
   - **anon public** (em "Project API keys")
3. Abra o `index.html` desta pasta e substitua nas linhas 14-15:
   ```javascript
   const SUPABASE_URL = "https://abcxyz.supabase.co";   // ← seu Project URL
   const SUPABASE_KEY = "eyJhbGci...";                   // ← seu anon public
   ```
4. Repita no arquivo `scripts/importar-cards.py` (linhas 22-23)

✅ **Verificação:** Abra o `index.html` no navegador → o badge "DEMO" não aparece mais

---

## ETAPA 2 — GITHUB (código-fonte)

### 2.1 Criar conta (se não tiver)
1. Acesse **https://github.com** → "Sign up" → conta gratuita

### 2.2 Criar repositório
1. No GitHub → botão verde **"New"** (ou https://github.com/new)
2. Preencha:
   - Repository name: **orl-flash**
   - Visibility: **Public**
   - Marque: **"Add a README file"**
3. Clique **"Create repository"**

### 2.3 Fazer upload dos arquivos
1. No repositório criado → clique **"Add file"** → **"Upload files"**
2. Arraste **todos os arquivos desta pasta** (index.html, vercel.json, supabase/, scripts/, data/)
3. Na caixa "Commit changes" → mensagem: **"Setup inicial ORL Flash"**
4. Clique **"Commit changes"**

✅ **Verificação:** Você vê todos os arquivos listados no repositório

---

## ETAPA 3 — VERCEL (publicação automática)

### 3.1 Criar conta
1. Acesse **https://vercel.com** → "Sign Up" → **"Continue with GitHub"**
   (isso já conecta as duas plataformas)

### 3.2 Importar o projeto
1. No Vercel dashboard → clique **"Add New…"** → **"Project"**
2. Em "Import Git Repository" → você verá `orl-flash` na lista → clique **"Import"**
3. Configurações:
   - Framework Preset: **Other** (não Next.js, não React — é HTML puro)
   - Root Directory: `.` (ponto — raiz do repositório)
   - Deixe o resto padrão
4. Clique **"Deploy"**
5. Aguarde ~30 segundos

✅ **Verificação:** Vercel mostra "Congratulations!" e uma URL tipo:
`https://orl-flash-seunome.vercel.app`

### 3.3 Domínio personalizado (opcional, depois)
- No painel do projeto no Vercel → "Domains" → adicione seu domínio

---

## ETAPA 4 — IMPORTAR CARDS DO CSV

### 4.1 Instalar Python (se não tiver)
- Windows: baixe em https://www.python.org/downloads → marque "Add to PATH"

### 4.2 Instalar dependência
Abra o Prompt de Comando e rode:
```
pip install requests
```

### 4.3 Preparar o CSV
1. Coloque o arquivo `Cap02_ORL_Flash.csv` (ou qualquer capítulo) na pasta `data/`
2. Confirme que o CSV tem as colunas:
   `ID, Grande_Area, Capitulo, Subtema, Tipo_Card, Pergunta, Resposta, Observacao, Imagem_Pergunta, Imagem_Resposta, Fonte, Pagina`

### 4.4 Executar o importador
No Prompt de Comando, navegue até esta pasta e rode:
```
python scripts/importar-cards.py
```
Você verá algo como:
```
📂 Lendo: data/Cap02_ORL_Flash.csv
📋 212 cards encontrados no CSV

🚀 Enviando para o Supabase...
  ✅ 100/212 cards enviados
  ✅ 200/212 cards enviados
  ✅ 212/212 cards enviados

========================================
✅ Enviados com sucesso: 212
========================================
```

✅ **Verificação:** Abra a URL do Vercel → os 212 cards aparecem no site!

---

## FLUXO DE TRABALHO DO DIA A DIA

```
1. Claude gera CSV do capítulo
2. Salve o CSV em data/
3. Rode: python scripts/importar-cards.py
4. Cards aparecem no site em segundos
5. Faça commit no GitHub → Vercel atualiza automaticamente
```

---

## PRÓXIMAS EVOLUÇÕES (quando quiser)

| Fase | O que adiciona | Tecnologia |
|------|---------------|------------|
| v2 | Login de usuários + progresso salvo | Supabase Auth |
| v3 | Dashboard de desempenho por área | Supabase + Charts |
| v4 | Algoritmo de revisão espaçada (SM-2) | Supabase + JS |
| v5 | Assinatura paga | Stripe + Supabase |
| v6 | App mobile | Capacitor ou React Native |

---

## DÚVIDAS FREQUENTES

**"O site trava ao abrir o HTML direto no celular?"**
Use a URL do Vercel, não o arquivo local — o celular precisa buscar os cards do Supabase pela internet.

**"Posso importar mais de um capítulo?"**
Sim. Rode o script para cada CSV. O script faz "upsert" — atualiza se o card já existe, insere se for novo.

**"Como atualizar um card depois de importar?"**
Edite o CSV e rode o script novamente — ele atualiza automaticamente (sem duplicar).

**"O que fazer quando chegar a hora do login e do Stripe?"**
Me chame — migro o projeto para Next.js + Vercel em uma sessão.
