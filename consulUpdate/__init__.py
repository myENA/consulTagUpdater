import consul


def get_nodes(session):
    nodes_dict = session.catalog.nodes()
    nodes_list = []

    # Get all of the Nodes from the nodes_dict
    for i in range(0, len(nodes_dict[1])):
        node = nodes_dict[1][i]['Node']
        nodes_list.append(node)

    return nodes_list


# Get all services on a specific node
def get_node_services(node, port=8500, api_key=''):
    node = consul.Consul(host=node, port=port, token=api_key)
    node_services = node.agent.services()

    services_tags = {}
    for k, v in node_services.iteritems():
        services_tags[k] = v['Tags']

    return services_tags


def get_service_node(session, service):
    services = session.health.service(service)
    return services[1][0]['Node']['Node']


def get_current_tags(session, service):
    tags = session.catalog.service(service)
    return tags[1][0]['ServiceTags']


def update_tag(session, service, tag_list, port=8500, api_key=''):
    node = get_service_node(session, service)
    n = consul.Consul(host=node, port=port, token=api_key)

    try:
        if n.agent.service.register(name=service, tags=tag_list):
            print "Service {0} has been updated with tags {1} on node {2}".format(service, tag_list, node)
        else:
            print "The tag update on service {0} has failed.".format(service)
    except Exception as e:
        print "An error has occurred with the request: {0}".format(e)


def list_services(session):
    print "Available services: "
    for k in session.agent.services().iteritems():
        print k[0]


def gen_new_tags(session, service, tags):
    current_tags = get_current_tags(session, service)

    new_tags = tags.split(',')
    for i in range(0, len(new_tags)):
        current_tags.append(new_tags[i])

    return current_tags
