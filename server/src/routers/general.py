from fastapi import APIRouter, Depends, status, exceptions

from repository import Repository

router = APIRouter()


@router.get('/countries/all')
def get_countries(repo: Repository = Depends()):
    return repo.get_countries()


@router.get('/countries/{country_name}/cities')
def get_cities(country_name: str,
               repo: Repository = Depends()):
    return repo.get_cities(country_name)


@router.get('/cities/{city_name}/universities')
def get_universities_by_city(city_name: str,
                             repo: Repository = Depends()):
    return repo.get_universities_by_city(city_name)


@router.get('/universities/{uni_name}')
def get_university_by_name(uni_name: str,
                           repo: Repository = Depends()):
    uni = repo.get_university_by_name(uni_name)
    if not uni: raise exceptions.HTTPException(status.HTTP_404_NOT_FOUND,
                                               detail='No such university')

    return uni

