#!/bin/sh

# Waiting for postgresql to start accepting connections
retry() {
  max_attempts="$1"; shift
  seconds="$1"; shift
  cmd="$@"
  attempt_num=1

  until $cmd
  do
    if [ $attempt_num -eq $max_attempts ]
    then
      echo "Attempt $attempt_num failed and there are no more attempts left!"
      return 1
    else
      echo "Attempt $attempt_num failed! Trying again in $seconds seconds..."
      attempt_num=`expr "$attempt_num" + 1`
      sleep "$seconds"
    fi
  done
}
echo "Waiting for postgres..."
retry 100 0.2 pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -d $DATABASE_NAME > /dev/null
echo "PostgreSQL started"

exec "$@"
