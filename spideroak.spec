Summary:	Online multi-platform backup, storage, access, sharing tool
Name:		spideroak
Version:	9681
Release:	0.1.1
License:	Proprietary
Group:		Applications/Networking
URL:		https://spideroak.com/
Source0:	%{name}-%{version}-config.tar.bz2
# Source0-md5:	404636ebed84c70577b876e479677c56
Source1:	%{name}-%{version}-i586.tar.bz2
# Source1-md5:	e28f6bedff7b1c70780c85fab0781b87
Source2:	%{name}-%{version}-x86_64.tar.bz2
# Source2-md5:	8229b6adbe8ad147ffda766d0fb24084
Patch0:		%{name}-desktopfile.patch
BuildRequires:	python-devel
#BuildRequires:	update-desktop-files
Requires:	python-asn1
Requires:	python-bsddb3
Requires:	python-cerealizer
Requires:	python-concurrentloghandler
Requires:	python-crypto
Requires:	python-louie
Requires:	python-nose
Requires:	python-openssl
Requires:	python-pycurl
Requires:	python-qt4
Requires:	python-setuptools
Requires:	python-simplejson
Requires:	python-transaction
Requires:	python-twisted
Requires:	python-zc-lockfile
Requires:	python-zdaemon
Requires:	python-zodb3
Requires:	python-zope-event
Requires:	python-zope-proxy
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_libdir}/%{name}

%description
Whether you need to access a document you have stored on a remote
server, synchronize data between a Mac, Windows or Linux device, share
important business documents with your clients, or just rest easy
knowing all of your data is safely, securely, and automatically backed
up - SpiderOak's free online backup, online sync and online sharing
solution can handle all your needs!

%prep
%ifarch %{ix86}
%setup -q -c -b 1
%else
%setup -q -c -b 2
%endif
%patch0

mv .%{_libdir}/SpiderOak %{name}
mv .%{_bindir} .
mv .%{_datadir}/* .

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_appdir}}
cp -a %{name}/* $RPM_BUILD_ROOT%{_appdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a applications/* $RPM_BUILD_ROOT%{_desktopdir}
cp -a pixmaps/* $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/SpiderOak
%{_desktopdir}/spideroak-gui.desktop
%{_pixmapsdir}/spideroak.png
%dir %{_appdir}
%dir %{_appdir}/bin

%attr(755,root,root) %{_appdir}/bin/SpiderOak
%attr(755,root,root) %{_appdir}/bin/activate_this.py
%attr(755,root,root) %{_appdir}/bin/inotify_dir_watcher

%dir %{_appdir}/lib
%dir %{_appdir}/lib/python2.6
%dir %{_appdir}/lib/python2.6/site-packages
%{_appdir}/lib/python2.6/orig-prefix.txt
%{_appdir}/lib/python2.6/*.py*
%{_appdir}/lib/python2.6/site-packages/*.py*
%{_appdir}/lib/python2.6/site-packages/pip-*.egg
%{_appdir}/lib/python2.6/site-packages/setuptools*
%{_appdir}/lib/python2.6/site-packages/easy-install*
%{_appdir}/lib/python2.6/site-packages/Spider[Oo]ak*
%{_appdir}/lib/python2.6/config
%{_appdir}/lib/python2.6/distutils
%{_appdir}/lib/python2.6/encodings
%{_appdir}/lib/python2.6/lib-dynload
