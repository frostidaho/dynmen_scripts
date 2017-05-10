dynmen_scripts
==============

A collection of scripts using `dynmen <https://github.com/frostidaho/dynmen>`_.
They're just intended for my personal use or
as examples for using dynmen.

Installation
------------
An issue I ran into in packaging these scripts was
how entry_points are created. If you install from
a wheel package the scripts created from the entry_points
specified in setup.py are significantly faster than if you
just use pip install on the directory. If you look at the
generated scripts it comes down to some additional imports.

With that in mind use the makefile to create a wheel package
and install it:

.. code-block:: bash

                make install-user


