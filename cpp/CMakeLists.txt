cmake_minimum_required(VERSION 3.0)

include(ExternalProject)

project(pylibtermkey_cpp VERSION ${VERSION_INFO})

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(thirdparty/pybind11)

set(LIBTERMKEY_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/libtermkey)
set(LIBTERMKEY_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/thirdparty/libtermkey)

set(PYLIBTERMKEY_LIBS ".libspylibtermkey_cpp")

if (NOT CMAKE_LIBRARY_OUTPUT_DIRECTORY)
    set(LIBTERMKEY_LIB_DIR "${LIBTERMKEY_BINARY_DIR}/${PYLIBTERMKEY_LIBS}")
else()
    set(LIBTERMKEY_LIB_DIR "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/${PYLIBTERMKEY_LIBS}")
endif()

file(MAKE_DIRECTORY ${LIBTERMKEY_LIB_DIR})

if (APPLE)
    SET(LIB_PATH "@loader_path")
else()
    SET(LIB_PATH "$ORIGIN")
endif()

ExternalProject_Add(libtermkey
    PREFIX ${LIBTERMKEY_BINARY_DIR}
    SOURCE_DIR ${LIBTERMKEY_SOURCE_DIR}
    BINARY_DIR ${LIBTERMKEY_BINARY_DIR}
    # this copy is used to build libtermkey out of tree, but it can cause make not realize that 
    # the libtermkey source files are updated; if modifying the libtermkey source files in this project
    # a clean build or modification to this project structure is required
    CONFIGURE_COMMAND cp -r ${LIBTERMKEY_SOURCE_DIR}/. ${LIBTERMKEY_BINARY_DIR}
    BUILD_COMMAND make
    INSTALL_COMMAND /bin/bash -c "cp -P ${LIBTERMKEY_BINARY_DIR}/.libs/libtermkey*${CMAKE_SHARED_LIBRARY_SUFFIX}* ${LIBTERMKEY_LIB_DIR}")

set(LIBTERMKEY_LIB ${LIBTERMKEY_LIB_DIR}/libtermkey${CMAKE_SHARED_LIBRARY_SUFFIX})

pybind11_add_module(pylibtermkey_cpp src/pylibtermkey_bind.cpp)
set(RPATH
    ${CMAKE_BUILD_RPATH}
    ${LIB_PATH}/${PYLIBTERMKEY_LIBS}
)
SET_TARGET_PROPERTIES(pylibtermkey_cpp PROPERTIES BUILD_RPATH ${RPATH})
add_dependencies(pylibtermkey_cpp libtermkey)
add_dependencies(pylibtermkey_cpp pybind11)
target_include_directories(pylibtermkey_cpp
    PUBLIC thirdparty/pybind11 ${LIBTERMKEY_BINARY_DIR})
target_link_libraries(pylibtermkey_cpp PUBLIC ${LIBTERMKEY_LIB})

# on macOS, patch the pylibtermkey_cpp library to point to a relative libtermkey
if (APPLE)
    add_custom_command(TARGET pylibtermkey_cpp POST_BUILD COMMAND install_name_tool -change /usr/local/lib/libtermkey.1.dylib @rpath/libtermkey.1.dylib $<TARGET_FILE:pylibtermkey_cpp>)
endif()
