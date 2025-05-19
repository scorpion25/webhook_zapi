from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Dados reais
ZAPI_URL = "https://api.z-api.io/instances/3E1664822BF440DCF6C9FE99C2B48794/token/3E6D6FDD5AF8252B380DACA8/send-text"
CLIENT_TOKEN = "F466390c69345429ba80cec680a7f5987S"
SUPORTE_NUMERO = "5519993203350"

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

# Alteração necessária para rodar na Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
