Troubleshooting Guide
=====================
If you are having any problems that you can't fix, look no further, because here is where you (Hopefully) find a solution to the problem.

If the problem you cannot solve, please submit an issue [here](https://github.com/RyanMaugin/Tachyon/issues), to get it fixed. Put please no
problems in the code. If that happens, please consult the [documentation](./documentation).


==============
### Installing

**Mac and Linux**
 - Access is denied!
	1. try executing setup.py with admin privilages, using `sudo python3 setup.py`
 - The computer says `Unreconised command: python3`, or something of that sort
	1. Try `python setup.py`. If you only have python 3 installed it will be called `python`.
	2. If the problem persists, install python from [python.org](https://www.python.org/downloads/), and make sure it is in the path varible (I think they do it for you already.)
- The computer says "ERROR IN LINE: XXX"
	1. Submit a bug [here](./documentation)

**Windows**
 - It doesn't work!!!
	1. Not supported yet. In the progress of doing it.
 - Adding the path variable (Windows 10) (For other versions, search [google](https://www.google.com/search?q=windows+edit+path&rlz=1C1CHBF_enUS706US706&oq=windows+edit+pa&aqs=chrome.0.0j69i57j0l4.4964j0j4&sourceid=chrome&ie=UTF-8). Cool programmers also use it, you know.)
	1. Make sure you have admin privilages
	2. To add the path variable, so that you can access this in the terminal, type `environment variables` in the search bar. 
	3. A option that says `Edit your system environment variables` should appear, by the time you enter `envir`.
	4. It will open up a window, that says `System Properties`
	5. On the bottom, there will have a button that says `Environment Variables`.
	6. On top, it will have a panel that says `User variables for <USER>`. Ignore that, unless you are installing it for your own user, and skip to step 8.
	7. Go to the bottom, where it says `System variables`. 
	8. Then scroll until you see the word `Path` or `PATH`.
	9. Double click one of them. It doesn't matter. You should see a popup that says `Edit environment variable`.
	10. Click the `New` button on the right.
	11. Add the path of this folder there.
	12. Click `OK` in all of the windows you just opened, and you are ready to get coding. Good luck and happy coding!
	13. For pictures go to <https://www.computerhope.com/issues/ch000549.htm>. I think this works for other versions of windows too.