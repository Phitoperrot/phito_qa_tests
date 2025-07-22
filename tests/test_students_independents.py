
import pytest
import requests
import json
import logging
import pdb
from config import BASE_URL

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cargar estudiantes desde el JSON dinámico
with open("tests/students.json", encoding="utf-8") as f:
    students = json.load(f)

@pytest.mark.parametrize("student_data", students)
def test_independent_student_flow(student_data):
    """
    Test independiente y parametrizado:
    - Usa datos dinámicos de students.json
    - Hace POST → GET → DELETE por cada estudiante
    - Totalmente independiente y paralelizable
    """
    # POST
    response = requests.post(BASE_URL, json=student_data)
    assert response.status_code == 201, f"POST failed: {response.status_code}"
    student = response.json()
    student_id = student.get("id")
    logger.info(f"✅ Created student {student_id}")

    # PUNTO DE DEBUG
    ##pdb.set_trace()

    # GET
    response = requests.get(f"{BASE_URL}/{student_id}")
    assert response.status_code == 200, f"GET failed: {response.status_code}"
    student_fetched = response.json()
    logger.info(f"📄 Student fetched: {student_fetched}")
    print(f">>> student_fetched: {student_fetched}")

    # Validar datos
    mismatches = []
    for key, expected_value in student_data.items():
        fetched_value = student_fetched.get(key, None)
        if fetched_value is None:
            logger.warning(f"⚠️ Key '{key}' not found in fetched data.")
        else:
            if fetched_value != expected_value:
                mismatches.append(f"Mismatch in {key}: expected '{expected_value}', got '{fetched_value}'")

    if mismatches:
        pytest.fail(";\n".join(mismatches))

    # DELETE
    del_response = requests.delete(f"{BASE_URL}/{student_id}")
    assert del_response.status_code in [200, 204], f"DELETE failed: {del_response.status_code}"
    logger.info(f"🗑️ Deleted student {student_id}")

