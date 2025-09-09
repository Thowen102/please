# -------- Project metadata --------
TARGET      := PuffQuestAdvance

# (Optional ROM header—safe defaults)
ROMTITLE    := PUFFQUEST ADV
ROMCODE     := PQAV
MAKER       := 01
REVISION    := 0

# -------- Auto-find Butano --------
# After the workflow checks out GValiente/butano into third_party/butano,
# butano.mk can live in:
#   third_party/butano/butano/butano.mk  (common)
#   third_party/butano/butano.mk         (older layout)
BUTANO_ROOT := $(CURDIR)/third_party/butano

ifeq ($(wildcard $(BUTANO_ROOT)/butano/butano.mk),)
  ifeq ($(wildcard $(BUTANO_ROOT)/butano.mk),)
    $(error Could not find butano.mk. Expected at \
      $(BUTANO_ROOT)/butano/butano.mk or $(BUTANO_ROOT)/butano.mk. \
      Ensure the workflow step 'Fetch Butano' created third_party/butano)
  endif
  LIBBUTANO := $(BUTANO_ROOT)
else
  LIBBUTANO := $(BUTANO_ROOT)/butano
endif

# -------- Include Butano build system --------
include $(LIBBUTANO)/butano.mk
