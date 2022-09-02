#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaFaceRecognizer" for configuration "Release"
set_property(TARGET SeetaFace::SeetaFaceRecognizer APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(SeetaFace::SeetaFaceRecognizer PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/SeetaFaceRecognizer.lib"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "SeetaFace::SeetaNet"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/SeetaFaceRecognizer.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaFaceRecognizer )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaFaceRecognizer "${_IMPORT_PREFIX}/lib/SeetaFaceRecognizer.lib" "${_IMPORT_PREFIX}/bin/SeetaFaceRecognizer.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
