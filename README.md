# NTUOSS Selenium & Facebook API for Udemy Workshop
### Instructions for Web Automation for Enrollment into ~800 Udemy courses worth ~$100,000

*by [Jarrett Yeo](https://github.com/jarrettyeo) for NTU Open Source Society*

*Date last updated: 10 November 2017*
___

**Disclaimer:** *This document is only meant to serve as a reference for the attendees of the workshop. It does not cover all the concepts or implementation details discussed during the actual workshop.*
___

### Questions

If you have a question, feel free to raise your hand any time during the workshop or email your questions to [me](mailto:shanwei96@gmail.com).

### Errors

For errors, typos or suggestions, please do not hesitate to [post an issue](https://github.com/jarrettyeo/UPDATE_THIS/issues/new). Thank you!
___

## Introduction

Udemy, one of the biggest online course platforms, offers tons of comprehensive courses for almost anything under the sun. Most of these are paid and can go up to $200, but there are many coupons out there on the Internet that offer those for free. Today, we will be showing you how we will hunt for these coupons and automate the enrollment into these courses using a bit of Python and Selenium magic.

## Sneak Preview

Here’s what you’ll be able to get for yourself just by attending this workshop:

~800 paid courses worth a total of $100,000

## What’s New

We have gotten feedback from you that there aren’t many takeaways from our previous sessions apart from copy-pasting. Let’s shake things up a bit for this workshop.

Instead of asking you to play the jigsaw puzzle of copy and pasting snippets of codes here and there, I’ll keep the copy-pasting of code to the minimal. I will be doing more of explaining what, why and how we are doing things in this session using a keynote presentation. We hope that you will be able to understand what we are trying to do even if you do not comprehend the code entirely, and learn about the thought processes behind solving problems with coding.

Additionally, all the files that we will be using have been uploaded on this repo so that you can always download them, understand them, and execute them easily. I have also structured this workshop into multiple checkpoints as well as instructions on helping you to catch up if you ever get lost.

Let’s get started!
___

## Index

<!-- TODO: write about index -->

___

## Workshop Overview

#### Part I

We need a place to store our data. For this workshop, we can settle for sqlite.

#### Part II

Next, we teach you how to retrieve Udemy coupons from Reddit first:

> [Reddit post](https://www.reddit.com/r/learnprogramming/comments/75ovw4/250_free_udemy_course_coupons/) by commandrbond (30-50% success rate)

I will be showing you how to get things up and running. In fact, I have cleaned the Udemy links in the above Reddit post and compiled them into a csv file to make things easier for you.

We’ll come back to scrapping more coupons in Part III (from Facebook!) and IV when we have time.

#### Part III

Next, we will use Selenium to create a webdriver to automate logging you into your account, and thereafter enroll you into all the once-paid-now-temporarily-free courses. That’s where the fun begins!

#### Part IV

Thereafter, we will be repeating the process but from a real Facebook page, but this time, it will put our web scrapping, JSON and API skills as well as patience to the test. We will not be repeating the explanations for web scrapping, but we will focus more on using the Facebook (and Bitly, we’ll explain) API and using JSON.

> [BestFreeCoupons Facebook Page](https://www.facebook.com/BestFreeCoupons) using Facebook Graph API (14% success rate)

#### Part V (Homework – Not covered in workshop)

As a bonus, the following resource is appended below but we will not be going through on scrapping them in this workshop:

> [LearnViral.com](https://udemycoupon.learnviral.com/coupon-category/free100-discount/) (18% success rate)

Additionally, you could always perform a simple, power search on Google to get the dirty job done easily. Or you could just create Google Search alerts. More on these in the actual section towards the end of the document.

Feel free to hit me up to check your homework with me!

#### Part VI

Possible future enhancements. Will be explained below.

___

## Part 0

#### 0.1 Workshop Requirements

For this workshop, you’ll need the following to get started:
1.	Python and pip installed
2.	Atom or any other text editor of your choice installed
3.	DB Browser for SQLite
4.	Chrome Webdriver – Chromium 2.27
5.	Udemy account (do this later)
6.	Bit.ly account (do this later)
7.	Facebook account (do this later)

Detailed instructions are found below.

#### 0.2 Install Python 3 and pip

Check [this](https://github.com/jarrettyeo/NTUOSS-PythonPipInstallation) out.

#### 0.3 Install a Text Editor

I suggest Atom.

#### 0.4 Install DB Browser for SQLite

Let’s make life a lot easier by installing [this](http://sqlitebrowser.org/).

#### 0.5 Download Chrome Webdriver (Chromium 2.27)

*Let's do this later.*

Browse to [this link](https://chromedriver.storage.googleapis.com/index.html?path=2.27/).

> **Note**<br>
> We are using Chromium 2.27 because there is a bug from 2.28 and onwards.<br><br>
> Download and save zip anywhere, we’ll unzip chromedriver.exe later in Part III. You do not need to do it now.

#### 0.6 Get a Udemy account

*Let's do this later.*

Sign up [here](https://www.udemy.com/).

#### 0.7 Get a Bit.ly account

*Let's do this later.*

Sign up [here](https://bitly.com/a/sign_up).

#### 0.8 Get a Facebook account

If you have an online social life, you can probably skip this step.

___

## Part I

#### 1.1 pip install

If you haven’t done so already, let’s use pip to install our dependencies:

**Windows**

Run cmd as administrator, then execute:

```
pip install sqlalchemy requests beautifulsoup4 selenium
```

**Mac**

Open the terminal, and execute:

```
sudo pip3 install sqlalchemy requests beautifulsoup4 selenium
```

Key in your password when prompted. You will not be able to see anything as you type your password into the console.

#### 1.2 Create Working Directory

Just create a folder on your Desktop titled "udemy-selenium".

For the adventurous you can run console commands as shown below to get the same task done.

**Windows**

```
cd C:\Users\YOUR_USERNAME\Desktop
mkdir udemy-selenium
cd udemy-selenium
```

**Mac**

```
cd Desktop
mkdir udemy-selenium
cd udemy-selenium
```

#### 1.3 Create tabledef.py

Now we need to create a py file that constructs our sqlite database in the working directory.

There is no need for you to copy-paste and create this file manually. Right-click [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/tabledef.py) and save it as ```tabledef.py``` into your working directory.

#### 1.4 Create SQLite Database

We’ll be using sqlalchemy to create and manage our sqlite database.

Make sure your terminal is in the working dir, then create the database by executing the following:

**Windows**

```
python tabledef.py
```

**Mac**

```
python3 tabledef.py
```

#### 1.5 Check SQLite Database

Browse to the working directory and check if you have a new file called ```courses.db```.

Double-click to open it with DB Browser for SQLite.

Optionally, you can set your machine to always open .db files with the program.

#### 1.6 Checkpoint 1

**Check 1 – Your working directory**

Do you now have ```courses.db``` and ```tabledef.py``` in your working directory?

**Check 2 – Your courses.db database (view in DB Browser)**

Do you see an empty table called courses?

Great! Let’s move on.

___

## Part II

#### 2.1 Cleaning up the Reddit post

Source 3 of our coupons comes from a [Reddit post](https://www.reddit.com/r/learnprogramming/comments/75ovw4/250_free_udemy_course_coupons/) by commandrbond.

If you take a close look at the links, there are extra text headers and some of them are not in proper format that we can use as URLs. We thus need to clean the data before we import the Udemy URLs into our database, but fret not, I have already done so for you as a CSV file.

Right-click [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/reddit.csv), save as ```reddit.csv``` into your working directory.

So you should have 3 files in your working dir now: ```tabledef.py```, ```reddit.csv``` and ```courses.db```.

#### 2.2 Importing CSV into SQLite database

Let’s check out the reddit.csv file. You can open it with Notepad or Atom or any text editor of your choice, even Excel works too.

I have made every URL sit on one line by itself, and I have also written a ```reddit-csv-udemy.py``` file to allow easy importing into our db.

Let’s check ```reddit-csv-udemy.py``` file out:

The code basically imports every Udemy URL as a separate entry into our db.

Right-click [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/reddit-csv-udemy.py), save as ```reddit-csv-udemy.py``` into your working dir, and execute the following:

**Windows**

```
python reddit-csv-udemy.py
```

**Mac**
```
python3 reddit-csv-udemy.py
```

Once your console is done executing the command, refresh your db on DB Browser for SQLite.

You will see 235 entries. Yay!

#### 2.3 Checkpoint 2A

**Check 1 – Your working directory**

Do you now have ```courses.db```, ```tabledef.py```, and ```reddit-csv-udemy.py``` in your working directory?

**Check 2 – Your courses.db database (view in DB Browser)**

Do you see 235 entries in the courses table with the ```udemy_url``` column filled?

Great! Let’s move on.

#### 2.4 Reviewing the HTML structure

Let’s take a look at a typical Udemy course page.

Open a new browser (I’ll be using incognito/private mode in Chrome and I recommend you the same). Next, hit ```F12``` or ```Control``` + ```Shift``` + ```I``` if you on Windows, or ```Command``` + ```Option``` + ```I``` on Mac, to open up Developer Tools.

For each of the 4 links below, let’s do a quick exercise:

1. Toggle Inspect Element Mode by hitting ```Control``` + ```Shift``` + ```C``` on Windows or Command+Shift+C on Mac.

2. Inspect (by hovering over) the course title, “Buy Now” button (for the “href” attribute), original price title, and discounted price title. Take note of the elements. We will be scrapping all our courses for the above – think about how we can uniquely identify them.

>**Rationale**<br>
> We are doing this so that we can quickly determine whether we should enroll into the Udemy course or not. We are only interested in Link 1-type courses (was paid, now free).

Let’s begin our exercise!

---

**[Link 1](https://www.udemy.com/ultimate-web/learn/v4/?couponCode=LRNWEB) – Was paid, now free**

Browse to the first link in our reddit.csv file.

$210 course going for $0 @ 100% off? Awesome!

**[Link 2](https://www.udemy.com/complete-beginners-guide-to-forex-trading/) – Was paid, now cheaper but still paid**

What about this?

Bummer! The course is on discount but we still need to pay for it. We’ll pass, things are only good when they are going for free.

**[Link 3](https://www.udemy.com/mastering-agile-scrum-project-management-pmi-rep/) – Was paid, still same price**

And this?

Not even a discount.

**[Link 4](https://www.udemy.com/make-money-become-a-shopify-expert-from-zero-to-hero/) – Is free itfp**

Lastly…

Course that’s free itfp? Nah it doesn’t seem like it’s worth it!

---

Have you figured out how to scrap the HTML elements?

#### 2.5 Reviewing the Web Scrapping / Automation Process

For us to know how we should program our webdriver to automate the course enrollment, we need to understand how the enrollment process works from the perspective of your web browser.

Let’s get started.

Now, let’s sign into your Udemy account from your browser. Navigate to one of Link 1’s (i.e. modules that were once paid, now temporarily free).

It goes without saying that you’ll enroll yourself into modules by clicking on the Enroll Now button. But before that, hover over the button. Notice how Udemy redirects you to the checkout page (i.e. another URL), then starts enrolling you into the course (the process of doing so is shown using a loading gif), and thereafter, shows you a success message.

We’ll come back to this later, but now we realise that it’s easier to retrieve the checkout link and access it directly, than to browse to the main course page, and figuring things from there.

#### 2.6 Scrapping the Udemy course page

The magic begins!

Right-click the link [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/reddit-udemy-checkout.py), and save as ```reddit-udemy-checkout.py``` on the same working directory.

Before we run the code, let’s take a brief look at what our code does.

What does the code do?

In summary, it filters the database for the reddit entries that we have identified by the source ```filter(Course.post_date == "reddit")``` and then its status of whether we have checked a course for its checkout URL by using ```filter(Course.status == "udemy url found")```.

For web scrapping, there are libraries/packages such as ```urllib``` and ```requests``` that can conduct simple HTML data requests, as well as more high-level HTML parsers like ```beautifulsoup```. Using what we have identified in Part II, our code will search for these identifiers and return us the data which we will store in our db.

For instance,

```python
# course_name
sample = soup.find("h1", "clp-lead__title")
course_name = sample.text
print("course_name:", course_name)

# checkout_url
sample = soup.find("a", "course-cta--buy")
checkout_url = "https://www.udemy.com" + sample.attrs['href']
print("checkout_url:", checkout_url)

# discounted_price
sample = soup.find("span", "price-text__current")
```

Finally it’s time! Let’s execute the following:

**Windows**

```
python reddit-udemy-checkout.py
```

**Mac**

```
python3 reddit-udemy-checkout.py
```

Additionally, you can always abuse the refresh button on DB Browser to watch the changes live.

> **Note**<br>
> We did not create any way for us to stop the code (that's bad). However, you can always hit or spam ```CTRL``` + ```C``` to stop the code from executing.

#### 2.7 Checkpoint 2B

**Check 1 – Your working directory**

Do you now have ```courses.db```, ```tabledef.py```, ```reddit-csv-udemy.py``` and ```reddit-udemy-checkout.py``` in your working directory?

**Check 2 – Your courses.db database (view in DB Browser)**

Do you see 235 entries in the courses table with the ```udemy_url``` and ```checkout_url``` columns filled?

Great! Let’s move on.

___

## Part III

#### 3.0 Introduction to Web Automation using Selenium

As if watching our console and database return us live results isn’t enough, we will now carry out some Selenium magic, where you will get to see your browser (technically, a webdriver) sign you into your Udemy account, and enroll you into all the free courses!

By the way, Selenium lets you automate web browsers such as Google Chrome, and according to its official project page [here](http://www.seleniumhq.org/), its main purpose is web application testing and automating administrative tasks.

#### 3.1 Extracting Chrome Webdriver into the working directory

Think of a webdriver as a special standalone browser that allows you to access and manipulate it easily. We will be using Chrome for this project.
If you haven’t done so already, download the chrome webdriver [here](https://chromedriver.storage.googleapis.com/index.html?path=2.27/).

We are using Chromium 2.27 because there is a bug from 2.28 and onwards.

Download and save zip anywhere, we’ll unzip chromedriver.exe into the working dir.

>**Important**<br>
>If you are prompted by Firewall, allow access to both private and public networks.

#### 3.2 Overview of Work Process

Before we begin, let’s look at the overview of this step.

1. Start the “web browser” (i.e. webdriver). We will be using Chrome as mentioned.

2. Open the login page.

3. Find the email and password fields.

4. Key in our email and password respectively.

5. Loop through all free courses and check if we have enrolled in them or not.

    1. If already enrolled, indicate so.
    2. If not, enroll.
    3. Else, if there is an error, skip it.

6. End

#### 3.3 Selenium Web Automation

Right-click this file [here](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/reddit-checkout-enroll.py), save as ```reddit-checkout-enroll.py``` into your working dir.

Don’t worry, we will be explaining the bulk of the code in the comments of the py file.

Remember to change the following to your Udemy email address and password, and your full working dir path:

```
UDEMY_EMAIL = "REPLACE_ME" # replace this with your access key, for example: UDEMY_EMAIL = "your_email_address@blah.com"
```

```
UDEMY_PASSWORD = "REPLACE_ME" # replace this with your access key, for example: UDEMY_PASSWORD = "ilovecplusplus"
```

```
UDEMY_FOLDER_PATH = "REPLACE_ME" # replace this with your access key, for example: UDEMY_FOLDER_PATH = "C:/Users/YOUR_USERNAME/udemy-selenium/"
```

> Windows users beware - change all \ to / in folder path

Finally, let’s execute our code!

**Windows**

```
python reddit-checkout-enroll.py
```

**Mac**

```
python3 reddit-checkout-enroll.py
```

Again, you can always watch the db for changes using DB Browser. It gives you a good idea of what we are doing live.

#### 3.4 Checking Udemy for Enrollment

Let’s hit ```CTRL``` + ```C``` after watching a couple of enrollments. We want to be sure that we have truly enrolled ourselves in the courses on Udemy. Let’s just log into our account using your browser and navigate to “My Courses”.

#### 3.5 Checkpoint 3

**Check 1 – Your working directory**

Do you now have ```courses.db```, ```tabledef.py```, ```reddit-csv-udemy.py```, ```reddit-udemy-checkout.py``` and ```reddit-checkout-enroll.py``` in your working directory?

**Check 2 – Your courses.db database (view in DB Browser)**

Do you see 235 entries in the courses table with the ```udemy_url```, ```checkout_url```, and ```remarks``` columns filled?

Great! Let’s move on.

___

## Part IV

#### 4.0 “Scrapping” Facebook for More Coupons

Now we will be looking at this Facebook page which regularly posts free coupon codes (a couple of new coupons per day).

> [BestFreeCoupons Facebook Page](https://www.facebook.com/BestFreeCoupons) using Facebook Graph API<br>
>(14% success rate)

Things are about to get crazy real fast, and I will be briefly explaining how things work. Sit tight!

#### 4.1 Overview of Work Process

First, we need to explore how the entire work process goes.

You can browse to the Facebook page and see the following work process plays out.

1. Access the Facebook page.

2. Get the bit.ly link from every Facebook post.

3. Convert the bit.ly link into the Udemy URL (i.e. expanding the link).

4. Go to the Udemy page and retrieve the checkout URL.

5. Finally, enroll yourself into the course. Same drill as above.

How tedious! Thankfully, we have already done up the code for you.

#### 4.2 Setting Things Up

Let’s get this done really quickly.

The same drill again. Right-click on all the following ```.py``` files and save them as their filenames are into your working dir.

[facebook-bitly.py](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/facebook-bitly.py)

[bitly-expanded.py](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/bitly-expanded.py)

[expanded-udemy.py](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/expanded-udemy.py)

[udemy-checkout.py](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/udemy-checkout.py)

[checkout-enroll.py](https://raw.githubusercontent.com/jarrettyeo/NTUOSS-SeleniumFacebookAPIforUdemy/master/checkout-enroll.py)

Notice how we have broken up each step in 4.1 into separate python files for clarity. We will explain to you briefly how things work using the source files.

Let’s edit ```checkout-enroll.py```. Remember to change the following to your Udemy email address and password, and your full working dir path:

```
UDEMY_EMAIL = "REPLACE_ME" # replace this with your access key, for example: UDEMY_EMAIL = "your_email_address@blah.com"
```

```
UDEMY_PASSWORD = "REPLACE_ME" # replace this with your access key, for example: UDEMY_PASSWORD = "ilovecplusplus"
```

```
UDEMY_FOLDER_PATH = "REPLACE_ME" # replace this with your access key, for example: UDEMY_FOLDER_PATH = "C:/Users/YOUR_USERNAME/udemy-selenium/"
```

> Windows users beware - change all \ to / in folder path

#### 4.3 Additional Requirements

Before we watch the magic unfold for the second time, let’s complete our setup first.

**Step 1 – Get a Facebook API key**

1. Login to Facebook

2. Go to [this link](https://developers.facebook.com/apps/).

3. Click on “Get Started”

4. Click “Add Your First Product”

5. Click “Show” to get your Facebook key.

> This API key will be your access token (parameter).

Let’s edit ```facebook-bitly.py```:

```
FACEBOOK_KEY = "REPLACE_ME" # replace this with your access key, for example: FACEBOOK_KEY = "1234567890|sdubgfownudgwer28ru8nc"
```

**Step 2 – Get a bitly API key**

1. Sign up for a bitly account [here](https://bitly.com/a/sign_up). Do not use Facebook to create an account (i.e. just sign up for a bitly account)

2. Go to [this link](https://app.bitly.com/bbt2/).

3. Click on top-right hamburger menu icon, click on your email, click on Generic Access Token, key in password, then Generate to get your bitly key.

>This API key will be your access token.

Let’s edit ```bitly-expanded.py```:

```
BITLY_ACCESS_TOKEN = "REPLACE_ME" # replace this with your access key, for example: BITLY_ACCESS_TOKEN = "894c3beijr893nrd398"
```

**Step 3 – Manually importing a custom bitly library**

Because the default ```bitly``` package installed by ```pip``` is [not compatible with Python 3](https://github.com/bitly/bitly-api-python/issues/39), we will need to manually provide edited bitly modules so that we can call the bitly API:

1. Navigate to [this Dropbox link](https://www.dropbox.com/s/7vbsda9hbgodq77/bitly.zip?dl=0), and download the zip file.

2. Unzip both ```bitly_api.py``` and ```bitly_http.py``` into the working dir.

**Step 4 - Installing certifi (Required for Mac OS only)**

Mac users may encounter the following error when using ```urllib```:

```
URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581)>
```

The error can be resolved by [installing the certifi package](https://stackoverflow.com/a/42334357), all you need to do is to execute the following command on your Terminal: 

```
/Applications/Python\ 3.6/Install\ Certificates.command
```


#### 4.4 Checkpoint 4

That took a while. Now, let’s do a thorough check on our files so that everything we need is in place.

**Check 1 – Your working directory**

Do you now have ```courses.db```, ```tabledef.py```, ```facebook-bitly.py```, ```bitly-expanded.py```, ```expanded-udemy.py```, ```udemy-checkout.py```, and ```checkout-enroll.py```, as well as ```bitly_api.py``` and ```bitly_http.py``` in your working directory?

**Check 2 – Your edited .py files (view in your Text Editor)**

1. Have you updated ```FACEBOOK_KEY``` in ```facebook-bitly.py```?

2. Have you updated ```BITLY_ACCESS_TOKEN``` in ```bitly-expanded.py```?

3. Have you updated ```UDEMY_EMAIL```, ```UDEMY_PASSWORD``` and ```UDEMY_FOLDER_PATH``` in ```checkout-enroll.py```?

#### 4.5 Executing the Code

Finally, we are now able to try our code!

Let’s start by running the following commands, one after another:

**Windows**

```
python facebook-bitly.py
python bitly-expanded.py
python expanded-udemy.py
python udemy-checkout.py
python checkout-enroll.py
```

**Mac**

```
python3 facebook-bitly.py
python3 bitly-expanded.py
python3 expanded-udemy.py
python3 udemy-checkout.py
python3 checkout-enroll.py
```

You probably do not have time to run through all of python files before this workshop ends. Just execute the files in order, loop through a couple of courses, hit ```CTRL``` + ```C``` to end the code execution, and move on to the next line of code.

Remember, you can stalk all changes in DB Browser.

___

## Part V (Homework – Not covered in workshop)

#### 5.0 Summary

As a bonus, the following resources are appended below but we will not be going through them in this workshop.

#### 5.1 LearnViral.com (18% success rate)

This website provides a list of both “good” and “bad” coupons (depending on users’ reported success rate with the coupons).

**DIY Exercise 1:**

With ```beautifulsoup4```, use [this base URL link](https://udemycoupon.learnviral.com/coupon-category/free100-discount/) and then loop through the pages from 1 to ~390 (i.e. last page of all coupons) and scrap all the required data.

#### 5.2 Google Advanced Search

Additionally, you could always perform a simple, power search on Google to get the dirty job done easily. That means no coding, phew!

**DIY Exercise 2:**

Browse to ```google.com``` in your browser. Search for this in the search box:

```
allinurl: "couponCode" site:udemy.com
```

Thereafter, sort results by date, filter by past week / 24 hours.

#### 5.3 Google Alerts

Alternatively and even more easily, just subscribe to alerts [here](https://www.google.com/alerts).

Google will send you “updates on free coupon codes” to your specified email address whenever it crawls the web for you. You can take my word for it – Google will for sure be able to do a faster and better job than you by far.

**DIY Exercise 3:**

Sign up for alerts with reference to the search query in DIY Exercise 2.

#### 5.4 Homework Review

Feel free to hit me up to check your homework with me or ask for further directions!

___

## Part VI

#### 6.0 Possible Future Enhancements

- Writing a duplicate check when importing Udemy links (demo only for now – code will be updated shortly)

- Writing a summary that shows you the number of unique courses that you have enrolled in, as well as the total net worth of your account (demo only for now – code will be updated shortly)

- Fixing the ```post_date``` column / Creating another column called ```source``` (e.g. reddt, facebook, learnviral.com) – This can be easily done using DB Browser for SQLite (demo only for now – code will be updated shortly)

- Asynchronous tasking using Celery – notice how Python checks courses one by one? Why not fire multiple instances of the code at once to speed things up?

- A central script (e.g. ```main.py```) that fires all above scripts

- Task scheduling to automatically check for new courses

___

## Test Info

This tutorial has been tested using a Windows 7 computer running Home Premium SP1. It is accurate as of 10 November 2017.

## Acknowledgements

Many thanks to [Chang Kai Lin, Ries](https://www.instagram.com/kailinchanggg/) for sacrificing her MacBook Air and loaning it to me indefinitely for testing, and the [NTU Open Source Society](https://github.com/ntuoss) committee for making this happen!

## Resources

[Python Docs](https://www.python.org/)

## Postface

Very regrettably, there are many areas of improvement for the code used in this workshop. I promise you that I will polish it when time permits.
