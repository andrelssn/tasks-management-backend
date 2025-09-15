def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_crud_workflow(client):
    # create
    r = client.post("/tasks", json={"title": "Tarefa 1", "description": "desc"})
    assert r.status_code == 201
    data = r.json()
    task_id = data["id"]
    assert data["title"] == "Tarefa 1"

    # list
    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # get
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 200
    assert r.json()["id"] == task_id

    # update
    r = client.put(f"/tasks/{task_id}", json={"title": "Tarefa 1 - editada"})
    assert r.status_code == 200
    assert r.json()["title"] == "Tarefa 1 - editada"

    # delete
    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204

    # verify deleted
    r = client.get(f"/tasks/{task_id}")
    assert r.status_code == 404
