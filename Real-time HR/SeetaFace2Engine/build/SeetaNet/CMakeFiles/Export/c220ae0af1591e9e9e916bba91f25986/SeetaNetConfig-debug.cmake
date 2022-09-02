#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaNet" for configuration "Debug"
set_property(TARGET SeetaFace::SeetaNet APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(SeetaFace::SeetaNet PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/SeetaNet_d.lib"
  IMPORTED_LINK_INTERFACE_LIBRARIES_DEBUG "Ws2_32"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/SeetaNet_d.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaNet )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaNet "${_IMPORT_PREFIX}/lib/SeetaNet_d.lib" "${_IMPORT_PREFIX}/bin/SeetaNet_d.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
