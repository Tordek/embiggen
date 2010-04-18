Embiggen
========

**Embiggen lets you write HTML code faster.**

You can write HTML in a CSS-like syntax, and have Embiggen handle the
expansion to full HTML code. It is meant to help you write long HTML blocks
in your text editor by letting you type fewer characters than needed.

Embiggen is written in Python, and requires Python 2.5 or newer (2.5 is
preinstalled in Mac OS X Leopard).

Usage and installation
----------------------
You may download the latest version of **Embiggen** from Github.

Afterwards, just call ``embiggen.py`` from you command line and start typing.

Credits
-------

Embiggen is written by Guillermo Freschi and is released under the 2-clause
BSD license. For more information, see the ``COPYING`` file.

This project is inspired by `Vadim Makeev`_'s `Zen Coding`_ and
`Rico Sta. Cruz`_'s `Sparkup`_.

.. _`Vadim Makeev`: http://pepelsbey.net
.. _`Zen Coding`: http://code.google.com/p/zen-coding/
.. _`Rico Sta. Cruz`: http://ricostacruz.com
.. _`Sparkup`: http://github.com/rstacruz/sparkup

Examples
--------

``span`` expands to::

    <span></span>

``div`` expands to::

    <div>

    </div>

``div#header`` expands to::

    <div id="header">

    </div>

``div#header.align-left`` expands to::

    <div id="header" class="align-left">

    </div>

``#header + #footer`` expands to::

    <div id="header">

    </div>
    <div id="footer">

    </div>

``a[href=index.html]{Home}`` expands to::

    <a href="index.html">Home</a>

``#menu > ul`` expands to::

    <div id="menu">
            <ul>

            </ul>
    </div>

``#menu > h3 + ul`` expands to::

    <div id="menu">
            <h3></h3>
            <ul>

            </ul>
    </div>

``#header > h1{Welcome to our site}`` expands to::

    <div id="header">
            <h1>Welcome to our site</h1>
    </div>


``#header > ul > li < p{Footer}`` expands to::

    <div id="header">
        <ul>
            <li></li>
        </ul>
        <p>Footer</p>
    </div>

