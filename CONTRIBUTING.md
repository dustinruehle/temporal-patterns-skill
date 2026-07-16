# Contributing

Thanks for helping improve the **temporal-patterns** skill. It's a single markdown
file, so most fixes are small and quick.

## The one rule

`SKILL.md` is the **single source of truth**. Everything else — the README, the
`.skill` package, the CHANGELOG — describes or is derived from it. Make your change
in `SKILL.md`, and never hand-edit the packaged `.skill` (it's a build artifact and
isn't committed).

## Kinds of contributions

### Fixing a routing rule
The problem→pattern routing map is the skill's most-used surface. If a symptom
routes to the wrong pattern, fix the row in the routing table. Keep the phrasing
symptom-first ("If the user is trying to…") — users describe problems, not pattern
names.

### Adding, renaming, or removing a pattern
A pattern appears in up to **three** places that must stay consistent:

1. The **routing map** table (symptom → pattern → `slug`).
2. The **full catalog by domain** section (name — `slug` — one-line description).
3. Any **composition** or **choosing-between-close-patterns** notes that reference it.

When you touch a pattern, grep for its slug and its name and update every occurrence.
Rules of the road:

- **Use the exact product name.** Pattern names are Temporal terminology — don't
  rename or pluralize creatively.
- **The `slug` must match the live docs.** Every pattern resolves to
  `https://docs.temporal.io/design-patterns/{slug}.md`. Verify the URL loads before
  merging (`make check-links` does this for the whole catalog).
- **Keep descriptions terse.** The catalog is a pointer, not the page. One line.
- **Don't invent patterns.** Only add patterns that exist in the
  [live index](https://docs.temporal.io/design-patterns.md). If the index has grown,
  reconcile against it.

### Bumping the catalog snapshot
The catalog is a snapshot (34 patterns / 10 domains at 1.0.0). When the live index
changes, re-fetch `https://docs.temporal.io/design-patterns.md`, reconcile, and note
the new counts in `SKILL.md`'s snapshot line.

## Local workflow

```sh
make lint          # validate SKILL.md frontmatter
make build         # package dist/temporal-patterns.skill from SKILL.md
make check-links   # verify every catalog slug resolves at docs.temporal.io
```

`make build` reproduces exactly what CI and the release workflow produce. CI runs
`lint` + `build` (and diffs the packaged `SKILL.md` against the source) on every PR;
`check-links` runs too but is non-blocking, since it depends on the live docs site.

## Pull request checklist

- [ ] The change is in `SKILL.md` (not the `.skill` artifact).
- [ ] Routing map, catalog, and composition notes are consistent for any touched pattern.
- [ ] New/changed slugs resolve on `docs.temporal.io` (`make check-links`).
- [ ] `make lint` passes.
- [ ] `CHANGELOG.md` has an entry under `## [Unreleased]`.

## Releasing (maintainers)

Releases are cut by pushing a tag; the `.skill` is built and attached automatically.

1. Bump `metadata.version` in `SKILL.md`.
2. Move the `## [Unreleased]` items in `CHANGELOG.md` under a new version heading.
3. Commit, then tag and push:
   ```sh
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
4. The **Release** workflow builds `temporal-patterns.skill` and uploads it to the
   GitHub Release for that tag.

Keep the tag (`vX.Y.Z`), the `metadata.version` in `SKILL.md`, and the CHANGELOG
heading in agreement.
