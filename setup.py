"""Setup script for alexa_roomba package."""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_file(filename):
    """Read a file and return its contents."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read requirements from requirements.txt
def read_requirements():
    """Parse requirements.txt and return list of requirements."""
    requirements = []
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        with open(req_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

setup(
    name='alexa-roomba',
    version='1.0.0',
    description='Voice-controlled Roomba via Amazon Echo with iRobot Open Interface',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',

    # Author information
    author='Zach Dodds, Sean Luke, James O\'Beirne, Martin Schaef',
    author_email='',  # Add if available

    # Project URLs
    url='https://github.com/antigenius0910/alexa_roomba',
    project_urls={
        'Bug Reports': 'https://github.com/antigenius0910/alexa_roomba/issues',
        'Source': 'https://github.com/antigenius0910/alexa_roomba',
        'Documentation': 'https://github.com/antigenius0910/alexa_roomba/blob/master/docs/',
        'Changelog': 'https://github.com/antigenius0910/alexa_roomba/blob/master/CHANGELOG.md',
    },

    # Package configuration
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'legacy', 'docs']),
    include_package_data=True,

    # Python version requirement
    python_requires='>=3.7',

    # Dependencies
    install_requires=read_requirements(),

    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-mock>=3.10.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },

    # Package classification
    classifiers=[
        # Development status
        'Development Status :: 5 - Production/Stable',

        # Intended audience
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        # License
        'License :: OSI Approved :: MIT License',

        # Programming language
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',

        # Topics
        'Topic :: Home Automation',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Software Development :: Embedded Systems',

        # Operating systems
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',

        # Environment
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',

        # Natural language
        'Natural Language :: English',
    ],

    # Keywords for discovery
    keywords=[
        'roomba',
        'irobot',
        'alexa',
        'echo',
        'voice-control',
        'smart-home',
        'iot',
        'robotics',
        'raspberry-pi',
        'serial',
        'open-interface',
        'automation',
        'home-automation',
    ],

    # Entry points (console scripts)
    entry_points={
        'console_scripts': [
            # Add console scripts if needed in the future
            # 'alexa-roomba=roomba.cli:main',
        ],
    },

    # Additional metadata
    zip_safe=False,
    platforms=['any'],
)
