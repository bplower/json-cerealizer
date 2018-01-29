import json
import json_cerealizer
import imp
import unittest
from datetime import datetime

class TestJSONCerealizer(unittest.TestCase):
    def test_patch_replaces_default_encoder(self):
        # Refresh our imports
        global json
        global json_cerealizer
        imp.reload(json)
        imp.reload(json_cerealizer)
        # Actual testing
        default = json.__dict__['_default_encoder']
        self.assertIsInstance(default, json.JSONEncoder)
        self.assertNotIsInstance(default, json_cerealizer.CerealJSONEncoder)
        json_cerealizer.patch()
        new = json.__dict__['_default_encoder']
        self.assertIsNot(default, new)
        self.assertIsInstance(new, json.JSONEncoder)
        self.assertIsInstance(new, json_cerealizer.CerealJSONEncoder)

    def test_unpatch_resets_default_encoder(self):
        # Refresh our imports
        global json
        global json_cerealizer
        imp.reload(json)
        imp.reload(json_cerealizer)
        # Actual testing
        default = json.__dict__['_default_encoder']
        # Make sure the starting case is as we're expecting
        self.assertIsInstance(default, json.JSONEncoder)
        self.assertNotIsInstance(default, json_cerealizer.CerealJSONEncoder)
        json_cerealizer.patch()
        # Make sure it was patched as expected
        self.assertIsInstance(json.__dict__['_default_encoder'],
                              json_cerealizer.CerealJSONEncoder)
        json_cerealizer.unpatch()
        self.assertIsInstance(json.__dict__['_default_encoder'],
                              json.JSONEncoder)
        self.assertNotIsInstance(json.__dict__['_default_encoder'],
                                 json_cerealizer.CerealJSONEncoder)

    def test_add_serializer(self):
        # Refresh our imports
        global json
        global json_cerealizer
        imp.reload(json)
        imp.reload(json_cerealizer)
        # Actual testing
        actual_serializers = json_cerealizer.CerealJSONEncoder.serializers
        self.assertEqual({}, actual_serializers)
        json_cerealizer.add_serializer(datetime, datetime.isoformat)
        expected_serializers = {datetime: datetime.isoformat}
        actual_serializers = json_cerealizer.CerealJSONEncoder.serializers
        self.assertEqual(expected_serializers, actual_serializers)

    def test_encoder(self):
        # Refresh our imports
        global json
        global json_cerealizer
        imp.reload(json)
        imp.reload(json_cerealizer)
        # Actual testing
        now = datetime.now()
        json_cerealizer.CerealJSONEncoder.register_instance(datetime, datetime.isoformat)
        result = json.dumps(now, cls=json_cerealizer.CerealJSONEncoder)
        self.assertEqual(result, json.dumps(now.isoformat()))


        # actual_serializers = json_cerealizer.CerealJSONEncoder.serializers
        # self.assertEqual({}, actual_serializers)
        # json_cerealizer.add_serializer(datetime, datetime.isoformat)
        # expected_serializers = {datetime: datetime.isoformat}
        # actual_serializers = json_cerealizer.CerealJSONEncoder.serializers
        # self.assertEqual(expected_serializers, actual_serializers)
