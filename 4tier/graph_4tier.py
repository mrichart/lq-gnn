import networkx as nx

def generate_graph(e1nginx_load, nginx_threads, mmc_threads, php_threads, phpio_threads, mongodb_threads, mongoio_threads,
                   nginx_replicas, mmc_replicas, php_replicas, phpio_replicas, mongodb_replicas, mongoio_replicas,
                   nginx_cores, mmc_cores, php_cores, phpio_cores, mongodb_cores, mongoio_cores,
                   e1nginx_avg_latency, e1php_avg_latency, e1mmc_avg_latency, e1phpio_avg_latency, e2phpio_avg_latency,
                   e1mongodb_avg_latency, e1mongoio_avg_latency, e2mongodb_avg_latency, e1nginx_p95_latency, e1php_p95_latency, e1mmc_p95_latency, e1phpio_p95_latency, e2phpio_p95_latency,
                     e1mongodb_p95_latency, e1mongoio_p95_latency, e2mongodb_p95_latency, e1nginx_p99_latency, e1php_p99_latency, e1mmc_p99_latency, e1phpio_p99_latency, e2phpio_p99_latency,
                        e1mongodb_p99_latency, e1mongoio_p99_latency, e2mongodb_p99_latency, deployment, validity, total_avg_latency, total_p95_latency, total_p99_latency):
    
    G = nx.DiGraph(validity=validity, total_avg_latency=total_avg_latency, total_p95_latency=total_p95_latency, total_p99_latency=total_p99_latency, deployment=deployment)

    # Task nodes
    G.add_node("NGINX", entity="task", num_threads=nginx_threads, num_replicas=nginx_replicas, num_cores=nginx_cores)
    G.add_node("PHP", entity="task", num_threads=php_threads, num_replicas=php_replicas, num_cores=php_cores)
    G.add_node("MMC", entity="task", num_threads=mmc_threads, num_replicas=mmc_replicas, num_cores=mmc_cores)
    G.add_node("PHPIO", entity="task", num_threads=phpio_threads, num_replicas=phpio_replicas, num_cores=phpio_cores)
    G.add_node("MONGODB", entity="task", num_threads=mongodb_threads, num_replicas=mongodb_replicas, num_cores=mongodb_cores)
    G.add_node("MONGOIO", entity="task", num_threads=mongoio_threads, num_replicas=mongoio_replicas, num_cores=mongoio_cores)

    # Entry nodes
    G.add_node("E1NGINX", entity="entry", proc_delay=0.087, load=e1nginx_load, avg_latency=e1nginx_avg_latency, p95_latency=e1nginx_p95_latency, p99_latency=e1nginx_p99_latency)
    G.add_node("E1PHP", entity="entry", proc_delay=0.496, load=0, avg_latency=e1php_avg_latency, p95_latency=e1php_p95_latency, p99_latency=e1php_p99_latency)
    G.add_node("E1MMC", entity="entry", proc_delay=0.0186, load=0, avg_latency=e1mmc_avg_latency, p95_latency=e1mmc_p95_latency, p99_latency=e1mmc_p99_latency)
    G.add_node("E1PHPIO", entity="entry", proc_delay=0.003, load=0, avg_latency=e1phpio_avg_latency, p95_latency=e1phpio_p95_latency, p99_latency=e1phpio_p99_latency)
    G.add_node("E2PHPIO", entity="entry", proc_delay=0.001, load=0, avg_latency=e2phpio_avg_latency, p95_latency=e2phpio_p95_latency, p99_latency=e2phpio_p99_latency)
    G.add_node("E1MONGODB", entity="entry", proc_delay=0.0753, load=0, avg_latency=e1mongodb_avg_latency, p95_latency=e1mongodb_p95_latency, p99_latency=e1mongodb_p99_latency)
    G.add_node("E2MONGODB", entity="entry", proc_delay=0.203, load=0, avg_latency=e2mongodb_avg_latency, p95_latency=e2mongodb_p95_latency, p99_latency=e2mongodb_p99_latency)
    G.add_node("E1MONGOIO", entity="entry", proc_delay=5.0, load=0, avg_latency=e1mongoio_avg_latency, p95_latency=e1mongoio_p95_latency, p99_latency=e1mongoio_p99_latency)

    # Edges between tasks and entries (both directions)
    G.add_edge("NGINX", "E1NGINX")
    G.add_edge("E1NGINX", "NGINX")
    G.add_edge("PHP", "E1PHP")
    G.add_edge("E1PHP", "PHP")
    G.add_edge("MMC", "E1MMC")
    G.add_edge("E1MMC", "MMC")
    G.add_edge("PHPIO", "E1PHPIO")
    G.add_edge("E1PHPIO", "PHPIO")
    G.add_edge("PHPIO", "E2PHPIO")
    G.add_edge("E2PHPIO", "PHPIO")
    G.add_edge("MONGODB", "E1MONGODB")
    G.add_edge("E1MONGODB", "MONGODB")
    G.add_edge("MONGODB", "E2MONGODB")
    G.add_edge("E2MONGODB", "MONGODB")
    G.add_edge("MONGOIO", "E1MONGOIO")
    G.add_edge("E1MONGOIO", "MONGOIO")

    # Edges between entries (downstream)
    G.add_edge("E1NGINX", "E1MMC", prob=1, net_delay=0.0, in_out=0)
    G.add_edge("E1PHP", "E1PHPIO", prob=1, net_delay=0.0, in_out=0)
    G.add_edge("E1PHP", "E2PHPIO", prob=1, net_delay=0.0, in_out=0)
    G.add_edge("E2MONGODB", "E1MONGOIO", prob=1, net_delay=0.0, in_out=0)
    if deployment == "edge-cloud":
        G.add_edge("E1NGINX", "E1PHP", prob=0.14, net_delay=35, in_out=0)
        G.add_edge("E1PHP", "E1MMC", prob=1, net_delay=35, in_out=0)
        G.add_edge("E1PHP", "E1MONGODB", prob=0.8572, net_delay=0.0, in_out=0)
        G.add_edge("E1PHP", "E2MONGODB", prob=0.1428, net_delay=0.0, in_out=0)
    elif deployment == "edge-fog-cloud":
        G.add_edge("E1NGINX", "E1PHP", prob=0.14, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MMC", prob=1, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MONGODB", prob=0.8572, net_delay=20, in_out=0)
        G.add_edge("E1PHP", "E2MONGODB", prob=0.1428, net_delay=20, in_out=0)
    elif deployment == "edge-fog":
        G.add_edge("E1NGINX", "E1PHP", prob=0.14, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MMC", prob=1, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MONGODB", prob=0.8572, net_delay=0.0, in_out=0)
        G.add_edge("E1PHP", "E2MONGODB", prob=0.1428, net_delay=0.0, in_out=0)


    #Edges between entries (upstream)
    G.add_edge("E1MMC", "E1NGINX", prob=1, net_delay=0.0, in_out=1) 
    G.add_edge("E1PHPIO", "E1PHP", prob=1, net_delay=0.0, in_out=1)
    G.add_edge("E2PHPIO", "E1PHP", prob=1, net_delay=0.0, in_out=1)
    G.add_edge("E1MONGOIO", "E2MONGODB", prob=1, net_delay=0.0, in_out=1)
    if deployment == "edge-cloud":
        G.add_edge("E1PHP", "E1NGINX", prob=0.14, net_delay=35, in_out=1)
        G.add_edge("E1MMC", "E1PHP", prob=1, net_delay=35, in_out=1)
        G.add_edge("E1MONGODB", "E1PHP", prob=0.8572, net_delay=0.0, in_out=1)
        G.add_edge("E2MONGODB", "E1PHP", prob=0.1428, net_delay=0.0, in_out=1)
    elif deployment == "edge-fog-cloud":
        G.add_edge("E1PHP", "E1NGINX", prob=0.14, net_delay=15, in_out=1)
        G.add_edge("E1MMC", "E1PHP", prob=1, net_delay=15, in_out=1)
        G.add_edge("E1MONGODB", "E1PHP", prob=0.8572, net_delay=20, in_out=1)
        G.add_edge("E2MONGODB", "E1PHP", prob=0.1428, net_delay=0.0, in_out=1)
    elif deployment == "edge-fog":
        G.add_edge("E1PHP", "E1NGINX", prob=0.14, net_delay=15, in_out=1)
        G.add_edge("E1MMC", "E1PHP", prob=1, net_delay=15, in_out=1)
        G.add_edge("E1MONGODB", "E1PHP", prob=0.8572, net_delay=0.0, in_out=1)
        G.add_edge("E2MONGODB", "E1PHP", prob=0.1428, net_delay=0.0, in_out=1)

    return G

