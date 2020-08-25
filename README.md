# 🩺 MCL Portal

This is the software that runs the website for the Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions, better known as the MCL Consortium, nominally hosted at https://mcl.nci.nih.gov/.

(Insert a badge of build status here.)

## 🚗 Getting Started

For installation instructions, see [`INSTALL.rst`](INSTALL.rst).

Developer notes are in [`notes.rst`](notes.rst).

## 📀 Software Environment

This software is primarily written in [Python](hhttps://www.python.org/) using the [Plone](https://plone.org/) content management system.  The source code is mainly under the `src` directory. It's typically built into a [Docker](https://www.docker.com/) image using the [`Dockerfile`](Dockerfile) provided.


### 👥 Contributing

You can start by looking at the [open issues](https://github.com/MCLConsortium/mcl-site/issues), forking the project, and submitting a pull request. You can also [contact us by email](mailto:ic-portal@jpl.nasa.gov) with suggestions.


### 🔢 Versioning

We use the [SemVer](https://semver.org/) philosophy for versioning this software. For versions available, see the [releases made](https://github.com/MCLConsortium/mcl-site/releases) on this project. We're starting off with version 5 because reasons.


## 👩‍🎨 Creators

The principal developers are:

- [Sean Kelly](https://github.com/nutjob4life)
- [David Liu](https://github.com/yuliujpl)

The QA team consists of:

- [Heather Kincaid](https://github.com/hoodriverheather)
- [Maureen Colbert](https://github.com/colbertm)

To contact the team as a whole, [email the Informatics Center](mailto:ic-portal@jpl.nasa.gov).


## 📃 License

The project is licensed under the [Apache version 2](LICENSE.txt) license.

Note that this package includes software from [Plone Docker](https://github.com/plone/plone.docker) licensed under the [GNU Public License version 2](GNU-LICENSE.txt). The source code for this software is included in the files [Dockerfile](Dockerfile), [docker-entrypoint.sh](docker-entrypoint.sh), [docker-initialize.py](docker-initialize.py), and [buildout.cfg](buildout.cfg).
