# Installing Beancount<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca) - Updated: November 2024

[<u>http://furius.ca/beancount/doc/install</u>](http://furius.ca/beancount/doc/install)

*Instructions for downloading and installing Beancount on your computer.*

## Releases<a id="releases"></a>

Beancount is a mature project: the first version was written in 2008. The current version of Beancount — branch "v3" — is stable and under continued maintenance and development. There is a [<u>mailing-list</u>](https://groups.google.com/forum/#!forum/beancount) and a [<u>PyPI</u>](https://pypi.python.org/pypi/beancount) page. The "master" branch is the development branch.

(Note: If you used the "v2" branch in the past, many of the tools have been removed from branch "v3" and moved to their own dedicated github projects under [<u>http://github.com/beancount</u>](http://github.com/beancount). Some of the tools, e.g. bean-report, bean-web, have been deprecated.)

## Where to Get It<a id="where-to-get-it"></a>

This is the official location for the source code:

> [<u>https://github.com/beancount/beancount</u>](https://github.com/beancount/beancount)

Download it like this, by using Git to make a clone on your machine:

    git clone https://github.com/beancount/beancount

## How to Install<a id="how-to-install"></a>

### Installing Python<a id="installing-python"></a>

Beancount uses Python 3.8 or above, which is a pretty recent version of Python (as of this writing), and a few common library dependencies. I try to minimize dependencies, but you do have to install a few. This is very easy.

First, you should have a working Python install. Install the latest stable version &gt;=3.8 using the download from [<u>python.org</u>](http://python.org). Make sure you have the development headers and libraries installed as well (e.g., the “Python.h” header file). For example, on a Debian/Ubuntu system you would install the **`python3-dev`** package.

Beancount supports setuptools since Feb 2016, and you will need to install dependencies. You will want to have the “pip3” tool installed. It’s installed by default along with Python3 by now—test this out by invoking “python3 -m pip --help” command.

### Installing Beancount<a id="installing-beancount"></a>

#### Installing Beancount using pipx<a id="installing-beancount-using-pipx"></a>

If you haven’t already, first [<u>install pipx</u>](https://github.com/pypa/pipx).

Next, use pipx to install Beancount. This should automatically download and install all the dependencies in a virtual environment.

    pipx install beancount

Confirm Beancount has been installed.

    pipx list

#### Installing Beancount using pip<a id="installing-beancount-using-pip"></a>

Installing Beancount using pip is no longer recommended, however you may install Beancount using

    sudo -H python3 -m pip install beancount

This should automatically download and install all the dependencies.

Note, however, that this will install the latest version that was pushed to the [<u>PyPI repository</u>](https://pypi.python.org/pypi/beancount/) and not the very latest version available from source. Releases to PyPI are made sporadically but frequently enough not to be too far behind.

**Warning: Proceed with caution this may break system libraries.**

#### Installing Beancount using pip from the Repository<a id="installing-beancount-using-pip-from-the-repository"></a>

You can also use pip to install Beancount from its source code repository directly:

    sudo -H python3 -m pip install git+https://github.com/beancount/beancount#egg=beancount

#### Installing Beancount from Source<a id="installing-beancount-from-source"></a>

Installing from source offers the advantage of providing you with the very latest version of the stable branch (“master”). The master branch should be as stable as the released version most of the time.

Get the source code from the official repository:

    git clone https://github.com/beancount/beancount

You might need to install some non-Python library dependencies, such as bison and flex and perhaps a few more (you'll find out when you try to build). It should be obvious what’s missing. If on Ubuntu, use apt get to install those.

If installing on Windows, see the Windows section below.

##### Build and Install Beancount from source using pip3<a id="build-and-install-beancount-from-source-using-pip3"></a>

You can then install all the dependencies and Beancount itself using pip:

    sudo -H python3 -m pip install .

##### Installing for Development<a id="installing-for-development"></a>

If you want to execute the source in-place for making changes to it, you can use the setuptools “develop” command to point to it:

    sudo python3 setup.py develop 

Warning: This modifies a .pth file in your Python installation to point to the path to your clone. You may or may not want this. I don't do this myself; the way I work is by compiling locally and setting up my shell's environment to find its libraries. You can do it like this:

    make build

You will need to have "meson" and "ninja" installed to do this. Both the PATH and PYTHONPATH environment variables need to be updated to pick up the imports and binaries locally as follows:

    export PATH=$PATH:/path/to/beancount/bin
    export PYTHONPATH=$PYTHONPATH:/path/to/beancount

###### Dependencies for Development<a id="dependencies-for-development"></a>

Beancount needs a few more tools for development. If you’re reading this, you’re a developer, so I’ll assume you can figure out how to install packages, skip the detail, and just list what you might need:

-   pytest: for unit tests

-   meson, meson-python, ninja: for building (on branch master)

-   ruff: for linting

-   [**<u>GNU flex</u>**](https://www.gnu.org/software/flex/): This lexer generator is needed if you intend to modify the lexer. It generated C code that chops up the input files into tokens for the parser to consume.

-   [**<u>GNU bison</u>**](http://www.gnu.org/software/bison/): This old-school parser generator is needed if you intend to modify the grammar. It generates C code that parses the tokens generated by flex. (I like using old tools like this because they are pretty low on dependencies, just C code. It should work everywhere.)\`

-   python-dateutil : to run the beancount.scripts.example example generator script.

#### Installing from Distribution Packages<a id="installing-from-distribution-packages"></a>

Various distributions may package Beancount. Here are links to those known to exist:

-   Arch: [<u>https://aur.archlinux.org/packages/beancount/</u>](https://aur.archlinux.org/packages/beancount/)

#### Windows Installation<a id="windows-installation"></a>

##### beancount v3<a id="beancount-v3"></a>

If you intend to use beancount v3, then there is probably no reason to install it without beanquery, as custom reports and bean-web are discontinued in v3.

In this case the simplest way to install beancount is to install beanquery, which will install beancount as a dependency.

To do this simply run the following command

    pip install beanquery

Or

    python -m pip install beanquery 

To test installation create a simple beancount ledger

E.g.,:

    ====================================

    2024-01-01 open Assets:Bank

    2024-01-01 open Equity:Opening-Balances

    2024-01-01 * "Opening Balance"

      Assets:Bank  1000.00 USD

      Equity:Opening-Balances

    ======================================

Save it to some file (e.g. tst.bean)

Then run

     bean-query tst.bean

Or

    python -m beanquery tst.bean

Confirm, that you get prompt like that

    Input file: "Beancount"

    Ready with 3 directives (2 postings in 1 transactions).

    beanquery>

Congratulations! Installation is successful

If for whatever reason you still want to install beancount standalone, you can do it like that:

    pip install beancount

Or

    python -m pip install beancount

##### beancount v2<a id="beancount-v2"></a>

To install the last v2 of beancount do the following:

**`pip install "beancount<3"`**

or

                    python -m pip install "beancount<3"

##### Native for development<a id="native-for-development"></a>

###### Install compiler<a id="install-compiler"></a>

Installing this package by pip requires compiling some C++ code during the installation procedure which is only possible if an appropriate compiler is available on the computer, otherwise you will receive an error message about missing *vsvarsall.bat* or *cl.exe*.

To be able to compile C++ code for Python you will need to install the same major version of the C++ compiler as your Python installation was compiled with. By running *python* in a console and looking for a text similar to *\[MSC v.1900 64 bit (AMD64)\]* you can determine which compiler was used for your particular Python distribution. In this example it is *v.1900*.

Using this number find the required Visual C++ version [<u>here</u>](https://stackoverflow.com/questions/2676763/what-version-of-visual-studio-is-python-on-my-computer-compiled-with). Since different versions seem to be compatible as long as the first two digits are the same you can in theory use any Visual C++ compiler between 1900 and 1999.

According to my experience both Python 3.8 and 3.6 was compiled with MSC v.1900 so you can do either of the following to satisfy this requirement:

-   Install the standalone [<u>Build Tools for Visual Studio 2017</u>](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=15) or

-   Install the standalone [<u>Visual C++ Build Tools 2015</u>](http://go.microsoft.com/fwlink/?LinkId=691126) or

-   Modify an existing Visual Studio 2017 installation

    -   Start the Visual Studio 2017 installer from *Add or remove programs*

    -   Select *Individual components*

    -   Check *VC++ 2017 version 15.9 v14.16 latest v141 tools* or newer under *Compilers, build tools, and runtimes*

    -   Install

-   Visual Studio 2019, 2022

    -   add C++ build tools: C++ core features, MSVC v142 build tools

If cl.exe is not in your path after installation, run Developer Command Prompt for Visual Studio and run the commands there.

######  Install winflexbison<a id="install-winflexbison"></a>

Download zip file with the latest version of the winflexbison

[<u>https://github.com/lexxmark/winflexbison/releases</u>](https://github.com/lexxmark/winflexbison/releases)

Extract archive to some directory (e.g. `C:\Program Files (x86)\winflexbison`)

[<u>Update the Path environmental</u>](https://www.youtube.com/watch?v=9umV9jD6n80) variable to include that directory ( e.g. ‘`C:\Program Files (x86)\winflexbison`’)

Reboot the PC

Open the command prompt

Issue the command

    win_bison --version

Confirm that you get a response with the win\_bizon version

######  Install build utilities<a id="install-build-utilities"></a>

    python -m pip install meson-python meson ninja

###### Get and Install beancount<a id="get-and-install-beancount"></a>

Get the latest version of the **beancount** from github and build it

    git clone https://github.com/beancount/beancount.git

    cd beancount

Install beancount from the source in editable mode

    python -m pip install --no-build-isolation -e .

###### Test beancount<a id="test-beancount"></a>

Install pytest

    python -m pip install pytest

Go to the inside directory and run unit tests

    cd beancount

    python -m pytest

Confirm that the majority of tests have passed (approx 70 tests out of approx 1100 total fail on Windows as of November 2024, which is mostly related to the fact, that unit tests are written assuming POSIX environment (see issue [<u>222</u>](https://github.com/beancount/beancount/issues/222), [<u>550</u>](https://github.com/beancount/beancount/issues/550) ))

#### With Cygwin<a id="with-cygwin"></a>

Windows installation is, of course, a bit different. It’s a breeze if you use Cygwin. You just have to prep your machine first. Here’s how.

-   Install the latest [<u>Cygwin</u>](https://www.cygwin.com/). This may take a while (it downloads a lot of stuff), but it is well worth it in any case. But before you kick off the install, make sure the following packages are all manually enabled in the interface provided by setup.exe (they’re not selected by default):

    -   python3

    -   python3-devel

    -   python3-setuptools

    -   git

    -   make

    -   gcc-core

    -   flex

    -   bison

-   Start a new Cygwin bash shell (there should be a new icon on your desktop) and install the pip3 installer tool by running this command:  
    **easy\_install-3.4 pip  
    **Make sure you invoke the version of easy\_install which matches your Python version, e.g. easy\_install-3.8 if you have Python 3.8 installed, or more.

At this point, you should be able to follow the instructions from the previous sections as is, starting from “Install Beancount using pip”.

#### With WSL<a id="with-wsl"></a>

The newly released Windows 10 Anniversary Update brings WSL 'Windows Subsystem for Linux' with [<u>bash on Ubuntu on Windows</u>](https://blogs.msdn.microsoft.com/wsl/2016/07/08/bash-on-ubuntu-on-windows-10-anniversary-update/) (installation instructions and more at [<u>https://msdn.microsoft.com/commandline/wsl/about</u>](https://msdn.microsoft.com/commandline/wsl/about)).

This makes beancount installation easy, from bash:

    sudo apt-get install python3-pip
    sudo pip3 install m3-cdecimal
    sudo pip3 install beancount --pre

This is not totally “Windows compatible”, as it is running in a pico-process, but provides a convenient way to get the Linux command-line experience on Windows. *(Contrib: willwray)*

### Checking your Install<a id="checking-your-install"></a>

You should be able to run the binaries from [<u>this document</u>](running_beancount_and_generating_reports.md). For example, running bean-check should produce something like this:

    $ bean-check

    usage: bean-check [-h] [-v] filename
    bean-check: error: the following arguments are required: filename

If this works, you can now go to the [<u>tutorial</u>](tutorial_example.md) and begin learning how Beancount works.

### Reporting Problems<a id="reporting-problems"></a>

If you need to report a problem, either send email on the mailing-list or [<u>file a ticket</u>](https://github.com/beancount/beancount/issues) on Github. Running the following command lists the presence and versions of dependencies installed on your computer and it might be useful to include the output of this command in your bug report:

    python3 -m beancount.scripts.deps

## Editor Support<a id="editor-support"></a>

There is support for some editors available:

-   Emacs support is provided [<u>in a separate repo</u>](https://github.com/beancount/beancount-mode). See the [<u>Getting Started</u>](getting_started_with_beancount.md) text for installation instruction.

-   Support for [<u>editing with Sublime</u>](https://sublime.wbond.net/packages/Beancount) has been contributed by [<u>Martin Andreas Andersen</u>](https://groups.google.com/d/msg/beancount/WvlhcCjNl-Q/s4wOBQnRVxYJ). See [<u>his github repo</u>](https://github.com/draug3n/sublime-beancount).

-   Support for editing with Vim has been contributed by [<u>Nathan Grigg</u>](https://github.com/nathangrigg). See [<u>his GitHub repo</u>](https://github.com/nathangrigg/vim-beancount).

-   Visual Studio Code currently has two extensions available. Both have been tested on Linux.

    -   [<u>Beancount</u>](https://marketplace.visualstudio.com/items?itemName=Lencerf.beancount), with syntax checking (bean-check) and support for accounts, currencies, etc. It not only allows selecting existing open accounts but also displays their balance and other metadata. Quite helpful!

    -   [<u>Beancount Formatter</u>](https://marketplace.visualstudio.com/items?itemName=dongfg.vscode-beancount-formatter), which can format the whole document, aligning the numbers, etc. using bean-format.

## If You Have Problems<a id="if-you-have-problems"></a>

If you run into any installation problems, [<u>file a ticket</u>](https://github.com/beancount/beancount/issues/) or email the [<u>mailing-list</u>](https://groups.google.com/forum/#!forum/beancount).

## Post-Installation Usage<a id="post-installation-usage"></a>

Normally the [<u>scripts located under beancount/bin</u>](https://github.com/beancount/beancount/tree/v2/bin) should be automatically installed somewhere in your executable path. For example, you should be able to just run “bean-check” on the command-line.
