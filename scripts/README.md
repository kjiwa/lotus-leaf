# UW Solar Power Monitor

## Development Scripts

### Table of Contents

1. clean.sh
2. setup.sh
3. build.sh
4. run.sh
5. start.sh

### clean.sh

Removes temporary files, runtime environments, and build artifacts from the source directory.

Run ```clean.sh --help``` to view additional configuration options.

### setup.sh

Installs build and runtime dependencies for the frontend and backend components of the web application. Three main steps are performed:

1. Install frontend dependencies specified in ```src/client/package.json```.
2. Install backend dependencies specified in ```src/server/requirements.txt```.
3. Install DB migration dependencies specified in ```db/requirements.txt```.

Run ```setup.sh --help``` to view additional configuration options.

### build.sh

Validates source code with static analysis tools (ESLint, Pylint), and produces a single JavaScript archive containing code, style information, images, and fonts.

When ```--nodebug``` is set (the default), build optimizations are enabled. JavaScript sources are optimized, obfuscated, and minified. This version offers the best performance and should be use in production, but will be difficult to debug, since the source code will be difficult to read.

When ```--debug``` is set, build optimizations are disabled. This option should be used when developing source code so that it can be more easily debugged.

Run ```build.sh --help``` to view additional configuration options.

### run.sh

This script runs the web server application and is a very thin wrapper over ```src/server/main.py```.

### start.sh

Sets up build and runtime environments, builds source code, and runs the web application. By default, this script is configured to perform an optimized build and connect to an in-memory SQLite database populated with sample data.

New developers should run this script with its default options the first time so that the development environment can be setup and to ensure that the system is configured correctly to run the application. The following invocation builds and runs an optimized web application with sample data.

```bash
$ scripts/start.sh
```
While developing, running this script with its default configuration can become time-consuming and cumbersome. This is because the setup stage is always executed. Skipping this step can cause a significant reduction in the time required to build and run the application. Use the ```--noclean``` and ```--nosetup``` options to prevent the clean and setup stages from executing.

The ```--debug``` flag should also be used when developing so that errors can be more easily debugged. The following invocation builds and runs a debuggable web application with sample data, and skips the setup stage.

```bash
$ scripts/start.sh --noclean --nosetup --debug
```

Run ```start.sh --help``` to view additional configuration options.
