# Contributing

Thanks for helping improve the **temporal-patterns** skill.

## Sources of truth

- `SKILL.md` and the files in `references/` are the skill. Make content changes
  there. Never edit the packaged `.skill`; it's a build artifact and isn't
  committed.
- For pattern facts, the live docs win: the index at
  `https://docs.temporal.io/design-patterns.md` and each pattern page. The pages
  are maintained in the `temporalio/documentation` repo, under
  `docs/design-patterns/`. To see what changed since the last refresh, read the
  commits to that folder.

## Kinds of contributions

### Fixing a route

The "Use it when" column of the catalog tables in `SKILL.md` is the most-used
surface. Write it symptom first, the way users describe problems. If the answer
is a feature rather than a pattern, change the features table instead.

### Adding, renaming or removing a pattern

Each pattern has one row in the catalog table for its domain:
`| Name | \`slug\` | Use it when |`. Its slug can also appear in:

1. The choosing and composition notes in `SKILL.md`.
2. `references/use-cases.md`, `references/anti-patterns.md` and
   `references/guides.md`.
3. The snapshot line in `SKILL.md` and the count in `README.md`.

Grep for the slug and the name and update every place. Rules:

- **Use the exact name from the live index.** Pattern names are Temporal product
  terms. `make check-links` fails if a name differs from the index.
- **The slug must match the live docs.** `make check-links` checks that every
  slug resolves and that the index has no pattern the catalog lacks.
- **Keep rows short.** The catalog points at the page; it doesn't replace it.
- **Don't invent patterns.** Add only patterns in the live index.

### Updating a feature or a release stage

The features table carries release stages as of a date. When a stage changes,
update the row and the date, and quote the stage exactly as the docs state it.

## Local workflow

```sh
make setup         # install PyYAML, once
make lint          # frontmatter, description length (1,024 max), references exist
make verify        # build dist/temporal-patterns.skill and diff it against the sources
make check-links   # catalog against the live docs, both ways, and every docs URL
```

CI runs `lint` and `verify` on every PR. `check-links` runs too but doesn't block,
because it depends on the live docs site.

If you change routing text, the description or the catalog, re-run the evals in
`evals/` and add a row to the results table in `evals/README.md`.

## Pull request checklist

- [ ] The change is in `SKILL.md` or `references/`, not the `.skill` package.
- [ ] Every place that names a touched pattern is consistent.
- [ ] `make lint`, `make verify` and `make check-links` pass.
- [ ] Routing or description changes have an eval run recorded in `evals/README.md`.
- [ ] `CHANGELOG.md` has an entry under `## [Unreleased]`.

## Releasing (maintainers)

A tag cuts a release; the workflow builds and attaches the `.skill`.

1. Bump `metadata.version` in `SKILL.md`.
2. Move the `## [Unreleased]` items in `CHANGELOG.md` under a new version heading.
3. Commit, then tag and push:
   ```sh
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
4. The Release workflow builds `temporal-patterns.skill` and uploads it to the
   GitHub release for that tag.

Keep the tag, `metadata.version` and the CHANGELOG heading in agreement.
