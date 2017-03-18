mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
project_dir := $(dir $(mkfile_path))
pkg_name := dynmen_scripts
setup_py := $(join $(project_dir), setup.py)

WHEELS = $(join $(project_dir), $(wildcard dist/dynmen_scripts*.whl))

.PHONY: install-user
install-user: build-wheel $(WHEELS) 
	@echo "----------------------------------------"
	@echo "Installing $(pkg_name) as $$USER"
	@echo -e "\twheel file: " $(word 2, $^)
	@echo "----------------------------------------"
	pip install --user --upgrade $(word 2, $^)

.PHONY: build-wheel
build-wheel: clean
	@echo "----------------------------------------"
	@echo "Building wheel for $(pkg_name)"
	@echo "----------------------------------------"
	python $(setup_py) bdist_wheel

.PHONY: uninstall
uninstall:
	@echo "----------------------------------------"
	@echo "Uninstalling $(pkg_name)"
	@echo "----------------------------------------"
	@echo $(pkg_name)
	-yes | pip uninstall $(pkg_name)


.PHONY: clean
clean:
	@echo "----------------------------------------"
	@echo "Cleaning"
	@echo "----------------------------------------"
	rm -rf $(project_dir)dist
	rm -rf $(project_dir)build
	rm -rf $(project_dir)dynmen_scripts.egg-info
