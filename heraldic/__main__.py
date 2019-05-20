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
    from heraldic.cli import regather

    parser = argparse.ArgumentParser(description="Run commands to interact with Heraldic indexer", prog='heraldic')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    parser_harvest = subparsers.add_parser('harvest', help='Harvest links in feeds or gathered sources')
    parser_harvest.add_argument('media', help='Specify only one media to harvest', nargs='?')
    parser_harvest.add_argument('-s', '--sources', help='Gather the sources of indexed documents instead of feeds',
                                action='store_true', default=False)
    parser_harvest.add_argument('-o', '--override', help='Gather again up-to-date documents', action='store_true',
                                default=False)
    parser_harvest.add_argument('-d', '--depth', help='Depth of recursive gathering of sources', type=int, default=0)
    parser_harvest.add_argument('-i', '--crawl-internally', help='Only crawl domains for this media', action='store_true',
                                default=False)
    parser_harvest.add_argument('-t', '--delay', help='Time between document gathering (in seconds)',
                                action='store_true', default=False)
    parser_harvest.add_argument('-r', '--recursive-step', help='Step between recursive crawling in gathered sources (0 disables)',
                                type=int, default=0)
    parser_harvest.set_defaults(func=harvest)

    parser_gather = subparsers.add_parser('gather', help='Gather one or several URLs')
    group = parser_gather.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='File containing one or several URLs (one per line)')
    group.add_argument('-i', '--stdin', help='Get URL from stdin', action='store_true', default=False)
    group.add_argument('-u', '--url', nargs='*', help='URL to gather')
    parser_gather.add_argument('-d', '--depth', help='Depth of recursive gathering of sources', type=int, default=0)
    parser_gather.add_argument('-o', '--override', help='Override last version instead of creating a new one', action='store_true',
                               default=False)
    parser_gather.add_argument('-t', '--test', help='Stop on optional parsing exception', action='store_true',
                               default=False)
    parser_gather.set_defaults(func=gather)

    parser_test = subparsers.add_parser('test', help='Gather test URLs for one or several medias')
    parser_test.add_argument('media', help='Specify only one media to test', nargs='?')
    parser_test.set_defaults(func=test)

    parser_regather = subparsers.add_parser('regather', help='Regather already indexed documents')
    parser_regather.add_argument('media', help='Specify requested media')
    parser_regather.add_argument('-a', '--attribute',
                                 help='Regather only documents which failed to extract a specific attribute')
    parser_regather.add_argument('-e', '--error',
                                 help='Regather only documents which encountered a specific Python error')
    parser_regather.add_argument('-o', '--override', help='Override last version instead of creating a new one',
                                 action='store_true', default=False)
    parser_regather.add_argument('-d', '--depth', help='Depth of recursive gathering of sources', type=int, default=0)
    parser_regather.add_argument('-t', '--test', help='Stop on optional parsing exception', action='store_true',
                                 default=False)
    parser_regather.set_defaults(func=regather)

    args = parser.parse_args()

    if args.command == 'regather' and args.error and not args.attribute:
        parser.error('You must specify an attribute when specifying an error')

    try:
        args.func(args)
    except AttributeError:
        # No command provided
        parser.print_help()

