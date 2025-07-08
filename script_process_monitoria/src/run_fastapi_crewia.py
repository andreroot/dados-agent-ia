import requests

url = "http://localhost:8000/executar-crew-data/"
params = {}  # ou outro valor conforme necessário

response = requests.post(url, data={"nome": "processos_error", "pergunta": "quantos processos estão com erros?"})

if response.ok:
    print("Resposta da API:", response.json())
else:
    print("Erro ao acessar a API:", response.status_code, response.text)

# curl -X POST "http://localhost:8000/executar-crew?nome=processos_error" -H "Content-Type: application/json" -d '{"pergunta": "quantos processos estão com erros"}'