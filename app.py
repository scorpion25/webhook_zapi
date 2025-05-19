from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Dados reais da Z-API
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
    print("📩 Dados recebidos do Z-API:", data, flush=True)

    numero = data.get("message", {}).get("phone")
    texto = data.get("message", "")

    print("🔎 Número recebido:", numero, flush=True)
    print("🔎 Texto recebido:", texto, flush=True)

    if numero and texto:
        texto = texto.strip().lower()

        if texto in ["1", "sim"]:
            resposta = "✅ Agradecemos seu retorno! Qualquer dúvida, estamos à disposição."
        elif texto in ["2", "não", "nao"]:
            resposta = f"⚠️ Sentimos muito! Encaminhando você ao suporte: https://wa.me/{SUPORTE_NUMERO}"
        else:
            resposta = "🤖 Por favor, responda com:\n1️⃣ - Sim\n2️⃣ - Não"

        payload = {"phone": numero, "message": resposta}
        print("📤 Enviando resposta para número:", numero, flush=True)
        print("📨 Conteúdo da mensagem:", resposta, flush=True)

        r = requests.post(ZAPI_URL, json=payload, headers=HEADERS)
        print("✅ Retorno da Z-API:", r.status_code, r.text, flush=True)
    else:
        print("⚠️ Número ou texto ausentes na mensagem recebida.", flush=True)

    return jsonify({"status": "ok"})

# Necessário para a Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
