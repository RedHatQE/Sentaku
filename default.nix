with import <nixpkgs> {};
with pkgs;
with python35Packages;
stdenv.mkDerivation rec {
  name = "sentaku-test";
  src = null;
  buildInputs = [
    bpython
    sqlite
    setuptools_scm
    pip
    wheel
    pytest
    flake8
    pygments
    sphinx
    requests2
    selenium
    virtualenv
    watchdog
    six
    attrs
  ];

  shellHook=''
  export PS1="(${name}) \w \\$ \[$(tput sgr0)\]"
  export PYTHONPATH="$PYTHONPATH:./src"
  

  build_docs() {
    sphinx-build -b html -d build/sphinx-doctrees docs build/htmldocs
  }

  autobuild_docs() {
    watchmedo shell-command docs src -R \
      -c 'sphinx-build -b html -d build/sphinx-doctrees docs build/htmldocs'
  }

  clean() {
    find -name \*.pyc -delete
    find -name __pycache__ -delete
    rm -rf build/sphinx-doctrees build/htmldocs
  }

  build_fresh_docs() {
    clean
    build_docs
  }

  test_clean() {
    clean
    py.test
  }

  '';
}
