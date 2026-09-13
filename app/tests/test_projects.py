from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Aurex Backend is running"

def test_create_project():
    response = client.post(
        "/projects/",
        json={
            "name": "Automated Test Project",
            "description": "Created during backend testing",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 100000,
            "progress_percentage": 50,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Automated Test Project"
    assert data["budget"] == 1000000
    assert data["progress_percentage"] == 50
    assert "risk_score" in data
    assert "risk_level" in data

def test_create_project_invalid_budget():
    response = client.post(
        "/projects/",
        json={
            "name": "Invalid Budget Project",
            "description": "Testing budget validation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 0,
            "expenditure": 0,
            "progress_percentage": 50,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert response.status_code == 422

def test_create_project_invalid_progress():
    response = client.post(
        "/projects/",
        json={
            "name": "Invalid Progress Project",
            "description": "Testing progress validation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 101,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert response.status_code == 422

def test_create_project_negative_progress():
    response = client.post(
        "/projects/",
        json={
            "name": "Negative Progress Project",
            "description": "Testing negative progress validation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": -1,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert response.status_code == 422

def test_get_nonexistent_project():
    response = client.get("/projects/999999")

    assert response.status_code == 404

def test_create_financial_record():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Financial Test Project",
            "description": "Created for financial API testing",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 50,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project = project_response.json()
    project_id = project["id"]

    response = client.post(
        f"/projects/{project_id}/financial",
        json={
            "record_date": "2026-09-09",
            "expenditure": "50000.00",
            "funding_received": "100000.00",
            "description": "Automated financial test"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == project_id
    assert data["expenditure"] == "50000.00"
    assert data["funding_received"] == "100000.00"

def test_create_financial_record_negative_expenditure():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Negative Financial Test",
            "description": "Testing financial validation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 50,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/financial",
        json={
            "record_date": "2026-09-09",
            "expenditure": "-50000.00",
            "funding_received": "100000.00",
            "description": "Invalid negative expenditure"
        }
    )

    assert response.status_code == 422

def test_create_financial_record_negative_funding():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Negative Funding Test",
            "description": "Testing funding validation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 50,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/financial",
        json={
            "record_date": "2026-09-09",
            "expenditure": "50000.00",
            "funding_received": "-100000.00",
            "description": "Invalid negative funding"
        }
    )

    assert response.status_code == 422

def test_create_progress_record():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Progress Test Project",
            "description": "Testing progress API",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 0,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/progress",
        json={
            "record_date": "2026-09-09",
            "progress_percentage": 50,
            "remarks": "Automated progress test"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == project_id
    assert data["progress_percentage"] == 50
    assert data["remarks"] == "Automated progress test"

def test_progress_updates_project_risk():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Risk Update Test Project",
            "description": "Testing risk recalculation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 850000,
            "progress_percentage": 50,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    progress_response = client.post(
        f"/projects/{project_id}/progress",
        json={
            "record_date": "2026-09-09",
            "progress_percentage": 20,
            "remarks": "Progress dropped for risk test"
        }
    )

    assert progress_response.status_code == 200

    updated_project = client.get(
        f"/projects/{project_id}"
    )

    assert updated_project.status_code == 200

    data = updated_project.json()

    assert data["progress_percentage"] == 20
    assert data["risk_score"] == 45
    assert data["risk_level"] == "MEDIUM"

def test_create_milestone():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Milestone Test Project",
            "description": "Testing milestone API",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 20,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/milestones",
        json={
            "name": "Foundation Complete",
            "planned_date": "2026-10-15",
            "status": "PENDING",
            "description": "Foundation work milestone"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["project_id"] == project_id
    assert data["name"] == "Foundation Complete"
    assert data["status"] == "PENDING"

def test_create_milestone_invalid_status():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Invalid Milestone Test",
            "description": "Testing milestone status validation",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 20,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/milestones",
        json={
            "name": "Invalid Status Milestone",
            "planned_date": "2026-10-15",
            "status": "INVALID_STATUS",
            "description": "This should be rejected"
        }
    )

    assert response.status_code == 422

def test_create_progress_at_100_percent():
    project_response = client.post(
        "/projects/",
        json={
            "name": "Full Progress Test",
            "description": "Testing 100 percent progress",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 0,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/progress",
        json={
            "record_date": "2026-09-09",
            "progress_percentage": 100,
            "remarks": "Project completed"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["progress_percentage"] == 100

def test_create_financial_record_for_nonexistent_project():
    response = client.post(
        "/projects/999999/financial",
        json={
            "record_date": "2026-09-09",
            "expenditure": "50000.00",
            "funding_received": "100000.00",
            "description": "Should fail because project does not exist"
        }
    )

    assert response.status_code == 404

def test_create_progress_record_for_nonexistent_project():
    response = client.post(
        "/projects/999999/progress",
        json={
            "record_date": "2026-09-09",
            "progress_percentage": 50,
            "remarks": "Should fail because project does not exist"
        }
    )

    assert response.status_code == 404

def test_create_milestone_for_nonexistent_project():
    response = client.post(
        "/projects/999999/milestones",
        json={
            "name": "Should Not Exist",
            "planned_date": "2026-10-15",
            "status": "PENDING",
            "description": "Should fail because project does not exist"
        }
    )

    assert response.status_code == 404

def test_create_project_with_minimum_budget():
    response = client.post(
        "/projects/",
        json={
            "name": "Minimum Budget Project",
            "description": "Testing minimum valid budget",
            "department": "Test Department",
            "location": "Test Location",
            "budget": 0.01,
            "expenditure": 0,
            "progress_percentage": 0,
            "planned_completion_date": "2027-12-31"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["budget"] == 0.01
    

def test_list_financial_records(client):
    project_response = client.post(
        "/projects/",
        json={
            "name": "Financial History Project",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 50
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    first_record = client.post(
        f"/projects/{project_id}/financial",
        json={
            "record_date": "2026-09-01",
            "expenditure": "100000.00",
            "funding_received": "200000.00",
            "description": "First financial entry"
        }
    )

    assert first_record.status_code == 200

    second_record = client.post(
        f"/projects/{project_id}/financial",
        json={
            "record_date": "2026-09-10",
            "expenditure": "150000.00",
            "funding_received": "250000.00",
            "description": "Latest financial entry"
        }
    )

    assert second_record.status_code == 200

    response = client.get(
        f"/projects/{project_id}/financial"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["record_date"] == "2026-09-10"
    assert data[1]["record_date"] == "2026-09-01"

def test_list_progress_records(client):
    project_response = client.post(
        "/projects/",
        json={
            "name": "Progress History Project",
            "budget": 1000000,
            "expenditure": 0,
            "progress_percentage": 0
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    first_record = client.post(
        f"/projects/{project_id}/progress",
        json={
            "record_date": "2026-09-01",
            "progress_percentage": 10,
            "remarks": "Initial progress"
        }
    )

    assert first_record.status_code == 200

    second_record = client.post(
        f"/projects/{project_id}/progress",
        json={
            "record_date": "2026-09-10",
            "progress_percentage": 25,
            "remarks": "Latest progress"
        }
    )

    assert second_record.status_code == 200

    response = client.get(
        f"/projects/{project_id}/progress"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["record_date"] == "2026-09-10"
    assert data[0]["progress_percentage"] == 25
    assert data[1]["record_date"] == "2026-09-01"
    assert data[1]["progress_percentage"] == 10