# Flask Queue Tool

Projeto simples desenvolvido para mostrar o funcionamento de uma API que recebe solicitações de processamento e gera tokens para que o solicitante acompanhe o processo de desenvolvimento da sua solicitação.

Para a construção deste projeto foram utilizados no back-end Python como base e Flask como framework responsável por criar a API de comunicação.

## Enviando requisição

\[ POST ]: `/api`

O sistema recebe um JSON no seguinte formato:

```json
[
    {
        "item": "item01",
        "valor": 10
    },
    {
        ...
    }
]
```
O valor é o custo de processamento do sistema, que nesta primeira versão é apenas simulada através de uma pausa de x segundos, onde x é o valor fornecido a API.

## Acompanhamento

\[ GET ]: `/check/{token}`

O usuário ao realizar a requisição, recebe alguns tokens de retorno, para acompanhar o processamento:

```json
{
    "message": "Itens recebidos para processamento",
    "processing_items": [
        {
            "hash": "INVALID_JOB_REQUEST",
            "index": 0,
            "item": "Teste1"
        },
        {
            "hash": "58c1d7e392964c12a3378b81ba69d255",
            "index": 1,
            "item": "Teste2"
        }
    ]
}
```

Caso o usuário, envie valores do tipo incorretos, será processado por um JSON schema, e retornará ao usuário a mensagem `INVALID_JOB_REQUEST` para o item que houve o erro de envio dos dados.

Para os dados corretos, o processamento segue normalmente.


Ao consultar o status do envio, será retornado duas possibilidades:

```json
{ "message": "Finalizado"}
```
ou então
```json
{ "message": "Em processamento"}
```

Assim que uma tarefa é concluida, ela é removida da lista de tarefas em execução, liberando espaço em memória.

## Deploy

Para realizar o deploy, basta clonar o repositório em sua maquina.
Em seguinda, entre na pasta do projeto e rode o seguinte comando em um terminal.

```
poetry install
```
Após o ambiente virtual ser criado, inicie utilizando `poetry shell`.

Para iniciar o serviço, prossiga com o comando `flask --app queue_tool run`.

* Caso deseje rodar em modo debug utilize `--debug`.

* Caso precise externalizar a aplicação para toda sua rede, utilize `--host 0.0.0.0`.

* Caso necessite de uma porta customizada, adicione `--port 80`.

## Pontos de melhoria futuro

* Adição de novas situações para os jobs.
* Adição de um banco de dados para armazenar os jobs concluidos.
* Testes unitários.
