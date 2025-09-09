from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="realtime-bg-remover",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A real-time background remover using OpenCV and MediaPipe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/realtime-bg-remover",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bg-remove=BackgroundRemover:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["BackgroundImages/*", "requirements.txt"],
    },
)