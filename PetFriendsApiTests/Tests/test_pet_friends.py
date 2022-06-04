import os.path

from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os
import multiprocessing as mp

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet(name = "ЛевТигр2", animal_type='Тигр',
                     age='15', pet_photo='images/tiger.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = "86d494a7-23ce-4815-b0a6-0cb76cbbcedd"
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

# def test_put_pet(name = "Gosha", animal_type = "Zhrat", age = "33"):
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#     pet_id = "9a912c0e-e9db-4c74-8e87-505c0f5b7982"
#     status, result = pf.put_pet(auth_key, name, animal_type, age, pet_id)
#     assert status == 200
#     assert result ['name'] == name

def test_get_api_key_for_invalid_user(email = valid_email, password = invalid_password):
    """Проверяем что доступ к ЛК невозможен при валидной почте и неверном пароле"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_for_invalid_password(email=invalid_email, password=valid_password):
    """Проверяем что доступ к ЛК невозможен при неверной почте и верном пароле"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверяем что доступ к ЛК невозможен при неверной почте и неверном пароле"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result

def test_add_new_pet_big_name (name = "ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2ЛевТигр2Лев",
                     animal_type='Тигр', age='15', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца с очень длинным именем"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_big_name(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_photo (name="ЛевТигр2",
    animal_type='Тигр', age='15'):
    """Проверка публикации питомца без фото"""
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400

def test_add_new_pet_without_name (name = "", animal_type='Тигр', age='15', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца без имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_name(auth_key, name, animal_type, age, pet_photo)
    assert status == 200 #ожидаем статус, 400 сайт не должен принять питомца без имени, если тест прошел, то это баг
    assert result['name'] == name

def test_add_new_pet_without_name2 (name = "", animal_type='Тигр', age='15', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца без имени"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_name2 (auth_key, name, animal_type, age, pet_photo)
    assert status == 400 #ожидаем статус, 400 сайт не должен принять питомца без имени
    assert result['name'] == name


def test_add_new_pet_without_animal_type (name="Pasha", animal_type='', age='23', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца без тпиа"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_animal_type(auth_key, name, animal_type, age, pet_photo)
    assert status == 400 #ожидаем 400, сайт не должен принять питомца без указания типа животного
    assert result['animal_type'] == animal_type

def test_add_new_pet_without_animal_type2 (name="Pasha", animal_type='', age='23', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца без тпиа"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_animal_type2 (auth_key, name, animal_type, age, pet_photo)
    assert status == 200 #Ожидаем статус 400 если тест проходит то это баг
    assert result['animal_type'] == animal_type


def test_add_new_pet_without_age(name="Pasha", animal_type='Тигр', age='', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца без возраста"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_animal_type(auth_key, name, animal_type, age, pet_photo)
    assert status == 400  # ожидаем 400, сайт не должен принять питомца без указания возраста
    assert result['animal_type'] == animal_type


def test_add_new_pet_without_age2(name="Pasha", animal_type='Тигр', age='', pet_photo='images/tiger.jpg'):
    """Проверка публикации питомца без возраста"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_animal_type2(auth_key, name, animal_type, age, pet_photo)
    assert status == 200  # Ожидаем статус 400 если тест проходит, то это баг
    assert result['animal_type'] == animal_type








