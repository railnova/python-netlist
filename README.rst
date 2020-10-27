=============
netlist
=============


Parse Altium designer (and probably other) netlist.


Description
===========

A netlist describes all the electrical connection between then components of a Printed Circuit Board. A typical Altium Designer generated Netlist looks like this::

    Wire List
    
    <<< Component List >>>
    100Ohms                         R1             0402
    1uF                             C10            1206
    
    <<< Wire List >>>
    
      NODE  REFERENCE  PIN #   PIN NAME       PIN TYPE    PART VALUE
    
    [00002] VCC
            R1         1                      PASSIVE     myresistor
            C10        2                      PASSIVE     mycap
    
    [00001] GND
            R1         2                      PASSIVE     myresistor
            C10        1                      PASSIVE     mycap
    
    

It contains
 1. a very crude BOM (value, designator, package)
 2. A list of all signal names and their connection.

In this example, 2 components are defined, and 2 nets are defined.

This module ignores the BOM, and concentrates only on nets.


SOM connection helper
=====================

On large System On Module, it can be very tedious and error-prone to define the different signal connection in device trees, or in an Hardware Design (for FPGA designs)

Using to the `find_pins` function, it is possible to retreive pin names from on a net name.
You first have to define your module connectors and pins this way::

    pz_pins = {
        "JX1" : {
            "9" : "R19",
            "10" : "T19",
            "11" : "T11",
            "12" : "T12",
            "13" : "T10",
            "14" : "U12",
        },
        "JX2" : {
            "13" : "G14",
            "14" : "J15",
            "17" : "C20",
            "18" : "B19",
        },
    }

in this example, the SOM has 2 connectors which are seperate parts on the PCB, called "JX1" and "JX2". Pin 9 of connector JX1 is named pin "R19" internally in the SOM.

This also works on components which have a single part (in this example only the first 2 pins are described)::

    stmf32F407_64_pins = {
    	"1" : "VBAT",
    	"2" : "PC13",
    }


Automatic Checks
================

Common Schematic capture mistakes can be caught analyzing the Netlist. The most common is probably unconnected pins due to a bad net label.

`check_orphands` lists all nets that have (by default) less than 2 connections.

Command-line tool
=================

You can call `python -m netlist` to invoque the command-line tool. Use the built-in help to lear to use it.
