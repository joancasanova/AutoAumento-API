# tests/test_setups.py

def test_setups_flow(client):
    # Creación de un setup
    setup_name = "test_setup"
    payload = {
        "model": "EleutherAI/gpt-neo-125M",
        "generation_prompts": {"system_prompt":"You are a teacher.","user_prompt":"Explain gravity"},
        "verification_prompts": [],
        "reference_data": []
    }

    # Guardar el setup
    response = client.post(f"/setups/{setup_name}", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "saved"

    # Listar setups
    response = client.get("/setups/")
    assert response.status_code == 200
    data = response.json()
    assert "setups" in data
    assert setup_name in data["setups"]

    # Obtener setup guardado
    response = client.get(f"/setups/{setup_name}")
    assert response.status_code == 200
    data = response.json()
    assert data["model"] == "EleutherAI/gpt-neo-125M"

    # Eliminar setup
    response = client.delete(f"/setups/{setup_name}")
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
