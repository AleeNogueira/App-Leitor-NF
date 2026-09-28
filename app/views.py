import json
from functools import wraps

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, UploadNotaFiscalForm
from .services.gemini_service import extrair_dados_nota_fiscal


def login_required_local(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.session.get("local_user_authenticated"):
            return redirect(f"{reverse('login')}?next={request.get_full_path()}")
        return view_func(request, *args, **kwargs)

    return wrapped_view


def login_view(request):
    if request.session.get("local_user_authenticated"):
        return redirect("upload_nota_fiscal")

    form = LoginForm(request.POST or None)
    erro = None
    if request.method == "POST" and form.is_valid():
        credentials_path = settings.BASE_DIR / "local_credentials.json"
        try:
            with credentials_path.open(encoding="utf-8") as credentials_file:
                credentials = json.load(credentials_file)
        except (OSError, json.JSONDecodeError):
            credentials = {}

        username = form.cleaned_data["username"]
        password_hash = credentials.get("password_hash", "")
        if username == credentials.get("username") and password_hash and check_password(
            form.cleaned_data["password"], password_hash
        ):
            request.session.cycle_key()
            request.session["local_user_authenticated"] = True
            request.session["local_username"] = username
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect("upload_nota_fiscal")

        erro = "Usuário ou senha inválidos."

    return render(request, "app/login.html", {"form": form, "erro": erro})


def logout_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    request.session.flush()
    return redirect("login")


@login_required_local
def upload_nota_fiscal(request):
    dados_extraidos = None
    erro = None
    dados_json = None

    if request.method == "POST":
        form = UploadNotaFiscalForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.cleaned_data["arquivo"]
            try:
                dados_extraidos = extrair_dados_nota_fiscal(arquivo)
                dados_json = json.dumps(dados_extraidos, ensure_ascii=False, indent=2)
            except (json.JSONDecodeError, ValueError):
                erro = "Não foi possível interpretar a resposta do Gemini. Tente novamente."
            except Exception as e:
                erro = f"Erro ao processar o arquivo: {e}"
    else:
        form = UploadNotaFiscalForm()

    return render(request, "app/upload.html", {
        "form": form,
        "dados": dados_extraidos,
        "dados_json": dados_json,
        "erro": erro,
    })
