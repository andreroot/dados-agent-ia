import requests

url = "http://172.16.128.133:5678/webhook/trigger_erros_operacionais"

params = {"processo": "insert_particularidade"}

headers = {"Content-Type": "application/json"}

data = {
    "chatId": "5511961594822@c.us",
    "mensagem": "Agent, inserir essas infromações na particularidade",
    "particularidade": {
        "msg_particularidade": "via teams Luis - 11/07",
        "data_particularidade": "2025-07-11",
        "alerta": "erros_boleta_inflacao_futuro",
        "boleta": "IC-VC252-25",
        "operador": "Rafael Campos"
    }
}

response = requests.post(url, params=params, headers=headers, json=data   )

if response.ok:
    print("Resposta da API:", response.json())
else:
    print("Erro ao acessar a API:", response.status_code, response.text)

# curl -X POST "http://localhost:8000/executar-crew?nome=processos_error" -H "Content-Type: application/json" -d '{"pergunta": "quantos processos estão com erros"}'

# curl -X POST 'http://172.16.128.133:5678/webhook/trigger_erros_operacionais??processo=inconsistencia_resultado' \
# -H "Content-Type: application/json" \
# -d '{"chatId": "5511961594822@c.us","mensagem": "Agent, enviar essas informações sobre alerta do portifolio"}'

# curl -X POST 'http://172.16.128.133:5678/webhook/trigger_erros_operacionais?processo=inconsistencia_posicao' -H "Content-Type: application/json" -d '{"chatId": "5511961594822@c.us","mensagem": "Agent, enviar informações sobre portifolio"}'

#curl -X POST 'http://172.16.128.133:5678/webhook/trigger_erros_operacionais?processo=insert_particularidade' -H "Content-Type: application/json"  -d '{"chatId": "5511940147165@c.us","mensagem": "Agent, inserir essas infromações na particularidade","particularidade":{ "msg_particularidade":"via teams Luis - 11/07","data_particularidade":"2025-07-11","alerta":"erros_boleta_inflacao_futuro","boleta":"IC-CC366-25","operador":"Rafael Campos"}}'