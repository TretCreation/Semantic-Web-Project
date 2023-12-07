import httpx
import pytest


def test_countries(req: httpx.Client):
    resp = req.get('/countries/all')
    body = resp.json()
    assert body[0] == 'Switzerland'
    assert body[1] == 'Norway'
    assert body[2] == 'Iceland'


@pytest.mark.parametrize('country,city', [('Norway', 'Sandnes'), ('France', 'Cannes')])
def test_cities(req: httpx.Client, country: str, city: str):
    resp = req.get(f'/countries/{country}/cities')
    body = resp.json()
    assert body[0] == city


@pytest.mark.parametrize('country,city,university',
                         [('Norway', 'Sandnes', 'VID Specialized University'),
                          ('France', 'Bordeaux', 'ARTS')]
                         )
def test_universities(req: httpx.Client, country: str, city: str, university: str):
    resp = req.get(f'/countries/{country}/cities/{city}/universities')
    body = resp.json()
    assert body[0] == university


@pytest.mark.parametrize('university', ['VID Specialized University', 'Montesquieu University'])
def test_university(req: httpx.Client, university: str):
    resp = req.get(f'/universities/{university}')
    body = resp.json()
    assert body['name']
    assert body['city']
    assert body['logo']
    assert body['students']
    assert body['site']


@pytest.mark.parametrize('university', ['Bursa', 'AR'])
def test_absent_university(req: httpx.Client, university: str):
    resp = req.get(f'/universities/{university}')
    body = resp.json()
    assert resp.status_code == 404
    assert body['detail'] == 'No such university'
