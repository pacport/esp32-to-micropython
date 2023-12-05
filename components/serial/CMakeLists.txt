idf_component_register(SRCS TinyFrame/TinyFrame.c
                    TinyFrame/TinyFrame.h
                    port/TF_Config.h
                    INCLUDE_DIRS ./TinyFrame/ ./port/
                    PRIV_INCLUDE_DIRS ./TinyFrame/ ./port/)

target_compile_definitions(${COMPONENT_LIB} PUBLIC "-DVARGS=1")
