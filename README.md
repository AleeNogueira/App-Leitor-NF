# Sistema de Upload e Extração de Nota Fiscal

Este projeto é uma aplicação Django para enviar arquivos de nota fiscal e extrair dados com a API do Gemini.

## Requisitos

- Python 3.11+
- Git
- Acesso à API do Gemini com chave válida

## Setup inicial

1. Clone o repositório.
2. Crie um ambiente virtual:

```powershell
python -m venv .venv
```

3. Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Instale as dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

5. Crie um arquivo `.env` com base no exemplo:

```powershell
Copy-Item .env.example .env
```

6. Preencha as variáveis no `.env`:

```env
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
GEMINI_API_KEY=sua_chave_do_gemini
DATABASE_URL=sqlite:///db.sqlite3
```

7. Execute as migrações:

```powershell
python manage.py migrate
```

8. Inicie o servidor:

```powershell
python manage.py runserver
```

9. Acesse:

```text
http://127.0.0.1:8000/
```

## Observações

- O arquivo `.env` não deve ser enviado para o Git.
- A chave do Gemini deve ser válida e com acesso habilitado.
- Caso a API retorne erro 403, verifique a chave e o acesso do projeto no Google AI Studio / Google Cloud.
