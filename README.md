# System Performance Analysis Dashboard
A simple dashboard to analyze the performance of several Linux-based systems using the sysstat SAR logs.

To use:

1. Download the files in the repository to a directory.
2. In the configs.py file, set the directory path to point to your plain-text log files.

**NOTE** - I developed this on a Mac and run it on a Linux machine.  Windows users shouldn't have a problem, but I don't know.  Buyer beware.

3. Review the requirements.txt and make sure all libraries are installed.  These are relatively minimal and easily obtained.
4. Run the main.py file using 'python /path/to/directory/main.py'
5. Navigate your browser to the ip address of the machine (perhaps 127.0.0.1 or other if installed remotely) on port 8090.
6. Enjoy!

Use the code how you please.  If you use it as a basis for your own project, be cool and give me a shout out.

Any questions, comments, or concerns - create an issue or just shoot me an email brad@darksbian.com

Brad

**Addendum** - Some users have pointed out to me that when running this code on OSX, you can sometimes get an error like "[SSL: CERTIFICATE_VERIFY_FAILED]".

This is a known issue with python >=3.6 and OSX.  The fix is simple and outlined here:  https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error

**NOTE2** I have left the running settings in debug mode with hot reload for changes.  Change this if you like.  It's recommended because the logs can get a bit noisy.  Additionally, this method of running the system is not designed for production use.  If you want to do that, I recommend checking the official docs for deploying a Dash application in a production environment.