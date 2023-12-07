
from pytest import fixture
import httpx


@fixture(scope='session')
def req():
    with httpx.Client(base_url='http://localhost:8000') as req:
        yield req
