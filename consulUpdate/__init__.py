import consul

c = consul.Consul(port=8500)


def get_nodes():
    nodes_dict = c.catalog.nodes()
    nodes_list = []

    # Get all of the Nodes from the nodes_dict
    for i in range(0, len(nodes_dict[1])):
        node = nodes_dict[1][i]['Node']
        nodes_list.append(node)

    return nodes_list


# Get all services on a specific node
def get_node_services(node, port=8500):
    node = consul.Consul(host=node, port=port)
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


def update_tag(node, service, tag_list, port=8500):
    n = consul.Consul(host=node, port=port)

    try:
        if n.agent.service.register(name=service, tags=tag_list):
            print
            "Service {0} has been updated with tags {1} on node {2}".format(service, tag_list, node)
        else:
            print
            "The tag update on service {0} has failed.".format(service)
    except Exception as e:
        print
        "An error has occurred with the request: {0}".format(e)


def list_services():
    print
    "Available services: "
    for k in c.agent.services().iteritems():
        print
        k[0]


def gen_new_tags(service, tags):
    current_tags = get_current_tags(service)

    new_tags = tags.split(',')
    for i in range(0, len(new_tags)):
        current_tags.append(new_tags[i])

    return current_tags
