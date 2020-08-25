=============
Python ARTMAP
=============

.. image:: https://img.shields.io/pypi/v/python_artmap.svg
        :target: https://pypi.python.org/pypi/python_artmap
..

        .. image:: https://img.shields.io/travis/DavidVinicius/python_artmap.svg
                :target: https://travis-ci.com/DavidVinicius/python_artmap

        .. image:: https://readthedocs.org/projects/python-artmap/badge/?version=latest
                :target: https://python-artmap.readthedocs.io/en/latest/?badge=latest
                :alt: Documentation Status


A Python Library of Neural network ARTMAP.

* Free software: MIT license


How install
-----------

.. code-block:: python

        pip install python_artmap

Features
--------
This library contains two of the main ART neural network

        * ARTMAP Fuzzy
        * ART Fuzzy

How use it
----------

.. code-block:: python

        from python_artmap import ARTMAPFUZZY
        
        input  = np.array([
                [0, 0], 
                [0, 1], 
                [1, 0], 
                [1, 1]        
        ])

        output  = np.array([
                [0],
                [0],
                [0],
                [1],
        ])

        ArtMap = ARTMAPFUZZY(input, output, rhoARTa=0.6, rhoARTb=0.9)
        ArtMap.train()

        ArtMap.test([0, 0]) #{'index': 0, 'ArtB': [0.0, 1.0], 'id': '0010'}
        ArtMap.test([0, 1]) #{'index': 0, 'ArtB': [0.0, 1.0], 'id': '0010'}
        ArtMap.test([1, 0]) #{'index': 0, 'ArtB': [0.0, 1.0], 'id': '0010'}
        ArtMap.test([1, 1]) #{'index': 1, 'ArtB': [1.0, 0.0], 'id': '1000'}



Credits
-------
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
