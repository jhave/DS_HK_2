# GA Data Science @ Hong Kong
## How to use this course

### Getting Ready

Getting ready for the course consists of preparing both yourself and your computer for Data Science. The [Prologue to Data Science](prologue.datascience.hk) is food for the brain and acts as the preresuite for this course.

OSX and Linux provide a better course experience, but it's possible to setup your Windows machine in very similar ways. The [Setup Instructions](http://nbviewer.ipython.org/github/ga-students/DS_HK_2/blob/gh-pages/notebooks/Guides%20-%20Setup%20Instructions.ipynb) cover all three platforms. Be sure to follow the instructions common to all three platforms first before the optional OS-specific installs.

[Git & Github](http://nbviewer.ipython.org/github/ga-students/DS_HK_2/blob/gh-pages/notebooks/Guides%20-%20Git%20%26%20GitHub.ipynb) have a dedicated instruction. Only follow the instructions under `Setup` and `Setup Course Materials`, as `Git Workflow` and `Useful Git Tips and Tools` are optional and advanced guidance.

### Notebooks

Lesson materials are distributed in iPython Notebooks. An index of the latest notebooks is available on the course page as [ga-students.github.io/DS_HK_2/](http://ga-students.github.io/DS_HK_2/).

To run the notebooks locally, run 

```bash
ipython notebook
```

in the terminal while inside of the `DS_HK_2/notebooks/` directory, as well as running 

```bash
python -m SimpleHTTPServer
``` 
in the same location in the terminal to serve up the pictures. You can combine them into one command by pasting the following into a file called `.bashrc` in your home directory.

```bash
ipynb(){
	nohup python -m SimpleHTTPServer >&/dev/null; 
	ipython notebook; 
	sudo kill $(sudo lsof -t -i:8000);
}
```
and running the 'ipynb' command in the terminal while inside of the `DS_HK_2/notebooks/` directory

### Questions

For questions, please turn to any of the following communication channels for support. 

* [GitHub Issues](https://github.com/ga-students/DS_HK_2/issues)
* Mailing List
* Email

### Contact

Data Science in Hong Kong is run by @tijptjik
