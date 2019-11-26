cmake_minimum_required(VERSION 3.1)
include(ExternalProject)
project(pylegu)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/")
set(THIRD_PARTY_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/third-party/")
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR} CACHE PATH "Install path prefix prepended on to install directories." FORCE)
endif()

# CCACHE
# ======
find_program(CCACHE_FOUND ccache)
message(STATUS "ccache: ${ASI_USE_CCACHE}")
if(CCACHE_FOUND)
  set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE ccache)
  set_property(GLOBAL PROPERTY RULE_LAUNCH_LINK ccache)
endif()

set(PYBIND11_VERSION 2.4.3)
set(PYBIND11_URL "${THIRD_PARTY_DIRECTORY}/pybind11-${PYBIND11_VERSION}.zip" CACHE STRING "URL to the Pybind11 repo")
ExternalProject_Add(pybind11
  URL               ${PYBIND11_URL}
  CONFIGURE_COMMAND ""
  BUILD_COMMAND     ""
  INSTALL_COMMAND   "")
ExternalProject_get_property(pybind11 SOURCE_DIR)
set(PYBIND11_SOURCE_DIR "${SOURCE_DIR}")

set(UCL_VERSION 1.03)
set(UCL_URL "${THIRD_PARTY_DIRECTORY}/ucl-${UCL_VERSION}.tar.gz" CACHE STRING "URL to the UCL")
set(UCL_INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/UCL)
set(UCL_PREFIX_DIR  ${UCL_INSTALL_DIR})

ExternalProject_Add(ucl
  URL               ${UCL_URL}
  PREFIX            ${UCL_PREFIX_DIR}
  CONFIGURE_COMMAND ${UCL_PREFIX_DIR}/src/ucl/configure --prefix=${UCL_INSTALL_DIR} --with-pic
  BUILD_COMMAND     ${MAKE}
  BUILD_IN_SOURCE   1
  UPDATE_COMMAND    ""
  BUILD_ALWAYS      0
)
include_directories("${UCL_INSTALL_DIR}/include")

set(Python_ADDITIONAL_VERSIONS 3.7 3.6 3.5 3.4)
find_package(PythonLibsNew REQUIRED)

add_library(pylegu SHARED pyLegu.cpp)

set_property(TARGET pylegu PROPERTY CXX_STANDARD 11)
set_property(TARGET pylegu PROPERTY CXX_STANDARD_REQUIRED ON)

target_include_directories(pylegu PUBLIC
  "${CMAKE_CURRENT_SOURCE_DIR}/"
  "${PYTHON_INCLUDE_DIR}"
  "${PYBIND11_SOURCE_DIR}/include"
  "${UCL_INSTALL_DIR}/include"
)

target_link_libraries(pylegu ${UCL_INSTALL_DIR}/lib/libucl.a)

add_dependencies(pylegu pybind11 ucl)

set_target_properties(pylegu PROPERTIES PREFIX "")
set_target_properties(pylegu PROPERTIES SUFFIX ".so")

