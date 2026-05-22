from config import SDK


def criar_preferencia(nome, valor):

    preference_data = {
        "items": [
            {
                "title": nome,
                "quantity": 1,
                "unit_price": float(valor)
            }
        ],
        "notification_url":
        "https://evolve-outback-mongoose.ngrok-free.dev/webhook"
    }

    preference_response = SDK.preference().create(
        preference_data
    )

    return preference_response["response"]["init_point"]