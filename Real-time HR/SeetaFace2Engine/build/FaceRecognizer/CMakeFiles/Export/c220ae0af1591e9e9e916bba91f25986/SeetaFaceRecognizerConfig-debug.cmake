#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaFaceRecognizer" for configuration "Debug"
set_property(TARGET SeetaFace::SeetaFaceRecognizer APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(SeetaFace::SeetaFaceRecognizer PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/SeetaFaceRecognizer_d.lib"
  IMPORTED_LINK_INTERFACE_LIBRARIES_DEBUG "SeetaFace::SeetaNet"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/SeetaFaceRecognizer_d.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaFaceRecognizer )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaFaceRecognizer "${_IMPORT_PREFIX}/lib/SeetaFaceRecognizer_d.lib" "${_IMPORT_PREFIX}/bin/SeetaFaceRecognizer_d.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
