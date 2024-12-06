# tests/test_generation.py

def test_generation_endpoint(client):
    payload = {
        "system_prompt": "You are a helpful assistant.",
        "user_prompt": "Write a short poem about the sky",
        "num_return_sequences": 1,
        "max_new_tokens": 50,
        "num_executions": 1
    }
    response = client.post("/generation/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    # Verificamos que hay al menos un resultado con "input" y "output"
    assert "input" in data["results"][0]
    assert "output" in data["results"][0]
