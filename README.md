# blablabla

roda `server.py` e acessa criando uma instância de API de `api.py`

---

## exemplo de uso com servidor já rodando e [visível para internet](https://ngrok.com/download):
```
$ python3 -i api.py
>>> my_api = API('SUA KEY AQUI', 'URL DO SEU SERVIDOR AQUI')
>>> my_api.denoise('ARQUIVO DE SOM AQUI')
>>> my_api.denoise('OUTRO ARQUIVO OU NAO', emotion=True)
>>> my_api.get_emotion('ALGUM ARQUIVO')
```

---

## métodos da classe API:
### `denoise`
#### parâmetros
- `AUDIO_PATH` (obrigatório): caminho do arquivo de som.
- `emotion`: booleano, se True irá analisar a emoção no arquivo denoised.

### `get_emotion`
#### parâmetros
- `AUDIO_PATH` (obrigatório): caminho do arquivo de som.

---

## usando ngrok e tornando seu servidor visível para a internet
```
$ ngrok http <porta>
```
a execução acima gerará um *NGROK_URL*, pega ele e usa no parâmetro `-u` de `server.py`. A *NGROK_URL* vai parecer algo como: `https://fb3204bd.ngrok.io`. O default do servidor é a porta 8081, mas o argumento opcional `--port` ou `-p` pode ser utilizado para setar uma porta qualquer.
```
$ server.py -k API_KEY -u NGROK_URL [-p <porta>]
```
