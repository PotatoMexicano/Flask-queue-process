import time
import uuid
from concurrent.futures import ThreadPoolExecutor
import threading

import jsonschema
from flask import Flask, jsonify, request
from jsonschema import validate

from queue_tool.model import Job
from queue_tool.database import create_db


pool = ThreadPoolExecutor(max_workers=12)
lock = threading.Lock()

def create_app():
    
    app = Flask(__name__)

    @app.cli.command('create-db')
    def cli_command_create_db() -> None:
        with lock:  
            create_db()
        print('Database created !')

    @app.route('/check/<hash>')
    def check_hash_status(hash: str):
        with lock:
            job = Job.select(hash=hash)
        
        if job is None:
            return jsonify({"message": "Job not found"}), 404

        return jsonify({"messaage": job.status}), 200

    @app.route('/api', methods=['POST'])
    def process_request():
        data = request.get_json()
        hash_queue = []

        for index, item in enumerate(data):

            if validate_item(item):

                hash_de_execucao = uuid.uuid4().hex

                item['hash'] = hash_de_execucao
                job = Job(item)

                with lock:
                    job.create()

                hash_queue.append({
                    "hash": hash_de_execucao,
                    "item": job.item,
                    "index": index
                })

                pool.submit(process_item, job)
                
            else:

                hash_queue.append({
                    "hash": "INVALID_JOB_REQUEST",
                    "item": item['item'],
                    "index": index
                })

        return jsonify({
            'message': 'Itens recebidos para processamento',
            'processing_items': hash_queue
        })

    def process_item(item: Job):
        time.sleep(item.valor)
        
        with lock:
            item = item.update()

        print(f"Finished: ", item.as_dict(), f'in {item.duration} seconds.')


    def validate_item(data) -> bool:
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
