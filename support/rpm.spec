Name:           mysqlfs
Version:        %{_version}
Release:        %{_release}.%{_githash}
Summary:        MySql-backed File System
License:        Open Source
URL:            https://andrea.brancatelli.it/category/tech/mysqlfs-tech/
AutoReqProv:    no
Provides:       mysqlfs
Requires:       mariadb-libs
Requires:       fuse-libs
Requires:       fuse


%description
MySql-backed File System

%prep

%build

%install
TOP_DIR=%_top_dir
BIN_DIR=${RPM_BUILD_ROOT}/usr/local/bin
SCHEMA_DIR=${RPM_BUILD_ROOT}/usr/local/share/mysqlfs/sql/update
SERVICE_DIR=${RPM_BUILD_ROOT}/usr/lib/systemd/system
MOUNT_POINT=${RPM_BUILD_ROOT}/mnt/mysqlfs

mkdir -p ${BIN_DIR}
cp -a ${TOP_DIR}/mysqlfs_setup ${BIN_DIR}
cp -a ${TOP_DIR}/src/mysqlfs ${BIN_DIR}
mkdir -p ${SCHEMA_DIR}
cp ${TOP_DIR}/src/sql/updates/* ${SCHEMA_DIR}
mkdir -p ${SERVICE_DIR}
cp ${TOP_DIR}/support/mysqlfs.service ${SERVICE_DIR}
mkdir -p ${MOUNT_POINT}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
/usr/local/bin/mysqlfs
/usr/local/bin/mysqlfs_setup
/usr/local/share/mysqlfs/
/usr/lib/systemd/system/mysqlfs.service
/mnt/mysqlfs

%post
# $1==1: new install
# $1==2: upgrade

if [ "$1" = 1 ]; then
	echo Performing post-install tasks for mysqlfs
	systemctl enable mysqlfs

	# Patch to allow mysqlfs built on CentOS-6
	# to run on CentOS-7. Not necessary if built
	# on CentOS-7.
	cd /usr/lib64/mysql
	ln -sf libmysqlclient.so libmysqlclient.so.16
fi

if [ "$1" = 2 ]; then
	echo Performing post-upgrade tasks for mysqlfs
	systemctl daemon-reload
fi

%preun
if [ "$1" = 0 ]
then
	echo Performing pre-uninstallation tasks for mysqlfs
	systemctl stop mysqlfs
	systemctl disable mysqlfs
fi

%postun

%changelog
