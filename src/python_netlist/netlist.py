#!/usr/bin/env python3
# Copyright 2020 Railnova SA
# Author: Charles-Henri Mousset
# 
# Netlist parsing for filling platform ios
from pprint import pprint


class Netlist:
    """A netlist is a dict of all the nets (signals) on a PCB, and of all its connections to the
    different components of that board."""

    def __init__(self, path):
        self.path = path
        netlist = {}
        with open(path, encoding='utf-8') as net:
            try:
                txt = net.readlines()
            except UnicodeDecodeError:
                print("\n!!! Make sure the symbol degree is not in the part description !!!\n")
                return
            i = 0
            while "NODE" not in txt[i]:
                i += 1
                break

            while i < len(txt):
                l = txt[i]
                l = l.strip()
                if '[' in l:
                    net_name = l.split()[1]
                    net_conns = []
                    i += 1
                    while len(txt[i]) > 4:
                        l = txt[i].strip()
                        tok = l.split()
                        net_conns.append({tok[0]: tok[1]})
                        i += 1
                    netlist.update({net_name: net_conns})
                i += 1
        self.netlist = netlist

    def find_pins(self, nets, con_to_pin, err_missing=True, err_multiple=True):
        """find the corresponding net connections in con_to_pin.
        If a net has multiple pins matching the net, raise an error.
        It returns a space-separated pin locations string.
        nets can be a single net name, or a python list"""
        pins = []
        if not isinstance(nets, list):
            nets = [nets]
        for n in nets:
            if n in self.netlist:
                ncomp = 0
                for conn in self.netlist[n]:
                    for component in conn:
                        if component in con_to_pin:
                            if ncomp and err_multiple:
                                errmsg = "net {} connected on multiple FPGA pads: {}".format(n, self.netlist[n])
                                raise Error(errmsg)
                            ncomp += 1
                            pin = conn[component]
                            try:
                                pins.append(con_to_pin[component][pin])
                            except:
                                if err_missing:
                                    raise Exception("pin {} of {} not mapped".format(pin, component))
                if ncomp == 0 and err_missing:
                    raise Exception("net {} has no associated pin!".format(n))
            elif err_missing:
                raise Exception("net {} not found in netlist!".format(n))
        return " ".join(pins)



    def check_orphans(self, min_pins=2):
        """return a list of nets that have less than min_pins connections"""
        netlist = self.netlist
        return {n: netlist[n] for n in netlist if
                len(netlist[n]) < min_pins and not (n.startswith('NC_') or ('_NC' in n) or ('.NC_' in n))}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Netlist tool')
    parser.add_argument('--out', type=str, help='JSON output file')
    parser.add_argument('--no-checks', default=False, action='store_true',
                        help="Don't perform checks")
    parser.add_argument('file', help="Netlist")
    args = parser.parse_args()

    print("...Parsing " + args.file + "...")
    netlist = Netlist(args.file)
    if not args.no_checks:
        print("###### Check Orphans ######")
        orphans = netlist.check_orphans()
        if len(orphans):
            print("## Possible orphans:")
            pprint(orphans)
            exit(1)
        else:
            print("No orphans: OK")

    if args.out:
        import json

        with open(args.out, 'w') as f:
            json.dump(netlist.netlist, f)
