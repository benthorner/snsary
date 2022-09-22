from snsary.utils import request


def test_retrying_session():
    session = request.retrying_session()
    assert session.get_adapter("http://something").max_retries.total == 3
    assert session.get_adapter("https://something").max_retries.total == 3
