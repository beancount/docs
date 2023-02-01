# Installing Beancount (v3)<a id="title"></a>

[<u>Martin Blais</u>](mailto:blais@furius.ca) - July 2020

[<u>http://furius.ca/beancount/doc/v3-install</u>](http://furius.ca/beancount/doc/v3-install)

*Instructions for downloading and running Beancount v3 (in development) on your computer. For v2, see this document instead: [Beancount - Install (v2)](installing_beancount.md)*

<table><tbody><tr class="odd"><td><em><strong>This document is about Beancount v3, an experimental in-development version (as of July 2020); Instructions for building the stable version (Beancount v2) can be found in <a href="installing_beancount.md"><u>this other document</u></a>.</strong></em></td></tr></tbody></table>

## Building with Bazel<a id="building-with-bazel"></a>

*Warning: This is an experimental development branch. Do not expect everything to be polished perfectly.*

### Bazel Dependencies<a id="bazel-dependencies"></a>

Beancount v3 uses the Bazel build system, which for the most part insulates you from local installs and dependencies from your computer.

The dependencies to install are:

-   **Bazel itself.** Follow instructions on [<u>https://bazel.build/</u>](https://bazel.build/)

-   **A C++ compiler.** Either g++ or clang works. I'm using clang-11.

-   **A Python runtime** (version 3.8 or above). Install from your distribution.

Bazel will download and compile all the libraries it requires itself (even the code generators, e.g., Bison), building them at their precise versions as specified in the build, so you will not have to worry about them.

### Building & Testing<a id="building-testing"></a>

Simply run the following command:

    bazel build //bin:all

There is currently no installation script, you have to run from source. You can run individual programs (e.g. bean-check) with this command:

    bazel run //bin:bean_check -- /path/to/ledger.beancount

Or if you don't care to automatically rebuild modified code, like this:

     ./bazel-bin/bin/bean_check /path/to/ledger.beancount

### Development<a id="development"></a>

You can run all the unit tests like this:

    bazel test //...

Because Bazel has a detailed account of all dependencies, re-running this command after modifying code will result in only the touched targets being re-tested; this makes iterative development with testing a bit more fun.

Another advantage is that since all the libraries the build depends on are downloaded and built, while this can be slow on the first build, it allows us to use very recently released versions of the code we depend on.

Targets are defined in BUILD files local to their directories. All the build rules can be found under //third\_party.

### Ingestion<a id="ingestion"></a>

The ingestion code involves importing code that lives outside the repository. Bazel binaries are self-contained and will fail to import modules that haven't been declared as dependencies, so running the `//bin:bean_extract` target, for example, probably won't work.

This does not work yet (short of building your import configuration as a py\_binary() target that would explicitly link to Beancount). This is doable without writing much Bazel code by defining a suitable WORKSPACE file that fetches the rules from it. I haven't produced an example of this yet (TBD).

As a workaround, you can set your PYTHONPATH to import from the source location and create a symlink to the parser .so file beforehand. You can do it like this:

    make bazel-link

### TBD<a id="tbd"></a>

A few build integration tasks remain to be done:

-   pytype is not supported yet.

-   pylint is not integrated in the build either.
