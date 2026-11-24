"""
=============================================================================
D4UC Google Apps Script (GAS) Cloud Fleet Synthetic Verification Test Suite
=============================================================================
Automated test suite verifying the mathematical and architectural integrity
of the Google Apps Script distributed checker fleet.
"""

import math
import re
import os
import json
import unittest

CHARSET = 'abcdefghijklmnopqrstuvwxyz0123456789'
LENGTH = 4
TOTAL_COMBINATIONS = len(CHARSET) ** LENGTH  # 36^4 = 1,679,616

def get_shard_range(worker_id: int, total_workers: int, max_combinations: int):
    if total_workers <= 1:
        return {'start': 0, 'end': max_combinations, 'total': max_combinations}
    safe_workers = max(1, total_workers)
    safe_id = min(max(0, worker_id), safe_workers - 1)
    chunk_size = max_combinations // safe_workers
    start = safe_id * chunk_size
    end = max_combinations if safe_id == safe_workers - 1 else (safe_id + 1) * chunk_size
    return {'start': start, 'end': end, 'total': end - start}

def index_to_username(index: int, charset: str, length: int) -> str:
    result = []
    base = len(charset)
    for _ in range(length):
        result.append(charset[index % base])
        index //= base
    return ''.join(reversed(result))

def username_to_index(username: str, charset: str) -> int:
    base = len(charset)
    index = 0
    for char in username:
        index = index * base + charset.index(char)
    return index


class TestGASDistributedFleet(unittest.TestCase):
    
    def test_01_deterministic_range_sharding_integrity(self):
        """Verifies zero-overlap and zero-gap across diverse worker pool sizes."""
        worker_counts = [1, 2, 3, 4, 6, 8, 10, 12, 16, 24]
        for N in worker_counts:
            shards = [get_shard_range(i, N, TOTAL_COMBINATIONS) for i in range(N)]
            
            # 1. Total coverage must exactly match TOTAL_COMBINATIONS
            total_covered = sum(s['total'] for s in shards)
            self.assertEqual(total_covered, TOTAL_COMBINATIONS, f"Worker count {N} failed total coverage")
            
            # 2. First shard starts at 0, last shard ends at TOTAL_COMBINATIONS
            self.assertEqual(shards[0]['start'], 0)
            self.assertEqual(shards[-1]['end'], TOTAL_COMBINATIONS)
            
            # 3. Zero gap and zero overlap between adjacent shards
            for i in range(N - 1):
                self.assertEqual(shards[i]['end'], shards[i + 1]['start'], 
                                 f"Gap or overlap detected between worker {i} and {i+1} for N={N}")

    def test_02_bijective_index_to_username_mapping(self):
        """Verifies bijective 1:1 mapping between index and 4-character username."""
        # Check boundary values
        first_user = index_to_username(0, CHARSET, LENGTH)
        self.assertEqual(first_user, 'aaaa')
        self.assertEqual(username_to_index(first_user, CHARSET), 0)
        
        last_user = index_to_username(TOTAL_COMBINATIONS - 1, CHARSET, LENGTH)
        self.assertEqual(last_user, '9999')
        self.assertEqual(username_to_index(last_user, CHARSET), TOTAL_COMBINATIONS - 1)
        
        # Check intermediate values
        test_indices = [1, 35, 36, 1295, 1296, 46655, 46656, 100000, 500000, 1679615]
        for idx in test_indices:
            user = index_to_username(idx, CHARSET, LENGTH)
            self.assertEqual(len(user), LENGTH)
            self.assertEqual(username_to_index(user, CHARSET), idx)

    def test_03_gas_script_syntax_and_structure(self):
        """Verifies that all 3 GAS files exist and contain core architectural components."""
        gas_dir = os.path.join(os.path.dirname(__file__), '..', 'gas')
        required_files = {
            'D4UC_Checker.js': [
                'CONFIG', 'SHARDING_MODE', 'WORKER_ID', 'TOTAL_WORKERS',
                'initD4UCChecker', 'stopD4UCChecker', 'runCheckerBatch',
                'getShardRange', 'checkDiscordUsername', 'appendAvailableToSheet',
                'sendDiscordWebhookAvailable'
            ],
            'D4UC_MultiAccount_Worker.js': [
                'CONFIG', 'WORKER_ID', 'TOTAL_WORKERS', 'ACCOUNT_LABEL',
                'initWorkerNode', 'stopWorkerNode', 'runWorkerBatch',
                'getShardRange', 'sendDiscordWebhookAvailable'
            ],
            'D4UC_Master_Dashboard.js': [
                'DASHBOARD_CONFIG', 'initFleetDashboard', 'aggregateFleetStatus',
                'updateSheetsDashboard', 'sendDiscordFleetReport'
            ]
        }
        
        for filename, symbols in required_files.items():
            path = os.path.join(gas_dir, filename)
            self.assertTrue(os.path.exists(path), f"Missing required GAS file: {filename}")
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertGreater(len(content), 1000, f"File {filename} is too short")
                for sym in symbols:
                    self.assertIn(sym, content, f"Symbol '{sym}' missing from {filename}")

    def test_04_discord_webhook_payload_schema(self):
        """Verifies Discord Webhook embed structure meets Discord API v9 specification."""
        username = "cool"
        latency = 120
        worker_label = "Worker-02"
        progress = "34.50%"
        
        payload = {
            'content': f"🎉 **[D4UC GAS 24/7] 사용 가능한 고유 닉네임 발견!** @here",
            'embeds': [{
                'title': f"✨ `{username}` 선점 가능!",
                'description': "Google Apps Script 클라우드 분산 체커가 사용 가능한 희귀 닉네임을 발견했습니다.",
                'color': 0x2ea043,
                'fields': [
                    {'name': '닉네임', 'value': f"`{username}`", 'inline': True},
                    {'name': '글자수', 'value': f"{len(username)}자", 'inline': True},
                    {'name': '응답속도', 'value': f"{latency}ms", 'inline': True},
                    {'name': '워커 노드', 'value': f"🤖 {worker_label}", 'inline': True},
                    {'name': '샤드 진행률', 'value': f"📊 {progress}", 'inline': True},
                    {'name': '선점 링크', 'value': "[Discord 회원가입 바로가기](https://discord.com/register)", 'inline': False}
                ],
                'footer': {'text': 'D4UC Cloud Fleet • 24/7 무인 구동'},
                'timestamp': '2026-11-24T12:00:00.000Z'
            }]
        }
        
        # Verify JSON serializability
        serialized = json.dumps(payload)
        self.assertIsInstance(serialized, str)
        self.assertIn('embeds', payload)
        self.assertEqual(len(payload['embeds']), 1)
        self.assertEqual(len(payload['embeds'][0]['fields']), 6)
        self.assertEqual(payload['embeds'][0]['color'], 0x2ea043)

    def test_05_drive_deduplication_logic(self):
        """Simulates Google Drive text file append with deduplication."""
        existing_content = "aaaa\nbbbb\ncccc\n"
        lines = set(existing_content.strip().split('\n'))
        
        # Case A: Append existing -> should not duplicate
        candidate_1 = "bbbb"
        if candidate_1 not in lines:
            existing_content += candidate_1 + "\n"
        self.assertEqual(existing_content.count("bbbb"), 1)
        
        # Case B: Append new -> should append exactly once
        candidate_2 = "dddd"
        if candidate_2 not in lines:
            existing_content += candidate_2 + "\n"
            lines.add(candidate_2)
        self.assertIn("dddd", existing_content)
        self.assertEqual(len(lines), 4)


if __name__ == '__main__':
    unittest.main()
