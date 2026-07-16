SKILL_NAME := temporal-patterns
SRC        := SKILL.md
DIST       := dist
PKG        := $(DIST)/$(SKILL_NAME).skill

.PHONY: build verify lint check-links clean

## Package the .skill from SKILL.md (output in dist/)
build: $(PKG)

$(PKG): $(SRC)
	@mkdir -p $(DIST)/$(SKILL_NAME)
	@cp $(SRC) $(DIST)/$(SKILL_NAME)/SKILL.md
	@rm -f $(PKG)
	@cd $(DIST) && zip -X -q -r $(SKILL_NAME).skill $(SKILL_NAME)/SKILL.md
	@rm -rf $(DIST)/$(SKILL_NAME)
	@echo "Built $(PKG)"

## Build, then confirm the packaged SKILL.md matches the source byte-for-byte
verify: build
	@unzip -p $(PKG) $(SKILL_NAME)/SKILL.md | diff - $(SRC) \
		&& echo "OK: package matches $(SRC)"
	@unzip -l $(PKG)

## Validate SKILL.md frontmatter
lint:
	@python3 scripts/validate_skill.py $(SRC)

## Verify every catalog slug resolves at docs.temporal.io
check-links:
	@python3 scripts/check_links.py $(SRC)

clean:
	@rm -rf $(DIST)
