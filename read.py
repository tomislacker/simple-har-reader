import json
from os import path
from types import *
import getopt
import sys

def get_input_output_bytes_from_files(
        json_files,
        show_output=False
):
    assert type(json_files) is ListType, "json_files is not a list: %r" % json_files

    browser_tx = 0
    browser_rx = 0

    file_index = 0
    for json_file in json_files:
        analysis_output = get_input_output_bytes_from_file(json_file)
        browser_tx += analysis_output['browser_tx']
        browser_rx += analysis_output['browser_rx']
        file_index += 1

        if show_output:
            print 'get_input_output_bytes_from_files[%i] -- Rx: %i Tx: %i' % (file_index, analysis_output['browser_rx'], analysis_output['browser_tx'])

    if show_output:
        print 'get_input_output_bytes_from_files[SUM] -- Rx: %i Tx: %i' % (browser_rx, browser_tx)

    return {
        'browser_tx': browser_tx,
        'browser_rx': browser_rx
    }

def get_input_output_bytes_from_file(
        json_file
):
    assert type(json_file) is StringType, "json_file is not a string: %r" % json_file
    assert path.isfile(json_file) or path.islink(json_file), "json_file is not a path to a file or link: %r" % json_file

    return get_input_output_bytes(
        json.loads(
            open(json_file, "rb").read()
        )
    )

def get_input_output_bytes(
        json_obj
):
    assert not type(json_obj) is NoneType, "No json_obj provided"
    assert type(json_obj) is DictType, "json_obj was type '%s' instead of dict: %r" % (type(json_obj), json_obj)

    browser_rx = 0
    browser_tx = 0

    for page_req in json_obj['log']['entries']:
        if type(page_req['response']['bodySize']) == IntType:
            browser_rx += page_req['response']['bodySize']

        if type(page_req['request']['headersSize']) == IntType:
            browser_tx += page_req['request']['headersSize']

    return {
        'browser_tx': browser_tx,
        'browser_rx': browser_rx
    }

if __name__ == '__main__':
    ###
    # Use getopt to parse the command line options
    ###
    args_parsed, args_remain = getopt.getopt(
        sys.argv[1:],
        'f:TP',
        [
            'file=',
            'get-transfer',
            'no-pretty-print'
        ]
    )

    target_files = []
    target_operation = None
    output_pretty_print = True

    ###
    # Validate and retain the command line arguments
    ###
    for opt, arg in args_parsed:
        if opt in ('-f', '--file'):
            target_files.append(arg)
        elif opt in ('-T', '--get-transfer'):
            target_operation = 'get_input_output_bytes_from_files'
        elif opt in ('-P', '--no-pretty-print'):
            output_pretty_print = False

    ###
    # Validate the target_operation variable
    ###
    if not target_operation:
        raise Exception('No target_operation specified')

    try:
        if not locals()[target_operation]:
            pass
    except KeyError:
        raise Exception('target_operation "%s" does not exist' % target_operation)

    ###
    # Ensure we have at least one file to operate on
    ###
    if len(target_files) == 0:
        raise Exception('No target_files specified')

    ###
    # Call the target_operation and output the results
    ###
    output = locals()[target_operation](target_files)

    if output_pretty_print:
        print json.dumps(
            output,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    else:
        print output