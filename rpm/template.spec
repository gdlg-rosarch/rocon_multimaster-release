Name:           ros-kinetic-rocon-test
Version:        0.8.1
Release:        0%{?dist}
Summary:        ROS rocon_test package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/rocon_test
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-kinetic-rocon-console
Requires:       ros-kinetic-rocon-launch
Requires:       ros-kinetic-rocon-python-utils
Requires:       ros-kinetic-roslaunch
Requires:       ros-kinetic-rospy
Requires:       ros-kinetic-rostest
Requires:       ros-kinetic-rosunit
BuildRequires:  ros-kinetic-catkin
BuildRequires:  ros-kinetic-rostest

%description
Rocon test framework (i.e. multi-launch rostest framework).

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_LIBDIR="lib" \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/kinetic" \
        -DCMAKE_PREFIX_PATH="/opt/ros/kinetic" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/kinetic/setup.sh" ]; then . "/opt/ros/kinetic/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/kinetic

%changelog
* Tue Jun 21 2016 Daniel Stonier <d.stonier@gmail.com> - 0.8.1-0
- Autogenerated by Bloom

