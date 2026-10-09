from setuptools import find_packages, setup

version = "0.1.0"

setup(
    name="passerelle-imio-iacitizen",
    version=version,
    author="iMio",
    author_email="support-ts@imio.be",
    description="iA.Citizen : requêtes passerelle des catégories spécifiques Smartweb",
    packages=find_packages(),
    include_package_data=True,
    data_files=[("/etc/passerelle/settings.d", ["settings.d/50passerelle_imio_iacitizen.py"])],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/IMIO/passerelle-imio-iacitizen",
    install_requires=[
        "django>=4.2",
    ],
    zip_safe=False,
)
