"""Integration tests for the 5 PRD courses: MSME, Strategy Bridge, Data Hygiene, Conduct, Python."""

from datetime import datetime, timezone
import pytest

from quanta.db.models import Certificate, User
from quanta.domain.catalog import CATALOG


def test_catalog_contains_all_28_courses():
    course_ids = [c["id"] for c in CATALOG]
    assert len(course_ids) == 28
    assert "msme-financial-literacy" in course_ids
    assert "spreadsheet-to-strategy-lab" in course_ids
    assert "data-hygiene" in course_ids
    assert "conduct-compliance-essentials" in course_ids
    assert "python-reluctant-investor" in course_ids
    assert course_ids[0] == "trading-fundamentals"
    assert course_ids[-1] == "algorithm-evaluation"


def test_course_metadata_schema_fields():
    for course in CATALOG:
        assert course["slug"]
        assert course["title"]
        assert course["level"]
        assert isinstance(course["audience_tags"], list)
        assert isinstance(course["language"], list)
        assert "funnel_cta" in course
        assert course["funnel_cta"]["label"]
        assert course["funnel_cta"].get("target_course_id") or course["funnel_cta"].get("target_url")


def test_analytics_event_recording(client):
    res = client.post(
        "/api/v1/analytics/events",
        json={
            "event_type": "course_start",
            "course_id": "msme-financial-literacy",
            "session_id": "sess-test-123",
            "metadata": {"source": "direct_url"},
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["event_id"]

    query_res = client.get(
        "/api/v1/analytics/events?course_id=msme-financial-literacy&event_type=course_start"
    )
    assert query_res.status_code == 200
    events = query_res.json()["events"]
    assert len(events) >= 1
    assert events[0]["course_id"] == "msme-financial-literacy"


def test_msme_capstone_validation(client):
    valid_csv = """month,opening_balance,cash_inflows,cash_outflows,closing_balance
1,10000000,15000000,12000000,13000000
2,13000000,16000000,11000000,18000000
3,18000000,14000000,15000000,17000000
4,17000000,18000000,12000000,23000000
5,23000000,20000000,16000000,27000000
6,27000000,22000000,18000000,31000000
7,31000000,19000000,17000000,33000000
8,33000000,21000000,15000000,39000000
9,39000000,24000000,19000000,44000000
10,44000000,25000000,20000000,49000000
11,49000000,23000000,18000000,54000000
12,54000000,26000000,22000000,58000000"""

    res = client.post(
        "/api/v1/courses/msme-financial-literacy/capstone",
        json={"content": valid_csv},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "passed"

    # Test invalid: continuity break
    broken_continuity = valid_csv.replace("2,13000000", "2,99999999")
    res_err = client.post(
        "/api/v1/courses/msme-financial-literacy/capstone",
        json={"content": broken_continuity},
    )
    assert res_err.status_code == 422
    assert "continuity" in res_err.json()["detail"].lower()

    # Test invalid: only 5 rows instead of 12
    short_csv = "\n".join(valid_csv.splitlines()[:6])
    res_short = client.post(
        "/api/v1/courses/msme-financial-literacy/capstone",
        json={"content": short_csv},
    )
    assert res_short.status_code == 422
    assert "12 monthly rows" in res_short.json()["detail"]

    # Test Indonesian number formatting: Rp and dots as thousand separators
    idr_formatted_csv = valid_csv.replace("10000000", "Rp 10.000.000").replace("15000000", "15.000.000")
    res_idr = client.post(
        "/api/v1/courses/msme-financial-literacy/capstone",
        json={"content": idr_formatted_csv},
    )
    assert res_idr.status_code == 200
    assert res_idr.json()["status"] == "passed"

    # Test negative closing balance generates a cash-gap warning instead of hard rejection
    seasonal_gap_csv = """month,opening_balance,cash_inflows,cash_outflows,closing_balance
1,10000000,5000000,20000000,-5000000
2,-5000000,10000000,4000000,1000000
3,1000000,5000000,4000000,2000000
4,2000000,5000000,4000000,3000000
5,3000000,5000000,4000000,4000000
6,4000000,5000000,4000000,5000000
7,5000000,5000000,4000000,6000000
8,6000000,5000000,4000000,7000000
9,7000000,5000000,4000000,8000000
10,8000000,5000000,4000000,9000000
11,9000000,5000000,4000000,10000000
12,10000000,5000000,4000000,11000000"""
    res_gap = client.post(
        "/api/v1/courses/msme-financial-literacy/capstone",
        json={"content": seasonal_gap_csv},
    )
    assert res_gap.status_code == 200
    assert res_gap.json()["status"] == "passed"
    assert "cash gap" in res_gap.json()["message"].lower()


def test_data_hygiene_capstone_validation(client):
    clean_csv = """id,date,amount,currency,category
tx_001,2026-01-05,150000.00,IDR,Bahan Baku
tx_002,2026-01-06,200000.00,IDR,Operasional
tx_003,2026-01-07,50.00,USD,Langganan SaaS"""

    res = client.post(
        "/api/v1/courses/data-hygiene/capstone",
        json={"content": clean_csv},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "passed"

    # Test invalid: date ambiguity (04/05/2026)
    bad_date_csv = clean_csv.replace("2026-01-05", "04/05/2026")
    res_bad_date = client.post(
        "/api/v1/courses/data-hygiene/capstone",
        json={"content": bad_date_csv},
    )
    assert res_bad_date.status_code == 422
    assert "ISO-8601" in res_bad_date.json()["detail"]

    # Test invalid: uncleaned currency symbol in amount
    bad_curr_csv = clean_csv.replace("150000.00", "Rp 150.000")
    res_bad_curr = client.post(
        "/api/v1/courses/data-hygiene/capstone",
        json={"content": bad_curr_csv},
    )
    assert res_bad_curr.status_code == 422
    assert "currency symbol" in res_bad_curr.json()["detail"].lower()

    # Test invalid: category drift outside canonical taxonomy
    bad_cat_csv = clean_csv.replace("Operasional", "MarketingGimmick123")
    res_bad_cat = client.post(
        "/api/v1/courses/data-hygiene/capstone",
        json={"content": bad_cat_csv},
    )
    assert res_bad_cat.status_code == 422
    assert "canonical taxonomy" in res_bad_cat.json()["detail"]

    # Test invalid: duplicate composite key
    dup_csv = clean_csv + "\ntx_001,2026-01-05,999.00,IDR,Operasional"
    res_dup = client.post(
        "/api/v1/courses/data-hygiene/capstone",
        json={"content": dup_csv},
    )
    assert res_dup.status_code == 422
    assert "duplicate composite key" in res_dup.json()["detail"].lower()


def test_certificate_pdf_and_privacy(client):
    from quanta.db.session import engine
    from sqlmodel import Session
    from uuid import uuid4

    test_cert_id = f"QTA-{str(uuid4()).upper()}"
    with Session(engine) as session:
        user = User(
            id=str(uuid4()),
            email=f"compliance_{uuid4().hex[:6]}@example.com",
            name="Compliance Scholar",
            hashed_password="pw",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        cert = Certificate(
            id=test_cert_id,
            user_id=user.id,
            course_key="test-conduct-key",
            record={
                "id": test_cert_id,
                "trackId": "conduct-compliance-essentials",
                "courseTitle": "Conduct & Compliance Essentials",
                "recipientName": "Compliance Scholar",
                "issuedAt": datetime.now(timezone.utc).isoformat(),
                "studyMinutes": 420,
                "scoreBand": "Distinction",
                "contentVersion": 1,
                "publicVerificationOptOut": False,
                "lessonIds": [],
                "examVersions": {},
            },
        )
        session.add(cert)
        session.commit()

    # Test PDF generation
    pdf_res = client.get(f"/api/v1/certificates/{test_cert_id}/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert pdf_res.content.startswith(b"%PDF-1.4")
    assert b"DISTINCTION" in pdf_res.content

    # Test public verification returns full name initially
    verify_res = client.get(f"/api/v1/certificates/{test_cert_id}/verify")
    assert verify_res.status_code == 200
    assert verify_res.json()["certificate"]["recipientName"] == "Compliance Scholar"
    assert verify_res.json()["certificate"]["scoreBand"] == "Distinction"


def test_parse_idr_amount_negative_and_accounting_formats():
    from quanta.services.learning import parse_idr_amount
    assert parse_idr_amount("-Rp 5.000.000") == -5000000.0
    assert parse_idr_amount("(Rp 5.000.000)") == -5000000.0
    assert parse_idr_amount("(5.000.000)") == -5000000.0
    assert parse_idr_amount("Rp -2.500.000,50") == -2500000.50
    assert parse_idr_amount("10.000.000-") == -10000000.0
    assert parse_idr_amount("Rp 10.000.000") == 10000000.0


def test_data_hygiene_capstone_with_uppercase_and_spaced_headers(client):
    csv_content = """ID, DATE, CATEGORY, AMOUNT, CURRENCY
1, 2024-01-15, penjualan, 1500000, IDR
2, 2024-01-16, operasional, 500000, IDR
"""
    res = client.post(
        "/api/v1/courses/data-hygiene/capstone",
        json={"content": csv_content},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "passed"


def test_certificate_pdf_privacy_withheld(client):
    from quanta.db.session import engine
    from quanta.db.models import Certificate, User
    from sqlmodel import Session
    from datetime import datetime, timezone
    from uuid import uuid4

    test_cert_id = f"QTA-{str(uuid4()).upper()}"
    with Session(engine) as session:
        user = User(
            id="privacy-user-id",
            email="privacy@example.com",
            name="Secret Scholar",
            hashed_password="pw",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        cert = Certificate(
            id=test_cert_id,
            user_id=user.id,
            course_key="test-privacy-key",
            record={
                "id": test_cert_id,
                "trackId": "conduct-compliance-essentials",
                "courseTitle": "Conduct & Compliance Essentials",
                "recipientName": "Secret Scholar",
                "issuedAt": datetime.now(timezone.utc).isoformat(),
                "studyMinutes": 420,
                "scoreBand": "Distinction",
                "contentVersion": 1,
                "publicVerificationOptOut": True,
                "lessonIds": [],
                "examVersions": {},
            },
        )
        session.add(cert)
        session.commit()

    pdf_res = client.get(f"/api/v1/certificates/{test_cert_id}/pdf")
    assert pdf_res.status_code == 200
    assert b"Secret Scholar" not in pdf_res.content
    assert b"Withheld by recipient" in pdf_res.content

    # Whitespace and lowercase tolerance in URL verification
    verify_res = client.get(f"/api/v1/certificates/%20{test_cert_id.lower()}%20/verify")
    assert verify_res.status_code == 200
    assert verify_res.json()["certificate"]["recipientName"] == "Withheld by recipient (authentic certificate confirmed)"

