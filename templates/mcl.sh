#!/bin/sh
#
# White River Computing "Peachland" server init.
#
# Starts and stops the supervisor for WRC's implementation of OODT.
#
# Note that templates/oodt.sh generates parts/templates/oodt. Are you
# editing the correct file?
#
# chkconfig: 345 88 11
# description: WRC OODT Supervisor

home="${buildout:directory}"
bin="${dollar}{home}/bin"
supervisord="${dollar}{bin}/supervisord"
supervisorctl="${dollar}{bin}/supervisorctl"

PATH=/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export PATH
TZ=UTC
export TZ

case "${dollar}1" in
start)
        echo "Starting White River OODT Supervisor"
        ${dollar}supervisord
        ;;
stop)
        echo "Stopping White River OODT Supervisor"
        ${dollar}supervisorctl shutdown
        ;;
restart)
        echo "Restarting White River OODT Supervisor"
        ${dollar}supervisorctl shutdown
        /bin/sleep 5
        ${dollar}supervisord
        ;;
graceful)
        echo "Restarting White River OODT processes under existing Supervisor"
        ${dollar}supervisorctl restart all
        ;;
status)
        ${dollar}supervisorctl status
        ;;
*)
        echo "Usage: ${dollar}0 {start|stop|restart|graceful|status}" 1>&2
        ;;
esac
exit 0
