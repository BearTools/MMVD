.. _installation_long:

Installation
============

We highly suggest to use method described below, as it's a standard way in
Python world.

1. Install global system requirements.  This may vary between systems; for
   Ubuntu Linux::

    $ sudo apt-get install python python-pip python-virtualenv

2. Make a virtual environment and activate it::

    $ virtualenv MMVD_venv
    $ source MMVD_venv/bin/activate

3. Clone this repository::

    (MMVD_venv)$ cd MMVD_venv
    (MMVD_venv)$ git clone https://github.com/WojciechFocus/MMVD.git
    (MMVD_venv)$ cd MMVD

4. Install this application::

    (MMVD_venv)$ python setup.py install

This should take care of installing all requirements.  The installation also
provides ``MMVD.py`` executable (saved in ``MMVD_venv/bin/MMVD.py``), that
you can run


Development
-----------

To install MMVD as an editable Python package, please follow steps 1-3 above.
For the 4th step look below:

4. Install this application as an editable Python package::

    (MMVD_venv)$ pip install -e .
