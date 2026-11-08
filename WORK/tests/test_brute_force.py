import unittest
from ciphers.brute_force import brute_caesar, brute_vigenere, find_best_candidate


class TestBruteForce(unittest.TestCase):
    def test_caesar(self):
        ciphertext = "Uifsf"
        # Shift 1 should decrypt to "There"
        decryptions = brute_caesar(ciphertext)
        # find the entry with shift 1
        found = next((s, p) for s, p in decryptions if s == 1)
        self.assertEqual(found[1], "There")

    def test_vigenere(self):
        ciphertext = "LXFOPVEFRNHR"
        # Known key "LEMON" gives plaintext "ATTACKATDAWN"
        decryptions = brute_vigenere(ciphertext, max_key_len=5)
        # Locate the result for the known key "lemon"
        lemon_plain = next((p for k, p in decryptions if k == "lemon"), None)
        self.assertIsNotNone(lemon_plain)
        self.assertEqual(lemon_plain, "ATTACKATDAWN")

    def test_best_candidate_no_match(self):
        # Provide decryptions that produce no dictionary words
        decryptions = [("x", "zzzzzz")]
        best = find_best_candidate(decryptions)
        self.assertEqual(best[2], 0)


if __name__ == "__main__":
    unittest.main()
