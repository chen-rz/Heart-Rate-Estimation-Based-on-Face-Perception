# Install script for directory: D:/HR Estimation/Real-time HR/SeetaFace2Engine

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/SeetaFace.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake" TYPE FILE FILES "D:/HR Estimation/Real-time HR/SeetaFace2Engine/cmake/SeetaFaceConfig.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/SeetaNet/cmake_install.cmake")
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/FaceDetector/cmake_install.cmake")
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/FaceTracker/cmake_install.cmake")
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/FaceLandmarker/cmake_install.cmake")
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/FaceRecognizer/cmake_install.cmake")
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/QualityAssessor/cmake_install.cmake")
  include("D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/example/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "D:/HR Estimation/Real-time HR/SeetaFace2Engine/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
