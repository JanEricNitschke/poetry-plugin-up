from pathlib import Path
from typing import List

from cleo.testers.application_tester import ApplicationTester
from poetry.core.packages.package import Package
from poetry.pyproject.toml import PyProjectTOML
from pytest_mock import MockerFixture

from tests.helpers import poetry_v1, poetry_v2


def test_command(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_command_with_latest(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = project_path / "expected_pyproject_with_latest.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up --latest") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_command_with_dry_run(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    expected = PyProjectTOML(tmp_pyproject_path).file.read()

    assert app_tester.execute("up --dry-run") == 0
    # assert pyproject.toml file not modified
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_not_called()


@poetry_v1
def test_command_with_no_install_v1(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up --no-install") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="lock")


@poetry_v2
def test_command_with_no_install_v2(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up --no-install") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="lock", args="--regenerate")


def test_command_reverts_pyproject_on_error(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        side_effect=Exception,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    expected = PyProjectTOML(tmp_pyproject_path).file.read()

    assert app_tester.execute("up") == 1
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_pinned_without_latest_fails(app_tester: ApplicationTester) -> None:
    assert app_tester.execute("up --pinned") == 1


def test_command_with_exclude(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = project_path / "expected_pyproject_with_exclude.toml"
    expected = PyProjectTOML(path).file.read()

    assert (
        app_tester.execute("up --exclude foo --exclude bar --exclude=grault")
        == 0
    )
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_exclude_zero_based_caret_without_latest_fails(
    app_tester: ApplicationTester,
) -> None:
    assert app_tester.execute("up --exclude-zero-based-caret") == 1


def test_command_preserve_wildcard(
    app_tester: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = (
        project_path
        / "expected_pyproject_with_latest_and_preserve_wildcard.toml"
    )
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("up --latest --preserve-wildcard") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_preserve_wildcard_without_latest_fails(
    app_tester: ApplicationTester,
) -> None:
    assert app_tester.execute("up --preserve-wildcard") == 1


@poetry_v2
def test_command_with_latest_project(
    patch_path_is_file: None,
    app_tester_v2: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path_v2: Path,
    tmp_pyproject_path_v2: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = project_path_v2 / "expected_pyproject_with_latest.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester_v2.execute("up --latest") == 0
    print(PyProjectTOML(tmp_pyproject_path_v2).file.read())
    print(expected)
    assert PyProjectTOML(tmp_pyproject_path_v2).file.read() == expected
    command_call.assert_called_once_with(name="update")


@poetry_v2
def test_command_with_dry_run_project(
    app_tester_v2: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    tmp_pyproject_path_v2: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    expected = PyProjectTOML(tmp_pyproject_path_v2).file.read()

    assert app_tester_v2.execute("up --dry-run") == 0
    # assert pyproject.toml file not modified
    assert PyProjectTOML(tmp_pyproject_path_v2).file.read() == expected
    command_call.assert_not_called()


@poetry_v2
def test_command_reverts_pyproject_on_error_project(
    app_tester_v2: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    tmp_pyproject_path_v2: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        side_effect=Exception,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    expected = PyProjectTOML(tmp_pyproject_path_v2).file.read()

    assert app_tester_v2.execute("up") == 1
    assert PyProjectTOML(tmp_pyproject_path_v2).file.read() == expected
    command_call.assert_called_once_with(name="update")


@poetry_v2
def test_pinned_without_latest_fails_project(
    app_tester: ApplicationTester,
) -> None:
    assert app_tester.execute("up --pinned") == 1


@poetry_v2
def test_exclude_zero_based_caret_without_latest_fails_project(
    app_tester_v2: ApplicationTester,
) -> None:
    assert app_tester_v2.execute("up --exclude-zero-based-caret") == 1


@poetry_v2
def test_command_preserve_wildcard_project(
    app_tester_v2: ApplicationTester,
    packages: List[Package],
    mocker: MockerFixture,
    project_path_v2: Path,
    tmp_pyproject_path_v2: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",  # noqa: E501
        return_value=None,
    )

    path = (
        project_path_v2
        / "expected_pyproject_with_latest_and_preserve_wildcard.toml"
    )
    expected = PyProjectTOML(path).file.read()

    assert app_tester_v2.execute("up --latest --preserve-wildcard") == 0
    assert PyProjectTOML(tmp_pyproject_path_v2).file.read() == expected
    command_call.assert_called_once_with(name="update")


@poetry_v2
def test_preserve_wildcard_without_latest_fails_project(
    app_tester_v2: ApplicationTester,
) -> None:
    assert app_tester_v2.execute("up --preserve-wildcard") == 1
