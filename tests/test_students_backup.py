import pytest
import requests
import json
import logging
from config import BASE_URL

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cargar datos desde students.json
with open("tests/students.json", encoding="utf-8") as f:
    students = json.load(f)

@pytest.mark.parametrize("student_data", students)
def test_create_and_validate_student(student_data):
    """
    Test que valida la creación y eliminación de estudiantes con datos de JSON.
    """
    # POST
    response = requests.post(f"{BASE_URL}", json=student_data)
    assert response.status_code == 201, f"POST failed: {response.status_code}"
    student = response.json()
    student_id = student["id"]
    logger.info(f"✅ Created student {student_id}")

    # (Opcional: aquí podrías hacer GET para validar datos)

    # DELETE
    del_response = requests.delete(f"{BASE_URL}/{student_id}")
    assert del_response.status_code in [200, 204]


