"""
End-to-End API Integration & Portal Route Verification Suite
KG-RAG Campus Assistant & Unified Student Hub
"""
import unittest
import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from models import db
from models.user import User
from models.material import StudyMaterial
from models.notice import Notice

class TestAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_01_portal_routes_render(self):
        """Verify all primary public web portal routes render with HTTP 200."""
        routes = ['/', '/student', '/departments', '/admissions', '/placements', '/facilities', '/contact', '/clubs', '/about']
        for r in routes:
            res = self.client.get(r)
            self.assertEqual(res.status_code, 200, f"Route {r} failed to render.")
        print("✓ All 9 public web portal views render with HTTP 200 OK")

    def test_02_pwa_assets_accessible(self):
        """Verify PWA manifest and Service Worker exist and return valid content."""
        res_m = self.client.get('/static/manifest.json')
        self.assertEqual(res_m.status_code, 200)
        data = json.loads(res_m.data)
        self.assertEqual(data.get('short_name'), 'SPHN Hub')

        res_sw = self.client.get('/static/sw.js')
        self.assertEqual(res_sw.status_code, 200)
        self.assertIn(b'sphn-hub-v1', res_sw.data)
        print("✓ PWA manifest and Service Worker are valid and accessible")

    def test_03_get_notices_api(self):
        """Verify /api/notices returns list of circular announcements."""
        res = self.client.get('/api/notices')
        self.assertEqual(res.status_code, 200)
        notices = res.get_json()
        self.assertIsInstance(notices, list)
        self.assertGreater(len(notices), 0, "No notices returned.")
        self.assertIn('title', notices[0])
        print(f"✓ /api/notices returned {len(notices)} valid campus circulars")

    def test_04_get_materials_api(self):
        """Verify /api/materials returns list and supports dept & sem filtering."""
        res = self.client.get('/api/materials')
        self.assertEqual(res.status_code, 200)
        materials = res.get_json()
        self.assertIsInstance(materials, list)
        self.assertGreater(len(materials), 0, "No study materials returned.")

        # Test filtering by department
        res_filter = self.client.get('/api/materials?dept=cse&sem=4')
        self.assertEqual(res_filter.status_code, 200)
        filtered = res_filter.get_json()
        self.assertGreaterEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['semester'], 4)
        print(f"✓ /api/materials returned {len(materials)} materials with working filter")

    def test_05_upload_material_api(self):
        """Verify /api/upload-material creates new study material."""
        payload = {
            'title': 'Unit 5: Cloud Security & Virtualization',
            'subject': 'Cloud Computing',
            'department': 'cse',
            'semester': '7',
            'description': 'Hypervisors, VM migration, and AWS shared responsibility model.',
            'file_url': 'https://drive.google.com/sample_cloud_notes'
        }
        res = self.client.post('/api/upload-material', data=payload)
        self.assertEqual(res.status_code, 200)
        res_data = res.get_json()
        self.assertEqual(res_data.get('status'), 'ok')
        self.assertIn('material_id', res_data)
        print("✓ /api/upload-material successfully registered new study resource")

    def test_06_chat_api_intents(self):
        """Verify /api/chat handles domain queries, fuzzy matching, and new intents."""
        test_queries = [
            ("give me notes for operating systems", "material_info"),
            ("what are the latest circulars", "notice_info"),
            ("where is block a", "building_info"),
            ("who is the hod of cse", "hod_info"),
            ("what is the fee structure for btech", "fee_info"),
            ("how are the placements", "placement_info")
        ]
        for query, expected_intent in test_queries:
            res = self.client.post('/api/chat', json={'message': query})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertEqual(data.get('intent'), expected_intent, f"Query '{query}' expected {expected_intent}, got {data.get('intent')}")
            self.assertTrue(len(data.get('response', '')) > 10, "Response string is too short.")
        print("✓ /api/chat accurately classified and routed all 6 intent categories")

    def test_07_chat_multi_turn_context(self):
        """Verify /api/chat preserves multi-turn session context."""
        # Turn 1: Mention ECE
        res1 = self.client.post('/api/chat', json={'message': 'tell me about ece department'})
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.get_json()['entities'].get('department'), 'ece')

        # Turn 2: Ask HOD without mentioning ECE
        res2 = self.client.post('/api/chat', json={'message': 'who is the hod?'})
        self.assertEqual(res2.status_code, 200)
        data2 = res2.get_json()
        self.assertEqual(data2['intent'], 'hod_info')
        self.assertEqual(data2['entities'].get('department'), 'ece')
        self.assertIn('Dr. K. Srinivas Rao', data2['response'])
        print("✓ Multi-turn dialogue context inherited 'ece' department across turns")

    def test_08_chat_feedback_api(self):
        """Verify /api/feedback saves user rating and comments."""
        res = self.client.post('/api/feedback', json={
            'message_id': 1,
            'rating': 5,
            'comment': 'Accurate response on course fee!'
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json().get('status'), 'ok')
        print("✓ /api/feedback recorded user satisfaction metrics")

if __name__ == '__main__':
    print("\n" + "=" * 65)
    print("  RUNNING FULL API INTEGRATION & PORTAL TEST SUITE")
    print("=" * 65)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIIntegration)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n" + "=" * 65)
        print("  ALL API INTEGRATION & PORTAL ROUTE TESTS PASSED!")
        print("=" * 65 + "\n")
        sys.exit(0)
    else:
        print("\n" + "=" * 65)
        print("  SOME TESTS FAILED!")
        print("=" * 65 + "\n")
        sys.exit(1)
