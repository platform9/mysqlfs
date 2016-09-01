#! vim noexpandtab
#
# Copyright (C) 2015-2016 Platform 9 Systems, Inc.
#
# Usage:
#
#   make rpm     # Makes the server RPM
#   make clean   # Cleans everything
#
############################################################
# common
BUILD_NUMBER ?= 0
GITHASH=$(shell git rev-parse --short HEAD)
MYSQLFS_VERSION ?= 0.4.2

default: ;

all: rpm

$(BUILD_DIR):
	mkdir -p $@


SUPPORT_DIR := $(shell pwd)
TOP_DIR := $(SUPPORT_DIR)/..
BUILD_DIR := $(TOP_DIR)/build
MYSQLFS_SRC_DIR := $(TOP_DIR)/src
MYSQLFS_BUILD_DIR := $(BUILD_DIR)/mysqlfs
MYSQLFS_SERVER_VERSION := $(MYSQLFS_VERSION)
FULL_MYSQLFS_SERVER_VERSION := $(MYSQLFS_SERVER_VERSION)-$(BUILD_NUMBER).$(GITHASH)
MYSQLFS_RPM_DIR := $(MYSQLFS_BUILD_DIR)/rpmbuild
MYSQLFS_RPM := $(MYSQLFS_RPM_DIR)/RPMS/x86_64/mysqlfs-$(FULL_MYSQLFS_SERVER_VERSION).x86_64.rpm
MYSQLFS_SPEC_FILE := $(MYSQLFS_BUILD_DIR)/rpm.spec
CMAKE := /usr/bin/cmake
FUSE_DEVEL_HDR := /usr/include/fuse/fuse.h
MYSQL_DEVEL_HDR := /usr/include/mysql/mysql.h
MYSQLFS_BIN := ${MYSQLFS_SRC_DIR}/mysqlfs

clean:
	for x in CMakeCache.txt CMakeFiles/ Config.h Makefile \
	cmake_install.cmake install_manifest.txt src/CMakeFiles/ mysqlfs.log \
	src/Makefile src/cmake_install.cmake \
	; do rm -rf "$(TOP_DIR)/$$x"; done
	rm -f $(MYSQLFS_BIN)
	rm -rf $(BUILD_DIR)

$(MYSQLFS_BUILD_DIR):
	mkdir -p $@

$(MYSQLFS_SPEC_FILE): | $(MYSQLFS_BUILD_DIR)
	cp $(TOP_DIR)/support/rpm.spec $@

rpm: $(MYSQLFS_RPM)

exe: $(MYSQLFS_BIN)


${CMAKE}:
	sudo yum -y install cmake

${FUSE_DEVEL_HDR}:
	sudo yum -y install fuse-devel

${MYSQL_DEVEL_HDR}:
	sudo yum -y install mysql-devel

$(MYSQLFS_BIN): ${CMAKE} ${FUSE_DEVEL_HDR} ${MYSQL_DEVEL_HDR}
	echo "Building binary ${MYSQLFS_BIN}"
	cd $(TOP_DIR) && cmake . && make


${MYSQLFS_RPM}: ${MYSQLFS_BIN} $(MYSQLFS_SPEC_FILE)
	echo "Building RPM"
	echo "MYSQLFS_RPM_DIR: $(MYSQLFS_RPM_DIR)"
	rpmbuild -bb --define "_topdir $(MYSQLFS_RPM_DIR)" \
	--define "_top_dir $(TOP_DIR)" \
	--define "_version $(MYSQLFS_SERVER_VERSION)" \
	--define "_release $(BUILD_NUMBER)" \
	--define "_githash $(GITHASH)" ${MYSQLFS_SPEC_FILE}

