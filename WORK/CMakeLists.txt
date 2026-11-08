cmake_minimum_required(VERSION 3.20)
project(crypto_test LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenSSL REQUIRED)

add_executable(crypto_driver
    crypto_driver.cpp
    crypto_utils.cpp
)

target_include_directories(crypto_driver PRIVATE ${OpenSSL_INCLUDE_DIR})
target_link_libraries(crypto_driver PRIVATE OpenSSL::SSL OpenSSL::Crypto)

# ---------- Tests ----------
add_executable(test_crypto
    tests/test_crypto.cpp
    crypto_utils.cpp
)
target_include_directories(test_crypto PRIVATE ${OpenSSL_INCLUDE_DIR})
target_link_libraries(test_crypto PRIVATE OpenSSL::SSL OpenSSL::Crypto)
enable_testing()
add_test(NAME CryptoUnitTest COMMAND test_crypto)
