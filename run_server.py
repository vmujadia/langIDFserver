import os
import time
from typing import Dict
from flask import request, jsonify, Flask
from load_models_langidentify import language_identify


class LocalFlask(Flask):

    def __init__(self, name):
        super().__init__(name)
        self.add_routes()

    def add_basic_routes(self):
        self.add_url_rule('/', 'index', self.index)
        self.add_url_rule('/health', 'health', self.health)
        self.add_url_rule('/readiness', 'readiness', self.readiness_check)
        self.add_url_rule('/liveness', 'liveness', self.liveness_check)
        self.add_url_rule('/status', 'status', self.status)

    def index(self):
        return 'Welcome to oneMT Server : ' + self.name

    @staticmethod
    def health():
        return jsonify(['ok'])

    # pylint: disable=no-self-use
    def liveness_check(self):
        return jsonify(['ok'])

    def readiness_check(self):
        if self.is_ready():
            return '', 204
        return jsonify(self.get_status()), 503

    def status(self):
        return jsonify(self.get_status())

    # pylint: disable=no-self-use
    def get_status(self) -> Dict[str, str]:
        return {}

    def is_ready(self) -> bool:
        return True

    def add_routes(self):
        self.add_basic_routes()
        self.add_url_rule('/langidentify', 'langidentify', self.langidentify, methods=["POST"])

    def error_models(self) -> Dict[str, str]:
        return {'error': 'models are not present'}

    def error(self, error_message) -> Dict[str, str]:
        return {'error': error_message}

    def langidentify(self):
        start_time = time.time()
        request_json = request.json or {}
        text = request_json.get('text') or request_json.get('input')
        out = {}
        print("incoming request : %s", request_json)
        if not text:
            print('text not specified: %s', request_json)
            return self.error('text not specified , mode can be _____'), 400
        out["output"]=[]
        if type(text)==list:
            for inst in text:
                response, score = language_identify(inst["source"])
                out['output'].append({
                        "source":inst["source"],
                        "langPrediction":[{"langCode" : response, "langScore" : score }]
                })
        print("Response:: %s", out)
        return jsonify(out), 200


app = LocalFlask(__name__)
print('** Initialization complete.')
