Summary:	Emacs Speaks Statistics add-on package for Emacs
Summary(pl.UTF-8):	Dodatek Emacs Speaks Statistics dla Emacsa - obsługa pakietów statystycznych
Name:		emacs-ess
Version:	5.2.6
Release:	1
License:	GPL
Group:		Applications/Editors
Source0:	http://ESS.R-project.org/downloads/ess/ess-%{version}.tar.gz
# Source0-md5:	ce4a94b220061df866bb17d103e64973
URL:		http://ESS.R-project.org/
BuildRequires:	emacs
Requires:	emacs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
Ten pakiet zawiera ESS (Emacs Speaks Statistics), dostarczający oparte
na Emacsie frontendy dla popularnych pakietów statystycznych.

ESS dostarcza inteligentny, spójny interfejs pomiędzy użytkownikiem i
oprogramowaniem. ESS współpracuje z S-PLUS, R, SAS, BUGS i innymi
pakietami do analiz statystycznych dla uniksów oraz systemów Microsoft
Windows i Apple Mac OS. ESS to pakiet dla edytorów tekstu GNU Emacs i
XEmacs, których możliwości wykorzystuje ESS przy kształtowaniu
tworzenia i używania programów statystycznych. ESS zna składnie i
gramatyki pakietów do analiz statystycznych i w oparciu o tę wiedzę
udostępnia spójne możliwości wyświetlania i edycji. ESS pomaga w
interaktywnym i wsadowym wykonywaniu instrukcji zapisanych w tych
językach analizy statystycznej.

%prep
%setup -q -n ess-%{version}
cd doc
chmod u+w html info # fix perms to ensure builddir can be deleted

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

INITDIR=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d
PKGLISP=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}-%{version}
INFODIR=$RPM_BUILD_ROOT%{_infodir}
install -D %{name}-init.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d/%{name}-init.el
install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_infodir}
%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LISPDIR=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}-%{version} \
	INFODIR=$RPM_BUILD_ROOT%{_infodir}
cp -a etc $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/%{name}-%{version}

install %{name}-init.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/site-start.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc ANNOUNCE ChangeLog README README.RPM doc/{NEWS,TODO,*.jpg,*.pdf,name-completion.txt,html}
%dir %{_datadir}/emacs/site-lisp/%{name}-%{version}
%{_datadir}/emacs/site-lisp/%{name}-%{version}/*
%{_datadir}/emacs/site-lisp/site-start.d/*
%{_infodir}/ess*
