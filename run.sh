check_process() {
  echo "$ts: checking python manage.py runserver"
  [ "python manage.py runserver" = "" ]  && return 0
  [ `pgrep -n python manage.py runserver` ] && return 1 || return 0
}

while [ 1 ]; do 
  # timestamp
  ts=`date +%T`

  echo "$ts: begin checking..."
  check_process "python manage.py runserver"
  [ $? -eq 0 ] && echo "$ts: not running, restarting..." && `python manage.py runserver 9090`
  sleep 5
done