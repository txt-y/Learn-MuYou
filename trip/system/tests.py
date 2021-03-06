import json

from django.test import TestCase, Client

from system.models import Slider


class SliderTest(TestCase):
    def setUp(self) -> None:
        # 测试前的准备工作
        Slider.objects.create(name='t1', typrs=11, img='a.jpg')
        Slider.objects.create(name='t2', typrs=13, img='b.jpg')
        self.client = Client()

    def test_slider_list(self):
        response = self.client.get('/system/slider/list/')  # get请求
        self.assertEqual(response.status_code, 200)  # 校验状态码

    def test_slider_list_types(self):
        response = self.client.get('/system/slider/list/', {'typrs': 11})  # get请求
        self.assertEqual(response.status_code, 200)  # 校验状态码
        data_list = json.loads(response.content)['objects']
        self.assertEqual(len(data_list), 2, '按条件查询失败')
