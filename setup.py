# _*_ coding: UTF-8 _*_

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='hunor',
    description='The son of Nimrod',
    long_description=readme(),
    keywords='test mutant analysis equivalent',
    version='0.2.0',
    url='https://github.com/marcioaug/hunor',
    author='Marcio Augusto Guimarães',
    author_email='masg@ic.ufal.br',
    license='MIT',
    packages=['hunor', 'hunor.tools'],
    install_requires=[
        'argparse==1.4.0',
        'beautifulsoup4==4.6.0',
        'graphviz==0.8.3'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['hunor=hunor.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Test :: Mutation'
    ]
)