import os
import mercadopago
from dotenv import load_dotenv

load_dotenv()

MERCADO_PAGO_TOKEN = os.getenv(
    "MERCADO_PAGO_TOKEN"
)

WEBHOOK_SECRET = os.getenv(
    "WEBHOOK_SECRET"
)

SDK = mercadopago.SDK(
    MERCADO_PAGO_TOKEN
)