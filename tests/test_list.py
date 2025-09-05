import pytest
from projects_organizer import app
from typer.testing import CliRunner
import yaml

projects = {
    "project1": {
        "title": "Project 1",
        "archived": True,
    },
    "project2": {
        "title": "Project 2",
    },
    "project3": {
        "title": "Project 3",
    },
}


@pytest.fixture(scope="session")
def projects_dir(tmp_path_factory):
    p_dir = tmp_path_factory.mktemp("projects")
    print(p_dir)
    for name, data in projects.items():
        (p_dir / name).mkdir()
        with open(p_dir / name / "index.md", "w") as f:
            f.write("---\n")
            f.write(
                yaml.dump(data, indent=2, default_flow_style=False, sort_keys=False)
            )
            f.write("---\n")
            f.write("My description")
    return p_dir


def test_list_basic(projects_dir):
    runner = CliRunner()
    test_args = ["-d", projects_dir, "list"]
    print(test_args)
    result = runner.invoke(app, test_args)
    print(result)
    output = result.stdout
    print(output)
    assert output == "- Project 1\n- Project 2\n- Project 3\n"
    assert result.exit_code == 0


# @pytest.mark.parametrize("projects_dir,filter,expected", [("projects_dir", 'not archived', "- project1\n- project2\n- project3\n")])
# def test_list_filter(projects_dir, filter, expected, request):
@pytest.mark.parametrize(
    "filter,expected",
    [
        ("unknown", ""),
        ("not unknown", "- Project 1\n- Project 2\n- Project 3\n"),
        ("archived", "- Project 1\n"),
        ("not archived", "- Project 2\n- Project 3\n"),
    ],
)
def test_list_filter(filter, expected, projects_dir):
    runner = CliRunner()
    # dir = request.getfixturevalue(projects_dir)
    # test_args = ['-d', dir, 'list', '-f', filter]
    test_args = ["-d", projects_dir, "list", "-f", filter]
    print(test_args)
    result = runner.invoke(app, test_args)
    print(result)
    output = result.stdout
    print(output)
    assert output == expected
    assert result.exit_code == 0
