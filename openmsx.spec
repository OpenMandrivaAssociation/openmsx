Summary:	Open source MSX emulator
Name:		openmsx
Version:	0.7.2
Release:	%{mkrel 2}
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		openmsx_fix_config.patch
License:	GPL+
Group:		Emulators
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
URL:		http://openmsx.sourceforge.net/
BuildRequires:	libSDL-devel
BuildRequires:	libSDL_image-devel
BuildRequires:	libmesaglu-devel
BuildRequires:	libpng-devel
BuildRequires:	libxml2-devel
BuildRequires:	tcl-devel libjack-devel glew-devel libSDL_ttf-devel

%description
The open source MSX emulator that tries to achieve
near-perfect emulation by using a novel emulation model.

%prep
%setup -q
# %patch0 -p0

%build
%configure2_5x

%make

%install
rm -rf %{buildroot}

# install bin files
install -d %{buildroot}%{_bindir}
   cp derived/*/bin/openmsx %{buildroot}%{_bindir}/openmsx

# install c-bios
install -d %{buildroot}%{_datadir}/openMSX/share/machines
   cp -r share/ %{buildroot}%{_datadir}/openMSX/
   cp -r Contrib/cbios/C-BIOS_MSX1/ %{buildroot}%{_datadir}/openMSX/share/machines/
   cp -r Contrib/cbios/C-BIOS_MSX2/ %{buildroot}%{_datadir}/openMSX/share/machines/
   cp -r Contrib/cbios/C-BIOS_MSX2+/ %{buildroot}%{_datadir}/openMSX/share/machines/

# menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/openmsx
Icon=emulators_section
Name=Openmsx
Comment=%{summary}
Categories=Emulator;
EOF

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog README doc/*
%{_bindir}/openmsx
%{_datadir}/openMSX/share/*
%{_datadir}/applications/mandriva-%{name}.desktop
