import setuptools

setuptools.setup(
    name="demopackage",
    version="0.0.1",
    author="Omer Mete Aydin",
    description="GNL - 03 Demo Package (NovaVision)",
    url="https://github.com/<kullanici-adin>/DemoPackage",
    license="MIT",
    install_requires=["sdk", "opencv-python-headless", "numpy"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        "novavision.demopackage",
        "novavision.demopackage.executors",
        "novavision.demopackage.models",
        "novavision.demopackage.utils",
    ],
    package_dir={"novavision.demopackage": "src"},
    python_requires=">=3.6",
)
