import json
import os
import tempfile
from pathlib import Path

from google import genai
from django.conf import settings

api_key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
if not api_key:
    raise ValueError("Chave da API do Gemini não encontrada. Configure GEMINI_API_KEY no arquivo .env.")

client = genai.Client(api_key=api_key)

PROMPT = """
Você é um extrator de dados de notas fiscais. Analise o arquivo
enviado e retorne APENAS um JSON válido (sem markdown, sem texto
adicional), seguindo exatamente este schema:

{
  "fornecedor": {
    "razao_social": "",
    "nome_fantasia": "",
    "cnpj": ""
  },
  "faturado": {
    "nome_completo": "",
    "cpf": ""
  },
  "numero": "",
  "data_emissao": "YYYY-MM-DD",
  "descricao_produtos": "",
  "valor_total": 0.00,
  "tipo_despesa": "",
  "parcelas": [
    {"numero_parcela": 1, "data_vencimento": "YYYY-MM-DD", "valor": 0.00}
  ]
}

Se algum campo não for encontrado no documento, retorne string vazia
ou lista vazia, nunca invente valores.
"""


def extrair_dados_nota_fiscal(arquivo_django):
    """
    Recebe um arquivo do Django (InMemoryUploadedFile) e retorna
    um dicionário com os dados extraídos pelo Gemini.
    """
    arquivo_django.seek(0)
    nome_arquivo = Path(arquivo_django.name or "arquivo.pdf").name
    extensao = Path(nome_arquivo).suffix or ".pdf"

    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as arquivo_temp:
        for chunk in arquivo_django.chunks():
            arquivo_temp.write(chunk)
        caminho_temporario = arquivo_temp.name

    try:
        uploaded_file = client.files.upload(
            file=caminho_temporario,
            config={"mime_type": arquivo_django.content_type or "application/octet-stream"},
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded_file, PROMPT],
        )

        texto = response.text.strip()
        texto = texto.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(texto)
    finally:
        if os.path.exists(caminho_temporario):
            os.remove(caminho_temporario)