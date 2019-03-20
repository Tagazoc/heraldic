#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main file !
"""

if __name__ == '__main__':
    import argparse
    from heraldic.cli import harvest
    from heraldic.cli import gather
    from heraldic.cli import test

    parser = argparse.ArgumentParser(description="Run commands to interact with Heraldic indexer", prog='heraldic')
    subparsers = parser.add_subparsers(help='sub-command help',)
    parser_harvest = subparsers.add_parser('harvest', help='Harvest links in supported feeds')
    parser_harvest.add_argument('media', help='Specify only one media to harvest', nargs='?')
    parser_harvest.add_argument('-o', '--override', help='Gather again up-to-date documents', action='store_true',
                                default=False)
    parser_harvest.add_argument('-d', '--depth', help='Depth of recursive gathering of sources', type=int, default=0)
    parser_harvest.set_defaults(func=harvest)

    parser_gather = subparsers.add_parser('gather', help='Gather one or several URLs')
    group = parser_gather.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='File containing one or several URLs (one per line)')
    group.add_argument('-i', '--stdin', help='Get URL from stdin', action='store_true', default=False)
    group.add_argument('-u', '--url', nargs='*', help='URL to gather')
    parser_gather.add_argument('-d', '--depth', help='Depth of recursive gathering of sources', type=int, default=0)
    parser_gather.add_argument('-o', '--override', help='Gather again up-to-date documents', action='store_true',
                               default=False)
    parser_gather.add_argument('-t', '--test', help='Stop on optional parsing exception', action='store_true',
                               default=False)
    parser_gather.set_defaults(func=gather)

    parser_test = subparsers.add_parser('test', help='Gather test URLs for one or several medias')
    parser_test.add_argument('media', help='Specify only one media to test', nargs='?')
    parser_test.set_defaults(func=test)

    parser_regather = subparsers.add_parser('regather', )

    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        # No command provided
        parser.print_help()

