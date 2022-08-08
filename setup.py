from setuptools import setup, find_packages
import os, pathlib
from setuptools.command.egg_info import egg_info

class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get('install', True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file('LICENSE.txt', self.egg_info)

        egg_info.run(self)

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="staratlaspy",
    version="0.1.30",
    description="Python module for parsing staratlas instructions (based on anchorpy).",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    readme = "README.md",
    license_files = ('LICENSE.txt',),
    license = 'Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License',
    cmdclass = {'egg_info': egg_info_ex},

    #url = "https://git.kryptonhub.com/the-club/staratlaspy",
    author = "Vlad Smirnov",
    author_email = "vlad@theclubguild.com",
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries :: Python Modules",
      "Programming Language :: Python :: 3"
    ],
    packages = ['staratlas'] +
               ['staratlas.utils'] +
               ['staratlas.marketplace'] +
               ['staratlas.marketplace.'+ s for s in ['accounts','errors','instructions','types']] +
               ['staratlas.faction'] +
               ['staratlas.faction.' + s for s in ['accounts', 'errors', 'instructions']] +
               ['staratlas.score'] +
               ['staratlas.score.' + s for s in ['accounts', 'errors', 'instructions', 'types']],
    package_dir = {'staratlas': '.'},
    python_requires=">=3.9, <4",
    install_requires=[
        'construct==2.10.67',
        'solders==0.2.0',
        'requests[socks]',
        'solana==0.23.1',
        'click==8.1.3',
        'anchorpy[cli]==0.9.1',
        'asyncclick==8.1.3.2'
    ],
    data_files=[("idls", [
        "idls/staratlas-score.json",
        "idls/staratlas-faction.json",
        "idls/staratlas-distributor.json",
        "idls/staratlas-marketplace.json"
    ])],
    include_package_data = True,
    entry_points={  # Optional
        "console_scripts": [
            "staratlas=staratlas.cli:cli",
        ],
    },
)

