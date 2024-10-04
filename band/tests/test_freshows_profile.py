from rest_framework import status
from rest_framework.test import APIClient
from band.models import FreshowsProfile
from model_bakery import baker
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def create_freshows_profile(api_client):
    def do_create_freshows_profile(freshows_profile):
        return api_client.post('/band/freshows_profile/', freshows_profile)
    return do_create_freshows_profile

@pytest.mark.django_db
class TestCreateFreshowsProfile:
    def test_if_the_user_is_anonymous_returns_401(self, create_freshows_profile):
        response= create_freshows_profile({'slogan':'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_the_user_is_not_admin_returns_403(self, api_client, create_freshows_profile, authenticate):
        authenticate()
        response= create_freshows_profile({'slogan':'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_the_user_if_data_is_invalid_returns_400(self, api_client, create_freshows_profile, authenticate):
        authenticate(is_staff= True)
        response= create_freshows_profile({'slogan':''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['slogan']is not None
    
    def test_if_the_user_if_data_is_valid_returns_201(self, api_client, create_freshows_profile, authenticate):
        authenticate(is_staff= True)
        response= create_freshows_profile({'slogan':'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id']>0

@pytest.mark.django_db
class TestRetrieveFreshowsProfile:
    def test_if_freshows_profile_exists_returns_200(self, api_client):
        freshows_profile= baker.make(FreshowsProfile)
        response= api_client.get(f'/band/freshows_profile/{freshows_profile.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id' : freshows_profile.id,
            'slogan' : freshows_profile.slogan
        }

@pytest.mark.django_db
class TestListFreshowsProfile:
    def test_if_freshows_profile_exists_returns_200(self, api_client):
        
        response= api_client.get(f'/band/freshows_profile/')

        assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def full_update_freshows_profile(api_client):
    def do_full_update_freshows_profile(freshows_profile):
        freshows_profile= baker.make(FreshowsProfile)
        return api_client.put(f'/band/freshows_profile/{freshows_profile.id}/')

    return do_full_update_freshows_profile

@pytest.mark.django_db
class TestUpdateFreshowsProfile:
    def test_if_the_user_is_anonymous_returns_401(self, full_update_freshows_profile):
        response= full_update_freshows_profile({'slogan':'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 
    
    def test_if_the_user_is_not_admin_returns_403(self, api_client, full_update_freshows_profile, authenticate):
        authenticate()
        response= full_update_freshows_profile({'slogan':'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_the_user_if_data_is_invalid_returns_400(self, api_client, full_update_freshows_profile, authenticate):
        authenticate(is_staff= True)
        response= full_update_freshows_profile({'slogan':''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['slogan']is not None
    
    def test_if_the_user_if_data_is_valid_returns_200(self, api_client, full_update_freshows_profile, authenticate):
        freshows_profile = baker.make(freshows_profile)
        

        authenticate(is_staff= True)
        response= api_client.put(f'/band/freshows_profile/{freshows_profile.id}/', {'slogan': 'a'})

        assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def partial_update_freshows_profile(api_client):
    def do_partial_update_freshows_profile(freshows_profile):
        freshows_profile= baker.make(FreshowsProfile)
        return api_client.patch(f'/band/freshows_profile/{freshows_profile.id}/')

    return do_partial_update_freshows_profile

@pytest.mark.django_db
class TestUpdateFreshowsProfile:
    def test_if_the_user_is_anonymous_returns_401(self, partial_update_freshows_profile):
        response= partial_update_freshows_profile({'slogan':'a'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 
    
    def test_if_the_user_is_not_admin_returns_403(self, api_client, partial_update_freshows_profile, authenticate):
        authenticate()
        response= partial_update_freshows_profile({'slogan':'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_the_user_if_data_is_invalid_returns_400(self, api_client, partial_update_freshows_profile, authenticate):
        freshows_profile = baker.make(FreshowsProfile)
        authenticate(is_staff= True)
        response= api_client.patch(f'/band/freshows_profile/{freshows_profile.id}/', {'slogan': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['slogan']is not None
    
    def test_if_the_user_if_data_is_valid_returns_200(self, api_client, partial_update_freshows_profile, authenticate):
        freshows_profile = baker.make(FreshowsProfile)
        

        authenticate(is_staff= True)
        response= api_client.patch(f'/band/freshows_profile/{freshows_profile.id}/', {'slogan': 'a'})

        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestDestroyFreshowsProfile:
    def test_if_freshows_profile_exists_returns_200(self, api_client, authenticate):
        freshows_profile= baker.make(FreshowsProfile)
        authenticate(is_staff= True)
        response= api_client.delete(f'/band/freshows_profile/{freshows_profile.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        

