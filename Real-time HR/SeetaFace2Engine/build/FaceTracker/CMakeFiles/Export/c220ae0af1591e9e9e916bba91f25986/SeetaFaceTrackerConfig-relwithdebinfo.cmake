#----------------------------------------------------------------
# Generated CMake target import file for configuration "RelWithDebInfo".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "SeetaFace::SeetaFaceTracker" for configuration "RelWithDebInfo"
set_property(TARGET SeetaFace::SeetaFaceTracker APPEND PROPERTY IMPORTED_CONFIGURATIONS RELWITHDEBINFO)
set_target_properties(SeetaFace::SeetaFaceTracker PROPERTIES
  IMPORTED_IMPLIB_RELWITHDEBINFO "${_IMPORT_PREFIX}/lib/SeetaFaceTracker.lib"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELWITHDEBINFO "SeetaFace::SeetaFaceDetector"
  IMPORTED_LOCATION_RELWITHDEBINFO "${_IMPORT_PREFIX}/bin/SeetaFaceTracker.dll"
  )

list(APPEND _cmake_import_check_targets SeetaFace::SeetaFaceTracker )
list(APPEND _cmake_import_check_files_for_SeetaFace::SeetaFaceTracker "${_IMPORT_PREFIX}/lib/SeetaFaceTracker.lib" "${_IMPORT_PREFIX}/bin/SeetaFaceTracker.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
