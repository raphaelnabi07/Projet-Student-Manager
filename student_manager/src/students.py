from student_manager.src.database import get_connection


def get_students():
    """
    Retourne la liste de tous les étudiants.
    """
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT id, first_name, last_name, email, class_name
            FROM students
            ORDER BY last_name, first_name
            """
        )

        return cursor.fetchall()


def add_student(first_name, last_name, email, class_name):
    """
    Ajoute un nouvel étudiant dans la base de données.
    """
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO students (first_name, last_name, email, class_name)
            VALUES (?, ?, ?, ?)
            """,
            (first_name, last_name, email, class_name)
        )
        connection.commit()


def delete_student(student_id):
    """
    Supprime un étudiant.
    """
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM students
            WHERE id = ?
            """,
            (student_id,)
        )
        connection.commit()


def search_students(name):
    """
    Recherche un étudiant par son nom ou son prénom.
    """
    with get_connection() as connection:
        search_term = f"%{name}%"
        cursor = connection.execute(
            """
            SELECT id, first_name, last_name, email, class_name
            FROM students
            WHERE first_name LIKE ? OR last_name LIKE ?
            ORDER BY last_name, first_name
            """,
            (search_term, search_term)
        )

        return cursor.fetchall()