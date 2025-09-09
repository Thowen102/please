# -------- Project metadata --------
TARGET := PuffQuestAdvance

# -------- Auto-find Butano (prefers env override) --------
# If LIBBUTANO is passed in (from CI), use it; otherwise search the repo.
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

# -------- (Optional) where code / headers / assets live --------
SRC_DIRS    := src
INC_DIRS    := include
DATA_DIRS   := graphics audio

# Let Butano know our project layout (keeps things explicit)
BN_PROJECT_NAME := $(TARGET)
BN_SOURCES      := $(shell find $(SRC_DIRS) -name '*.cpp')
BN_INCLUDES     := $(addprefix -I,$(INC_DIRS))
BN_DATA_DIRS    := $(DATA_DIRS)

# -------- Include Butano build system --------
include $(LIBBUTANO)/butano.mak
