from http import HTTPStatus
from .models import Product, ProdCategory

from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/index.html')
        self.assertEqual(response.context_data['title'], 'Store')


class ProductViewTestCase(TestCase):
    fixtures = ('cats', 'prods')

    def check_params(self, response, title, qs_db):
        qs_response = response.context_data.get('object_list')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], title)
        self.assertQuerysetEqual(qs_response, qs_db, ordered=False)

    def test_all_cats(self):
        response = self.client.get(reverse('products:category', args=(0,)))
        qs_db = Product.objects.all()[:3]
        self.check_params(response=response, title='Store - Catalog', qs_db=qs_db)

    def test_single_cat(self):
        for cat in ProdCategory.objects.all():
            response = self.client.get(reverse('products:category', args=(cat.id,)))
            qs_db = cat.product_set.all()[:3]
            self.check_params(response=response, title=cat.name, qs_db=qs_db)
