pkg_name := dynmen_scripts

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
project_dir := $(dir $(mkfile_path))
src_dir := $(join $(project_dir), src/$(pkg_name)/)
setup_py := $(join $(project_dir), setup.py)
# The following regex based on: http://unix.stackexchange.com/a/146752
pkg_version := $(shell grep -oP 'version="\K[^"]+' $(setup_py))
dist_dir := $(join $(project_dir), dist/)
wheel := $(join $(dist_dir), $(pkg_name)-$(pkg_version)-py2.py3-none-any.whl)
python_src = $(wildcard $(src_dir)*.py)

.PHONY: install-user
install-user: $(wheel)
	@echo "----------------------------------------"
	@echo "Installing $(pkg_name) as $$USER"
	@echo "----------------------------------------"
	python -m pip install --user --upgrade $(wheel)

$(wheel): $(python_src)
	@echo "----------------------------------------"
	@echo "Building wheel $(wheel)"
	@echo "----------------------------------------"
	@python $(setup_py) bdist_wheel

.PHONY: uninstall
uninstall:
	@echo "----------------------------------------"
	@echo "Uninstalling $(pkg_name)"
	@echo "----------------------------------------"
	@echo $(pkg_name)
	-yes | python -m pip uninstall $(pkg_name)

.PHONY: clean
clean:
	@echo "----------------------------------------"
	@echo "Cleaning"
	@echo "----------------------------------------"
	rm -rf $(dist_dir)
	rm -rf $(project_dir)build
	rm -rf $(project_dir)src/*.egg-info
	rm -rf $(project_dir).venv/
	git clean -dxf

.PHONY: venv
venv: .venv;

.venv:
	util/new_venv.sh

