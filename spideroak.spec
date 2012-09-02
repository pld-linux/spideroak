Summary:	Online multi-platform backup, storage, access, sharing tool
Name:		spideroak
Version:	9948
Release:	0.7
License:	Proprietary
Group:		Applications/Networking
URL:		https://spideroak.com/
# https://spideroak.com/directdownload?platform=otherlinux&arch=i386
Source0:	https://spideroak.com/directdownload?platform=fedora&arch=i386#/%{name}-%{version}.i386.rpm
# NoSource0-md5:	36ceccb84dacec4aa1aa999ca0629e67
NoSource:	0
Source1:	https://spideroak.com/directdownload?platform=fedora&arch=x86_64#/%{name}-%{version}.x86_64.rpm
# NoSource1-md5:	4ec6cee6ec6cb9083c10b29aaf8278f8
NoSource:	1
Patch0:		%{name}-desktopfile.patch
BuildRequires:	python-devel
BuildRequires:	rpm-utils
#BuildRequires:	update-desktop-files
#Requires:	python-asn1
#Requires:	python-bsddb3
#Requires:	python-cerealizer
#Requires:	python-concurrentloghandler
#Requires:	python-crypto
#Requires:	python-louie
#Requires:	python-nose
#Requires:	python-openssl
Requires:	python-pycurl
#Requires:	python-qt4
Requires:	python-setuptools
Requires:	python-simplejson
#Requires:	python-transaction
#Requires:	python-twisted
#Requires:	python-zc-lockfile
#Requires:	python-zdaemon
#Requires:	python-zodb3
#Requires:	python-zope-event
#Requires:	python-zope-proxy
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_libdir}/%{name}

# generate no Provides from private modules
%define		_noautoprovfiles	%{_libdir}/%{name}

# provided by package itself, but autodeps disabled
%define		_noautoreq		libcrypto.so.10 libssl.so.10 libc.so.6(GLIBC_PRIVATE)

# a zip and executable at the same time
%define		_noautostrip	.*/library.zip\\|.*/SpiderOak\\|.*/py

# debuginfo wouldn't be useful
%define		_enable_debug_packages	0

%description
Whether you need to access a document you have stored on a remote
server, synchronize data between a Mac, Windows or Linux device, share
important business documents with your clients, or just rest easy
knowing all of your data is safely, securely, and automatically backed
up - SpiderOak's free online backup, online sync and online sharing
solution can handle all your needs!

%prep
%setup -qcT
%ifarch %{ix86}
SOURCE=%{SOURCE0}
%endif
%ifarch %{x8664}
SOURCE=%{SOURCE1}
%endif
rpm2cpio $SOURCE | cpio -i -d

%patch0

mv usr/lib/SpiderOak lib
mv usr/bin .
mv usr/share/* .

cat <<'EOF' > bin/SpiderOak
#!/bin/sh
export LD_LIBRARY_PATH="%{_appdir}:$LD_LIBRARY_PATH"
expor QT_PLUGIN_PATH=
export SpiderOak_EXEC_SCRIPT="$0"
exec %{_appdir}/SpiderOak "$@"
EOF

# make into symlink, looks cleaner than hardlink:
# we can attach executable attrs to binary and leave no attrs for symlink in
# %files section.
ln -sf SpiderOak lib/library.zip
ln -sf SpiderOak lib/py

# you'll need this if you cp -a complete dir in source
# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_appdir}}
cp -a lib/* $RPM_BUILD_ROOT%{_appdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a applications/* $RPM_BUILD_ROOT%{_desktopdir}
cp -a pixmaps/* $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/SpiderOak
%{_desktopdir}/spideroak.desktop
%{_pixmapsdir}/spideroak.png
%dir %{_appdir}
%attr(755,root,root) %{_appdir}/SpiderOak
%attr(755,root,root) %{_appdir}/inotify_dir_watcher
%{_appdir}/library.zip
%{_appdir}/py
%attr(755,root,root) %{_appdir}/*.so*
%{_appdir}/Louie-1.1-py*.egg
%{_appdir}/SpideroakVersionMatcher-1.1-py*.egg
%{_appdir}/Twisted-10.2.0-py*.egg
%{_appdir}/ZConfig-2.9.0-py*.egg
%{_appdir}/ZODB3-3.10.3-py*.egg
%{_appdir}/nose-1.1.1-py*.egg
%{_appdir}/py_bcrypt-0.2-py*.egg
%{_appdir}/pyasn1-0.0.13-py*.egg
%{_appdir}/pycrypto-2.3-py*.egg
%{_appdir}/setuptools-0.6c11-py*.egg
%{_appdir}/simplejson-2.1.6-py*.egg
%{_appdir}/transaction-1.1.1-py*.egg
%{_appdir}/zc.lockfile-1.0.0-py*.egg
%{_appdir}/zdaemon-2.0.4-py*.egg
%{_appdir}/zope.interface-3.6.4-py*.egg
%{_appdir}/zope.event-3.5.0_1-py*.egg

