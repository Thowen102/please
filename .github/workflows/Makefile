# Output
TARGET := PuffQuestAdvance


# Path to Butano library inside third_party
# GitHub Action sets LIBBUTANO env; fallback for local builds
LIBBUTANO ?= $(CURDIR)/third_party/butano/butano


# Game metadata
ROMTITLE := PUFFQUEST ADV
ROMCODE := PQAV
MAKER := 01
REVISION := 0


# Optional: link std libs if needed (strings, etc)
# DEFAULTLIBS := true


# Increase sprite/text budgets a bit
STACKTRACE :=


# Include Butano makefile
include $(LIBBUTANO)/butano.mk
