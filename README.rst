==========================
clms.statstool
==========================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/clms.statstool/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/clms.statstool/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/clms.statstool/master
  :target: https://ci.eionet.europa.eu/job/eea/job/clms.statstool/job/master/display/redirect
  :alt: Master

The clms.statstool is a Plone add-on to save the download stats of the CLMS portal

.. contents::


Main features
=============

It provides several methods to register download requests from users.
It provides several REST API endpoints to request the download requests (WIP)

Install
=======

* Add clms.statstool to your eggs section in your buildout and
  re-run buildout::

    [buildout]
    eggs +=
      clms.statstool

* You can download a sample buildout from:

  - https://github.com/eea/clms.statstool/tree/master/buildouts/plone5

* Or via docker::

    $ docker run --rm -p 8080:8080 -e ADDONS="clms.statstool" plone

* Install *clms.statstool* within Site Setup > Add-ons


Buildout installation
=====================

- `Plone 5+ <https://github.com/eea/clms.statstool/tree/master/buildouts/plone5>`_


Source code
===========

- `Plone 5+ on github <https://github.com/eea/clms.statstool>`_


Eggs repository
===============

- https://pypi.python.org/pypi/clms.statstool
- http://eggrepo.eea.europa.eu/simple


Plone versions
==============
It has been developed and tested for Plone 5 and python 3. See buildouts section above.


How to contribute
=================
See the `contribution guidelines (CONTRIBUTING.md) <https://github.com/eea/clms.statstool/blob/master/CONTRIBUTING.md>`_.

Copyright and license
=====================

clms.statstool (the Original Code) is free software; you can
redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc., 59
Temple Place, Suite 330, Boston, MA 02111-1307 USA.

The Initial Owner of the Original Code is European Environment Agency (EEA).
Portions created by Eau de Web are Copyright (C) 2009 by
European Environment Agency. All Rights Reserved.


Funding
=======

EEA_ - European Environment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`EEA Web Systems Training`: http://www.youtube.com/user/eeacms/videos?view=1
