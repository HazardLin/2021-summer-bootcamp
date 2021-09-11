from flask import Flask
from flask import request
import pandas as pd

app = Flask(__name__)
DATA_FILE_NAME = "client_rate.json"


@app.route("/")
def default():
    return "FIRST PROJECT - we have " + str(len(get_client_rates())) + " clients in total."


def get_client_rates():
    df = pd.read_json(DATA_FILE_NAME)
    return df.to_dict()


@app.route("/rate/<client_id>")
def get_client_rate(client_id) -> str:
    rates = get_client_rates()
    if client_id in rates:
        return str(rates[client_id]["rate"])
    return "0"


@app.route("/rate", methods=['POST'])
def upsert_client_rate() -> str:
    param = request.get_json()
    client_id = param['client_id']
    rate = param['rate']

    update_client_rates(client_id, rate)
    return str(param)


def update_client_rates(client_id: str, rate: float) -> None:
    """
    update or insert a client_id - rate pair.

    :param client_id: string, e.g. 'client1'
    :param rate: float, e.g. 0.1
    :return:
    """
    rates = get_client_rates()
    rates[client_id] = {"rate": rate}
    df = pd.DataFrame.from_dict(rates)
    df.to_json(DATA_FILE_NAME)


if __name__ == "__main__":
    app.run()
