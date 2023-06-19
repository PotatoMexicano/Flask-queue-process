from flask import Flask, jsonify, request
from concurrent.futures import ThreadPoolExecutor
import time
import uuid
import jsonschema
from jsonschema import validate

app = Flask(__name__)
pool = ThreadPoolExecutor(max_workers=12)
processed_itens = {}

INVALID_JOB: dict = {'item': 'INVALID_JOB_REQUEST', 'valor': 0}

class Job:

    item: str = None
    valor: int = None
    hash: str = None
    validade: bool = False
    status: bool = False

    def __init__(self, data):

        if (validade := self.valida_data(data=data)) is False:
            return Job(INVALID_JOB)

        self.validade = validade

        self.item = data['item']
        self.valor = data['valor']
        self.hash = data['hash']
        self.status = 'Em processamento'

    def __str__(self) -> str:
        return str(self.item)

    def __repr__(self) -> str:
        return f"Job(item='{self.item}')"

    def __bool__(self) -> bool:
        if not isinstance(self, Job):
            return False

        if not hasattr(self, 'item'):
            return False

        if not hasattr(self, 'valor'):
            return False

        if not hasattr(self, 'hash'):
            return False

        if not hasattr(self, 'validade'):
            return False

        if not hasattr(self, 'status'):
            return False

        return True

    def as_dict(self) -> dict:
        return {
            'item': self.item,
            'valor': self.valor,
            'validade': self.validade,
            'status': self.status,
        }

    def valida_data(self, data) -> bool:
        if not isinstance(data, dict):
            return False

        if not 'item' in data:
            return False

        if not 'valor' in data:
            return False

        if not 'hash' in data:
            return False

        return True

def process_item(item: Job):
    time.sleep(item.valor)
    item.status = 'finalizado'

    processed_itens[item.hash] = item
    print(f"Processado: ", item.as_dict())

    return item.__dict__

def validate_data(data) -> bool:
    schema = {
        "type": "object",
        "properties": {
            "item": {"type": "string"},
            "valor": {"type": "number"}
        },
        "required": ["item", "valor"]
    }

    try:
        validate(data, schema)
        return True
    except jsonschema.ValidationError as err:
        return False

@app.route('/check/<hash>')
def check_hash_status(hash: str):
    if hash in processed_itens:
        return jsonify({'message': 'Finalizado'})
    else:
        return jsonify({'message': 'Em processamento'})

@app.route('/api', methods=['POST'])
def process_request():
    data = request.get_json()
    hash_queue = []
    results = []

    for index, item in enumerate(data):
        if validate_data(item):
            hash_de_execucao = uuid.uuid4().hex
            item['hash'] = hash_de_execucao
            job = Job(item)

            hash_queue.append({"hash": hash_de_execucao, "item": job.item, "index": index})
            results.append(pool.submit(process_item, job))
        else:
            hash_queue.append({"hash": "INVALID_JOB_REQUEST", "item": item['item'], "index": index})

    # processed_items = [result.result() for result in results]
    return jsonify({'message': 'Itens recebidos para processamento', 'processing_items': hash_queue})

if __name__ == '__main__':

    app.run(debug=True)
