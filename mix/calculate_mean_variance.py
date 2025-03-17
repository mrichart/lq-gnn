import argparse
from pathlib import Path
import json
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate mean and variance of the dataset.")
    parser.add_argument("--input_dir", type=Path, default=Path("train"), help="Directory containing the dataset.")
    return parser.parse_args()

def calculate_print(input_dir):
    # Load the JSON data
    with open(input_dir / "data.json", "r") as f:
        dataset = json.load(f)

    num_threads = []
    num_cores = []
    proc_delay = []
    load = []
    avg_rt = []
    p95_rt = []
    p99_rt = []
    total_avg_rt = []
    total_p95_rt = []
    total_p99_rt = []
    ms_avg_rt = []
    ms_p95_rt = []
    ms_p99_rt = []

    # Extract the values
    for data in dataset:
        num_threads.extend([node['num_threads'] for node in data['nodes'] if node['entity'] == 'task'])
        num_cores.extend([node['num_cores'] for node in data ['nodes'] if node['entity'] == 'task'])        
        proc_delay.extend([node['proc_delay'] for node in data['nodes'] if node['entity'] == 'activity'])
        load.extend([node['load'] for node in data['nodes'] if 'load' in node])
        avg_rt.extend([node['avg_rt'] for node in data['nodes'] if node['entity'] == 'path'])
        p95_rt.extend([node['p95_rt'] for node in data['nodes'] if node['entity'] == 'path'])
        p99_rt.extend([node['p99_rt'] for node in data['nodes'] if node['entity'] == 'path'])
        ms_avg_rt.extend([node['ms_avg_rt'] for node in data['nodes'] if node['entity'] == 'task'])
        ms_p95_rt.extend([node['ms_p95_rt'] for node in data['nodes'] if node['entity'] == 'task'])
        ms_p99_rt.extend([node['ms_p99_rt'] for node in data['nodes'] if node['entity'] == 'task'])
        total_avg_rt.append(data['graph']['total_avg_rt'])
        total_p95_rt.append(data['graph']['total_p95_rt'])
        total_p99_rt.append(data['graph']['total_p99_rt'])



    # Calculate the mean and variance
    num_threads_mean = np.mean(num_threads)
    num_threads_var = np.var(num_threads)
    num_threads_std = np.std(num_threads)
    num_threads_max = np.max(num_threads)
    num_threads_min = np.min(num_threads)
    num_threds_hist = np.histogram(num_threads, bins=100)

    num_cores_mean = np.mean(num_cores)
    num_cores_var = np.var(num_cores)
    num_cores_std = np.std(num_cores)
    num_cores_max = np.max(num_cores)
    num_cores_min = np.min(num_cores)
    num_cores_hist = np.histogram(num_cores, bins=100)

    proc_delay_mean = np.mean(proc_delay)
    proc_delay_var = np.var(proc_delay)
    proc_delay_std = np.std(proc_delay)
    proc_delay_max = np.max(proc_delay)
    proc_delay_min = np.min(proc_delay)
    proc_delay_hist = np.histogram(proc_delay, bins=100)

    load_mean = np.mean(load)
    load_var = np.var(load)
    load_std = np.std(load)
    load_max = np.max(load)
    load_min = np.min(load)
    load_hist = np.histogram(load, bins=100)

    avg_rt_mean = np.mean(avg_rt)
    avg_rt_var = np.var(avg_rt)
    avg_rt_std = np.std(avg_rt)
    avg_rt_max = np.max(avg_rt)
    avg_rt_min = np.min(avg_rt)
    avg_rt_hist = np.histogram(avg_rt, bins=100)

    p95_rt_mean = np.mean(p95_rt)
    p95_rt_var = np.var(p95_rt)
    p95_rt_std = np.std(p95_rt)
    p95_rt_max = np.max(p95_rt)
    p95_rt_min = np.min(p95_rt)
    p95_rt_hist = np.histogram(p95_rt, bins=100)

    p99_rt_mean = np.mean(p99_rt)
    p99_rt_var = np.var(p99_rt)
    p99_rt_std = np.std(p99_rt)
    p99_rt_max = np.max(p99_rt)
    p99_rt_min = np.min(p99_rt)
    p99_rt_hist = np.histogram(p99_rt, bins=100)

    ms_avg_rt_mean = np.mean(ms_avg_rt)
    ms_avg_rt_var = np.var(ms_avg_rt)
    ms_avg_rt_std = np.std(ms_avg_rt)
    ms_avg_rt_max = np.max(ms_avg_rt)
    ms_avg_rt_min = np.min(ms_avg_rt)
    ms_avg_rt_hist = np.histogram(ms_avg_rt, bins=100)
    ms_avg_rt_median = np.median(ms_avg_rt)
    ms_avg_rt_25th_percentile = np.percentile(ms_avg_rt, 25)
    ms_avg_rt_75th_percentile = np.percentile(ms_avg_rt, 75)

    ms_p95_rt_mean = np.mean(ms_p95_rt)
    ms_p95_rt_var = np.var(ms_p95_rt)
    ms_p95_rt_std = np.std(ms_p95_rt)
    ms_p95_rt_max = np.max(ms_p95_rt)
    ms_p95_rt_min = np.min(ms_p95_rt)
    ms_p95_rt_hist = np.histogram(ms_p95_rt, bins=100)
    ms_p95_rt_median = np.median(ms_p95_rt)
    ms_p95_rt_25th_percentile = np.percentile(ms_p95_rt, 25)
    ms_p95_rt_75th_percentile = np.percentile(ms_p95_rt, 75)

    ms_p99_rt_mean = np.mean(ms_p99_rt)
    ms_p99_rt_var = np.var(ms_p99_rt)
    ms_p99_rt_std = np.std(ms_p99_rt)
    ms_p99_rt_max = np.max(ms_p99_rt)
    ms_p99_rt_min = np.min(ms_p99_rt)
    ms_p99_rt_hist = np.histogram(ms_p99_rt, bins=100)

    total_avg_rt_mean = np.mean(total_avg_rt)
    total_avg_rt_var = np.var(total_avg_rt)
    total_avg_rt_std = np.std(total_avg_rt)
    total_avg_rt_max = np.max(total_avg_rt)
    total_avg_rt_min = np.min(total_avg_rt)
    total_avg_rt_hist = np.histogram(total_avg_rt, bins=100)
    total_avg_rt_median = np.median(total_avg_rt)
    total_avg_rt_25th_percentile = np.percentile(total_avg_rt, 25)
    total_avg_rt_75th_percentile = np.percentile(total_avg_rt, 75)

    total_p95_rt_mean = np.mean(total_p95_rt)
    total_p95_rt_var = np.var(total_p95_rt)
    total_p95_rt_std = np.std(total_p95_rt)
    total_p95_rt_max = np.max(total_p95_rt)
    total_p95_rt_min = np.min(total_p95_rt)
    total_p95_rt_hist = np.histogram(total_p95_rt, bins=100)
    total_p95_rt_median = np.median(total_p95_rt)
    total_p95_rt_25th_percentile = np.percentile(total_p95_rt, 25)
    total_p95_rt_75th_percentile = np.percentile(total_p95_rt, 75)

    total_p99_rt_mean = np.mean(total_p99_rt)
    total_p99_rt_var = np.var(total_p99_rt)
    total_p99_rt_std = np.std(total_p99_rt)
    total_p99_rt_max = np.max(total_p99_rt)
    total_p99_rt_min = np.min(total_p99_rt)
    total_p99_rt_hist = np.histogram(total_p99_rt, bins=100)
    
    import matplotlib.pyplot as plt
    
    # Plot the box plot for total_avg_rt
    plt.figure(figsize=(10, 6))
    plt.boxplot(total_avg_rt, vert=True, sym='')
    plt.title('Box Plot of Total Average Response Time')
    plt.xlabel('Total Average Response Time')
    plt.savefig("total_avg_rt_boxplot.png")

    # Plot the box plot for total_p95_rt
    plt.figure(figsize=(10, 6))
    plt.boxplot(total_p95_rt, vert=True, sym='')
    plt.title('Box Plot of Total 95% Response Time')
    plt.xlabel('Total 95% Response Time')
    plt.savefig("total_p95_rt_boxplot.png")

    # Plot the box plot for ms_avg_rt
    plt.figure(figsize=(10, 6))
    plt.boxplot([x / 1000 for x in ms_avg_rt], vert=True, sym='')
    plt.title('Box Plot of Microservice Average Response Time')
    plt.xlabel('Microservice Average Response Time')
    plt.savefig("ms_avg_rt_boxplot.png")

    # Plot the box plot for ms_p95_rt
    plt.figure(figsize=(10, 6))
    plt.boxplot(ms_p95_rt, vert=True, sym='')
    plt.title('Box Plot of Microservice 95% Response Time')
    plt.xlabel('Microservice 95% Response Time')
    plt.savefig("ms_p95_rt_boxplot.png")

    # # Calculate ECDF
    # ms_avg_rt_sorted = np.sort([x / 1000 for x in ms_avg_rt])
    # ecdf = np.arange(1, len(ms_avg_rt_sorted) + 1) / len(ms_avg_rt_sorted)

    # # Plot ECDF
    # plt.figure(figsize=(10, 6))
    # plt.plot(ms_avg_rt_sorted, ecdf, marker='.', linestyle='none')
    # plt.xlabel('ms_avg_rt')
    # plt.ylabel('ECDF')
    # plt.title('ECDF of ms_avg_rt')
    # plt.grid(True)
    # plt.savefig("ecdf_ms_avg_rt.png")

    # Print the results
    print(f'num_threads: mean={num_threads_mean}, variance={num_threads_var}, std={num_threads_std}, max={num_threads_max}, min={num_threads_min}')
    print(f'num_cores: mean={num_cores_mean}, variance={num_cores_var}, std={num_cores_std}, max={num_cores_max}, min={num_cores_min}')
    print(f'proc_delay: mean={proc_delay_mean}, variance={proc_delay_var}, std={proc_delay_std}, max={proc_delay_max}, min={proc_delay_min}')
    print(f'load: mean={load_mean}, variance={load_var}, std={load_std}, max={load_max}, min={load_min}')
    print(f'avg_rt: mean={avg_rt_mean}, variance={avg_rt_var}, std={avg_rt_std}, max={avg_rt_max}, min={avg_rt_min}')
    print(f'p95_rt: mean={p95_rt_mean}, variance={p95_rt_var}, std={p95_rt_std}, max={p95_rt_max}, min={p95_rt_min}')
    print(f'p99_rt: mean={p99_rt_mean}, variance={p99_rt_var}, std={p99_rt_std}, max={p99_rt_max}, min={p99_rt_min}')
    print(f'ms_avg_rt: mean={ms_avg_rt_mean}, variance={ms_avg_rt_var}, std={ms_avg_rt_std}, max={ms_avg_rt_max}, min={ms_avg_rt_min}')
    print(f'ms_p95_rt: mean={ms_p95_rt_mean}, variance={ms_p95_rt_var}, std={ms_p95_rt_std}, max={ms_p95_rt_max}, min={ms_p95_rt_min}')
    print(f'ms_p99_rt: mean={ms_p99_rt_mean}, variance={ms_p99_rt_var}, std={ms_p99_rt_std}, max={ms_p99_rt_max}, min={ms_p99_rt_min}')
    print(f'total_avg_rt: mean={total_avg_rt_mean}, variance={total_avg_rt_var}, std={total_avg_rt_std}, max={total_avg_rt_max}, min={total_avg_rt_min}')
    print(f'total_p95_rt: mean={total_p95_rt_mean}, variance={total_p95_rt_var}, std={total_p95_rt_std}, max={total_p95_rt_max}, min={total_p95_rt_min}')
    print(f'total_p99_rt: mean={total_p99_rt_mean}, variance={total_p99_rt_var}, std={total_p99_rt_std}, max={total_p99_rt_max}, min={total_p99_rt_min}')

    print(f'\n')

    print(f'total_avg_rt: min={total_avg_rt_min/1000}, 25th percentile={total_avg_rt_25th_percentile/1000}, median={total_avg_rt_median/1000}, 75th percentile={total_avg_rt_75th_percentile/1000}, max={total_avg_rt_max/1000}')
    print(f'total_p95_rt: min={total_p95_rt_min/1000}, 25th percentile={total_p95_rt_25th_percentile/1000}, median={total_p95_rt_median/1000}, 75th percentile={total_p95_rt_75th_percentile/1000}, max={total_p95_rt_max/1000}')
    print(f'ms_avg_rt: min={ms_avg_rt_min/1000}, 25th percentile={ms_avg_rt_25th_percentile/1000}, median={ms_avg_rt_median/1000}, 75th percentile={ms_avg_rt_75th_percentile/1000}, max={ms_avg_rt_max/1000}')
    print(f'ms_p95_rt: min={ms_p95_rt_min/1000}, 25th percentile={ms_p95_rt_25th_percentile/1000}, median={ms_p95_rt_median/1000}, 75th percentile={ms_p95_rt_75th_percentile/1000}, max={ms_p95_rt_max/1000}')

    # print(f'num_threads histogram: {num_threds_hist}')
    # print(f'num_cores histogram: {num_cores_hist}')
    # print(f'proc_delay histogram: {proc_delay_hist}')
    # print(f'load histogram: {load_hist}')
    # print(f'avg_rt histogram: {avg_rt_hist}')
    # print(f'p95_rt histogram: {p95_rt_hist}')
    # print(f'p99_rt histogram: {p99_rt_hist}')
    # print(f'ms_avg_rt histogram: {ms_avg_rt_hist}')
    # print(f'ms_p95_rt histogram: {ms_p95_rt_hist}')
    # print(f'ms_p99_rt histogram: {ms_p99_rt_hist}')
    # print(f'total_avg_rt histogram: {total_avg_rt_hist}')
    # print(f'total_p95_rt histogram: {total_p95_rt_hist}')
    # print(f'total_p99_rt histogram: {total_p99_rt_hist}')

    print(f'Dataset size: {len(dataset)}')

if __name__ == "__main__":
    args = parse_args()
    calculate_print(args.input_dir)

