import pytest

from student_manager.src.database import get_connection
from student_manager.src.students import (
    get_students,
    add_student,
    delete_student,
    search_students,
)


@pytest.fixture
def setup_database(tmp_path, monkeypatch):
    """Prépare une base SQLite temporaire pour les tests."""

    database_file = tmp_path / "test_students.db"

    def get_test_connection():
        import sqlite3
        return sqlite3.connect(database_file)

    monkeypatch.setattr(
        "student_manager.src.students.get_connection",
        get_test_connection,
    )

    with get_test_connection() as connection:
        connection.execute("""
            CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT,
                class_name TEXT
            )
        """)

    return database_file


def test_add_student(setup_database):
    """ vérifier l’ajout d’un étudiant """
    student_id = add_student(
        "Alice", "Martin", "alice@example.com", "BTS SIO"
    )

    assert student_id == 1


def test_get_students(setup_database):
    # À compléter :  vérifier la récupération de la liste des étudiants.
    add_student("Alice", "Martin", "alice@example.com", "BTS SIO")
    add_student("Bob", "Durand", "bob@example.com", "BTS SIO")

    students = get_students()

    assert len(students) == 2
    # tri par nom : Durand avant Martin
    assert students[0][1:3] == ("Bob", "Durand")
    assert students[1][1:3] == ("Alice", "Martin")

def test_delete_student(setup_database):
    # À compléter : vérifier la suppression d’un étudiant.
    alice_id = add_student("Alice", "Martin", "alice@example.com", "BTS SIO")
    add_student("Bob", "Durand", "bob@example.com", "BTS SIO")

    delete_student(alice_id)

    students = get_students()
    assert len(students) == 1
    assert students[0][1] == "Bob"

def test_search_students(setup_database):
    # À compléter : vérifier la recherche d’étudiants à partir d’un nom ou d'un prénom.
    add_student("Alice", "Martin", "alice@example.com", "BTS SIO")
    add_student("Bob", "Durand", "bob@example.com", "BTS SIO")

    by_last_name = search_students("Martin")
    by_first_name = search_students("Bob")

    assert len(by_last_name) == 1
    assert by_last_name[0][1] == "Alice"
    assert len(by_first_name) == 1
    assert by_first_name[0][2] == "Durand"

def test_search_students_no_result(setup_database):
    # À compléter : vérifier le comportement de la recherche lorsqu’aucun étudiant ne correspond au critère indiqué.
    add_student("Alice", "Martin", "alice@example.com", "BTS SIO")

    results = search_students("Inconnu")

    assert results == []