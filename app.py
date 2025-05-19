@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Dados recebidos do Z-API:", data)

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
        print("📤 Enviando resposta para número:", numero)
        print("📨 Conteúdo da mensagem:", resposta)

        r = requests.post(ZAPI_URL, json=payload, headers=HEADERS)
        print("✅ Retorno da Z-API:", r.status_code, r.text)

    return jsonify({"status": "ok"})
