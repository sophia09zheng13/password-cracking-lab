# Lab: Password Cracking

<img align=right src=img/black-hackerman.webp width=250px />

Recall that in computer science,
"hacking" is a good thing.
It is the process of building cool stuff.
"Cracking" is the bad thing that muggles usually mean when they talk about hacking.
Cracking is the process of breaking stuff.

In this lab, you'll get your first taste of cracking.
You'll learn how to crack the passwords of encrypted zip files using python,
and see that the basic tools for cracking are the same as the basic tools for hacking.

You will also review:
1. creating your own meaningful python programs from scratch
1. opening zip files in python
1. using try/except to handle exceptions

## Part 0: Setup

Clone this repo and then cd into the clone.

## Part 1: Background

**Working with zip files in python**

This repo contains several interesting zip files.
The first is an encrypted zip file called `guido_secrets.zip`.
In this first part of the lab,
you'll learn how to open up and decrypt this file in python.

Python can open password protected zip files using the built-in `zipfile` module.
Create a new python file with the following code:
```
from zipfile import ZipFile
with ZipFile('guido_secrets.zip') as zf:
    password = b'BFDL'
    zf.extractall(pwd=password)
```
Notice:
1. After running this program,
    a new file `guido_secrets/secrets.txt` has been created.

    > **Recall:**
    > The string above is called a *relative path*.
    > The part to the left of the `/` is a folder name,
    > and the part to the right is the name of the file.
    > You will often see python tutorials giving relative paths like this to files,
    > and so you should make sure you understand why this is the correct relative path to the created file.
    
    The file contains a poem called *The Zen of Python*.
    This is a particularly famous poem that every pythonista should read through at least once.
    (You should open the file in VSCode and read the poem.)

1. The `password` variable is a `bytes` object and not a `str`.
   It's common for the sequence of bytes to correspond to an English language ASCII sequence,
   but it's not required.
   It is impossible to have zip file passwords with non-latin characters (e.g. Chinese characters) that cannot be stored in ASCII.

   Try changing the `password` variable to `'BFDL'` instead of `b'BFDL'` and you should get a `TypeError`.
   (And hopefully it makes sense why.)
   
   Recall that if we have a variable with type `str`, we can convert it into a `bytes` object using the `.encode` function:
   ```
   password_str = 'BFDL'
   password = password_str.encode('ascii')
   ```
   is equivalent to
   ```
   password = b'BFDL'
   ```

1. Now try changing the byte sequence to anything other than `BFDL`.

   You should get an error message.
   Exactly which error message you get will depend on your system's settings, but common ones include `RuntimeError`, `BadZipfile`, and `zlib.error`).
   
   Depending on your computer's settings, files may or may not be created.
   But even if they are created, they will not contain the correct information.

**Zip bombs**

Zip files are particularly dangerous objects from a cracking perspective due to something called a "zip bomb".
Antivirus software often opens up zip files and looks inside for virus software.
But just the act of opening up a zip bomb can break a computer:
opening the zip file requires decompressing the file,
which can use up all the space on your hard drive.

For example:

1. The file `42.zip` is only 42KB large.
   But if you unzip it, it takes up 4.5PB of disk space on your computer!
   PB stands for petabytes, and 1 petabyte is 1000 terabytes (or 1,000,000 gigabytes).

   <img src=img/zipbomb.jpg width=400px>

   > **Note:**
   > The file `42.zip` is password protected so that it is not accidentally extracted.
   > If you're feeling brave, you can extract it with password `42`.

1. Even worse is the file [quine.zip](https://wgreenberg.github.io/quine.zip/).
   This file actually contains an exact copy of itself inside of it!
   Antivirus software traditionally opens zip files inside of other zip files,
   and so will get stuck opening `quine.zip` in an infinite loop of opening this file forever.

   It is safe to manually inspect this file,
   and I recommend you do.
   You can see that the file contains another file exactly like itself.
   Try opening the nested zip file a couple of times,
   and you'll keep seeing a copy of the same zip file appearing.

   <img src=img/zipbomb-dawg.jpg width=400px>

Python has no built-in protection against zip bombs,
so you should never open an untrusted zip file from python
(since it might be a bomb).

<!--
I promise that the files I'm giving you aren't zip bombs :)
-->

## Part 2: Cracking

**The Scenario:**

