import optparse
import sys

import consul

parser = optparse.OptionParser()
parser.add_option('-p', action="store", dest="port", default=8500, help="Define port default=8500")
parser.add_option('-H', action="store", dest="host", help="Define host [REQUIRED]")
parser.add_option('-k', action="store", dest="api_key", help="Set API key")
parser.add_option('--ls', action="store_true", dest="list_services", help="List available services")
parser.add_option('-S', action="store", dest="service", help="Define which services to edit, "
                                                             "comma separated list \n"
                                                             "service1,service2,service3")
parser.add_option('-f', action="store", dest="filter", help="Filter services for tag updates")
parser.add_option('--get-tags', action="store", dest="getTags", help="Get tags for service")
parser.add_option('-T', action="store", dest="tags", type="string", help="Define list of new tags to "
                                                                         "add to service [REQUIRED]")
parser.add_option('-U', action="store_true", default=False, dest="update", help="Update specified service with tag")
parser.add_option('--node-services', action="store_true", default=False, dest="list_node_services",
                  help="Define tag to add to service")
parser.add_option('-n', action="store", dest="node", help="Define node for --node-services")
parser.add_option('--prefix', action="store", dest="prefix", help="The prefix to update a tag with. used with -Rs")
parser.add_option('--Rs', action="store_true", dest="regex", help="Combine the prefix and the service name to create a new"
                                                            "tag. ex. -S test --prefix proxy- -Rs would create a tag"
                                                            "proxy-test.")
parser.add_option('-r', action="store", dest="rm", help="Remove an exact service tag(s) ex: -r TAGNAME or -r TAG1,TAG2")
parser.add_option('-R', action="store", dest="rm_regex", help="Remove a service tag with 'regex' match."
                                                              "ex: -R urlprefix-* ")

(opts, args) = parser.parse_args()

port = opts.port

c = consul.Consul(host=opts.host, port=port,token=opts.api_key)


def get_nodes():
    nodes_dict = c.catalog.nodes()
    nodes_list = []

    # Get all of the Nodes from the nodes_dict
    for i in range(0, len(nodes_dict[1])):
        node = nodes_dict[1][i]['Node']
        nodes_list.append(node)

    return nodes_list


# Get all services on a specific node
def get_node_services(service, node, port=8500, api_key=''):
    node = consul.Consul(host=node, port=port, token=api_key)
    node_services = node.agent.services()

    services_tags = {}
    for k, v in node_services.iteritems():
        services_tags[k] = v['Tags']

    return services_tags


def get_service_node(service):
    services = c.health.service(service)
    return services[1][0]['Node']['Node']


def get_current_tags(service):
    tags = c.catalog.service(service)
    return tags[1][0]['ServiceTags']


def update_tag(service, tag_list, port=8500, api_key=''):
    node = get_service_node(service)
    n = consul.Consul(host=node, port=port, token=api_key)

    try:
        if n.agent.service.register(name=service, tags=tag_list):
            print "Service {0} has been updated with tags {1} on node {2}".format(service, tag_list, node)
        else:
            print "The tag update on service {0} has failed.".format(service)
    except Exception as e:
        print "An error has occurred with the request: {0}".format(e)


def list_services():
    print "Available services: "
    print c.catalog.services()[1]


# Use the tags from -T and combine with current tags
def gen_new_tags(service):
    current_tags = get_current_tags(service)

    tags = opts.tags.split(',')
    for i in range(0, len(tags)):
        current_tags.append(tags[i])

    return current_tags


# Find all services that match the pass string to filter on.
def filtered_update(pattern):
    services = c.catalog.services()
    filtered_services = dict()

    for k, v in services[1].iteritems():
        matches = [s for s in v if pattern in s]
        if matches:
            filtered_services[k] = matches

    return filtered_services


def main():



    if opts.filter and opts.regex:
        if not opts.prefix:
            print "Please define the prefix --prefix"
            sys.exit(1)
        else:
            f_services = filtered_update(opts.filter)

            for k, v in f_services.iteritems():
                ctags = get_current_tags(k)
                ctags.append(opts.prefix + k)
                update_tag(k, ctags)

    if opts.update and (opts.tags and opts.filter):
        f_services = filtered_update(opts.filter)
        new_tags = opts.tags.split(',')
        for k, v in f_services.iteritems():
            tags = get_current_tags(k)
            for i in new_tags:
                tags.append(i)
                update_tag(k, tags)

    elif opts.update and (opts.service and opts.tags):
        services = opts.service.split(',')
        try:
            for i in range(0, len(services)):
                new_tags = gen_new_tags(services[i])
                update_tag(services[i], new_tags, port=opts.port)
        except Exception as e:
            print "Update failed: {0}".format(e)
            sys.exit(1)
    else:
        pass

    if opts.list_services:
        list_services()

    if opts.list_node_services and not opts.node:
        print "Please specify a node to get a list of services"
        sys.exit(1)
    elif opts.list_node_services:
        node_services = get_node_services(opts.node, opts.port)
        print node_services

    if opts.filter and not opts.update:
        f_services = filtered_update(opts.filter)
        print f_services

    # removes a list of tags from a service
    if opts.rm:
        rm_tags = opts.rm.split(',')
        filtered_tags = filtered_update(opts.rm)
        for k, v in filtered_tags.iteritems():
            ctags = set(get_current_tags(k))
            diff = list(ctags.difference(set(rm_tags)))
            update_tag(k, diff)

    # Removes a "regex" matched tag from all services that have a match
    if opts.rm_regex:
        services = filtered_update(opts.rm_regex)
        for k, v in services.iteritems():
            ctags = set(get_current_tags(k))
            diff = list(ctags - set(v))
            update_tag(k, diff)

if __name__ == "__main__":
    main()