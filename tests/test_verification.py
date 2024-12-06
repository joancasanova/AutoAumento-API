# tests/test_verification.py

def test_verification_endpoint(client):
    # Suponiendo un resultado generado previamente.
    generated_results = [
        {"input":"example_input","output":"This is a generated text about the sky"}
    ]

    verification_prompts = [
        {
            "name": "embedding",
            "context": "You are a verifier.",
            "instruction": "Check if '{input}' and '{output}' are similar.",
            "num_return_sequences":1,
            "max_new_tokens":50,
            "num_positive":1,
            "positive_responses":["Sí","sí","yes"]
        }
    ]

    payload = {
        "verification_prompts": verification_prompts,
        "generated_results": generated_results
    }

    response = client.post("/verification/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert "verification_status" in data["results"][0]
    # No podemos asegurar si será confirmada, a revisar o fallido, ya que depende de la lógica y el modelo.
    # Al menos verificamos que el campo exista.
