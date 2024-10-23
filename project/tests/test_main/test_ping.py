def test_ping(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Aquesa Launch App APIs",
        "environment": "testing",
        "testing": True,
    }
