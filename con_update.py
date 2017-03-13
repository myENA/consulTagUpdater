import optparse
import sys

from consulUpdate import *

parser = optparse.OptionParser()
parser.add_option('--ls', action="store_true", dest="list_services", help="List available services")
parser.add_option('-S', action="store", dest="service", help="Define which services to edit, "
                                                             "comma separated list \n"
                                                             "service1,service2,service3 [REQUIRED]")

parser.add_option('--get-tags', action="store", dest="getTags", help="Get tags for service")
parser.add_option('-T', action="store", dest="tags", type="string", help="Define list of new tags to "
                                                                         "add to service [REQUIRED]")
parser.add_option('-U', action="store_true", default=False, dest="update", help="Update specified service with tag")
parser.add_option('--node-services', action="store_true", default=False, dest="list_node_services",
                  help="Define tag to add to service")
parser.add_option('-n', action="store", dest="node", help="Define node for --node-services")
parser.add_option('-p', action="store", dest="port", default=8500, help="Define port default=8500")
parser.add_option('-H', action="store", dest="host", help="Define host default=127.0.0.1")

(opts, args) = parser.parse_args()

if not opts.host:
    print "Please set the host flag (-H)"
    sys.exit()
else:
    host = opts.host

port = opts.port

c = consul.Consul(host=host, port=port)


if opts.update and (not opts.service or not opts.tags):
    print "Please define the service or service list with the -S flag and/or the tags to add with -T"
    sys.exit()
elif opts.update and opts.service and opts.tags:
    services = opts.service.split(',')
    try:
        for i in range(0, len(services)):

            new_tags = gen_new_tags(c, services[i], opts.tags)
            update_tag(c, services[i], new_tags, port=opts.port)

    except Exception as e:
        print "Update failed: {0}".format(e)
        sys.exit()
else:
    pass

if opts.list_services:
    list_services(c)

if opts.list_node_services and not opts.node:
    print "Please specify a node to get a list of services"
    sys.exit()
elif opts.list_node_services:
    node_services = get_node_services(opts.node, opts.port)
    print node_services