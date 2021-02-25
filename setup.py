from setuptools import setup

if __name__ == "__main__":
    setup(
        install_requires=[["buildbot[bundle]", "hvac", "names", "retry"]],
        extras_require={
            "docs": [
                "pyimport",
                "pypandoc",
                "sphinx-autodoc-annotation",
                "sphinx",
                "sphinxcontrib.apidoc",
                "sphinxcontrib.pandoc_markdown",
                "yummy_sphinx_theme",
            ],
            "tests": [
                "pytest-bdd",
                "pytest-cov",
                "pytest-html",
                "pytest-sugar",
                "pytest-watch",
                "pytest",
                "tox",
            ],
            "tools": [
                "autoflake",
                "bandit",
                "black",
                "bump2version",
                "bump2version",
                "isort",
                "mypy",
                "pylint",
                "quickdocs",
                "twine",
                "wheel",
            ],
        },
    )
