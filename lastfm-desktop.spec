%define		git	09012013

Name:		lastfm-desktop
# app/client/client.pro:VERSION
Version:	2.1.28
Release:	0.%{git}.2
Summary:	The official Last.fm desktop application suite
Group:		Sound
License:	GPLv3+
URL:		http://github.com/lastfm/lastfm-desktop
# From project's git
Source:		%{name}-%{git}.tar.bz2
Source1:	%{name}.png
Patch0:		lastfm-desktop-09012013-api.patch
Patch1:		lastfm-desktop-09012013-linkage.patch
Patch2:		lastfm-desktop-09012013-static.patch
Patch3:		lastfm-desktop-09012013-datapath.patch
Patch4:		lastfm-desktop-09012013-i18n.patch
Patch5:		lastfm-desktop-09012013-css.patch
BuildRequires:	imagemagick
BuildRequires:	ffmpeg-devel
BuildRequires:	liblastfm-devel
BuildRequires:	pkgconfig(libgpod-1.0)
BuildRequires:	pkgconfig(phonon)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt4-devel

%description
The official Last.fm desktop application suite.

%prep
%setup -q -n %{name}-%{git}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%qmake_qt4
%make
pushd i18n
lrelease *
popd
for N in 16 32 64 128; do convert %{SOURCE1} -resize ${N}x${N} $N.png; done

%install
install -D _bin/Last.fm\ Scrobbler %{buildroot}%{_bindir}/%{name}
install -D 16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D 32.png %{buildroot}%{_liconsdir}/%{name}.png
install -D 64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png
install -D 128.png %{buildroot}%{_iconsdir}/hicolor/128x128/apps/%{name}.png

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Last.fm Scrobbler
Comment=Last.fm Scrobbler
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;Audio;AudioVideo;
EOF

mkdir -p %{buildroot}%{_datadir}/%{name}/i18n
cp i18n/*.qm %{buildroot}%{_datadir}/%{name}/i18n/
cp app/client/Last.fm\ Scrobbler.css %{buildroot}%{_datadir}/%{name}/lastfm-desktop.css

%files
%doc COPYING README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png

