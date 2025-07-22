import pytest
import requests
import logging
import json
import pdb
from config import BASE_URL

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Cargar un estudiante desde el JSON
with open("tests/students.json", encoding="utf-8") as f:
    students = json.load(f)

student_data = students[0]  # Tomamos solo el primero para este flujo

@pytest.mark.dependency()
def test_create_student():
    """
    Paso 1: Crear un estudiante.
    Guarda el student_id para los siguientes pasos.
    """
    response = requests.post(BASE_URL, json=student_data)
    assert response.status_code == 201, f"POST failed: {response.status_code}"

    student = response.json()
    pytest.student_id = student["id"]
    logger.info(f"✅ Created student {pytest.student_id}")

@pytest.mark.dependency(depends=["test_create_student"])
def test_validate_student():
    """
    Paso 2: Validar que el estudiante existe y los datos son correctos.
    """
    response = requests.get(f"{BASE_URL}/{pytest.student_id}")
    assert response.status_code == 200, f"GET failed: {response.status_code}"

    student_fetched = response.json()
    logger.info(f"📄 Student fetched: {student_fetched}")
    print(">>> student_fetched:", student_fetched)

    # Validar claves presentes
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

    logger.info(f"🔎 Validated student {pytest.student_id} data.")

@pytest.mark.dependency(depends=["test_create_student", "test_validate_student"])
def test_delete_student():
    """
    Paso 3: Eliminar el estudiante.
    """
    response = requests.delete(f"{BASE_URL}/{pytest.student_id}")
    assert response.status_code in [200, 204], f"DELETE failed: {response.status_code}"
    logger.info(f"🗑️ Deleted student {pytest.student_id}")

