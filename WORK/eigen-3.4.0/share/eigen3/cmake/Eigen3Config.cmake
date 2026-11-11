# Minimal CMake configuration file for Eigen3.
# This file is used by CMake's `find_package(Eigen3 ...)` to provide
# include directories, target definitions, and version information.
# It follows the same format as the top‑level configuration file so that
# both paths are interchangeable.

set(EIGEN3_VERSION_STRING "3.4.0")
set(EIGEN3_VERSION "3.4.0")
set(EIGEN3_FOUND TRUE)
set(EIGEN3_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/../../Eigen")
set(EIGEN3_INCLUDE_DIRS "${EIGEN3_INCLUDE_DIR}")
set(EIGEN3_LIBRARIES "")
set(EIGEN3_ROOT "${CMAKE_CURRENT_LIST_DIR}/../..")
set(EIGEN3_VERSION_OK TRUE)

if(NOT TARGET Eigen3::Eigen)
  add_library(Eigen3::Eigen INTERFACE)
  target_include_directories(Eigen3::Eigen INTERFACE ${EIGEN3_INCLUDE_DIRS})
endif()
