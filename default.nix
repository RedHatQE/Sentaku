with import <nixpkgs> {};
with pkgs;
with python35Packages;


let
  dectate = buildPythonPackage rec {
    name = "dectate-${version}";
    version = "0.12";
    buildInputs = [pytest];
    checkPhase = "py.test";
    src = fetchurl {
      url = "mirror://pypi/d/dectate/${name}.tar.gz";
      sha256="14hc65695r89x1ivm1gj3dcvsn2mk6a5ax01sl7s5cp1nyj8bfd3";
    };
  };
  attrs = python35Packages.attrs.overrideDerivation (old: rec {
    name = "attrs-${version}";
    version = "16.3.0";
    src = fetchurl {
      url = "mirror://pypi/a/attrs/${name}.tar.gz";
      sha256="1k1w8xg7mbd9r8624irnwnzlf3g8lqymba2sw6xz6diyf9vk2840";
    };
  });
  env = buildEnv {
    name = "sentaku-deps";
    paths =
    [
      dectate attrs
      python ipython
      gitAndTools.gitFull
      ncurses
      bpython
      setuptools_scm
      pytest
      requests2
      selenium
    ];
  };
in buildPythonPackage rec {
  name = "sentaku-test";
  src = ./.;
  buildInputs = [
    flake8
    sphinx
  ];
  checkPhase = "py.test";

  propagatedBuildInputs = [env];


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
    rm -rf build/
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
