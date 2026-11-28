"""Structural guarantees for the ordered, prerequisite-aware curriculum."""

from quanta.domain.catalog import CATALOG, EXAMS, LESSONS


def _by_id():
    return {course["id"]: course for course in CATALOG}


def test_catalog_is_ordered_by_explicit_sequence():
    sequences = [course["sequence"] for course in CATALOG]
    assert sequences == sorted(sequences)
    assert len(sequences) == len(set(sequences)) == 28
    assert sequences == [10 * (index + 1) for index in range(len(CATALOG))]
    assert CATALOG[0]["id"] == "trading-fundamentals"
    assert CATALOG[-1]["id"] == "algorithm-evaluation"


def test_every_course_carries_curriculum_metadata():
    for course in CATALOG:
        assert 1 <= course["stage_number"] <= 12
        assert course["stage"]
        assert course["stage_name"]
        assert 0 <= course["difficulty"] <= 5
        assert course["estimated_hours"] > 0
        assert course["focus_summary"].strip()
        assert len(course["skills"]) >= 3
        assert course["course_type"] in {
            "core",
            "foundation",
            "specialization",
            "workshop",
            "capstone",
            "reference",
            "on-ramp",
        }
        assert course["learning_outcomes"]
        assert not (course["is_core"] and course["is_specialization"])
        if course["is_capstone"]:
            assert course["course_type"] == "capstone"


def test_prerequisites_exist_and_appear_earlier():
    by_id = _by_id()
    position = {course["id"]: index for index, course in enumerate(CATALOG)}
    for course in CATALOG:
        for field in (
            "prerequisite_course_ids",
            "prerequisite_any_of",
            "recommended_course_ids",
        ):
            for prerequisite in course[field]:
                assert prerequisite in by_id, f"{course['id']}: {prerequisite}"
                assert prerequisite != course["id"]
                assert position[prerequisite] < position[course["id"]], (
                    f"{prerequisite} must precede {course['id']}"
                )


def test_prerequisite_graph_is_acyclic():
    indegree = {course["id"]: 0 for course in CATALOG}
    edges = {course["id"]: [] for course in CATALOG}
    for course in CATALOG:
        for prerequisite in (
            course["prerequisite_course_ids"] + course["prerequisite_any_of"]
        ):
            edges[prerequisite].append(course["id"])
            indegree[course["id"]] += 1
    ready = [course_id for course_id, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for dependent in edges[node]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
    assert visited == len(CATALOG)


def test_pedagogical_order_and_alternative_prerequisites():
    position = {course["id"]: index for index, course in enumerate(CATALOG)}
    ordered = [
        "trading-fundamentals",
        "security-analysis",
        "statistical-foundations",
        "econometrics",
        "strategy-lab",
        "stock-machine-learning",
        "stock-bots",
        "c-hpc-trading",
        "algorithm-evaluation",
    ]
    assert [position[course_id] for course_id in ordered] == sorted(
        position[course_id] for course_id in ordered
    )
    assert position["lab-workshop"] > position["statistical-foundations"]
    assert position["valuation-uncertainty"] > position["statistical-foundations"]
    assert position["web3"] > position["c-hpc-trading"]
    capstone = _by_id()["algorithm-evaluation"]
    assert set(capstone["prerequisite_any_of"]) == {
        "stock-bots",
        "stock-machine-learning",
        "c-hpc-trading",
    }
    casebook = _by_id()["real-world-casebook"]
    assert set(casebook["prerequisite_any_of"]) == {
        "forensic-accounting",
        "credit-distress",
        "bank-analysis",
    }


def test_advanced_concepts_do_not_precede_their_foundations():
    position = {course["id"]: index for index, course in enumerate(CATALOG)}
    first_occurrence = {}
    # Match teaching phrases rather than incidental citations. A literature
    # reference that names a method is not the same as teaching it.
    terms = {
        "GARCH": ("GARCH(", "GARCH(1,1)"),
        "cointegration": ("Engle–Granger", "Engle-Granger"),
        "Deflated Sharpe": ("Deflated Sharpe Ratio",),
        "Black-Litterman": ("Black–Litterman", "Black-Litterman"),
    }
    for course in CATALOG:
        text = " ".join(
            f"{module.get('title', '')} {module.get('content', '')}"
            for module in course["modules"]
        )
        for term, phrases in terms.items():
            if any(phrase.lower() in text.lower() for phrase in phrases):
                first_occurrence.setdefault(term, course["id"])
    for term in terms:
        assert (
            position[first_occurrence[term]]
            >= position["statistical-foundations"]
        ), f"{term} is taught before its quantitative foundation"


def test_funnel_cta_points_to_the_next_sequenced_course():
    for index, course in enumerate(CATALOG):
        cta = course["funnel_cta"]
        assert cta["label"]
        if index + 1 < len(CATALOG):
            assert cta["target_course_id"] == CATALOG[index + 1]["id"]
        else:
            assert cta["target_course_id"] == "curriculum"


def test_courses_api_returns_the_same_ordered_catalog(client):
    response = client.get("/api/v1/courses")
    assert response.status_code == 200
    assert [course["id"] for course in response.json()] == [
        course["id"] for course in CATALOG
    ]
    assert [course["sequence"] for course in response.json()] == [
        course["sequence"] for course in CATALOG
    ]


def test_lesson_and_exam_identifiers_remain_unique_and_attached():
    assert len(LESSONS) == len(set(LESSONS))
    assert len(EXAMS) == len(set(EXAMS))
    for course in CATALOG:
        module_ids = {module["id"] for module in course["modules"]}
        assert len(module_ids) == len(course["modules"])
        for exam in course["exams"]:
            assert set(exam["moduleIds"]) <= module_ids
            for question in exam["questions"]:
                assert question["lessonId"] in module_ids