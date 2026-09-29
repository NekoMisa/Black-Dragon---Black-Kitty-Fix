# -*- cmake -*-
include(Prebuilt)

set(NVAPI ON CACHE BOOL "Use NVAPI.")

if (NVAPI)
  if (WINDOWS)
    add_library( ll::nvapi INTERFACE IMPORTED )
    target_compile_definitions(ll::nvapi INTERFACE LL_NVAPI=1)
    target_link_libraries( ll::nvapi INTERFACE nvapi)
    use_prebuilt_binary(nvapi)
  endif (WINDOWS)
endif (NVAPI)

