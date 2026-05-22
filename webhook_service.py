from config import SDK, WEBHOOK_SECRET
import hmac
import hashlib
from mercadopago.resources.merchant_order import MerchantOrder

def validar_assinatura(request):

    print("\n=== ENTROU NA VALIDAÇÃO ===")

    x_signature = request.headers.get("x-signature")
    x_request_id = request.headers.get("x-request-id")

    data_id = (
        request.args.get("data.id")
        or request.args.get("id")
    )

    print("\nX-SIGNATURE:", x_signature)
    print("X-REQUEST-ID:", x_request_id)
    print("DATA.ID:", data_id)

    if not x_signature:
        print("Sem x-signature")
        return False

    partes = x_signature.split(",")

    ts = None
    hash_recebido = None

    for parte in partes:
        chave_valor = parte.split("=")

        if len(chave_valor) == 2:
            chave = chave_valor[0].strip()
            valor = chave_valor[1].strip()

            if chave == "ts":
                ts = valor
            elif chave == "v1":
                hash_recebido = valor

    print("\nTIMESTAMP:", ts)
    print("HASH RECEBIDO:", hash_recebido)

    if not data_id or not x_request_id or not ts:
        print("Campos insuficientes para assinatura")
        return False

    manifesto = f"id:{data_id};request-id:{x_request_id};ts:{ts};"

    print("\nMANIFESTO:", manifesto)

    assinatura = hmac.new(
        WEBHOOK_SECRET.encode(),
        manifesto.encode(),
        hashlib.sha256
    ).hexdigest()

    print("\nASSINATURA GERADA:", assinatura)

    if assinatura == hash_recebido:
        print("ASSINATURA VÁLIDA")
        return True

    print("ASSINATURA INVÁLIDA")
    return False

def processar_webhook(dados):

    print("\n=== WEBHOOK RECEBIDO ===")
    print(dados)

    if not dados:
        return

    payment_id = dados.get("data", {}).get("id")

    if not payment_id:
        print("Sem payment_id")
        return

    print(f"Payment ID: {payment_id}")

    pagamento = SDK.payment().get(payment_id)

    status_code = pagamento["status"]

    print(f"HTTP STATUS: {status_code}")

    if status_code != 200:
        print("Pagamento não encontrado")
        return

    response = pagamento["response"]
    status_pagamento = response["status"]

    print(f"STATUS PAGAMENTO: {status_pagamento}")

    if status_pagamento == "approved":
        pagamento_aprovado(payment_id)

    elif status_pagamento == "pending":
        pagamento_pendente(payment_id)

    elif status_pagamento == "rejected":
        pagamento_rejeitado(payment_id)

    else:
        print(f"Status não tratado: {status_pagamento}")


def pagamento_aprovado(payment_id):

    print(" PAGAMENTO APROVADO")
    print(f"Pedido pago: {payment_id}")

    # exemplo:
    # atualizar banco
    # liberar produto
    # enviar email


def pagamento_pendente(payment_id):

    print("⏳ PAGAMENTO PENDENTE")
    print(f"Aguardando pagamento: {payment_id}")


def pagamento_rejeitado(payment_id):

    print(" PAGAMENTO REJEITADO")
    print(f"Pagamento recusado: {payment_id}")

def processar_merchant_order(dados):

    print("\n=== MERCHANT ORDER ===")
    print(dados)

    merchant_order_url = dados.get("resource")

    if not merchant_order_url:
        print("Sem resource")
        return

    merchant_order_id = merchant_order_url.split("/")[-1]

    print("\nMERCHANT ORDER ID:", merchant_order_id)

    merchant_order = SDK.merchant_order().get(merchant_order_id)

    if merchant_order["status"] != 200:
        print("Merchant order não encontrada")
        return

    response = merchant_order["response"]

    pagamentos = response.get("payments", [])

    print("\nPAGAMENTOS:", pagamentos)

    if not pagamentos:
        print("Sem pagamentos")
        return

    payment_id = pagamentos[0]["id"]

    print("\nPAYMENT ID:", payment_id)

    pagamento = SDK.payment().get(payment_id)

    status_pagamento = pagamento["response"]["status"]

    print("STATUS PAGAMENTO:", status_pagamento)

    if status_pagamento == "approved":
        pagamento_aprovado(payment_id)

    elif status_pagamento == "pending":
        pagamento_pendente(payment_id)

    elif status_pagamento == "rejected":
        pagamento_rejeitado(payment_id)