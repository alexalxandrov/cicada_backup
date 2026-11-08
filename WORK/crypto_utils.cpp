#include "crypto_utils.hpp"
#include <iomanip>

// Helper to throw on EVP errors
static void check_evp(int ret) {
    if (ret <= 0) {
        throw std::runtime_error("OpenSSL EVP error");
    }
}

// ---------------------------------------------------------------------------
// AES‑256‑CBC helpers
// ---------------------------------------------------------------------------
CryptoResult CryptoUtils::encrypt_aes_256_cbc(
    const std::string &plaintext,
    const std::vector<unsigned char> &key,
    const std::vector<unsigned char> &iv) {
    CryptoResult res;
    res.iv = iv;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) throw std::runtime_error("Failed to create EVP_CIPHER_CTX");
    try {
        check_evp(EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key.data(), iv.data()));
        int outlen = plaintext.size() + EVP_CIPHER_block_size(EVP_aes_256_cbc());
        res.ciphertext.resize(outlen);
        int tmp_len = 0;
        check_evp(EVP_EncryptUpdate(ctx, res.ciphertext.data(), &tmp_len,
            reinterpret_cast<const unsigned char *>(plaintext.data()), plaintext.size()));
        res.ciphertext.resize(tmp_len);
        int final_len = 0;
        check_evp(EVP_EncryptFinal_ex(ctx, res.ciphertext.data() + tmp_len, &final_len));
        res.ciphertext.resize(tmp_len + final_len);
        // tag unused for CBC
    } catch (...) {
        EVP_CIPHER_CTX_free(ctx);
        throw;
    }
    EVP_CIPHER_CTX_free(ctx);
    return res;
}

std::string CryptoUtils::decrypt_aes_256_cbc(
    const CryptoResult &res,
    const std::vector<unsigned char> &key) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) throw std::runtime_error("Failed to create EVP_CIPHER_CTX");
    try {
        check_evp(EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key.data(), res.iv.data()));
        int outlen = res.ciphertext.size() + EVP_CIPHER_block_size(EVP_aes_256_cbc());
        std::vector<unsigned char> plaintext(outlen);
        int tmp_len = 0;
        check_evp(EVP_DecryptUpdate(ctx, plaintext.data(), &tmp_len, res.ciphertext.data(), res.ciphertext.size()));
        int final_len = 0;
        check_evp(EVP_DecryptFinal_ex(ctx, plaintext.data() + tmp_len, &final_len));
        plaintext.resize(tmp_len + final_len);
        return std::string(reinterpret_cast<const char *>(plaintext.data()), plaintext.size());
    } catch (...) {
        EVP_CIPHER_CTX_free(ctx);
        throw;
    }
    EVP_CIPHER_CTX_free(ctx);
}

// ---------------------------------------------------------------------------
// ChaCha20‑Poly1305 helpers
// ---------------------------------------------------------------------------
CryptoResult CryptoUtils::encrypt_chacha20_poly1305(
    const std::string &plaintext,
    const std::vector<unsigned char> &key,
    const std::vector<unsigned char> &iv,
    const std::vector<unsigned char> &aad) {
    CryptoResult res;
    res.iv = iv;
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) throw std::runtime_error("Failed to create EVP_CIPHER_CTX");
    try {
        check_evp(EVP_EncryptInit_ex(ctx, EVP_chacha20_poly1305(), nullptr, nullptr, nullptr));
        check_evp(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, iv.size(), nullptr));
        check_evp(EVP_EncryptInit_ex(ctx, nullptr, nullptr, key.data(), iv.data()));
        int outlen = 0;
        if (!aad.empty()) {
            check_evp(EVP_EncryptUpdate(ctx, nullptr, &outlen, aad.data(), aad.size()));
        }
        res.ciphertext.resize(plaintext.size());
        check_evp(EVP_EncryptUpdate(ctx, res.ciphertext.data(), &outlen, reinterpret_cast<const unsigned char *>(plaintext.data()), plaintext.size()));
        res.ciphertext.resize(outlen);
        res.tag.resize(16); // Poly1305 tag length
        check_evp(EVP_EncryptFinal_ex(ctx, res.ciphertext.data() + outlen, &outlen));
        res.ciphertext.resize(res.ciphertext.size() + outlen);
        check_evp(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_GET_TAG, 16, res.tag.data()));
    } catch (...) {
        EVP_CIPHER_CTX_free(ctx);
        throw;
    }
    EVP_CIPHER_CTX_free(ctx);
    return res;
}

std::string CryptoUtils::decrypt_chacha20_poly1305(
    const CryptoResult &res,
    const std::vector<unsigned char> &key,
    const std::vector<unsigned char> &aad) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) throw std::runtime_error("Failed to create EVP_CIPHER_CTX");
    try {
        check_evp(EVP_DecryptInit_ex(ctx, EVP_chacha20_poly1305(), nullptr, nullptr, nullptr));
        check_evp(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_IVLEN, res.iv.size(), nullptr));
        check_evp(EVP_DecryptInit_ex(ctx, nullptr, nullptr, key.data(), res.iv.data()));
        if (!aad.empty()) {
            check_evp(EVP_DecryptUpdate(ctx, nullptr, nullptr, aad.data(), aad.size()));
        }
        std::vector<unsigned char> plaintext(res.ciphertext.size());
        int outlen = 0;
        check_evp(EVP_DecryptUpdate(ctx, plaintext.data(), &outlen, res.ciphertext.data(), res.ciphertext.size()));
        plaintext.resize(outlen);
        check_evp(EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_AEAD_SET_TAG, 16, const_cast<unsigned char *>(res.tag.data())));
        check_evp(EVP_DecryptFinal_ex(ctx, plaintext.data() + outlen, &outlen));
        plaintext.resize(plaintext.size() + outlen);
        return std::string(reinterpret_cast<const char *>(plaintext.data()), plaintext.size());
    } catch (...) {
        EVP_CIPHER_CTX_free(ctx);
        throw;
    }
    EVP_CIPHER_CTX_free(ctx);
}
