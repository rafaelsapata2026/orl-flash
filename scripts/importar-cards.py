#!/usr/bin/env python3
"""
ORL Flash — Importador de CSV para Supabase
============================================
Como usar:
  1. Coloque o arquivo CSV na pasta /data/
  2. Preencha as 3 variáveis abaixo (SUPABASE_URL, SUPABASE_KEY, CSV_FILE)
  3. Execute: python scripts/importar-cards.py

Requisitos:
  pip install requests
"""

import csv
import json
import sys
import os

try:
    import requests
except ImportError:
    print("❌ Instale requests: pip install requests")
    sys.exit(1)

# ============================================================
#  CONFIGURE AQUI — preencha com seus dados do Supabase
# ============================================================
SUPABASE_URL = "https://SEU_PROJETO.supabase.co"          # Project URL
SUPABASE_KEY = "SEU_ANON_KEY_AQUI"                        # anon/public key
CSV_FILE     = "data/Cap02_ORL_Flash.csv"                 # caminho do CSV
# ============================================================

ENDPOINT = f"{SUPABASE_URL}/rest/v1/flashcards"
HEADERS  = {
    "apikey":          SUPABASE_KEY,
    "Authorization":   f"Bearer {SUPABASE_KEY}",
    "Content-Type":    "application/json",
    "Prefer":          "resolution=merge-duplicates",      # upsert: atualiza se já existe
}

COLUNAS_ESPERADAS = {
    "ID", "Grande_Area", "Capitulo", "Subtema", "Tipo_Card",
    "Pergunta", "Resposta", "Observacao",
    "Imagem_Pergunta", "Imagem_Resposta", "Fonte", "Pagina"
}

def ler_csv(caminho):
    if not os.path.exists(caminho):
        print(f"❌ Arquivo não encontrado: {caminho}")
        sys.exit(1)

    cards = []
    with open(caminho, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        colunas = set(reader.fieldnames or [])
        faltando = COLUNAS_ESPERADAS - colunas
        if faltando:
            print(f"⚠️  Colunas ausentes no CSV: {faltando}")

        for i, row in enumerate(reader, 1):
            card = {
                "id":              int(row.get("ID", i)),
                "grande_area":     row.get("Grande_Area", "").strip(),
                "capitulo":        row.get("Capitulo", "").strip(),
                "subtema":         row.get("Subtema", "").strip(),
                "tipo":            row.get("Tipo_Card", "PR").strip(),
                "pergunta":        row.get("Pergunta", "").strip(),
                "resposta":        row.get("Resposta", "").strip(),
                "observacao":      row.get("Observacao", "").strip(),
                "imagem_pergunta": row.get("Imagem_Pergunta", "").strip(),
                "imagem_resposta": row.get("Imagem_Resposta", "").strip(),
                "fonte":           row.get("Fonte", "").strip(),
                "pagina":          row.get("Pagina", "").strip(),
            }
            if not card["pergunta"] or not card["resposta"]:
                print(f"  ⚠️  Linha {i} ignorada (pergunta ou resposta vazios)")
                continue
            cards.append(card)

    return cards

def enviar_lote(cards, lote=100):
    total   = len(cards)
    enviado = 0
    erros   = 0

    for inicio in range(0, total, lote):
        fatia = cards[inicio:inicio + lote]
        resp  = requests.post(ENDPOINT, headers=HEADERS, json=fatia, timeout=30)

        if resp.status_code in (200, 201):
            enviado += len(fatia)
            print(f"  ✅ {enviado}/{total} cards enviados")
        else:
            erros += len(fatia)
            print(f"  ❌ Erro no lote {inicio}-{inicio+len(fatia)}: {resp.status_code} — {resp.text[:200]}")

    return enviado, erros

def main():
    if SUPABASE_URL.startswith("https://SEU"):
        print("❌ Configure SUPABASE_URL e SUPABASE_KEY no script antes de executar.")
        sys.exit(1)

    print(f"📂 Lendo: {CSV_FILE}")
    cards = ler_csv(CSV_FILE)
    print(f"📋 {len(cards)} cards encontrados no CSV\n")

    print(f"🚀 Enviando para o Supabase...")
    ok, err = enviar_lote(cards)

    print(f"\n{'='*40}")
    print(f"✅ Enviados com sucesso: {ok}")
    if err:
        print(f"❌ Erros: {err}")
    print(f"{'='*40}")
    print("Feito! Abra o site para ver os cards.")

if __name__ == "__main__":
    main()
