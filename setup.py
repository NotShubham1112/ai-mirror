from setuptools import setup, find_packages

setup(
    name="pixel-ai-mirror",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "llama-cpp-python",
        "rich",
        "numpy",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "pixel-chat=run_ai_mirror:main",
        ],
    },
    author="Shubham Kambli",
    description="An emotion-aware AI companion for the AI Mirror project.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NotShubham1112/ai-mirror",
    python_requires=">=3.10",
)
