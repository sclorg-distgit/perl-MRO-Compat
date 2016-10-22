%{?scl:%scl_package perl-MRO-Compat}

# MRO is part of the Perl core since 5.9.5
%global mro_in_core 1

Name:		%{?scl_prefix}perl-MRO-Compat
Version:	0.12
Release:	12%{?dist}
Summary:	Mro::* interface compatibility for Perls < 5.9.5
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/MRO-Compat/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/MRO-Compat-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(Cwd)
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:	%{?scl_prefix}perl(File::Path)
BuildRequires:	%{?scl_prefix}perl(File::Spec)
# Module
%if ! %{mro_in_core}
BuildRequires:	%{?scl_prefix}perl(Class::C3) >= 0.24
BuildRequires:	%{?scl_prefix}perl(Class::C3::XS) >= 0.08
%endif
# Test
BuildRequires:	%{?scl_prefix}perl(Test::More) >= 0.47
%if !%{defined perl_small}
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage)
%endif
# Runtime
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
%if ! %{mro_in_core}
Requires:	%{?scl_prefix}perl(Class::C3) >= 0.24
Requires:	%{?scl_prefix}perl(Class::C3::XS) >= 0.08
%endif

%description
The "mro" namespace provides several utilities for dealing with method
resolution order and method caching in general in Perl 5.9.5 and higher.
This module provides those interfaces for earlier versions of Perl (back
to 5.6.0 anyways).

It is a harmless no-op to use this module on 5.9.5+. That is to say,
code which properly uses MRO::Compat will work unmodified on both older
Perls and 5.9.5+.

If you're writing a piece of software that would like to use the parts
of 5.9.5+'s mro:: interfaces that are supported here, and you want
compatibility with older Perls, this is the module for you.

%prep
%setup -q -n MRO-Compat-%{version}

# Fix script interpreter
%{?scl:scl enable %{scl} '}perl -MExtUtils::MakeMaker -e %{?scl:'"}'%{?scl:"'}ExtUtils::MM_Unix->fixin(q{t/15pkg_gen.t})%{?scl:'"}'%{?scl:"'}%{?scl:'}

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%clean
rm -rf %{buildroot}

%files
%doc ChangeLog README t/
%{perl_vendorlib}/MRO/
%{_mandir}/man3/MRO::Compat.3pm*

%changelog
* Tue Jul 19 2016 Petr Pisar <ppisar@redhat.com> - 0.12-12
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-11
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-8
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 0.12-7
- Do not hard-code interpreter name

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.12-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.12-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec  5 2012 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Bump Class::C3 dependency on 5.8, which in turn will automatically install
    Class::C3::XS if possible
  - Fix nonfunctional SYNOPSIS (CPAN RT#78325)
- This release by BOBTFISH -> update source URL
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- BR: perl(Cwd), perl(File::Path), perl(File::Spec) for bundled Module::Install
- Bump perl(Class::C3) version requirement to 0.24
- Drop unnecessary version requirement for perl(ExtUtils::MakeMaker)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.11-10
- Perl 5.16 rebuild

* Thu Jan 26 2012 Paul Howarth <paul@city-fan.org> - 0.11-9
- Spec clean-up:
  - Only require Class::C3 with perl < 5.9.5
  - Require Class::C3::XS for performance and consistency, but only with
    perl < 5.9.5
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Make %%files list more explicit
  - Classify buildreqs by build/module/test
  - Don't use macros for commands
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.11-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.11-3
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.11-1
- Auto-update to 0.11 (by cpan-spec-update 0.01)
- Altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- Altered br on perl(Class::C3) (0.19 => 0.20)

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.10-1
- Update to 0.10

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jun 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.09
- Update to 0.09

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.07-1
- Update to 0.07

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-6
- Rebuild for new perl

* Thu Dec 06 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-5
- Bump

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-4
- Update INstall -> install

* Wed Dec 05 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-3
- Add Test::Pod deps

* Tue Dec 04 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-2
- Make Class::C3 dep explicit

* Tue Sep 18 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.05-1
- Specfile autogenerated by cpanspec 1.71