def generate_graph_directed(e1nginx_load, nginx_threads, mmc_threads, php_threads, phpio_threads, mongodb_threads, mongoio_threads,
                   nginx_replicas, mmc_replicas, php_replicas, phpio_replicas, mongodb_replicas, mongoio_replicas,
                   nginx_cores, mmc_cores, php_cores, phpio_cores, mongodb_cores, mongoio_cores,
                   e1nginx_latency, e1php_latency, e1mmc_latency, e1phpio_latency, e2phpio_latency,
                   e1mongodb_latency, e1mongoio_latency, e2mongodb_latency, deployment):
    G = nx.DiGraph()

    # Task nodes
    G.add_node("NGINX", entity="task", num_threads=nginx_threads, num_replicas=nginx_replicas, num_cores=nginx_cores)
    G.add_node("PHP", entity="task", num_threads=php_threads, num_replicas=php_replicas, num_cores=php_cores)
    G.add_node("MMC", entity="task", num_threads=mmc_threads, num_replicas=mmc_replicas, num_cores=mmc_cores)
    G.add_node("PHPIO", entity="task", num_threads=phpio_threads, num_replicas=phpio_replicas, num_cores=phpio_cores)
    G.add_node("MONGODB", entity="task", num_threads=mongodb_threads, num_replicas=mongodb_replicas, num_cores=mongodb_cores)
    G.add_node("MONGOIO", entity="task", num_threads=mongoio_threads, num_replicas=mongoio_replicas, num_cores=mongoio_cores)

    # Entry nodes
    G.add_node("E1NGINX", entity="entry", proc_delay=0.087, load=e1nginx_load, latency=e1nginx_latency)
    G.add_node("E1PHP", entity="entry", proc_delay=0.496, load=0, latency=e1php_latency)
    G.add_node("E1MMC", entity="entry", proc_delay=0.0186, load=0, latency=e1mmc_latency)
    G.add_node("E1PHPIO", entity="entry", proc_delay=0.003, load=0, latency=e1phpio_latency)
    G.add_node("E2PHPIO", entity="entry", proc_delay=0.001, load=0, latency=e2phpio_latency)
    G.add_node("E1MONGODB", entity="entry", proc_delay=0.0753, load=0, latency=e1mongodb_latency)
    G.add_node("E2MONGODB", entity="entry", proc_delay=0.203, load=0, latency=e2mongodb_latency)
    G.add_node("E1MONGOIO", entity="entry", proc_delay=5.0, load=0, latency=e1mongoio_latency)

    # Edges between tasks and entries (both directions)
    G.add_edge("NGINX", "E1NGINX")
    G.add_edge("E1NGINX", "NGINX")
    G.add_edge("PHP", "E1PHP")
    G.add_edge("E1PHP", "PHP")
    G.add_edge("MMC", "E1MMC")
    G.add_edge("E1MMC", "MMC")
    G.add_edge("PHPIO", "E1PHPIO")
    G.add_edge("E1PHPIO", "PHPIO")
    G.add_edge("PHPIO", "E2PHPIO")
    G.add_edge("E2PHPIO", "PHPIO")
    G.add_edge("MONGODB", "E1MONGODB")
    G.add_edge("E1MONGODB", "MONGODB")
    G.add_edge("MONGODB", "E2MONGODB")
    G.add_edge("E2MONGODB", "MONGODB")
    G.add_edge("MONGOIO", "E1MONGOIO")
    G.add_edge("E1MONGOIO", "MONGOIO")

    # Edges between entries (downstream)
    G.add_edge("E1NGINX", "E1MMC", prob=1, net_delay=0.0, in_out=0)
    G.add_edge("E1PHP", "E1PHPIO", prob=1, net_delay=0.0, in_out=0)
    G.add_edge("E1PHP", "E2PHPIO", prob=1, net_delay=0.0, in_out=0)
    G.add_edge("E2MONGODB", "E1MONGOIO", prob=1, net_delay=0.0, in_out=0)
    if deployment == "edge-cloud":
        G.add_edge("E1NGINX", "E1PHP", prob=0.14, net_delay=35, in_out=0)
        G.add_edge("E1PHP", "E1MMC", prob=1, net_delay=35, in_out=0)
        G.add_edge("E1PHP", "E1MONGODB", prob=0.8572, net_delay=0.0, in_out=0)
        G.add_edge("E1PHP", "E2MONGODB", prob=0.1428, net_delay=0.0, in_out=0)
    elif deployment == "edge-fog-cloud":
        G.add_edge("E1NGINX", "E1PHP", prob=0.14, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MMC", prob=1, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MONGODB", prob=0.8572, net_delay=20, in_out=0)
        G.add_edge("E1PHP", "E2MONGODB", prob=0.1428, net_delay=20, in_out=0)
    elif deployment == "edge-fog":
        G.add_edge("E1NGINX", "E1PHP", prob=0.14, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MMC", prob=1, net_delay=15, in_out=0)
        G.add_edge("E1PHP", "E1MONGODB", prob=0.8572, net_delay=0.0, in_out=0)
        G.add_edge("E1PHP", "E2MONGODB", prob=0.1428, net_delay=0.0, in_out=0)

    return G