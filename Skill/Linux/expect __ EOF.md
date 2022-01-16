apt install expect

```plain
/usr/bin/expect << EOF
 spawn smbpasswd -a $USER_NAME
 expect "password:"
 send -- "$USER_PASS\n"
 expect "password:"
 send -- "$USER_PASS\n"
 expect "#"
EOF
```

