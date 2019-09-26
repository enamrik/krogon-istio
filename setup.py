from setuptools import setup, find_packages


def read_file(filename):
    with open(filename) as f:
        return f.read()


setup(
    python_requires="~=3.7",
    name="krogon-istio",
    version=read_file("./krogon_istio/VERSION").strip(),
    description="Tool for generating and executing K8s templates",
    long_description=read_file("README.md"),
    author="Kirmanie L Ravariere",
    author_email="enamrik@gmail.com",
    license=read_file("LICENSE"),
    packages=find_packages(exclude=("tests", "outputs")),
    package_data={"krogon_istio": ["URL", "VERSION", "*.txt", "*.yml", "*.template", "**/*.sh", "*.ini", "bin/**/*"]},
    include_package_data=True,
    install_requires=[
        'ruamel.yaml==0.15.87'
    ],
    extras_require={
        'dev': [
            'pytest',
            'dictdiffer==0.7.1'
        ]
    },
)
