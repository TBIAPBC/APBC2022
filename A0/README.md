# A0 - Warm up assignment: Hello World

Dear APBC people,

in this assignment, you should write---for warm up---a program that
accepts a single file name on the command line and prints (to standard
output)

  * "Hello World!", adding a line break
  * and the content of the file
  * NO additional line break
  * use [HelloWorld-test1.in](https://github.com/TBIAPBC/APBC2022/blob/master/A0/HelloWorld-test1.in) as input
  * output should be like [HelloWorld-test1.out](https://github.com/TBIAPBC/APBC2022/blob/master/A0/HelloWorld-test1.out)

Then, submit your program via Github (of course, this step is the
actual purpose of the HelloWorld assignment, which should be simple to
implement for all of you, otherwise.) For these tasks follow the
instructions below.

For the interesting part of this assignment, i.e. the submission, we
need a few preparations:

* Register as user in Github (github.com), if you didn't do so already.

* Mail us (mtw at tbi.univie.ac.at) your clear name and github
  account name, such that we can register you as member of our team on
  Github.

* Find this text at https://github.com/TBIAPBC/APBC2022/tree/master/A0

* Read some git docu (git-scm.com), e.g. start with this [Introduction](https://www.tbi.univie.ac.at/~jlandersen/_static/git.pdf).
  After getting some idea, it's best to learn the rest while using git. Probably handy are Git Cheat Sheets,
  e.g. [this](https://education.github.com/git-cheat-sheet-education.pdf).
  Moreover, git is always there to help (use '--help') on the linux command line. For example
```
  git help
  git help tutorial
  git clone --help
```

Now let's get to the thing:

* Open a Linux terminal

* Clone our APBC-Github repository from https://github.com/TBIAPBC/APBC2022. For this purpose, run in the terminal
```
  git clone git@github.com:TBIAPBC/APBC2022.git
```
  to clone using [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh).

  If you clone via SSH, you might consider [SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), which allow you to connect to GitHub without supplying your username and password each time.

  The clone command fills the directory APBC with the contents from the central repository (together with all the version and meta-information in subdirectory .git).
* Unless already done, configure your user name and email address:
```
  cd APBC2022
  git config user.name "your name"
  git config user.email "your mail address"
```

* Create a new branch named after your github account name; change to this branch
```
  git branch $githubname
  git checkout $githubname
```

* __NOTE: You should NEVER write anything into the master branch of our repository!__ Always use your *own branch*. To this end, create a new branch for every assignment, e.g. $githubname-A0 / $githubname-A1 etc.

* Write the "Hello world" program according to the above specification. The programming language is your choice (as for all coming assignments).

* Copy the solution to subdir A0; the file must be named following this scheme: $githubname-HelloWorld.$suffix,
  where the suffix depends on your programming language; e.g. suffix='.py'

* Add your changes and commit them. For this, run these commands in the root dir of APBC2022:
```
  git add A0/$githubname-HelloWorld.$suffix
  git commit
```

* Push your branch to the same branch in the repository on Github
```
  git push --set-upstream origin $githubname:$githubname
```
  The --set-upstream causes git to remember the upstream branch; it can be ommitted in follow-up pushs from your branch.

* Go to https://github.com/TBIAPBC/APBC2022; make a pull request (PR) from your branch into the master branch.

* If you get stuck let us know via the comment functionality in the PR on github. Include all necessary information, what went wrong and
  how we can help e.g.:

```
  ping @mtw
  My program is not executed with error XYZ
```

* After successful testing (optional) and if you like your program, write another comment (alternatively, file a review request) to let us know we
  should review the submission. If everything is ok, we will merge your submission into the branch 'master' (or tell you what to
  improve).

```
  @mtw , please review
```

Happy hacking!
