check_process() {
  echo "$ts: checking python manage.py runserver 9090"
  [ "python manage.py runserver 9090" = "" ]  && return 0
  [ `pgrep -n python manage.py runserver 9090` ] && return 1 || return 0
}

while [ 1 ]; do 
  # timestamp
  ts=`date +%T`

  echo "$ts: begin checking..."
  check_process "python manage.py runserver 9090"
  [ $? -eq 0 ] && echo "$ts: not running, restarting..." && `python manage.py runserver 9090 &`
  sleep 5
done