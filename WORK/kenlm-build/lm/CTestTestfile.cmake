# CMake generated Testfile for 
# Source directory: /Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm
# Build directory: /Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/lm
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(left_test "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/tests/left_test" "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/test.arpa")
set_tests_properties(left_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/cmake/KenLMFunctions.cmake;61;add_test;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/cmake/KenLMFunctions.cmake;76;KenLMAddTest;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/CMakeLists.txt;71;AddTests;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/CMakeLists.txt;0;")
add_test(partial_test "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/tests/partial_test" "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/test.arpa")
set_tests_properties(partial_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/cmake/KenLMFunctions.cmake;61;add_test;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/cmake/KenLMFunctions.cmake;76;KenLMAddTest;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/CMakeLists.txt;71;AddTests;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/CMakeLists.txt;0;")
add_test(model_test "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/tests/model_test" "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/test.arpa" "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/test_nounk.arpa")
set_tests_properties(model_test PROPERTIES  _BACKTRACE_TRIPLES "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/cmake/KenLMFunctions.cmake;61;add_test;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/CMakeLists.txt;76;KenLMAddTest;/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/CMakeLists.txt;0;")
subdirs("common")
subdirs("builder")
subdirs("filter")
subdirs("interpolate")
