#
# This is a project Makefile. It is assumed the directory this Makefile resides in is a
# project subdirectory.
#

PROJECT_NAME := xmodem_sender

EXTRA_COMPONENT_DIRS := $(realpath ../../)
EXTRA_COMPONENT_DIRS += $(IDF_PATH)/examples/common_components/protocol_examples_common

ifneq (,$(wildcard $(IDF_PATH)/components/esp8266/*))
export IDF_TARGET = esp8266
else
ifndef IDF_TARGET
export IDF_TARGET := esp32
endif
endif

SDKCONFIG_DEFAULTS := ./sdkconfig.defaults.$(IDF_TARGET)

include $(IDF_PATH)/make/project.mk

