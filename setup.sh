#!/bin/bash

# Linux/macOS wrapper for setup.py
# Finds python3.12 and creates the class project folder with a virtualenv inside.
# Defaults to ~/Desktop/myfiles or a parent folder of script; pass a folder in first argument to override.
# Made for ENG209 VM; may need adjustments on other systems.

main() {
	set -euC

	local -r DEFAULT_COURSE_FOLDER="${HOME}/Desktop/myfiles"
	local -r PYTHON_PATH="${PYTHON_PATH:-/opt/python3.12.2/bin/python3.12}"
	local -r SETUP_URL="https://raw.githubusercontent.com/eng209/assets/refs/heads/main/tools/setup.py"
	local -r SETUP_CMD=$(realpath -q "$0")

	if [[ "${SETUP_CMD:-}" =~ ^.*eng209_[0-9]{4}[/\]setup.sh$ ]]; then
		# Install may fall back to setup's folder unless it is in a git repository
		if [[ ! -d $(dirname "${SETUP_CMD}")/.git ]]; then
			local -r SETUP_FOLDER=$(dirname $(dirname "${SETUP_CMD}"))
		fi
	fi

	case "${1-}" in
		-h|--help) cat <<- EOF
			Usage: $0 [/path/to/folder]

			If not specified the folder default to ${DEFAULT_COURSE_FOLDER}, or a parent of setup scripts.
			The folder must exist and be writable.
		EOF
		return ;;
	esac

	local COURSE_FOLDER="${1:-}"

	if [[ -n "${COURSE_FOLDER-}" ]]; then
		if [[ ! -d "${COURSE_FOLDER}" ]]; then
			echo "${COURSE_FOLDER} does not exist or is not a folder. Try: ./setup.sh /path/to/folder"
			return
		fi
	elif [[ -d "${DEFAULT_COURSE_FOLDER}" ]]; then
		COURSE_FOLDER="${DEFAULT_COURSE_FOLDER}"
	elif [[ -n "${SETUP_FOLDER:-}" ]]; then
		COURSE_FOLDER=${SETUP_FOLDER}
	else
		echo "Cannot identify a target folder. Try: ./setup.sh /path/to/folder"
		return
	fi

	COURSE_FOLDER=$(realpath "${COURSE_FOLDER}")
	touch "${COURSE_FOLDER}" || return

	for python_exe in ${PYTHON_PATH} $(type -a -P -- python3.12 python3); do
		if [[ $("${python_exe}" --version 2>&1) =~ ^Python\ 3\.12 ]]; then
			local -r PYTHON_EXE="${python_exe}"
			break
		fi
	done

	if [[ ! -x "${PYTHON_EXE-}" ]]; then
		echo "Python 3.12 not found. Try: PYTHON_PATH=/path/to/python.exe ./setup.sh"
		return
	fi

	"${PYTHON_EXE}" -- <<-EOF
		import urllib.request
		import runpy
		import sys

		url = '${SETUP_URL}'
		with urllib.request.urlopen(url) as response:
		    code = response.read()
		    sys.argv = ['setup.py', '--base', '${COURSE_FOLDER}']
		    exec(compile(code, url, 'exec'))
EOF

}

main "$@"
