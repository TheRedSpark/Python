import json

from package import variables as v
import requests

import unittest

host = "http://0.0.0.0:8080"


class TestWeatherGet(unittest.TestCase):
    def test_success(self):
        response = requests.get(f"{host}/v1/weather", headers={"token": f"{v.token_techcluster_unit_tests}"},
                                data='{"lat":51.0,"lon":13.7}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":1,"konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,1:"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/weather", headers={"token": f"{v.token_techcluster_unit_tests}"},
                                data='{"lat":51.0,"lon":13.7}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/weather", headers={"token": f"{v.token_techcluster_unit_tests}-unauth"},
                                data='{"lat":51.0,"lon":13.7}')
        self.assertEquals(response.status_code, 403)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/weather", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestBrokkoliPut(unittest.TestCase):
    def test_success(self):
        response = requests.put(f"{host}/v1/brokkoli", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":1,"konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,1:"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.put(f"{host}/v2/brokkoli", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.put(f"{host}/v1/brokkoli", headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                                                "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 403)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/brokkoli", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestBrokkoliGet(unittest.TestCase):
    def test_success(self):
        response = requests.get(f"{host}/v1/brokkoli/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/brokkoli/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/brokkoli/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth"})
        self.assertEquals(response.status_code, 403)

    def test_data_prov(self):
        response = requests.get(f"{host}/v1/brokkoli/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                       "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","prozente":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)


class TestRitalinPut(unittest.TestCase):
    def test_success(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":1,"konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,1:"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.put(f"{host}/v2/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 403)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/ritalin", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestKoffeinGet(unittest.TestCase):
    def test_success(self):
        response = requests.get(f"{host}/v1/koffein/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/koffein/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/koffein/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth"})
        self.assertEquals(response.status_code, 403)

    def test_data_prov(self):
        response = requests.get(f"{host}/v1/koffein/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                      "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","starke":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)


class TestKoffeinPut(unittest.TestCase):
    def test_success(self):
        response = requests.put(f"{host}/v1/koffein", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","starke":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/koffein", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":"1","sorte":"Test","starke":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/koffein", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"starke":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.put(f"{host}/v2/koffein", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","starke":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.put(f"{host}/v1/koffein", headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","starke":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 403)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/koffein", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestRitalinGet(unittest.TestCase):
    def test_success(self):
        response = requests.get(f"{host}/v1/ritalin/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/ritalin/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/ritalin/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth"})
        self.assertEquals(response.status_code, 403)

    def test_data_prov(self):
        response = requests.get(f"{host}/v1/ritalin/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                      "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)


class TestAlkoholPut(unittest.TestCase):
    def test_success(self):
        response = requests.put(f"{host}/v1/alkohol", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","prozente":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/alkohol", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":1,"konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/alkohol", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,1:"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.put(f"{host}/v2/alkohol", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.put(f"{host}/v1/alkohol", headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                                               "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/alkohol", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestAlkoholGet(unittest.TestCase):
    def test_success(self):
        response = requests.get(f"{host}/v1/alkohol/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/alkohol/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/alkohol/gesamt",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth"})
        self.assertEquals(response.status_code, 403)

    def test_data_prov(self):
        response = requests.get(f"{host}/v1/alkohol/gesamt", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                      "Content-Type": "application/json"},
                                data='{"menge":1,"sorte":1,"konsumart":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)


class TestSkillPut(unittest.TestCase):
    def test_success(self):
        response = requests.put(f"{host}/v1/skill", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                             "Content-Type": "application/json"},
                                data='{"kategorie":"Test","skill":"Unittesti"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/skill", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                             "Content-Type": "application/json"},
                                data='{"kategorie":"1,"skill":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/skill", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                             "Content-Type": "application/json"},
                                data='{"skill":"Vape"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.put(f"{host}/v2/skill", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                             "Content-Type": "application/json"},
                                data='{"kategorie":"Test","skill":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.put(f"{host}/v1/skill", headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                                             "Content-Type": "application/json"},
                                data='{"kategorie":"Test","skill":"Unittesti"}')
        self.assertEquals(response.status_code, 403)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/skill", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestFinazenPut(unittest.TestCase):
    def test_success(self):
        response = requests.put(f"{host}/v1/finanzen", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                "Content-Type": "application/json"},
                                data='{"preis":1,"kategorie":"Test","subkategorie":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_data_type(self):
        response = requests.put(f"{host}/v1/finanzen", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                "Content-Type": "application/json"},
                                data='{"preis":"1","kategorie":"Test","subkategorie":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_incomplete_data(self):
        response = requests.put(f"{host}/v1/finanzen", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                "Content-Type": "application/json"},
                                data='{"preis":1,"subkategorie":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_url_version(self):
        response = requests.put(f"{host}/v2/finanzen", headers={"token": f"{v.token_techcluster_unit_tests}",
                                                                "Content-Type": "application/json"},
                                data='{"preis":1,"kategorie":"Test","subkategorie":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.put(f"{host}/v1/finanzen", headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                                                "Content-Type": "application/json"},
                                data='{"preis":1,"kategorie":"Test","subkategorie":"Test","bemerkung":"Unittesti"}')
        self.assertEquals(response.status_code, 403)

    def test_no_data_prov(self):
        response = requests.put(f"{host}/v1/finanzen", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)


class TestStatusGet(unittest.TestCase):
    def test_success(self):
        response = requests.get(f"{host}/v1/status", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/status", headers={"token": f"{v.token_techcluster_unit_tests}"})
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/status", headers={"token": f"{v.token_techcluster_unit_tests}-unauth"})
        self.assertEquals(response.status_code, 403)


class TestKineticaGet(unittest.TestCase):

    def test_success(self):
        response = requests.get(f"{host}/v1/ballistic",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"wind_speed":0.2,"wind_direction":50.6,"distance_to_target":1000,'
                                     '"muzzle_velocity":300.5,"air_pressure":40.6,"temperature":11.6,"firing_angle":-1,'
                                     '"mass_of_the_bullet":15.4,"diameter_of_the_bullet":3.0}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/ballistic",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"wind_speed":0.2,"wind_direction":50.6,"distance_to_target":1000,'
                                     '"muzzle_velocity":300.5,"air_pressure":40.6,"temperature":11.6,"firing_angle":-1,'
                                     '"mass_of_the_bullet":15.4,"diameter_of_the_bullet":3.0}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/ballistic",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                         "Content-Type": "application/json"},
                                data='{"wind_speed":0.2,"wind_direction":50.6,"distance_to_target":1000,'
                                     '"muzzle_velocity":300.5,"air_pressure":40.6,"temperature":11.6,"firing_angle":-1,'
                                     '"mass_of_the_bullet":15.4,"diameter_of_the_bullet":3.0}')
        self.assertEquals(response.status_code, 403)

    def test_bullet_slow(self):
        response = requests.get(f"{host}/v1/ballistic",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"wind_speed":0.2,"wind_direction":50.6,"distance_to_target":1000,'
                                     '"muzzle_velocity":3,"air_pressure":40.6,"temperature":11.6,"firing_angle":-1,'
                                     '"mass_of_the_bullet":15.4,"diameter_of_the_bullet":3.0}')
        self.assertEquals(response.status_code, 409)



class TestCleverPassGenerate(unittest.TestCase):

    def test_success(self):
        response = requests.get(f"{host}/v1/cleverpasswort/generate",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"length":10,"numbers":true,"lowercase_letters":true,'
                                     '"uppercase_letters":true,"symbols":true,"spaces":true,'
                                     '"exclude_similar_characters":true,"strict":true}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/cleverpasswort/generate",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"length":10,"numbers":true,"lowercase_letters":true,'
                                     '"uppercase_letters":true,"symbols":true,"spaces":true,'
                                     '"exclude_similar_characters":true,"strict":true}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/cleverpasswort/generate",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                         "Content-Type": "application/json"},
                                data='{"length":10,"numbers":true,"lowercase_letters":true,'
                                     '"uppercase_letters":true,"symbols":true,"spaces":true,'
                                     '"exclude_similar_characters":true,"strict":true}')
        self.assertEquals(response.status_code, 403)

    def test_wrong_data(self):
        response = requests.get(f"{host}/v1/cleverpasswort/generate",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"length":10,"numbers":true,"lowercase_letters":true,'
                                     '"uppercase_letters":true,"symbols":true,"spaces":true,'
                                     '"exclude_similar_characters":true,"strict":222}')
        self.assertEquals(response.status_code, 401)



class TestCleverPassAnalyze(unittest.TestCase):

    def test_success(self):
        response = requests.get(f"{host}/v1/cleverpasswort/analyse",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"passwort":"dfgsdfg253z6!!"}')
        self.assertEquals(response.status_code, 200)

    def test_wrong_url_version(self):
        response = requests.get(f"{host}/v2/cleverpasswort/analyse",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"passwort":"dfgsdfg253z6!!"}')
        self.assertEquals(response.status_code, 401)

    def test_wrong_user(self):
        response = requests.get(f"{host}/v1/cleverpasswort/analyse",
                                headers={"token": f"{v.token_techcluster_unit_tests}-unauth",
                                         "Content-Type": "application/json"},
                                data='{"passwort":"dfgsdfg253z6!!"}')
        self.assertEquals(response.status_code, 403)

    def test_wrong_data(self):
        response = requests.get(f"{host}/v1/cleverpasswort/analyse",
                                headers={"token": f"{v.token_techcluster_unit_tests}",
                                         "Content-Type": "application/json"},
                                data='{"passwort":dfgsdfg253z6!!}')
        self.assertEquals(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
