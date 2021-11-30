# Py-Builder
A simple command line tool to build CPython from source.

Pairs nicely with [brettcannon/python-launcher](https://github.com/brettcannon/python-launcher).

# TODO:
  - [ ] Documentation
  - [ ] Verbose flag
  - [ ] Dryrun flag
    - Wrap all `subprocess.run` calls in a custom function?
  - [ ] Clone Functionality
    - Cache in `XDG_CACHE_HOME` unless overidden in Configuration.
  - [ ] Configuration file ( Should be in `XDG_CONFIG_HOME` by default)
  - [ ] `pipx` installable.
  - [x] `pre-commit` stuff.
  - [ ] Better Tracebacks

# Bonus TODOs:
  - [ ] Add Rich/textual support???
  - [ ] Add regex tag search functionality.
  - [ ] Pass addtional options to `./configure`, `make`, and `make altinstall`
    - See https://docs.python.org/3/using/configure.html#configure-options
