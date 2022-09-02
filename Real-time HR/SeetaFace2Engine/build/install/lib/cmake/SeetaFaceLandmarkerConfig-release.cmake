#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaFaceLandmarker" for configuration "Release"
set_property(TARGET SeetaFace::SeetaFaceLandmarker APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(SeetaFace::SeetaFaceLandmarker PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/SeetaFaceLandmarker.lib"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "SeetaFace::SeetaNet"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/SeetaFaceLandmarker.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaFaceLandmarker )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaFaceLandmarker "${_IMPORT_PREFIX}/lib/SeetaFaceLandmarker.lib" "${_IMPORT_PREFIX}/bin/SeetaFaceLandmarker.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
