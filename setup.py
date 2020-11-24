from setuptools import setup, find_packages

desc = "A short-lived certificate tool based on the Zero Trust network mode"

setup(
    name="mtls-qt",
    author="Danny Grove <danny@drgrovellc.com>",
    url="https://github.com/drGrove/mtls-qt",
    description=desc,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/drGrove/mtls-qt",
        "Source": "https://github.com/drGrove/mtls-qt",
        "Tracker": "https://github.com/drGrove/mtls-qt/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Security :: Cryptography",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires='>=3.8',
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
    packages=find_packages(exclude=["test"]),
    package_data={
        "mtls_qt": [
            "assets/*.png"
        ]
    },
    entry_points={
        "console_scripts": [
            "mtls-qt = mtls_qt.main:main"
        ]
    },
    install_requires=[
        "PyQT5",
        "mtls"
    ],
    zip_safe=True,
    include_package_data=True,
)
