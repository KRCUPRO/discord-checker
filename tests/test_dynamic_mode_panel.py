# tests/test_dynamic_mode_panel.py
import sys
from pathlib import Path

root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(root))

from src.generator import (
    create_generator,
    MaskPatternGenerator,
    NumericGenerator,
    DictionaryGenerator,
    PatternGenerator,
    PermutationGenerator,
    RandomGenerator,
    HybridGenerator
)
from src.generator.base import DiscordRuleValidator

def test_all_mode_generators():
    print("[TEST 1] Testing generator output across all 7 modes and lengths (3, 4, 5, 6)...")
    modes = ["hybrid", "custom", "numeric", "dictionary", "pattern", "permutation", "random"]
    lengths = [3, 4, 5, 6]

    for m in modes:
        for l in lengths:
            cfg = {"mode": m, "length": l}
            if m == "custom":
                cfg["prefix"] = "a"
                cfg["suffix"] = "z"
            gen = create_generator(cfg)
            samples = []
            for _ in range(10):
                cand = gen.next_username()
                if cand:
                    samples.append(cand)
                    assert len(cand) == l, f"Mode {m} length {l} generated wrong length: {cand} (len {len(cand)})"
                    assert DiscordRuleValidator.is_valid(cand), f"Invalid per Discord rules: {cand}"
            print(f"   • Mode: {m:12s} | Length: {l} | Verified {len(samples)} samples: {samples[:3]}")

    print("   ✅ Test 1 Passed: All 7 mode generators generate valid usernames for all lengths.")

def test_custom_mask_prefix_suffix_dot():
    print("[TEST 2] Testing Custom Mask with prefix, suffix, middle dot...")
    # Len 5, suffix vip, middle dot required -> ?.vip
    gen = MaskPatternGenerator(length=5, suffix="vip", middle_dot="required")
    mask = gen._resolve_mask()
    assert mask == "?.vip", f"Expected '?.vip', got '{mask}'"
    for _ in range(20):
        c = gen.next_username()
        assert len(c) == 5
        assert c.endswith("vip")
        assert c[1] == "."
    print(f"   • Custom Mask '?.vip' verified: 20 samples (e.g. {c})")
    print("   ✅ Test 2 Passed: Custom mask behavior verified.")

def main():
    print("=====================================================================")
    print("🚀 [D4UC V2] Dynamic Mode Panel & All Generator Testing")
    print("=====================================================================")
    test_all_mode_generators()
    test_custom_mask_prefix_suffix_dot()
    print("=====================================================================")
    print("🎉 ALL DYNAMIC MODE GENERATOR TESTS PASSED WITH EXIT CODE 0!")
    print("=====================================================================")

if __name__ == "__main__":
    main()
