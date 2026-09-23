import json
from django.shortcuts import render
from .forms import UploadNotaFiscalForm
from .services.gemini_service import extrair_dados_nota_fiscal


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
