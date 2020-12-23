from setuptools import setup

if __name__ == "__main__":
    setup(
        packages=["buildbot_abstract"],
        package_dir={"buildbot_abstract": "src"},
        install_requires=[["buildbot[bundle]", "hvac", "names", "retry"]],
        extras_require={
            "dev": ["black", "autoflake", "isort", "mypy", "wheel"],
        },
    )
