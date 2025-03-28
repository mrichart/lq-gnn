import networkx as nx
import json
import numpy as np
from pathlib import Path

def get_microservice_names(input_graph_dir):
    with open(Path(input_graph_dir) / "graph.json") as f:
        json_data = json.load(f)
        microservices = json_data["microservices"]
        service_names = [microservice["service_name"] for microservice in microservices]
        return service_names

def get_request_paths(input_graph_dir):
    with open(Path(input_graph_dir) / "path.json") as f:
        json_data = json.load(f)
        return json_data
    
def get_path_ids(input_graph_dir, service_name):
    file = input_graph_dir / "microservice" / f"{service_name}.json"
    with open(file) as f:
        json_data = json.load(f)
        paths = json_data["paths"]
        path_ids = [path["code_path_id"] for path in paths]
        return path_ids

def get_stage_names(input_graph_dir, service_name, path_id):  
    file = input_graph_dir / "microservice" / f"{service_name}.json"
    with open(file) as f:
        json_data = json.load(f)
        paths = json_data["paths"]
        for path in paths:
            if path["code_path_id"] == path_id:
                stages = path["stages"]
                stage_names = [stage["stage_name"] for stage in stages]
                return stage_names
            
def get_stage_ids(input_graph_dir, service_name, path_id):  
    file = input_graph_dir / "microservice" / f"{service_name}.json"
    with open(file) as f:
        json_data = json.load(f)
        paths = json_data["paths"]
        for path in paths:
            if path["code_path_id"] == path_id:
                stages = path["stages"]
                stage_ids = [stage["path_stage_id"] for stage in stages]
                return stage_ids
        
#returns proc delay of a stage in microseconds
def get_stage_proc_delay(input_graph_dir, service_name, path_id, stage_id):
    file = input_graph_dir / "microservice" / f"{service_name}.json"
    #print ("service_name: ", service_name)
    #print ("path_id: ", path_id)
    #print ("stage_id: ", stage_id)
    with open(file) as f:
        json_data = json.load(f)
        paths = json_data["paths"]
        for path in paths:
            if path["code_path_id"] == path_id:
                stages = path["stages"]
                for st in stages:
                    if st["path_stage_id"] == stage_id:
                        return (st["recv_time_model"]["latency"])

def get_stage_is_blocking(input_graph_dir, service_name, path_id, stage_id):
    file = input_graph_dir / "microservice" / f"{service_name}.json"
    #print ("service_name: ", service_name)
    #print ("path_id: ", path_id)
    #print ("stage_id: ", stage_id)
    with open(file) as f:
        json_data = json.load(f)
        paths = json_data["paths"]
        for path in paths:
            if path["code_path_id"] == path_id:
                stages = path["stages"]
                for st in stages:
                    if st["path_stage_id"] == stage_id:
                        return 1 if st["blocking"] else 0

def get_map_services_machines(input_graph_dir):
    file = input_graph_dir / "graph.json"
    with open(file) as f:
        json_data = json.load(f)
        microservices = json_data["microservices"]
        map_services_machines = {}
        for microservice in microservices:
            service_name = microservice["service_name"]
            machine = microservice["machine_id"]
            map_services_machines[service_name] = machine
        return map_services_machines
    
def get_machine_links_latencies(input_graph_dir):
    file = input_graph_dir / "machines.json"
    with open(file) as f:
        json_data = json.load(f)
        machines = json_data["machines"]
        num_machines = len(machines)
        machine_links_latencies = np.inf * np.ones((num_machines, num_machines))
        links = json_data["links"]
        for link in links:
            machine1 = link["machine_id_1"]
            machine2 = link["machine_id_2"]
            latency = link["latency"]
            machine_links_latencies[machine1][machine2] = latency
            machine_links_latencies[machine2][machine1] = latency
        return machine_links_latencies

def get_latency_between_services(input_graph_dir, service1, service2, machine_latencies):
    map_services_machines = get_map_services_machines(input_graph_dir)
    #machine_links_latencies = get_machine_links_latencies(input_graph_dir)
    machine1 = map_services_machines[service1]
    machine2 = map_services_machines[service2]
    #return machine_links_latencies[machine1][machine2]        TODO    
    return machine_latencies[machine1][machine2]
    
