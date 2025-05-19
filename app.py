from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Substitua pelos seus dados reais
ZAPI_URL = "https://api.z-api.io/instances/3E1664822BF440DCF6C9FE99C2B48794/token/3E6D6FDD5AF8252B380DACA8/send-text"
CLIENT_TOKEN = "F466390c69345429ba80cec680a7f5987S"
SUPORTE_NUMERO = "5519993203350"  # número de suporte no formato internacional

HEADERS = {
    "Content-Type": "application/json",
    "Client-Token": CLIENT_TOKEN
}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Recebido:", data)

    numero = data.get("message", {}).get("phone")
    texto = data.get("message", {}).get("text", "").strip().lower()

    if numero and texto:
        if texto in ["1", "sim"]:
            resposta = "✅ Agradecemos seu retorno! Qualquer dúvida, estamos à disposição."
        elif texto in ["2", "não", "nao"]:
            resposta = f"⚠️ Sentimos muito! Encaminhando você ao suporte: https://wa.me/{SUPORTE_NUMERO}"
        else:
            resposta = "🤖 Por favor, responda com:\n1️⃣ - Sim\n2️⃣ - Não"

        payload = {"phone": numero, "message": resposta}
        r = requests.post(ZAPI_URL, json=payload, headers=HEADERS)
        print("Resposta enviada:", r.json())

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run()
