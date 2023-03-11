#!/bin/bash

# Dedent text alike python's textwrap.dedent function
dedent() { (_text=${1:-""}; _PYTHON=${2:-python3}; if [[ ! -z "${_text}" ]]; then echo "Text: ${_text}"; ${_PYTHON} -c "from textwrap import dedent; print(dedent('${_text}'.replace('\t', ' '*4)))"; else echo "Missing text argument!"; exit 2; fi; unset _text;) }

diagnose() {
# source: https://www.baeldung.com/linux/heredoc-herestring
cat <<-EOF
args: ${args}
================================
    - alpha: ${_alpha}
    - beta: ${_beta}
    - version: ${_version}
    - verbose: ${_verbose}
--------------------------------
EOF
}

trygetopt() { 
    # getopt "h:" --> this expects parameters
    # getopt "h" --> this DOENOT expect parameters
    _alpha=1;
    _beta=2;
    _verbose=false;
    _version="0.0.1";
    # Program Name
    _PROGNAME="trygetopts";
    # Access Arguments
    args=$(getopt --name=${_PROGNAME} -o "ha:b:v::V" -l "help,alpha:,beta:,version::,verbose" -- "$@"); 
    errcode=$?;
    # Handle Error
    if [ $errcode -ne 0 ]; then echo "Usage: ..."; exit 2; fi;

    
    # boolean evaluation
    # source: https://tinyurl.com/bash-boolean-if-statement
    if [ "$_verbose" == "true" ]; then
        echo -e "\n ${args}\n";
    fi
    eval set -- "${args}";

    # while true; do
    while :; do
        # Note:
        # sources:
        # - https://www.shellscript.sh/examples/getopt/
        # - https://stackoverflow.com/a/52674277/8474894
        # - https://stackoverflow.com/a/16483297/8474894
        # - https://www.baeldung.com/linux/use-command-line-arguments-in-bash-script
        # "shift 2;" is the same as "shift; shift;"
        case "$1" in
        -h|--help)
            echo "Help: Usage...";
            shift 1; break ;;
        -V|--verbose)
            _verbose=true;
            shift 1 ;;
        -v|--version)
            shift 1;
            _version="${1:-${_version}}";
            shift 1 ;;
        -a|--alpha)
            shift 1;
            _alpha="${1:-${_alpha}}";
            shift 1 ;;
        -b|--beta)
            shift 1;
            _beta="${1:-${_beta}}";
            shift 1 ;;
        --)
            shift 1; break ;;
        esac
    done
    if [ "$_verbose" == "true" ]; then
        echo -e "\n ${args}
        >> a: ${_alpha}
        >> b: ${_beta} 
        >> verbose: ${_verbose} 
        >> version: ${_version}\n";
    fi

    diagnose;

    # unset variables
    unset \
        _PROGNAME \
        _alpha \
        _beta \
        _version \
        _verbose \
        ;
}
