# Contributing

All contributions are welcome! :wave:

Here are a few ways in which you can help:

- Discovered a bug? Please open a [bug report](https://github.com/florimondmanca/djangorestframework-api-key/issues/new?template=bug_report.md).
- Have a feature you'd like to see implemented? Please open a [Feature Request](https://github.com/florimondmanca/djangorestframework-api-key/issues/new?template=feature_request.md).
- For any other contribution, please open a [discussion](https://github.com/florimondmanca/djangorestframework-api-key/issues/new?template=discussion.md).

**NOTE**: for **non-trivial changes** we *highly* encourage you to **open an issue** first. This will allow maintainers and contributors to confirm that the problem you are trying to solve is well-posed, in the scope of the project, and/or can't be solved with existing features.

### Install

Installing locally requires [Pipenv](https://github.com/pypa/pipenv) and Python 3.7.

1. Fork the repo
2. Clone it on your local
3. Install dependencies with Pipenv: `$ pipenv install --dev`
4. Activate using `$ pipenv shell`

### Tests

Run the tests using:

```bash
$ pytest
```

### Generating migrations

This package includes migrations. To update them in case of changes without setting up a Django project, run:

```bash
$ python scripts/makemigrations.py
```

## Notes to maintainers

### CI/CD

Travis CI is in use to automatically:

- Test the package on supported versions of Python and Django.
- Release _tagged commits_ to PyPI.

See `.travis.yml` for further details.

### Releasing

When ready to release a new version, use [bumpversion](https://pypi.org/project/bumpversion/) to update the package's version:

```bash
$ bumpversion (patch | minor | major)
```

This will create a new commit and tag that commit with the new version. See [.bumpversion.cfg](.bumpversion.cfg) for more info.

Then, push the tagged commit to remote:

```bash
$ git push --tags
```
