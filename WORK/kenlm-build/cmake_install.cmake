# Install script for directory: /Users/oleg/Documents/GitHub/cicada_backup/kenlm

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake/kenlmTargets.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake/kenlmTargets.cmake"
         "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/CMakeFiles/Export/f61db19fcc8b11c56ccf9a2f68669a85/kenlmTargets.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake/kenlmTargets-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake/kenlmTargets.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake" TYPE FILE FILES "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/CMakeFiles/Export/f61db19fcc8b11c56ccf9a2f68669a85/kenlmTargets.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake" TYPE FILE FILES "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/CMakeFiles/Export/f61db19fcc8b11c56ccf9a2f68669a85/kenlmTargets-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/util" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/bit_packing.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/ersatz_progress.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/exception.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/fake_ostream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/file.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/file_piece.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/file_stream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/fixed_array.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/float_to_string.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/getopt.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/have.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/integer_to_string.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/joint_sort.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/mmap.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/multi_intersection.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/murmur_hash.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/parallel_read.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/pcqueue.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/pool.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/probing_hash_table.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/proxy_iterator.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/read_compressed.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/scoped.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/sized_iterator.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/sorted_uniform.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/spaces.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/string_piece.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/string_piece_hash.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/string_stream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/thread_pool.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/tokenize_piece.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/usage.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/util/double-conversion" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/bignum-dtoa.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/bignum.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/cached-powers.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/diy-fp.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/double-conversion.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/double-to-string.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/fast-dtoa.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/fixed-dtoa.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/ieee.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/string-to-double.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/strtod.h"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/double-conversion/utils.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/util/stream" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/block.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/chain.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/config.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/count_records.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/io.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/line_input.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/multi_progress.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/multi_stream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/rewindable_stream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/sort.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/stream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/util/stream/typed_stream.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/lm" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/bhiksha.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/binary_format.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/blank.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/config.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/enumerate_vocab.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/facade.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/left.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/lm_exception.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/max_order.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/model.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/model_type.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/ngram_query.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/partial.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/quantize.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/read_arpa.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/return.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/search_hashed.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/search_trie.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/sizes.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/state.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/trie.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/trie_sort.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/value.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/value_build.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/virtual_interface.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/vocab.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/weights.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/word_index.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/lm/builder" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/adjust_counts.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/combine_counts.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/corpus_count.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/debug_print.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/discount.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/hash_gamma.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/header_info.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/initial_probabilities.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/interpolate.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/output.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/payload.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/builder/pipeline.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/lm/common" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/compare.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/joint_order.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/model_buffer.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/ngram.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/ngram_stream.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/print.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/renumber.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/size_option.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/common/special.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/lm/filter" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/arpa_io.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/count_io.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/format.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/phrase.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/thread.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/vocab.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/filter/wrapper.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "headers" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kenlm/lm/interpolate" TYPE FILE FILES
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/backoff_matrix.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/backoff_reunification.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/bounded_sequence_encoding.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/interpolate_info.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/merge_probabilities.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/merge_vocab.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/normalize.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/pipeline.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/split_worker.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/tune_derivatives.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/tune_instances.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/tune_matrix.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/tune_weights.hh"
    "/Users/oleg/Documents/GitHub/cicada_backup/kenlm/lm/interpolate/universal_vocab.hh"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/kenlm/cmake" TYPE FILE FILES "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/kenlmConfig.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/util/cmake_install.cmake")
  include("/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/lm/cmake_install.cmake")

endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
if(CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_COMPONENT MATCHES "^[a-zA-Z0-9_.+-]+$")
    set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
  else()
    string(MD5 CMAKE_INST_COMP_HASH "${CMAKE_INSTALL_COMPONENT}")
    set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INST_COMP_HASH}.txt")
    unset(CMAKE_INST_COMP_HASH)
  endif()
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/Users/oleg/Documents/GitHub/cicada_backup/kenlm-build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
