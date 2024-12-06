# tests/test_domain.py
from app.domain.services.verifier_service import VerifierService

def test_verifier_service_embedding():
    vs = VerifierService(threshold=0.9, upper_threshold=0.995)
    # Caso: similarity baja
    assert vs.verify_embedding(0.5) == False
    # Caso: similarity entre threshold y upper_threshold
    assert vs.verify_embedding(0.95) == True
    # Caso: similarity muy alta
    assert vs.verify_embedding(0.999) == False

def test_verifier_service_consensus():
    vs = VerifierService()
    # Caso: respuestas positivas suficientes
    responses = ["Sí, está bien", "sí claro", "Yes indeed", "No", "Sí, seguro"]
    # De 5 respuestas, al menos 4 deben ser positivas (num_ok=4 por defecto)
    # Aquí tenemos 3 positivas seguras ("Sí, está bien","sí claro","Yes indeed") y 1 "Sí, seguro" = 4
    # => True
    assert vs.verify_consensus(responses) == True

    # Caso: no suficientes positivas
    responses = ["No", "No", "No", "Sí", "No"]
    # Solo 1 positiva, no llega a 4
    assert vs.verify_consensus(responses) == False
