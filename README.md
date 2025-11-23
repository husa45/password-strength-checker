# Password strength checker
In our modern day life ,While all of our confidential data is stored online ,It is important to have secure authentication methods ,And unsurprisingly the first line of defense is A password.
But we ca'nt choose any password ,because due to computational improvements ,it more easier to crack weak short passwords maybe within an hour or less.

That's why I created this project ,
A GUI based python project that let's you choose a certain password and it will show you it's strength .

It also utilizes have I been pwned API 
to check whether the candidate password was exposed in a data breach before ,displaying a message accordingly .

**To use this program you need to clone the repo first :**
```
git clone (this repo link)
```

**Install dependencies :**
```
pip install -r requirements.txt
```
Or pip3 depending on what version of pip is already installed .

**Now,run it ,and you are good to go:**
```
python3   password_strength.py 
```

## ❗Note :You need to be connected to the internet in order to use the checking for password pwnage.
