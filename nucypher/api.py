from __future__ import print_function
from pyumbral import test_pre as test_pre
import sys
import zerorpc
import json

class CalcApi(object):

    def calc(self, text):
        """based on the input text, return the int result"""
        try:
            output = test_pre(text)
            return json.dumps(output)
        except Exception as e:
            return e

    def echo(self, text):
        """echo any text"""
        return text

def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)

def main():
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(CalcApi())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()
