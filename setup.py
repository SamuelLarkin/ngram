from setuptools import setup
from setuptools import find_packages


ROOT = os.path.dirname(__file__)

def get_long_description(doc_filename = 'README.md'):
    with open(os.path.join(ROOT, doc_filename), encoding='utf-8') as f:
        markdown_txt = f.read()
        return markdown_txt




setup(
        name='ngram',

        version=get_version(),

        description='Utility to create ngram or cbow out of sentences.',
        long_description=get_long_description(),
        long_description_content_type="text/markdown",

        url='https://github.com/Samuel.Larkin/ngram',

        author='Samuel Larkin',
        author_email='Samuel.Larkin@gmail.com',
        maintainer_email='Samuel.Larkin@gmail.com',

        license='Apache License 2.0',

        python_requires='>=3',

        packages=find_packages(exclude=("test", "test.*")),

        setup_requires=None,
        tests_require=['unittest'],

        extras_require={
            'optional': None,
            'dev': None,
            },

        #install_requires=install_requires,

        entry_points = {
            'console_scripts': [
                'ngram = ngram.ngram:main',
                ],
            }

        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3 :: Only',
            ],

        #cmdclass=cmdclass,
        )