def generate_graph(input_graph_dir, load, threads, replicas, cores, machine_latencies, avg_rt, p95_rt, p99_rt, deployment, valid, total_avg_rt, total_p95_rt, total_p99_rt, micro_cpu, micro_requests, micro_avg_rt, micro_p95_rt, micro_p99_rt):
    
    G = nx.DiGraph(valid=valid, total_avg_rt=total_avg_rt, total_p95_rt=total_p95_rt, total_p99_rt=total_p99_rt, deployment=deployment)

    # Task nodes
    service_names = get_microservice_names(input_graph_dir)
    for service in service_names:
        G.add_node(service, entity="task", num_threads=threads[service], num_replicas=replicas[service], num_cores=cores[service], cpu_util=micro_cpu[service], num_requests=micro_requests[service], ms_avg_rt=micro_avg_rt[service], ms_p95_rt=micro_p95_rt[service], ms_p99_rt=micro_p99_rt[service])
        
        # paths = get_path_ids(input_graph_dir, service)
        # for path_id in paths:
        #     # Entry nodes
        #     entry = service + '_' + str(path_id)
        #     G.add_node(entry, entity="entry")
        #     # Edges between tasks and entries (both directions)
        #     G.add_edge(service, entry)
        #     G.add_edge(entry, service)

    # Path nodes
    request_paths = get_request_paths(input_graph_dir)
    for path in request_paths:
        path_id = path["micro_service_path_id"]
        # print ("parsing path_id: ", path_id, avg_rt, p95_rt, p99_rt)
        path_prob = path["probability"]
        G.add_node(str(path_id), entity="path", load=path_prob*load/100, avg_rt=avg_rt[path_id], p95_rt=p95_rt[path_id], p99_rt=p99_rt[path_id])
        nodes = path["nodes"]
        nodeid_to_servicename = {}
        for node in nodes:
            service = node["service_name"]
            nodeid = node["node_id"]
            nodeid_to_servicename[nodeid] = service
        i = 0
        prev_activity = None
        for node in nodes:
            service = node["service_name"]
            #print ("parsing service: ", service)
            if service == "client":
                continue
            ms_path_id = node["code_path"]
            start_stage = node["start_stage"]
            end_stage = node["end_stage"]
            stage_ids = get_stage_ids(input_graph_dir, service, ms_path_id)
            proc_delay = 0
            end_stage = end_stage if end_stage != -1 else stage_ids[-1]
            for st in range(start_stage, end_stage+1):
                proc_delay += get_stage_proc_delay(input_graph_dir, service, ms_path_id, st)
            #entry = service + '_' + str(ms_path_id)
            activity = service + '_' + str(ms_path_id) + '_' + str(start_stage) + '_' + str(path_id)
            if G.has_node(activity):
                activity = activity + '_' + str(i)

            # create node with proc delay in nanoseconds
            G.add_node(activity, entity="activity", proc_delay=proc_delay/1000, blocking=get_stage_is_blocking(input_graph_dir, service, ms_path_id, start_stage))
            G.add_edge(service, activity)
            G.add_edge(activity, service)
            if prev_activity is not None:
                G.add_edge(prev_activity, activity, in_out=0)
                G.add_edge(activity, prev_activity, in_out=1)
            prev_activity = activity
            #G.add_edge(activity, entry)
            G.add_edge(activity, str(path_id))
            G.add_edge(str(path_id), activity, label=str(i))
            i += 1


            childs = node["childs"]
            for child in childs:
                child_service = nodeid_to_servicename[child]
                if child_service == "client" or get_latency_between_services(input_graph_dir, service, child_service, machine_latencies) == np.inf or get_latency_between_services(input_graph_dir, service, child_service, machine_latencies) == 0:
                    continue
                network_activity = activity + '_' + service + '_' + child_service
                G.add_node(network_activity, entity="activity", proc_delay=get_latency_between_services(input_graph_dir, service, child_service, machine_latencies), blocking=0)
                if prev_activity is not None:
                    G.add_edge(prev_activity, network_activity, in_out=0)
                    G.add_edge(network_activity, prev_activity, in_out=1)
                prev_activity = activity
                G.add_edge(str(path_id), network_activity)
                G.add_edge(network_activity, str(path_id))
    return G