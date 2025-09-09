# -------- Project metadata --------
TARGET := PuffQuestAdvance

# -------- LIBBUTANO handling --------
# Prefer LIBBUTANO passed on the make command line (from CI step).
# If not provided, try to auto-detect in third_party/butano/*.
LIBBUTANO ?=
ifeq ($(strip $(LIBBUTANO)),)
  BUTANO_ROOT := $(CURDIR)/third_party/butano
  ifneq ("$(wildcard $(BUTANO_ROOT)/butano/butano.mak)","")
    LIBBUTANO := $(BUTANO_ROOT)/butano
  else ifneq ("$(wildcard $(BUTANO_ROOT)/butano.mak)","")
    LIBBUTANO := $(BUTANO_ROOT)
  else
    $(error Could not find butano.mak. Expected at \
      $(BUTANO_ROOT)/butano/butano.mak or $(BUTANO_ROOT)/butano.mak)
  endif
endif

# -------- Project layout --------
SRC_DIRS  := src
INC_DIRS  := include
DATA_DIRS := graphics audio

# Explicitly tell Butano where things are
BN_PROJECT_NAME := $(TARGET)
BN_SOURCES      := $(shell find $(SRC_DIRS) -name '*.cpp')
BN_INCLUDES     := $(addprefix -I,$(INC_DIRS))
BN_DATA_DIRS    := $(DATA_DIRS)

# -------- Bring in Butano build system --------
include $(LIBBUTANO)/butano.mak
