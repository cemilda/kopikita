import shutil

import pytest

from app import app as flask_app
from db import init_db


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"
    invoice_dir = tmp_path / "invoices"
    shutil.copytree(flask_app.config["INVOICE_DIR"], invoice_dir)
    flask_app.config.update(TESTING=True, DATABASE=str(db_path), INVOICE_DIR=str(invoice_dir))
    init_db(str(db_path))
    with flask_app.test_client() as c:
        yield c


def login(client, username, password):
    resp = client.post("/login", json={"username": username, "password": password})
    assert resp.status_code == 200, resp.get_json()
    return resp.get_json()["auth"]["token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}
