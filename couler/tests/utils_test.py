# Copyright 2021 The Couler Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64

from couler.core import utils
from couler.tests.argo_test import ArgoBaseTestCase


class PyfuncTest(ArgoBaseTestCase):
    def test_argo_safe_name(self):
        self.assertIsNone(utils.argo_safe_name(None))
        self.assertEqual(utils.argo_safe_name("a_b"), "a-b")
        self.assertEqual(utils.argo_safe_name("a.b"), "a-b")
        self.assertEqual(utils.argo_safe_name("a_.b"), "a--b")
        self.assertEqual(utils.argo_safe_name("_abc."), "-abc-")

    def test_body(self):
        # Check None
        self.assertIsNone(utils.body(None))
        # A real function
        code = """
func_name = utils.workflow_filename()
# Here we assume that we are using `pytest` or `python -m pytest`
# to trigger the unit tests.
self.assertTrue(func_name in ["pytest", "runpy"])
"""
        self.assertEqual(code, utils.body(self.test_get_root_caller_filename))

    def test_get_root_caller_filename(self):
        func_name = utils.workflow_filename()
        # Here we assume that we are using `pytest` or `python -m pytest`
        # to trigger the unit tests.
        self.assertTrue(func_name in ["pytest", "runpy"])

    def test_invocation_location(self):
        def inner_func():
            func_name, _ = utils.invocation_location()
            self.assertEqual("test-invocation-location", func_name)

        inner_func()

    def test_encode_base64(self):
        s = "test encode string"
        encode = utils.encode_base64(s)
        decode = str(base64.b64decode(encode), "utf-8")
        self.assertEqual(s, decode)

    def test_check_gpu(self):
        with self.assertRaises(TypeError):
            utils.gpu_requested("cpu=1")
        self.assertFalse(utils.gpu_requested(None))
        self.assertFalse(utils.gpu_requested({}))
        self.assertFalse(utils.gpu_requested({"cpu": 1}))
        self.assertFalse(utils.gpu_requested({"cpu": 1, "memory": 2}))
        self.assertTrue(utils.gpu_requested({"gpu": 1}))
        self.assertTrue(utils.gpu_requested({" gpu ": 1}))
        self.assertTrue(utils.gpu_requested({"GPU": 1}))
        self.assertTrue(utils.gpu_requested({"cpu": 1, "memory": 2, "gpu": 1}))

    def test_non_empty(self):
        self.assertFalse(utils.non_empty(None))
        self.assertFalse(utils.non_empty([]))
        self.assertFalse(utils.non_empty({}))
        self.assertTrue(utils.non_empty(["a"]))
        self.assertTrue(utils.non_empty({"a": "b"}))
