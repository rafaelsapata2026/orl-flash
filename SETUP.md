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
