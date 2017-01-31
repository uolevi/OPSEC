# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
A Python script to change user's password to an unknown random one.

You may use it in virtual machines basically to force you to go back to
a safe and clean snapshot (because after running it you do not know your
password to install anything, for example). In such a case, of course
remember to take that clean and safe snapshot before running it...

Remember also to turn off screen saver before leaving the screen.

If the machine gets compromised, there is no change to access the real
passwords you are using (in the clean snapshot).

Currently salted SHA512 is used to hide the generated random temporary 
password. Why? Just for fun. Even if an attack via lookup tables is not
an issue here, script uses 16 bytes long salt, just for fun.

Thanks to:
    * http://stackoverflow.com/questions/4749083/is-there-a-way-to-script-in-python-to-change-user-passwords-in-linux-if-so-how/9227779
    * http://stackoverflow.com/questions/3854692/generate-password-in-python
    * http://stackoverflow.com/questions/7479442/high-quality-simple-random-password-generator
    * http://stackoverflow.com/questions/36239289/python-password-program

Example use cases:
    * Put it cron and run it every 10th minute.
    * Run it just before you install and test new software.
    * Run it just before you start browsing some funny or malicious webpages.
    * Run it before you open your emails.
    * <you name it>

"""

import os
import subprocess,crypt,random

# characters to be used in the password, you may select your own
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#?@/,._:*<>=+-%()[]|{}"
# "salt is a string chosen from the set of [a-zA-Z0-9./]"
SALTCHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./"
# wanted password length
PASSWORDLENGTH = 40
# user's password to be changed
LOGIN = "putyournamehere"

def generate_temp_password(length):
    if not isinstance(length, int) or length < PASSWORDLENGTH:
        raise ValueError("Temp password's length must be positive and equal or longer than " + PASSWORDLENGTH + ".")
    return "".join(CHARS[ord(c) % len(CHARS)] for c in os.urandom(length))

password = generate_temp_password(PASSWORDLENGTH)
print password
salt = ''.join(random.choice(SALTCHARS) for i in range(16))
print salt
shadow_password = crypt.crypt(password, '$6$'+salt+'$')
print shadow_password

# Just for additional obfuscation
password = generate_temp_password(PASSWORDLENGTH)
salt = ''.join(random.choice(SALTCHARS) for i in range(16))

r = subprocess.call(('usermod', '-p', shadow_password, LOGIN))

if r != 0:
    raise ValueError("Error in changing password for " + LOGIN)
