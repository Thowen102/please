# -------- Project metadata --------
TARGET := PuffQuestAdvance

# -------- LIBBUTANO handling --------
# We prefer LIBBUTANO passed by CI; otherwise try to auto-detect.
LIBBUTANO ?= $(CURDIR)/third_party/butano/butano

# If the usual path doesn't exist, try older layout (without the extra /butano)
ifeq ("$(wildcard $(LIBBUTANO)/butano_dka.mak)","")
  LIBBUTANO := $(CURDIR)/third_party/butano
endif

# Hard fail if we still can't find the toolchain makefile:
ifeq ("$(wildcard $(LIBBUTANO)/butano_dka.mak)","")
  $(error Could not find butano_dka.mak. Looked in \
    $(CURDIR)/third_party/butano/butano and $(CURDIR)/third_party/butano)
endif

# -------- Project layout --------
SRC_DIRS  := src
INC_DIRS  := include
DATA_DIRS := graphics audio

# Tell Butano where our stuff lives
BN_PROJECT_NAME := $(TARGET)
BN_SOURCES      := $(shell find $(SRC_DIRS) -name '*.cpp')
BN_INCLUDES     := $(addprefix -I,$(INC_DIRS))
BN_DATA_DIRS    := $(DATA_DIRS)

# -------- Include Butano build system (toolchain-specific) --------
# Directly include the devkitARM makefile; this avoids the extra indirection
# that was producing a wrong absolute path (/butano_dka.mak).
include $(LIBBUTANO)/butano_dka.mak
