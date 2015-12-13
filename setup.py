#!/usr/bin/env python3
#
#

import os
import sys

if sys.version_info.major < 3: print("you need to run meds with python3") ; os._exit(1)

try: use_setuptools()
except: pass

try:
    from setuptools import setup
except Exception as ex: print(str(ex)) ; os._exit(1)

setup(
    name='meds',
    version='1066',
    url='https://pikacode.com/bart/meds',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description=" Antipsychotica zijn in hun werking benadeling van de gezondheid.",
    license='MIT',
    include_package_data=False,
    zip_safe=False,
    install_requires=["beautifulsoup4", "sleekxmpp", "feedparser"],
    scripts=["bin/meds", "bin/meds-ps", "bin/meds-local", "bin/meds-sed", "bin/meds-udp", "bin/meds-do", "bin/meds-docs", "bin/meds-doctest"],
    packages=['meds',
              'meds.bots',
              'meds.mods',
             ],
    long_description="""

Wetboek van Strafrecht:

1) Antipsychotica zijn in hun werking benadeling van de gezondheid.
2) Daarmee is toedienen van deze medicijnen mishandeling zoals vernoemd in het wetboek van strafrecht.
3) Het doen laten verdwijnen van gevaar is het oogmerk.

Verdrag tegen foltering:

1) Een maatregel is geen straf.
2) Een ambtsbevel is geen rechtvaardiging.
3) Geen enkele omstandigheid is een rechtvaardiging.

EVRM:

1) Recht op leven
2) Verbod van foltering
3) Recht op vrijheid en veiligheid
4) Recht op daadwerkelijk rechtsmiddel
5) Verbod van misbruik van recht

""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Utilities'],
)
