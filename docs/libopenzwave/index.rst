=================
API documentation
=================

---------------
Getting Started
---------------

pyozw (python-openzwave) has almost been completely rewritten. This was done
to improve performance and also make the API more user friendly. Unfortunaly
during this process we were forced to break API. So anything that was written
for pyozw <= 0.4x is going to need to be written over. We are sorry for doing
this to you, but as you will see it is for the better.

We have squeezed every drop of performance we can out of the library. We have
seen time improvements of > 80%.


--------------
Changes in API
--------------

The new Notification/Signal system.
-----------------------------------

please see :py:mod:`libopenzwave.signals`

|

Controller Commands
-------------------

There used to be a lock when using any controller commands. Which meant only a
single controller command could be running at any given time. This lock has
been removed. You now have the ability to queue commands. below is a list of
methods that make use of this queuing feature.

The list below is seperated by which signal to use in order to get updates on
a controller command that is running. You have the ability to register a
callback to a signal providing the object you want to get signal updates from.

|

* `libopenzwave.SIGNAL_NODE_CONTROLLER_COMMAND`

    * :py:func:`libopenzwave.node.ZWaveNode.update_neighbors`
    * :py:func:`libopenzwave.node.ZWaveNode.create_button`
    * :py:func:`libopenzwave.node.ZWaveNode.delete_button`
    * :py:func:`libopenzwave.node.ZWaveNode.heal`
    * :py:func:`libopenzwave.node.ZWaveNode.update_return_route`
    * :py:func:`libopenzwave.node.ZWaveNode.delete_return_routes`
    * :py:func:`libopenzwave.node.ZWaveNode.send_information`
    * :py:func:`libopenzwave.node.ZWaveNode.network_update`
    * :py:func:`libopenzwave.controller.ZWaveController.create_new_primary`
    * :py:func:`libopenzwave.controller.ZWaveController.transfer_primary_role`
    * :py:func:`libopenzwave.controller.ZWaveController.replication_send`
    * :py:func:`libopenzwave.controller.ZWaveController.receive_configuration`

* `libopenzwave.SIGNAL_NETWORK_CONTROLLER_COMMAND`

    * :py:func:`libopenzwave.network.ZWaveNetwork.add_node`
    * :py:func:`libopenzwave.network.ZWaveNetwork.replace_failed_node`
    * :py:func:`libopenzwave.network.ZWaveNetwork.remove_node`

|

Here is a use example of command notifications.

.. code-block:: python

    node = network.nodes[10]

    def callback(sender, state, **kwargs):
        print(sender.id)
        print('Command label:', state.label)
        print('Command:', state.command)
        print('Command tooltip:', state.command.doc)
        print('State:', state.state)
        print('State tooltip:', state.state.doc)
        print('Error:', state.error)
        print('Error tooltip:', state.error.doc)

        if state.state in ('Completed', 'Failed'):
            libopenzwave.SIGNAL_NODE_CONTROLLER_COMMAND.unregister(callback, node)


    libopenzwave.SIGNAL_NODE_CONTROLLER_COMMAND.register(callback, node)

    node.update_neighbors()

|

Because of this new system you will be able to provide some for of a visual
identifier that a command is being run on a specific node. and you will be
able to update the user as to the progress of that command for that specific
node. You will also be able to provide the same thing for network wide commands.

|

There is a pretty major overhaul of how nodes are handled. A ZWaveNode instance
no longer has methods or properties that do not belong to it. When a node gets
loaded the class for that instance gets dynamically created based on the command
classes the node supports. So you have to make sure you test and see if a node
supports a command class before accessing methods or properties for that command
class.

I added support for devices that have multiple "nodes" built into them. This is
commonly seen in special lighting controllers. An example of this would be a
landscape lighting that has multiple zones. Each zone of that lighting controller
should be presented to the user as a device that can be turned on and off. So
what I did was I created virtual nodes which function just like a normal node would.
The instances are dynamically created using the command classes and the ZWaveNode
class just like a normal node is. you can test if a node is a virtual node by using
the `is_endpoint` propertyfor that node.


The real magic to the changes I have made is when you want to populate a GUI.
You can take a look at the libopenzwave_man portion of this library. It is not
yet finished but it will help you to understand how to create GUI controls for
the various command classes

---------
Contents
---------

.. toctree::
    :maxdepth: 1

    signals <signals>
    network module <network>
    controller module <controller>
    option module <option>
    node module <node>
    node types module <node_types>
    command_classes module <command_classes/index>
    group module <association_group>
    value module <value>
    scene module <scene>
    object module <object>
    exception module <exception>
    common definitions <data>

