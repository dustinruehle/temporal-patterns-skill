SKILL_NAME := temporal-patterns
SRC        := SKILL.md
REFS       := $(wildcard references/*.md)
DIST       := dist
PKG        := $(DIST)/$(SKILL_NAME).skill
PYTHON     ?= python3

.PHONY: setup build verify lint check-links clean

## Install the one Python dependency the checks need (PyYAML)
setup:
	@$(PYTHON) -m pip install --quiet pyyaml

## Package the .skill from SKILL.md and references/ (output in dist/)
build: $(PKG)

$(PKG): $(SRC) $(REFS)
	@rm -rf $(DIST)/$(SKILL_NAME) $(PKG)
	@mkdir -p $(DIST)/$(SKILL_NAME)/references
	@cp $(SRC) $(DIST)/$(SKILL_NAME)/SKILL.md
	@cp $(REFS) $(DIST)/$(SKILL_NAME)/references/
	@cd $(DIST) && zip -X -q -r $(SKILL_NAME).skill $(SKILL_NAME)
	@rm -rf $(DIST)/$(SKILL_NAME)
	@echo "Built $(PKG)"

## Build, then confirm every packaged file matches its source byte for byte
verify: build
	@for f in $(SRC) $(REFS); do \
		unzip -p $(PKG) $(SKILL_NAME)/$$f | diff -q - $$f >/dev/null \
			|| { echo "MISMATCH: $$f"; exit 1; }; \
	done && echo "OK: package matches $(SRC) and $(words $(REFS)) reference file(s)"
	@unzip -l $(PKG)

## Validate SKILL.md frontmatter, description length and references
lint:
	@$(PYTHON) scripts/validate_skill.py $(SRC)

## Check the catalog against the live docs, both ways, plus every docs URL
check-links:
	@$(PYTHON) scripts/check_links.py $(SRC)

clean:
	@rm -rf $(DIST)
