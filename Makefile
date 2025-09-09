# ================== Project ==================
TARGET := PuffQuestAdvance

# ================== devkitPro toolchain (set here so CI never depends on container env) ==================
DEVKITPRO ?= /opt/devkitpro
DEVKITARM ?= $(DEVKITPRO)/devkitARM
export DEVKITPRO DEVKITARM

# Ensure the toolchain binaries are on PATH for sub-makefiles
PATH := $(DEVKITARM)/bin:$(PATH)
export PATH

# ================== Butano path ==================
# Passed in by workflow; falls back to common checkout locations.
LIBBUTANO ?= $(CURDIR)/third_party/butano/butano
ifeq ("$(wildcard $(LIBBUTANO)/butano.mak)","")
  LIBBUTANO := $(CURDIR)/third_party/butano
endif
ifeq ("$(wildcard $(LIBBUTANO)/butano.mak)","")
  $(error Could not find butano.mak under third_party/butano. Make sure the workflow cloned GValiente/butano)
endif

# ================== Project layout ==================
SRC_DIRS  := src
INC_DIRS  := include
DATA_DIRS := graphics audio

BN_PROJECT_NAME := $(TARGET)
BN_SOURCES      := $(shell find $(SRC_DIRS) -name '*.cpp')
BN_INCLUDES     := $(addprefix -I,$(INC_DIRS))
BN_DATA_DIRS    := $(DATA_DIRS)

# ================== Include Butano build system ==================
# Use the main Butano makefile; it will bring in the devkitARM-specific rules.
include $(LIBBUTANO)/butano.mak
