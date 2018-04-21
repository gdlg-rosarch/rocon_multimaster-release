# Script generated with Bloom
pkgdesc="ROS - This doesn't do everything you need for multimaster, however it does provide the building blocks common to most or all multimaster systems. In particular, it provides the gateway model, which is an upgrade on old foreign_relay and master_sync concepts."
url='http://www.ros.org/wiki/rocon_multimaster'

pkgname='ros-kinetic-rocon-multimaster'
pkgver='0.8.1_3'
pkgrel=1
arch=('any')
license=('BSD'
)

makedepends=('ros-kinetic-catkin'
)

depends=('ros-kinetic-rocon-gateway'
'ros-kinetic-rocon-gateway-tests'
'ros-kinetic-rocon-gateway-utils'
'ros-kinetic-rocon-hub'
'ros-kinetic-rocon-hub-client'
'ros-kinetic-rocon-test'
'ros-kinetic-rocon-unreliable-experiments'
)

conflicts=()
replaces=()

_dir=rocon_multimaster
source=()
md5sums=()

prepare() {
    cp -R $startdir/rocon_multimaster $srcdir/rocon_multimaster
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

