#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaQualityAssessor" for configuration "RelWithDebInfo"
set_property(TARGET SeetaFace::SeetaQualityAssessor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(SeetaFace::SeetaQualityAssessor PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/SeetaQualityAssessor.lib"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/SeetaQualityAssessor.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaQualityAssessor )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaQualityAssessor "${_IMPORT_PREFIX}/lib/SeetaQualityAssessor.lib" "${_IMPORT_PREFIX}/bin/SeetaQualityAssessor.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