For this lab, you're going to pretend that it's the year 2015 and you are an analyst at the [GRU](https://en.wikipedia.org/wiki/GRU),
the infamous Russian spy agency.
One of your agents has risked their life to bring you the file `whitehouse_secrets.zip`.
This file was stolen from an IT worker at the white house,
and contains secret details of the upcoming US presidential election.
Your job is to access these details.
(Your bosses want to use them as part of an operation to manipulate the 2016 election.)

Unfortunately, the file is encrypted and you don't know the password.
Fortunately, you have some leads that will help you guess the password:

1. In July 2015, the website [Ashley-Madison (ashleymadison.com) had a major data leak](https://en.wikipedia.org/wiki/Ashley_Madison_data_breach).
   Ashley-Madison is a dating website for married people to find extra-marital lovers without their spouse's knowledge.

   <img src=img/ashley-madison2.jpg width=500px />

   A group of hackers called [The Impact Team](https://krebsonsecurity.com/tag/impact-team/) wanted to punish users of this website who they saw as immoral.
   And so they broke into the website,
   downloaded all the user data,
   and leaked this data on the internet.
   (Notice how the screenshot of the webpage above says the data is secure and encrypted... these claims are *always* marketing lies...)
   This leak is famous as the first major occurrence of [hacktivism](https://en.wikipedia.org/wiki/Hacktivism).

1. You know that the IT worker who created the `whitehouse_secrets.zip` is an active user of Ashley-Madison.
   This IT worker, like [most people](https://www.infosecurity-magazine.com/blogs/your-employees-reusing-passwords/),
   reuses the same password for everything they do.
   So one of the leaked passwords from Ashley-Madison will decrypt the `whitehouse_secrets.zip` file.
   You just have to figure out which one.

**Historical Aside:**

This scenario is not made up.
The military news website DefenseOne [reports that](https://www.defenseone.com/threats/2015/08/ashley-madison-hack-opm-government-military/119279/) 45 White House staffers had accounts at Ashley-Madison and more than 10000 military personnel had accounts.
The [Associated Press](https://apnews.com/article/1c34b10bff3744f386706480333ef9f5) confirms that a White House IT staffer was among the users.

Because of the national security implication of adultery,
adultery will [typically disqualify someone](https://news.clearancejobs.com/2013/01/15/adultery-and-security-clearances/) from getting a security clearance in the United States.
And even though adultery is not against the law for civilians,
adultery is a [felony offense](https://militarybenefits.info/ucmj-adultery/) for anyone in the military.

**Your Tasks:**

1. [The SecLists github repo](https://github.com/danielmiessler/SecLists/) contains lots of security related datasets,
   including the passwords of the Ashley-Madison leak.
    These passwords are located at `Passwords/Leaked-Databases/Ashley-Madison.txt`.
    Download this file.

1. Create a program `password_cracker.py` that finds the password of the zip file.
   Your program should:

    1. Open then file `Ashley-Madison.txt`
       and create a list called `passwords` that contains all of the passwords.

    1. For each password in `passwords`,
       try opening `whitehouse_secrets.zip` with that password.
       If it successfully opens, then print out the password.

       > **HINT:**
       > You should use a `try`/`except` clause to determine whether the zip file opened,
       > and perform different operations based on whether the file opened or not.

       > **HINT:**
       > There are many passwords in the `Ashley-Madison.txt` file.
       > Trying all possible passwords will take a long time (5-10 minutes).
       > You should print some debugging information every 10000 iterations of the for loop so that you can verify that your program is making progress.
       > In my solution, I print the current iteration number and the current password.
       > Since the passwords are ordered ASCIIbetically,
       > you can get a sense of when your program will be finished by seeing how close your current password is to the end of the alphabet.

       Once the file is successfully decrypted,
       you should have a new file `whitehouse_secrets/secrets.txt` that contains President Obama's secrets.

    1. Commit your `password_cracker.py` and `whitehouse_secrets/secrets.txt` files to the git repo and push them to github.

        Submit the link to your repo to canvas.

1. (Optional, but recommended)
   Change your passwords so that you're not using the same password for everything.
   I personally like to memorize all my passwords,
   but other people prefer using password managers to store the passwords.
   Firefox has an [excellent one built-in](https://www.mozilla.org/en-US/firefox/lockwise/).

   According to Snowden, the NSA is capable of guessing up to [1 trillion passwords per second](https://news.ycombinator.com/item?id=8448894),
   and [john the ripper](https://www.openwall.com/john/) is a famous open source tool that's capable of guessing millions of passwords per second on an ordinary computer.
   (Your python program is probably capable of guessing between 10,000-100,000 passwords per second, which is a lot slower than john the ripper.)
   So using strong passwords that are hard to guess is important.
   The [XKCD comic has a great technique](https://www.explainxkcd.com/wiki/index.php/936:_Password_Strength) for generating easy-to-remember passwords that not even the NSA can crack.
# password-cracking-lab
