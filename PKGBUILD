# Script generated with Bloom
pkgdesc="ROS - A hub acts as a shared key-value store for multiple ros systems (primarily used by gateways)."
url='http://ros.org/wiki/rocon_gateway'

pkgname='ros-kinetic-rocon-gateway'
pkgver='0.8.1_3'
pkgrel=1
arch=('any')
license=('BSD'
)

makedepends=('ros-kinetic-catkin'
'ros-kinetic-roslint'
)

depends=('python2-crypto'
'ros-kinetic-gateway-msgs'
'ros-kinetic-rocon-console'
'ros-kinetic-rocon-gateway-utils'
'ros-kinetic-rocon-hub-client'
'ros-kinetic-rocon-python-comms'
'ros-kinetic-rocon-python-redis'
'ros-kinetic-rocon-python-utils'
'ros-kinetic-rocon-python-wifi'
'ros-kinetic-rosgraph'
'ros-kinetic-roslib'
'ros-kinetic-rosparam'
'ros-kinetic-rospy'
'ros-kinetic-rosservice'
'ros-kinetic-rostopic'
'ros-kinetic-std-srvs'
'ros-kinetic-zeroconf-avahi'
'ros-kinetic-zeroconf-msgs'
)

conflicts=()
replaces=()

_dir=rocon_gateway
source=()
md5sums=()

prepare() {
    cp -R $startdir/rocon_gateway $srcdir/rocon_gateway
}

build() {
  # Use ROS environment variables
  source /usr/share/ros-build-tools/clear-ros-env.sh
  [ -f /opt/ros/kinetic/setup.bash ] && source /opt/ros/kinetic/setup.bash

  # Create build directory
  [ -d ${srcdir}/build ] || mkdir ${srcdir}/build
  cd ${srcdir}/build

  # Fix Python2/Python3 conflicts
  /usr/share/ros-build-tools/fix-python-scripts.sh -v 2 ${srcdir}/${_dir}

  # Build project
  cmake ${srcdir}/${_dir} \
        -DCMAKE_BUILD_TYPE=Release \
        -DCATKIN_BUILD_BINARY_PACKAGE=ON \
        -DCMAKE_INSTALL_PREFIX=/opt/ros/kinetic \
        -DPYTHON_EXECUTABLE=/usr/bin/python2 \
        -DPYTHON_INCLUDE_DIR=/usr/include/python2.7 \
        -DPYTHON_LIBRARY=/usr/lib/libpython2.7.so \
        -DPYTHON_BASENAME=-python2.7 \
        -DSETUPTOOLS_DEB_LAYOUT=OFF
  make
}

package() {
  cd "${srcdir}/build"
  make DESTDIR="${pkgdir}/" install
}

