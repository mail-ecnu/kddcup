# -*- coding: utf-8 -*-
# @File: agent.py
# @Author: Xiaocheng Tang
# @Date:   2020-03-17 17:03:34


class Agent(object):
  """ Agent for dispatching and reposition """

  def __init__(self):
    """ Load your trained model and initialize the parameters """
    pass

  def dispatch(self, dispatch_observ):
    """ Compute the assignment between drivers and passengers at each time step
    :param dispatch_observ: a list of dict, the key in the dict includes:
        order_id, int
        driver_id, int
        order_driver_distance, float
        order_start_location, a list as [lng, lat], float
        order_finish_location, a list as [lng, lat], float
        driver_location, a list as [lng, lat], float
        timestamp, int
        order_finish_timestamp, int
        day_of_week, int
        reward_units, float
        pick_up_eta, float

    :return: a list of dict, the key in the dict includes:
        order_id and driver_id, the pair indicating the assignment
    """

    """
    dispatch_observ.sort(key=lambda od_info: od_info['reward_units'], reverse=True)
    assigned_order = set()
    assigned_driver = set()
    dispatch_action = []
    for od in dispatch_observ:
      # make sure each order is assigned to one driver, and each driver is assigned with one order
      if (od["order_id"] in assigned_order) or (od["driver_id"] in assigned_driver):
        continue
      assigned_order.add(od["order_id"])
      assigned_driver.add(od["driver_id"])
      dispatch_action.append(dict(order_id=od["order_id"], driver_id=od["driver_id"]))
    return dispatch_action
    """

    id_order = list({}.fromkeys(od['order_id'] for od in dispatch_observ).keys())
    id_driver = list({}.fromkeys(od['driver_id'] for od in dispatch_observ).keys())
    order_id = dict((order, idx) for idx, order in enumerate(id_order))
    driver_id = dict((driver, idx) for idx, driver in enumerate(id_driver))
    N = len(order_id)
    M = len(driver_id)

    import networkx as nx
    G = nx.complete_bipartite_graph(N, M)
    for od in dispatch_observ:
      order = order_id[od['order_id']]
      driver = N + driver_id[od['driver_id']]
      G.edges[order, driver]['weight'] = -od['reward_units']

    from networkx.algorithms.bipartite.matching import minimum_weight_full_matching
    match = minimum_weight_full_matching(G)

    dispatch_action = []
    for idx, order in enumerate(id_order):
      dispatch_action.append({'driver_id': id_driver[match[idx] - N], 'order_id': order})
    return dispatch_action

  def reposition(self, repo_observ):
    """ Compute the reposition action for the given drivers
    :param repo_observ: a dict, the key in the dict includes:
        timestamp: int
        driver_info: a list of dict, the key in the dict includes:
            driver_id: driver_id of the idle driver in the treatment group, int
            grid_id: id of the grid the driver is located at, str
        day_of_week: int

    :return: a list of dict, the key in the dict includes:
        driver_id: corresponding to the driver_id in the od_list
        destination: id of the grid the driver is repositioned to, str
    """
    repo_action = []
    for driver in repo_observ['driver_info']:
      # the default reposition is to let drivers stay where they are
      repo_action.append({'driver_id': driver['driver_id'], 'destination': driver['grid_id']})
    return repo_action
