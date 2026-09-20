import json
from django.shortcuts import render
from .forms import UploadNotaFiscalForm
from .services.gemini_service import extrair_dados_nota_fiscal
from django.shortcuts import redirect
from .models import Fornecedor, Faturado, NotaFiscal, TipoDespesa, Parcela


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



def confirmar_nota_fiscal(request):
    if request.method == "POST":
        dados = json.loads(request.POST["dados_json"])

        fornecedor, _ = Fornecedor.objects.get_or_create(
            cnpj=dados["fornecedor"]["cnpj"],
            defaults={
                "razao_social": dados["fornecedor"]["razao_social"],
                "nome_fantasia": dados["fornecedor"]["nome_fantasia"],
            },
        )
        faturado, _ = Faturado.objects.get_or_create(
            cpf=dados["faturado"]["cpf"],
            defaults={"nome_completo": dados["faturado"]["nome_completo"]},
        )
        tipo_despesa, _ = TipoDespesa.objects.get_or_create(
            nome=dados["tipo_despesa"]
        )

        nota = NotaFiscal.objects.create(
            fornecedor=fornecedor,
            faturado=faturado,
            numero=dados["numero"],
            data_emissao=dados["data_emissao"],
            descricao_produtos=dados["descricao_produtos"],
            valor_total=dados["valor_total"],
        )
        nota.tipos_despesa.add(tipo_despesa)

        for p in dados["parcelas"]:
            Parcela.objects.create(
                nota_fiscal=nota,
                numero_parcela=p["numero_parcela"],
                data_vencimento=p["data_vencimento"],
                valor=p["valor"],
            )

        return redirect("nota_fiscal_sucesso")