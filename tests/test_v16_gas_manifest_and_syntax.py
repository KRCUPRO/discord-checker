# tests/test_v16_gas_manifest_and_syntax.py
# Unit test for D4UC Google Apps Script 24/7 Engine
import unittest
import json
import os


class TestGasManifestAndSyntax(unittest.TestCase):
    def setUp(self):
        # Resolve path relative to tests directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.gas_js_path = os.path.join(base_dir, 'gas', 'D4UC_Checker.js')
        self.gas_manifest_path = os.path.join(base_dir, 'gas', 'appsscript.json')

    def test_appsscript_json_validity(self):
        self.assertTrue(os.path.exists(self.gas_manifest_path), f"appsscript.json does not exist at {self.gas_manifest_path}")
        with open(self.gas_manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        self.assertEqual(manifest.get("runtimeVersion"), "V8")
        self.assertIn("oauthScopes", manifest)
        scopes = manifest["oauthScopes"]
        self.assertIn("https://www.googleapis.com/auth/script.external_request", scopes)
        self.assertIn("https://www.googleapis.com/auth/drive", scopes)
        self.assertIn("https://www.googleapis.com/auth/spreadsheets", scopes)
        self.assertIn("https://www.googleapis.com/auth/script.scriptapp", scopes)

    def test_gas_script_structure_and_functions(self):
        self.assertTrue(os.path.exists(self.gas_js_path), f"D4UC_Checker.js does not exist at {self.gas_js_path}")
        with open(self.gas_js_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Check critical functions
        expected_functions = [
            'initD4UCChecker',
            'stopD4UCChecker',
            'setupScheduledTrigger',
            'clearAllTriggers',
            'runCheckerBatch',
            'checkDiscordUsername',
            'getOrCreateFolder',
            'appendAvailableToFile',
            'saveStateToDriveJson',
            'getOrCreateSpreadsheet',
            'appendAvailableToSheet',
            'isColabActive',
            'indexToUsername',
            'sendDiscordWebhookAvailable'
        ]
        for fn in expected_functions:
            self.assertRegex(code, rf'function\s+{fn}\s*\(', f"Function {fn} missing in D4UC_Checker.js")

        # Check CONFIG presence and parameters
        self.assertIn("const CONFIG = {", code)
        self.assertIn("EXECUTION_MODE", code)
        self.assertIn("TRIGGER_MODE", code)
        self.assertIn("MAX_EXECUTION_TIME_MS: 270000", code)
        self.assertIn("DRIVE_FOLDER_NAME", code)
        self.assertIn("ENABLE_SPREADSHEET", code)


if __name__ == '__main__':
    unittest.main()
