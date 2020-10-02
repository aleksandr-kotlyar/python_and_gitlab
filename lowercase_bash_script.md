```shell script
 $ function lowercase(){ arg1=$1; echo "$1" | tr '[:upper:]' '[:lower:]'; }
 $ echo $REMOTE
 TruE
 $ echo $BROWSER
 FireFOX
 $ lowercase $REMOTE
 true
 $ lowercase $BROWSER
 firefox
 $ pytest ${TEST_SCOPE} --remote=$(lowercase $REMOTE) --browser=$(lowercase $BROWSER)
```