

PROJECT(NfcrdlibEx1_BasicDiscoveryLoop)


FILE(GLOB NfcrdlibEx1_BasicDiscoveryLoop_Sources
    *.c
    src/*.c
)

include_directories(
    intfs
	types
)

#ADD_EXECUTABLE(NfcrdlibEx1_BasicDiscoveryLoop
#    ${NfcrdlibEx1_BasicDiscoveryLoop_Sources}
#)

ADD_LIBRARY(${PROJECT_NAME}
    ${NfcrdlibEx1_BasicDiscoveryLoop_Sources}
)

TARGET_LINK_LIBRARIES(
    NfcrdlibEx1_BasicDiscoveryLoop
    NxpRdLib_Osal
    NxpRdLib_Platform
    NxpRdLib_acDiscLoop
    NxpRdLib_halHw
    NxpRdLib_balReg
    NxpRdLib_KeyStore
    NxpRdLib_phTools
    NxpRdLib_palFelica
    NxpRdLib_palI18092mPI
    NxpRdLib_palI14443p4a
    NxpRdLib_palI14443p4
    NxpRdLib_palI14443p4
    NxpRdLib_palMifare
    NxpRdLib_alFelica
    NxpRdLib_alMful
    NxpRdLib_alMfdf
    NxpRdLib_alT1T
    NxpRdLib_alTop
    NxpRdLib_alMfc
    NxpRdLib_palSli15693
    NxpRdLib_palI18000p3m3
    NxpRdLib_alI15693
    NxpRdLib_alI18000p3m3
    NxpRdLib_alSli
    NxpRdLib_palEpcUid
    NxpRdLib_lnLlcp
    NxpRdLib_palI14443p4mC
    NxpRdLib_palI18092mT
    NxpRdLib_ceT4T
    NxpRdLib_palEpcUid
)

