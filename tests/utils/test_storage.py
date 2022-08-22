import os
import pickle

import pytest

from snsary.utils.storage import _get_storage_backend, get_storage


@pytest.fixture
def storage_path(mocker, tmp_path):
    path = str(tmp_path / "test.ss")
    mocker.patch.dict(os.environ, STORAGE_PATH=path)
    return path


def test_get_storage(mocker):
    mocker.patch.dict(os.environ, {}, clear=True)
    store = get_storage()

    assert "__getitem__" in dir(store)
    assert "__contains__" in dir(store)
    assert "__setitem__" in dir(store)
    assert "clear" in dir(store)
    assert id(store) == id(get_storage())


def test_get_storage_backend_mock(mocker):
    mocker.patch.dict(os.environ, {}, clear=True)
    assert type(_get_storage_backend()) == dict


def test_get_storage_backend(storage_path):
    data = pickle.dumps(dict(test=123))
    open(storage_path, "wb").write(data)
    assert _get_storage_backend()["test"] == 123


def test_get_storage_backend_not_exist(storage_path):
    backend = _get_storage_backend()
    assert backend.ttl == 86400
    assert backend.maxsize == float("inf")


def test_get_storage_backend_ttl(storage_path, mocker):
    mocker.patch.dict(os.environ, STORAGE_TTL="123")
    assert _get_storage_backend().ttl == 123


def test_get_storage_backend_corrupt(storage_path):
    open(storage_path, "wb").write(b"something")
    assert len(_get_storage_backend()) == 0


def test_get_storage_backend_empty(storage_path):
    open(storage_path, "wb").close()
    assert os.path.exists(storage_path)
    assert len(_get_storage_backend()) == 0


def test_get_storage_backend_at_exit(mocker, storage_path):
    mock_atexit = mocker.patch("atexit.register")

    backend = _get_storage_backend()
    mock_atexit.assert_called()

    backend["test"] = 123
    mock_atexit.mock_calls[0].args[0]()

    backend = pickle.load(open(storage_path, "rb"))
    assert backend["test"] == 123
