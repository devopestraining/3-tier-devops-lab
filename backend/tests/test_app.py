import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import app


def test_home():
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/")

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.data.decode())

    assert response.status_code == 200


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200


#def test_db_test():
 #   client = app.test_client()

  #  response = client.get("/db-test")

   # assert response.status_code in [200, 500]
