#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaFaceTracker" for configuration "Debug"
set_property(TARGET SeetaFace::SeetaFaceTracker APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(SeetaFace::SeetaFaceTracker PROPERTIES
  IMPORTED_IMPLIB_DEBUG "${_IMPORT_PREFIX}/lib/SeetaFaceTracker_d.lib"
  IMPORTED_LINK_INTERFACE_LIBRARIES_DEBUG "SeetaFace::SeetaFaceDetector"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/SeetaFaceTracker_d.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaFaceTracker )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaFaceTracker "${_IMPORT_PREFIX}/lib/SeetaFaceTracker_d.lib" "${_IMPORT_PREFIX}/bin/SeetaFaceTracker_d.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
