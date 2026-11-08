#include "crypto_utils.hpp"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <chrono>

static std::string to_hex(const std::vector<unsigned char> &v) {
    std::ostringstream oss;
    for (unsigned char c : v) {
        oss << std::hex << std::setw(2) << std::setfill('0') << (int)c;
    }
    return oss.str();
}

// Generate random bytes using OpenSSL RAND_bytes
static std::vector<unsigned char> rand_bytes(size_t len) {
    std::vector<unsigned char> buf(len);
    if (RAND_bytes(buf.data(), len) != 1) {
        throw std::runtime_error("RAND_bytes failed");
    }
    return buf;
}

int main() {
    std::string plaintext = "The quick brown fox jumps over the lazy dog.";
    std::cout << "Plaintext: " << plaintext << "\n";

    /*
    // AES‑256‑CBC (currently disabled due to OpenSSL 3 compatibility issues)
    auto key_aes = rand_bytes(32);
    auto iv_aes = rand_bytes(16);
    CryptoResult enc_aes = CryptoUtils::encrypt_aes_256_cbc(plaintext, key_aes, iv_aes);
    std::cout << "AES‑CBC ciphertext: " << to_hex(enc_aes.ciphertext) << "\n";
    std::string dec_aes = CryptoUtils::decrypt_aes_256_cbc(enc_aes, key_aes);
    std::cout << "AES‑CBC decrypted: " << dec_aes << "\n";
    std::cout << "AES‑CBC success: " << (dec_aes == plaintext) << "\n\n";
    */

    // ChaCha20‑Poly1305
    auto key_chacha = rand_bytes(32);
    auto iv_chacha = rand_bytes(12); // nonce size for ChaCha20
    std::vector<unsigned char> aad; // empty AAD
    CryptoResult enc_chacha = CryptoUtils::encrypt_chacha20_poly1305(plaintext, key_chacha, iv_chacha, aad);
    std::cout << "ChaCha20‑Poly1305 ciphertext: " << to_hex(enc_chacha.ciphertext) << "\n";
    std::cout << "Tag: " << to_hex(enc_chacha.tag) << "\n";
    std::string dec_chacha = CryptoUtils::decrypt_chacha20_poly1305(enc_chacha, key_chacha, aad);
    std::cout << "ChaCha20‑Poly1305 decrypted: " << dec_chacha << "\n";
    std::cout << "ChaCha20‑Poly1305 success: " << (dec_chacha == plaintext) << "\n\n";

    // Simple benchmark
    const int iterations = 1000;
    std::string dummy = std::string(1024, 'a'); // 1 KiB
    // Disable AES benchmark to avoid OpenSSL 3 issues
    auto bench_aes = [&]() {};
    auto bench_chacha = [&]() {
        auto k = rand_bytes(32);
        auto iv = rand_bytes(12);
        CryptoResult r = CryptoUtils::encrypt_chacha20_poly1305(dummy, k, iv, {});
        CryptoUtils::decrypt_chacha20_poly1305(r, k, {});
    };

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) bench_aes();
    auto mid = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) bench_chacha();
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> dur_aes = mid - start;
    std::chrono::duration<double> dur_chacha = end - mid;
    std::cout << "AES‑256‑CBC " << iterations << " ops: " << dur_aes.count() << " s\n";
    std::cout << "ChaCha20‑Poly1305 " << iterations << " ops: " << dur_chacha.count() << " s\n";

    return 0;
}
