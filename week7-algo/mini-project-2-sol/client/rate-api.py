import requests


def get_rate(client_id: str) -> float:
    response = requests.get("http://127.0.0.1:5000/rate/" + client_id)
    return float(response.content)


def upsert_client_rate(client_id: str, rate: float) -> str:
    response = requests.post("http://127.0.0.1:5000/rate",
                             json={"client_id": client_id, "rate": rate})
    return str(response.content)


# -----------------------Here are tests for API ------------------------
def test_get_rate():
    assert get_rate('client2') == 0.1
    assert get_rate('client-2') == 0.0


def test_upsert_rate():
    upsert_client_rate("client1", 0.5)
    assert get_rate('client1') == 0.5

    upsert_client_rate('client-1', 0.8)
    assert get_rate('client-1') == 0.8


if __name__ == '__main__':
    test_get_rate()
    test_upsert_rate()
