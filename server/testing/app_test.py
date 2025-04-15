import json
import pytest

class TestPlant:
    @pytest.fixture(autouse=True)
    def _setup(self, test_client):
        self.client = test_client
    '''Flask application in app.py'''

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        assert(response.status_code == 200)

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = self.client.get('/plants/1')
        data = json.loads(response.data.decode())

        assert(type(data) == dict)
        assert(data["id"])
        assert(data["name"])

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
        response = self.client.patch(
            '/plants/1',
            json={
                "is_in_stock": False
            },
            headers={'Content-Type': 'application/json'}
        )
        data = json.loads(response.data.decode())

        assert(type(data) == dict)
        assert(data["id"])
        assert(data["is_in_stock"] == False)

    def test_plant_by_id_delete_route_deletes_plant(self):
        '''returns JSON representing updated Plant object at "/plants/<int:id>".'''
        # First create a plant to delete
        response = self.client.post('/plants', json={
            "name": "Test Delete",
            "image": "delete.jpg",
            "price": 100.00,
            "is_in_stock": True
        })
        plant_id = json.loads(response.data)['id']
        
        response = self.client.delete(f'/plants/{plant_id}')
        data = response.data.decode()

        assert(not data)
