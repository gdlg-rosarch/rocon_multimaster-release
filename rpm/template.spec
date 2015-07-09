Name:           ros-indigo-rocon-hub-client
Version:        0.7.10
Release:        0%{?dist}
Summary:        ROS rocon_hub_client package

Group:          Development/Libraries
License:        BSD
URL:            http://ros.org/wiki/rocon_hub_client
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-gateway-msgs
Requires:       ros-indigo-rocon-gateway-utils
Requires:       ros-indigo-rocon-python-redis
Requires:       ros-indigo-rospy
BuildRequires:  ros-indigo-catkin

%description
Client api for discovery and connection to rocon hubs. It also has a few
convenience api for manipulating data on the hub.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Thu Jul 09 2015 Daniel Stonier <d.stonier@gmail.com> - 0.7.10-0
- Autogenerated by Bloom

* Thu Jul 09 2015 Daniel Stonier <d.stonier@gmail.com> - 0.7.9-0
- Autogenerated by Bloom

* Mon Apr 27 2015 Daniel Stonier <d.stonier@gmail.com> - 0.7.8-0
- Autogenerated by Bloom

* Mon Mar 23 2015 Daniel Stonier <d.stonier@gmail.com> - 0.7.7-0
- Autogenerated by Bloom

* Fri Nov 21 2014 Daniel Stonier <d.stonier@gmail.com> - 0.7.6-0
- Autogenerated by Bloom

* Tue Sep 23 2014 Daniel Stonier <d.stonier@gmail.com> - 0.7.5-0
- Autogenerated by Bloom

* Mon Aug 25 2014 Daniel Stonier <d.stonier@gmail.com> - 0.7.4-0
- Autogenerated by Bloom

