from student_manager.src.database import get_connection


def add_grade(student_id, subject_id, grade):
    """
        Ajoute une note pour un étudiant et une matière.
    """
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO grades (student_id, subject_id, grade)
            VALUES (?, ?, ?)
            """,
            (student_id, subject_id, grade)
        )
        connection.commit()


def get_grades_by_student(student_id):
    """
        Retourne les notes d'un étudiant avec le nom de la matière.
    """
    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT g.id, s.name, g.grade
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = ?
            """,
            (student_id,)
        )
        return cursor.fetchall()


def get_student_average(student_id):
    """
    Retourne la moyenne d'un étudiant.
    """

    with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT AVG(grade)
            FROM grades
            WHERE student_id = ?
            """,
            (student_id,)
        )

        result = cursor.fetchone()

        return result[0] if result[0] is not None else 0