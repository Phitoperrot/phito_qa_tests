import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
import requests
import logging
from config import BASE_URL

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@pytest.fixture
def create_and_cleanup_student():
    """
    Fixture: crea un estudiante antes del test y lo elimina después.
    Devuelve student_id y student_data.
    """
    student_data = {
        "first_name": "John",
        "middle_name": "Michael",
        "last_name": "Doe",
        "date_of_birth": "2000-01-01"
    }

    # setup → POST
    post_response = requests.post(BASE_URL, json=student_data)
    assert post_response.status_code == 201, f"POST failed: {post_response.status_code}"

    post_json = post_response.json()
    student_id = post_json["id"]
    logger.info(f"✅ Student created with id: {student_id}")

    yield student_id, student_data  # pasa el control al test

    # teardown → DELETE
    del_response = requests.delete(f"{BASE_URL}/{student_id}")
    assert del_response.status_code in [200, 204], f"DELETE failed: {del_response.status_code}"
    logger.info(f"🧹 Student {student_id} deleted after test.")