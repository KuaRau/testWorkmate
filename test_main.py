import pytest
from main import give_report


@pytest.fixture
def create_test_csv_files(tmpdir):
    file1_content = """name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,4.6,"Swift, Kotlin, React Native, iOS",Mobile Team,3
Elena Popova,Backend Developer,43,4.8,"Java, Spring Boot, MySQL, Redis",API Team,4
"""

    file2_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.9,"Python, Django, PostgreSQL, Docker",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
"""

    file3_content = """name,position,completed_tasks,performance,skills,team,experience_years
John Smith,Mobile Developer,29,4.5,"Python, ML, SQL, Pandas",AI Team,3
"""

    p1 = tmpdir.join("test1.csv")
    p1.write(file1_content)
    p2 = tmpdir.join("test2.csv")
    p2.write(file2_content)
    p3 = tmpdir.join("test3.csv")
    p3.write(file3_content)
    return str(p1), str(p2), str(p3)


def test_generate_performance_report(create_test_csv_files):
    file1, file2, file3 = create_test_csv_files
    report = give_report([file1, file2, file3])


    expected_order = [
        ('Backend Developer', 4.85),
        ('Frontend Developer', 4.7),
        ('Mobile Developer', 4.55)
    ]

    assert len(report) == 3

    for (actual_pos, actual_perf), (expected_pos, expected_perf) in zip(report, expected_order):
        assert actual_pos == expected_pos
        assert actual_perf == pytest.approx(expected_perf)


def test_generate_performance_report_with_empty_files(tmpdir):

    p1 = tmpdir.join("empty1.csv")
    p1.write("name,position,completed_tasks,performance,skills,team,experience_years\n")
    p2 = tmpdir.join("empty2.csv")
    p2.write("name,position,completed_tasks,performance,skills,team,experience_years\n")
    report = give_report([str(p1), str(p2)])
    assert report == []


def test_generate_performance_report_with_missing_file():

    report = give_report(['non_existent_file.csv'])
    assert report == []


def test_generate_performance_report_with_malformed_data(tmpdir):

    file_content = """name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,4.6,"Swift, Kotlin, React Native, iOS",Mobile Team,3
Elena Popova,Backend Developer,43,, "Java, Spring Boot, MySQL, Redis",API Team,4
Chris Wilson,DevOps Engineer,39,invalid,"Docker, Jenkins, GitLab CI, AWS",Infrastructure Team,5
Olga Kuznetsova,Frontend Developer,42,4.7,"Vue.js, JavaScript, Webpack, Sass",Web Team,3
"""

    p1 = tmpdir.join("malformed.csv")
    p1.write(file_content)
    report = give_report([str(p1)])
    expected = [
        ('Frontend Developer', 4.7),
        ('Mobile Developer', 4.6)
    ]
    assert report == expected