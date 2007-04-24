%define name      openmsx
%define version   0.6.2
%define release   %mkrel 1

Summary:   Open source MSX emulator
Name:      %{name}
Version:   %{version}
Release:   %{release}
Source0:   %{name}-%{version}.tar.bz2
Patch0:    openmsx_fix_config.patch
License:   GPL
Group:     Emulators
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL:       http://openmsx.sourceforge.net/
BuildRequires:   libSDL-devel, libSDL_image-devel, %{mklibname tcl 8.4}
BuildRequires:   libmesaglu-devel, libpng-devel, libxml2-devel
BuildRequires:   tcl-devel

%description
The open source MSX emulator that tries to achieve
near-perfect emulation by using a novel emulation model.


%prep
%setup -q
%patch0 -p0

%build
%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT

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
mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
   command="%{_bindir}/openmsx" \
   icon="emulators_section.png" \
   title="Openmsx" \
   longtitle="%{summary}" \
   needs="x11" \
   section="More Applications/Emulators"
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog GPL README TODO doc/*
%{_bindir}/openmsx
%{_datadir}/openMSX/share/*
%_menudir/%name
