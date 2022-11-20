set(PROJECT_SOURCE_FILES
 #PSF
)
set(PROJECT_INCLUDE_FILES
 #PIF
)
set(PROJECT_LINK_LIBRARIES
 #PLL
)
set(PROJECT_DIR main)
cmake_minimum_required(VERSION 3.23)
project(${PROJECT_DIR})

add_executable(${PROJECT_DIR}
	${PROJECT_SOURCE_FILES}
	${PROJECT_INCLUDE_FILES}
)

target_include_directories(${PROJECT_DIR} PUBLIC
	"include"
)
#CQPend

# You may put any custom settings down here.
# CQP will not change anything after `#CQPend`