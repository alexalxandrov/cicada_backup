# -----------------------------------------------------------------------------
# Minimal CMake configuration file for Eigen3.
# -----------------------------------------------------------------------------
# This file is used by CMake's `find_package(Eigen3 ...)` to provide
# include directories, target definitions, and version information.
#
# The FindEigen3.cmake module looks for the following lines using a regular
# expression that matches *exactly* the pattern:
#   set(EIGEN3_VERSION_STRING "<ver>")
#   set(EIGEN3_VERSION "<ver>")
# Therefore the syntax must match the upstream source exactly: no spaces
# after the opening parenthesis, the string must be quoted, and no trailing
# comments are allowed.
set(EIGEN3_VERSION_STRING "3.4.0")
set(EIGEN3_VERSION "3.4.0")
# Keep backward compatibility with older scripts that may include the
# cached version file.
include(${CMAKE_CURRENT_LIST_DIR}/Eigen3ConfigVersion.cmake)
# The original file may define EIGEN3_VERSION_OK; we provide a default if
# it is not set.
if(NOT DEFINED EIGEN3_VERSION_OK)
  set(EIGEN3_VERSION_OK TRUE)
endif()
# Basic metadata used by consumers.
set(EIGEN3_FOUND TRUE)
set(EIGEN3_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/Eigen")
set(EIGEN3_INCLUDE_DIRS "${EIGEN3_INCLUDE_DIR}")
set(EIGEN3_LIBRARIES "")
set(EIGEN3_ROOT "${CMAKE_CURRENT_LIST_DIR}")
# Provide an INTERFACE library that consumers can link against.
if(NOT TARGET Eigen3::Eigen)
  add_library(Eigen3::Eigen INTERFACE)
  target_include_directories(Eigen3::Eigen INTERFACE ${EIGEN3_INCLUDE_DIRS})
endif()
