*******************
Empowring customize
*******************




Models
======

.. py:class:: GiscedataPolissa

    .. note:: This class is extended by this module adding the following
        attributes

    .. py:attribute:: empowering_profile_id

        Relation with a :class:`EmpoweringCustomizeProfile`


.. py:class:: EmpoweringCustomizeProfile

    Main class to customize Empowering services

    .. py:attribute:: name

        Name of the custmitzation

    .. py:attribute:: contracts_ids

        List of contracts that have this customitzation

    .. py:attribute:: channels_ids

        List of :class:`EmpoweringCustomizeProfileChannel`

    .. py:attribute:: interval_id

        Relation of :class:`EmpoweringCustomizeInterval`


.. py:class:: EmpoweringCustomizeTemplate

    .. py:attribute:: name

        Name of the template

    .. py:attribute:: path

        Path to the template, it can be an URL

.. py:class:: EmpoweringCustomizeChannel

    .. py:attribute:: name

        Channel of comunication for the service

    .. py:attribute:: default_template_id

        Default template to use with this channel if is not defined in the

        Relation with a :class:`EmpoweringCustomizeTemplate`


.. py:class:: EmpoweringCustomizeProfileChannel

    .. py:attribute:: profile_id

        Relation with a :class:`EmpoweringCustomizeProfile`

    .. py:attribute:: channel_id

        Relation with a :class:`EmpoweringCustomizeChannel`

    .. py:attribute:: template_id

        Template to use with this :attr:`channel_id` in this :attr:`profile_id`


.. py:class:: EmpoweringCustomizeInterval

    .. py:attribute:: number

        Quantification of interval

    .. py:attribute:: measure

        Measure for the interval, one of:

          * on_demand
          * days
          * weeks
          * months

        .. note::
            **on_demand** is special, and no :attr:`number` is needed for
            this type of measure