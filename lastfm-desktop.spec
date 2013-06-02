%define oname lastfm-scrobbler

Summary:	The official Last.fm desktop application suite
Name:		lastfm-desktop
Version:	2.1.35
Release:	1
License:	GPLv3+
Group:		Sound
Url:		http://github.com/lastfm/lastfm-desktop
Source0:	https://github.com/lastfm/lastfm-desktop/archive/%{name}-%{version}.tar.gz
Source1:	%{name}.png
Patch1:		lastfm-desktop-09012013-linkage.patch
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
%setup -q
%patch1 -p1

%build
%qmake_qt4 QMAKE_CXXFLAGS_RELEASE= PREFIX=%{_prefix}
%make

%install
install -D _bin/lastfm-scrobbler %{buildroot}%{_bindir}/%{name}

# install menu icons
for N in 16 32 48 64 128;
do
convert %{SOURCE1} -resize ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

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

mkdir -p %{buildroot}%{_datadir}/%{oname}/i18n
cp i18n/*.qm %{buildroot}%{_datadir}/%{oname}/i18n/
cp app/client/Last.fm\ Scrobbler.css %{buildroot}%{_datadir}/%{oname}/

%files
%doc COPYING README.md
%{_bindir}/%{name}
%{_datadir}/%{oname}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

