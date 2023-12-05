set(include_dirs
    include
    )

idf_component_register(SRCS "src/esp_xmodem_sender.c"
                            "src/esp_xmodem_receiver.c"
                            "src/esp_xmodem_transport.c"
                            "src/esp_xmodem_common.c"
                    INCLUDE_DIRS "${include_dirs}"
                    PRIV_INCLUDE_DIRS "src/priv"
                    REQUIRES
                    PRIV_REQUIRES)
