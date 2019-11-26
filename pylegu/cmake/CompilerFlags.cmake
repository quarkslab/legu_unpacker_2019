include(CheckCCompilerFlag)
include(CheckCXXCompilerFlag)
if(__add_compiler_flags)
	return()
endif()
set(__add_compiler_flags ON)

function(append value)
  foreach(variable ${ARGN})
    set(${variable} "${${variable}} ${value}" PARENT_SCOPE)
  endforeach(variable)
endfunction()

function(append_if condition value)
  if (${condition})
    foreach(variable ${ARGN})
      set(${variable} "${${variable}} ${value}" PARENT_SCOPE)
    endforeach(variable)
  endif()
endfunction()

macro(ADD_FLAG_IF_SUPPORTED flag name)
  CHECK_C_COMPILER_FLAG("${flag}"   "C_SUPPORTS_${name}")
  CHECK_CXX_COMPILER_FLAG("${flag}" "CXX_SUPPORTS_${name}")

  if (C_SUPPORTS_${name})
    target_compile_options(jadxjni INTERFACE ${flag})
  endif()

  if (CXX_SUPPORTS_${name})
    target_compile_options(jadxjni INTERFACE ${flag})
  endif()
endmacro()



ADD_FLAG_IF_SUPPORTED("-Wall"                      WALL)
ADD_FLAG_IF_SUPPORTED("-Wextra"                    WEXTRA)
ADD_FLAG_IF_SUPPORTED("-Wpedantic"                 WPEDANTIC)
ADD_FLAG_IF_SUPPORTED("-fstack-protector-all"      STACK_PROTECTOR)
ADD_FLAG_IF_SUPPORTED("-fomit-frame-pointer"       OMIT_FRAME_POINTER)
ADD_FLAG_IF_SUPPORTED("-fno-strict-aliasing"       NO_STRICT_ALIASING)
ADD_FLAG_IF_SUPPORTED("-fexceptions"               EXCEPTION)
ADD_FLAG_IF_SUPPORTED("-fvisibility=hidden"        VISIBILITY)
ADD_FLAG_IF_SUPPORTED("-fdiagnostics-color=always" DIAGNOSTICS_COLOR)
ADD_FLAG_IF_SUPPORTED("-fcolor-diagnostics"        COLOR_DIAGNOSTICS)

ADD_FLAG_IF_SUPPORTED("-Wno-expansion-to-defined"  NO_EXPANSION_TO_DEFINED)


