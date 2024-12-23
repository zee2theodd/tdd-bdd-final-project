######################################################################
# Product API Service Test Suite
######################################################################
import os
from unittest import TestCase
from service import app
from service.common import status
from service.models import db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductRoutes(TestCase):
    """Product Service tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        cls.client = app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.remove()
        db.drop_all()

    def setUp(self):
        """Runs before each test"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function to bulk create products
    ############################################################
    def _create_products(self, count: int = 1) -> list:
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ############################################################
    # Test Cases for Product API
    ############################################################

    def test_index(self):
        """It should return the home page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health(self):
        """It should return health status"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_create_product_with_invalid_data(self):
        """It should not Create a Product with invalid data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_product(self):
        """It should Get a single Product"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should return 404 when Product is not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = self._create_products(1)[0]
        new_data = test_product.serialize()
        new_data["name"] = "Updated Name"
        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Updated Name")

    def test_update_product_not_found(self):
        """It should return 404 when updating a non-existent Product"""
        response = self.client.put(f"{BASE_URL}/0", json={"name": "Does Not Exist"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_not_found(self):
        """It should return 204 when deleting a non-existent Product"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_products(self):
        """It should List all Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_products_by_category(self):
        """It should List Products filtered by category"""
        products = self._create_products(3)
        category_name = products[0].category.name
        response = self.client.get(BASE_URL, query_string={"category": category_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["category"] == category_name for p in data))

    def test_list_products_by_availability(self):
        """It should List Products filtered by availability"""
        self._create_products(2)
        response = self.client.get(BASE_URL, query_string={"available": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products_by_name(self):
        """It should List Products filtered by name"""
        products = self._create_products(1)
        name = products[0].name
        response = self.client.get(BASE_URL, query_string={"name": name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["name"] == name for p in data))
