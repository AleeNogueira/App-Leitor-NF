## Acesso à aplicação

O acesso de demonstração usa o usuário `admin` e a senha `admin`.


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
Se erro execute 
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
``` 
e depois o comando 
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
8. Para criar uma nova chave no SECRET_KEY:
```porwershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```powershell
python manage.py migrate
```

9. Inicie o servidor:

```powershell
python manage.py runserver
```

10. Acesse:

```text
http://127.0.0.1:8000/
```

