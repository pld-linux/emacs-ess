Summary:	Emacs Speaks Statistics add-on package for Emacs
Name:		emacs-ess
Version:	5.2.6
Release:	1
License:	GPL
Group:		Applications/Editors
Source0:	http://ESS.R-project.org/downloads/ess/ess-%{version}.tar.gz
# Source0-md5:	ce4a94b220061df866bb17d103e64973
URL:		http://ESS.R-project.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildArch:	noarch
BuildRequires:	emacs
Requires:	emacs

%description
This package provides Emacs Speaks Statistics (ESS), which provides
Emacs-based front ends for popular statistics packages.

ESS provides an intelligent, consistent interface between the user and
the software. ESS interfaces with S-PLUS, R, SAS, BUGS and other
statistical analysis packages under the Unix, Microsoft Windows, and
Apple Mac OS operating systems. ESS is a package for the GNU Emacs and
XEmacs text editors whose features ESS uses to streamline the creation
and use of statistical software. ESS knows the syntax and grammar of
statistical analysis packages and provides consistent display and
editing features based on that knowledge. ESS assists in interactive
and batch execution of statements written in these statistical
analysis languages.

%prep
%setup -q -n ess-%{version}
( cd doc && chmod u+w html info ) # fix perms to ensure builddir can be deleted

%build
%{__make}

# create an init file that is loaded when a user starts up emacs to
# tell emacs to autoload our package's Emacs code when needed
cat > %{name}-init.el <<"EOF"
;;; Set up %{name} for Emacs.
;;;
;;; This file is automatically loaded by emacs's site-start.el
;;; when you start a new emacs session.

(require 'ess-site)

EOF

# create a README.RPM file to document any quirks of this package
cat > README.RPM <<EOF
README for %{name}-%{version}-%{release} RPM package

Generally, there will be no need to modify your .emacs file in order
to use the features of this package -- they are enabled by default
when you start Emacs.

Cheers,
Tom

--
Tom Moertel <tom-rpms@moertel.com>
EOF


%install
rm -rf $RPM_BUILD_ROOT
INITDIR=${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/site-start.d
PKGLISP=${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/%{name}-%{version}
INFODIR=${RPM_BUILD_ROOT}%{_infodir}
%{__install} -D %{name}-init.el ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/site-start.d/%{name}-init.el
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/%{name}-%{version}
%{__install} -d ${RPM_BUILD_ROOT}%{_infodir}
%{__make} install \
          PREFIX=${RPM_BUILD_ROOT}%{_prefix} \
          LISPDIR=${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/%{name}-%{version} \
          INFODIR=${RPM_BUILD_ROOT}%{_infodir}
%{__cp} -a etc ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/%{name}-%{version}

%{__install} %{name}-init.el ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp/site-start.d/

%clean
%{__rm} -rf ${RPM_BUILD_ROOT}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc README README.RPM ANNOUNCE COPYING VERSION ChangeLog doc
%dir %{_datadir}/emacs/site-lisp/%{name}-%{version}
%{_datadir}/emacs/site-lisp/%{name}-%{version}/*
%{_datadir}/emacs/site-lisp/site-start.d/*
%{_infodir}/ess*
