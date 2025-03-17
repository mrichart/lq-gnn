import argparse
from pathlib import Path
import json
import numpy as np
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(description="Run LQN and compare against simulator.")
    parser.add_argument("--input_dir", type=Path, default=Path("train"), help="Directory containing the dataset.")
    parser.add_argument("--debug", action="store_true", help="Print debug information.")
    return parser.parse_args()

def read_compare(input_dir, debug=False):
    # Load the JSON data
    with open(input_dir / "data.json", "r") as f:
        dataset = json.load(f)

    print("Dataset loaded.")
    print("Dataset length: ", len(dataset))

    total_avg_rt = []
    total_p95_rt = []
    total_p99_rt = []
    
    threads = {}
    cores = {}
    replicas = {}
    cpu_util = {}
    num_requests = {}
    ms_avg_rt = {}
    ms_p95_rt = {}
    ms_p99_rt = {}
    data = dataset[0]
    for node in data['nodes']:
        if node['entity'] == 'task':
            ms_avg_rt[node['id']] = []
            ms_p95_rt[node['id']] = []
            ms_p99_rt[node['id']] = []

    lqn_th = []
    lqn_rt = []
    lqn_ngx_rt = []
    lqn_ht_rt = []
    lqn_ht_redis_rt = []
    lqn_ps_rt = []
    lqn_mmc_rt = []
    lqn_mdb_rt = []
    lqn_mdb_io_rt = []

    fog_cloud_latency = 0
    edge_fog_latency = 0

    mape = 0
    mae = 0
    rmse = 0

    i=0
    fail = 0

    # Extract the values
    for data in dataset:
        # Consider only the first 100 data points (for testing faster)
        #i+=1
        #if i>10:
        #    break
        
        deployment = data['graph']['deployment']
        # Extract the configuration values of the scenario
        load = 0
        edge_fog_latency = 0
        fog_cloud_latency = 0
        for node in data['nodes']:
            if node['entity'] == 'task':
                threads[node['id']] = node['num_threads']
                cores[node['id']] = node['num_cores']
                replicas[node['id']] = node['num_replicas']
                cpu_util[node['id']] = node['cpu_util']
                num_requests[node['id']] = node['num_requests']
            elif node['entity'] == 'path':
                load += node['load']
            elif node['entity'] == 'activity' and 'home_timeline_post_storage' in node['id']:
                edge_fog_latency = node['proc_delay']
                if debug:
                    print(node['id'])
                    print(deployment)
                    print(node['proc_delay'])
            elif node['entity'] == 'activity' and 'post_storage_post_storage_mongodb' in node['id']:
                fog_cloud_latency = node['proc_delay']
                if debug:
                    print(node['id'])
                    print(deployment)
                    print(node['proc_delay'])
        
        # Execute the LQN model
        # Create and write to a file
        with open("input.txt", "w") as f:
            f.write("0 " + str(int(load)) + "\n" 
                #+ "1 " + str(threads['nginx']) + "\n"
                #+ "2 " + str(threads['home_timeline']) + "\n"
                + "3 " + str(threads['home_timeline_redis']) + "\n"
                + "4 " + str(threads['post_storage']) + "\n"
                + "5 " + str(threads['post_storage_memcached']) + "\n"
                + "6 " + str(threads['post_storage_mongodb']) + "\n"
                + "7 " + str(threads['mongo_io']) + "\n"
                + "8 " + str(cores['nginx']) + "\n"
                + "9 " + str(cores['home_timeline']) + "\n"
                + "10 " + str(cores['home_timeline_redis']) + "\n"
                + "11 " + str(cores['post_storage']) + "\n"
                + "12 " + str(cores['post_storage_memcached']) + "\n"
                + "13 " + str(cores['post_storage_mongodb']) + "\n"
                + "14 " + str(cores['mongo_io']) + "\n"
                + "15 " + str(fog_cloud_latency/1000000) + "\n"
                + "16 " + str(edge_fog_latency/1000000) + "\n"
                + "-1 0")

        if debug:
            print("Load: ", load)
            print("nginx: ", threads['nginx'], " - ", cores['nginx'])
            print("home_timeline: ", threads['home_timeline'], " - ", cores['home_timeline'])
            print("home_timeline_redis: ", threads['home_timeline_redis'], " - ", cores['home_timeline_redis'])
            print("post_storage: ", threads['post_storage'], " - ", cores['post_storage'])
            print("post_storage_memcached: ", threads['post_storage_memcached'], " - ", cores['post_storage_memcached'])
            print("post_storage_mongodb: ", threads['post_storage_mongodb'], " - ", cores['post_storage_mongodb'])
            print("mongo_io: ", threads['mongo_io'], " - ", cores['mongo_io'])
            print("Fog-Cloud Latency: ", fog_cloud_latency)
            print("Edge-Fog Latency: ", edge_fog_latency)

        # Run the LQN model
        output = subprocess.run(["lqns", "-w", "../../../lqn-models/social-net-ht/social-net-ht-params.lqnx"], capture_output=True, text=True)
        output_array = output.stdout.splitlines()

        # Extract the LQN metrics
        lqn_metrics = output_array[-1].split(",")
        if debug:
            print("LQN Metrics: ", lqn_metrics)

        # If the throughput is less than 98% of the load, consider it as a failure
        if float(lqn_metrics[0])/load <= 0.98:
            fail += 1
            continue

        # Save the LQN metrics
        lqn_th.append(float(lqn_metrics[0]))
        lqn_rt.append(float(lqn_metrics[1]))
        lqn_ngx_rt.append(float(lqn_metrics[2]))
        lqn_ht_rt.append(float(lqn_metrics[3]))
        lqn_ht_redis_rt.append(float(lqn_metrics[4]))
        lqn_ps_rt.append(float(lqn_metrics[5]))
        lqn_mmc_rt.append(float(lqn_metrics[6]))
        lqn_mdb_rt.append(float(lqn_metrics[7]))
        lqn_mdb_io_rt.append(float(lqn_metrics[8]))

        # Extract the simulator metrics
        total_avg_rt.append(data['graph']['total_avg_rt']/1000)
        total_p95_rt.append(data['graph']['total_p95_rt']/1000)
        total_p99_rt.append(data['graph']['total_p99_rt']/1000)
        for node in data['nodes']:
            if node['entity'] == 'task':
                ms_avg_rt[node['id']].append(node['ms_avg_rt']/1000)
                ms_p95_rt[node['id']].append(node['ms_p95_rt']/1000)
                ms_p99_rt[node['id']].append(node['ms_p99_rt']/1000)

        if debug:
            print(data['graph']['total_avg_rt']/1000, " ", data['graph']['total_p95_rt']/1000, " ", data['graph']['total_p99_rt']/1000)
            print("\n")
            for node in data['nodes']:
                if node['entity'] == 'task':
                    print(node['ms_avg_rt']/1000, " ", node['ms_p95_rt']/1000, " ", node['ms_p99_rt']/1000)

    print("Fail: ", fail)
    print("\n")

    # Calculate the MAPE, MAE, and RMSE
    mape = np.mean(np.abs(np.subtract(total_avg_rt, lqn_rt)) / total_avg_rt) * 100
    mae = np.mean(np.abs(np.subtract(total_avg_rt, lqn_rt)))
    rmse = np.sqrt(np.mean(np.square(np.subtract(lqn_rt, total_avg_rt))))
    msle = np.mean(np.square(np.log(np.add(total_avg_rt, 1)) - np.log(np.add(lqn_rt, 1))))

    print("Total MAPE: ", mape)
    print("Total MAE: ", mae)
    print("Total RMSE: ", rmse)
    print("Total MSLE: ", msle)
    print("\n")

    #Calculate the MAPE, MAE, and RMSE for each component
    mape_ngx = np.mean(np.abs(np.subtract(ms_avg_rt['nginx'], lqn_ngx_rt)) / ms_avg_rt['nginx']) * 100
    mae_ngx = np.mean(np.abs(np.subtract(ms_avg_rt['nginx'], lqn_ngx_rt)))
    rmse_ngx = np.sqrt(np.mean(np.square(np.subtract(lqn_ngx_rt, ms_avg_rt['nginx']))))
    msle_ngx = np.mean(np.square(np.log(np.add(ms_avg_rt['nginx'], 1)) - np.log(np.add(lqn_ngx_rt, 1))))
    
    mape_ht = np.mean(np.abs(np.subtract(ms_avg_rt['home_timeline'], lqn_ht_rt)) / ms_avg_rt['home_timeline']) * 100
    mae_ht = np.mean(np.abs(np.subtract(ms_avg_rt['home_timeline'], lqn_ht_rt)))
    rmse_ht = np.sqrt(np.mean(np.square(np.subtract(lqn_ht_rt, ms_avg_rt['home_timeline']))))
    msle_ht = np.mean(np.square(np.log(np.add(ms_avg_rt['home_timeline'], 1)) - np.log(np.add(lqn_ht_rt, 1))))
    
    mape_ht_redis = np.mean(np.abs(np.subtract(ms_avg_rt['home_timeline_redis'], lqn_ht_redis_rt)) / ms_avg_rt['home_timeline_redis']) * 100
    mae_ht_redis = np.mean(np.abs(np.subtract(ms_avg_rt['home_timeline_redis'], lqn_ht_redis_rt)))
    rmse_ht_redis = np.sqrt(np.mean(np.square(np.subtract(lqn_ht_redis_rt, ms_avg_rt['home_timeline_redis']))))
    msle_ht_redis = np.mean(np.square(np.log(np.add(ms_avg_rt['home_timeline_redis'], 1)) - np.log(np.add(lqn_ht_redis_rt, 1))))
    
    mape_ps = np.mean(np.abs(np.subtract(ms_avg_rt['post_storage'], lqn_ps_rt)) / ms_avg_rt['post_storage']) * 100
    mae_ps = np.mean(np.abs(np.subtract(ms_avg_rt['post_storage'], lqn_ps_rt)))
    rmse_ps = np.sqrt(np.mean(np.square(np.subtract(lqn_ps_rt, ms_avg_rt['post_storage']))))
    msle_ps = np.mean(np.square(np.log(np.add(ms_avg_rt['post_storage'], 1)) - np.log(np.add(lqn_ps_rt, 1))))

    mape_mmc = np.mean(np.abs(np.subtract(ms_avg_rt['post_storage_memcached'], lqn_mmc_rt)) / ms_avg_rt['post_storage_memcached']) * 100
    mae_mmc = np.mean(np.abs(np.subtract(ms_avg_rt['post_storage_memcached'], lqn_mmc_rt)))
    rmse_mmc = np.sqrt(np.mean(np.square(np.subtract(lqn_mmc_rt, ms_avg_rt['post_storage_memcached']))))
    msle_mmc = np.mean(np.square(np.log(np.add(ms_avg_rt['post_storage_memcached'], 1)) - np.log(np.add(lqn_mmc_rt, 1))))
    
    mape_mdb = np.mean(np.abs(np.subtract(ms_avg_rt['post_storage_mongodb'], lqn_mdb_rt)) / ms_avg_rt['post_storage_mongodb']) * 100
    mae_mdb = np.mean(np.abs(np.subtract(ms_avg_rt['post_storage_mongodb'], lqn_mdb_rt)))
    rmse_mdb = np.sqrt(np.mean(np.square(np.subtract(lqn_mdb_rt, ms_avg_rt['post_storage_mongodb']))))
    msle_mdb = np.mean(np.square(np.log(np.add(ms_avg_rt['post_storage_mongodb'], 1)) - np.log(np.add(lqn_mdb_rt, 1))))
    
    mape_mdb_io = np.mean(np.abs(np.subtract(ms_avg_rt['mongo_io'], lqn_mdb_io_rt)) / ms_avg_rt['mongo_io']) * 100
    mae_mdb_io = np.mean(np.abs(np.subtract(ms_avg_rt['mongo_io'], lqn_mdb_io_rt)))
    rmse_mdb_io = np.sqrt(np.mean(np.square(np.subtract(lqn_mdb_io_rt, ms_avg_rt['mongo_io']))))
    msle_mdb_io = np.mean(np.square(np.log(np.add(ms_avg_rt['mongo_io'], 1)) - np.log(np.add(lqn_mdb_io_rt, 1))))

    #Calculate the mean of the MAPE, MAE, and RMSE for each component
    mean_mape = (mape_ngx + mape_ht + mape_ht_redis + mape_ps + mape_mmc + mape_mdb + mape_mdb_io) / 6
    mean_mae = (mae_ngx + mae_ht + mae_ht_redis + mae_ps + mae_mmc + mae_mdb + mae_mdb_io) / 6
    mean_rmse = (rmse_ngx + rmse_ht + rmse_ht_redis + rmse_ps + rmse_mmc + rmse_mdb + rmse_mdb_io) / 6
    mean_msle = (msle_ngx + msle_ht + msle_ht_redis + msle_ps + msle_mmc + msle_mdb + msle_mdb_io) / 6

    print("MS MAPE: ", mean_mape)
    print("MS MAE: ", mean_mae)
    print("MS RMSE: ", mean_rmse)
    print("MS MSLE: ", mean_msle)

if __name__ == "__main__":
    args = parse_args()
    read_compare(args.input_dir, args.debug)
