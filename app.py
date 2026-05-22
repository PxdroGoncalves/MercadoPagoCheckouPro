from flask import Flask, request, jsonify , render_template
from service import criar_preferencia
from webhook_service import (
    processar_webhook,
    validar_assinatura,
    processar_merchant_order
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "index.html"
    )


@app.route("/pagamento", methods=["POST"])
def pagamento():

    data = request.json

    link = criar_preferencia(
        data["nome"],
        data["valor"]
    )

    return jsonify({
        "checkout_url": link
    })


@app.route("/webhook", methods=["POST"])
def webhook():

    dados = request.json

    print("\nWEBHOOK RECEBIDO:")
    print(dados)

    topic = request.args.get("topic")

    # merchant order
    if topic == "merchant_order":
        processar_merchant_order(
            dados
        )

        return jsonify({
            "status": "merchant order recebida"
        }), 200

    assinatura_valida = validar_assinatura(
        request
    )

    if not assinatura_valida:
        return jsonify({
            "erro": "assinatura inválida"
        }), 401

    processar_webhook(dados)

    return jsonify({
        "status": "recebido"
    }), 200

if __name__ == "__main__":
    app.run(debug=True)