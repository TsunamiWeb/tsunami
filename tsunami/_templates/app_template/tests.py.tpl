from tsunami.test import BaseTestCase
from tsunami import test_utils
import unittest


class ExampleTestCase(BaseTestCase):

    # tests that are asynchronous
    @test_utils.unittest_run_loop
    async def test_example(self):
        resp = await self.client.request("GET", "/api/v1.0/{appname}/example")
        assert resp.status != 200
