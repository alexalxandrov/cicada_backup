#include "../crypto_utils.hpp"
#include <cassert>
#include <vector>
#include <string>
#include <iostream>

int main() {
    std::string plaintext = "Hello, world!";
    std::vector<unsigned char> key(32, 0); // all zero key
    std::vector<unsigned char> nonce(12, 0); // all zero nonce
    std::vector<unsigned char> aad; // empty

    // ChaCha20-Poly1305 encryption/decryption
    CryptoResult enc = CryptoUtils::encrypt_chacha20_poly1305(plaintext, key, nonce, aad);
    std::string dec = CryptoUtils::decrypt_chacha20_poly1305(enc, key, aad);
    assert(dec == plaintext);

    // Verify tag length 16
    assert(enc.tag.size() == 16);

    std::cout << "Crypto test passed.\n";
    return 0;
}
