def user_payload(
        uid=1,
        name="Cathal",
        email="cathal@atu.ie",
        age=25,
        student_id="s1234567",
):
    return{
        "userid": uid,
        "name": name,
        "email": email,
        "age": age,
        "student_id": student_id,
    }

def test_create_user_returns_201(client):
    response = client.post("/api/users", json=user_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["userid"] == 1
    assert data["name"] == "Cathal"
    assert data["email"] == "cathal@atu.ie"