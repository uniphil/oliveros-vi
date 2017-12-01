with import <nixpkgs> {};

stdenv.mkDerivation {
    name = "glsl";
    buildInputs = [
        glslviewer
        python36Full
        python36Packages.virtualenv
        # python36Packages.pyserial
    ];
    shellHook = ''
        SOURCE_DATE_EPOCH=$(date +%s)  # so that we can use python wheels
        virtualenv -p $(type -p python3) venv > /dev/null
        export PATH=$PWD/venv/bin:$PATH > /dev/null
        alias dev='glslviewer shader.frag -l -x 0 -y 0 -w 1280 -h 720'
    '';
}
