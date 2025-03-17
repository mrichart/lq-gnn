import os
import re
import shutil
import json
import argparse
import numpy as np
from  graph_mili import generate_graph
from networkx.readwrite import json_graph
from pathlib import Path
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Generate dataset for training.")
    parser.add_argument("--input_dir", type=Path, default=Path("logs"), help="Directory containing raw data.")
    parser.add_argument("--output_dir", type=Path, default=Path("data/raw"), help="Directory where to store the dataset.")
    parser.add_argument("--output_valid_dir", type=Path, default=Path("data/raw_valid"), help="Directory where to store the valid dataset.")
    parser.add_argument("--train_dir", type=Path, default=Path("data/train"), help="Directory where to store the training dataset.")
    parser.add_argument("--train_valid_dir", type=Path, default=Path("data/train_valid"), help="Directory where to store the training dataset.")
    parser.add_argument("--validation_dir", type=Path, default=Path("data/validation"), help="Directory where to store the validation dataset.")
    parser.add_argument("--validation_valid_dir", type=Path, default=Path("data/validation_valid"), help="Directory where to store the validation dataset.") 
    parser.add_argument("--test_dir", type=Path, default=Path("data/test"), help="Directory where to store the test dataset.")
    parser.add_argument("--test_valid_dir", type=Path, default=Path("data/test_valid"), help="Directory where to store the test dataset.")
    parser.add_argument("--validation_ratio", type=float, default=0.1, help="Ratio of validation samples.")
    parser.add_argument("--test_ratio", type=float, default=0.1, help="Ratio of test samples.")
    parser.add_argument("--random_seed", type=int, default=42, help="Random seed for reproducibility.")
    parser.add_argument("--input_graph_dir", type=Path, default=Path("~/uqsim-power-management-beta/architecture/4tier/json"), help="Directory containing input graphs.")
    parser.add_argument("--rejection_threshold", type=float, default=0.02, help="Threshold for indicating a deployment is not feasible.")
    return parser.parse_args()

def _empty_dirs(dirs=None):
    if dirs is None:
        return
    elif isinstance(dirs, (Path, str)):
        dirs = [Path(dirs)]
    for _dir in dirs:
        assert isinstance(_dir, Path)
        for file in [f for f in _dir.glob("*") if f.is_file()]:
            file.unlink()

def generate_graphs(input_graph_dir, input_dir, output_dir, output_valid_dir, rejection_threshold):
    #print("Generating graphs")
    file_num = 0
    for filename in os.listdir(input_dir):
        #print(f"Processing file {filename}")
        filename_parts = []
        if os.path.isfile(os.path.join(input_dir, filename)):
            filename_clean = os.path.splitext(filename)[0]  # Remove everything after the '.'
            filename_parts = filename_clean.split("_")  # Split by '_'
            conf_map = {}
            for p in range(len(filename_parts)-1):
                if filename_parts[p+1].isdigit():
                    conf_map[filename_parts[p]] = int(filename_parts[p+1])
                else:
                    conf_map[filename_parts[p]] = filename_parts[p+1]

        complete_log = False
        reached_micro_stats = False
        path_avg_rt = {}
        path_p95_rt = {}
        path_p99_rt = {}
        total_avg_rt = np.inf
        total_p95_rt = np.inf
        total_p99_rt = np.inf
        accepted_requests = 0
        micro_cpu = {}
        micro_requests = {}
        micro_avg_rt = {}
        micro_p95_rt = {}
        micro_p99_rt = {}
        with open(os.path.join(input_dir, filename), "r") as file:
            for line in file:
                if line.startswith("Simulation ended at"):
                    complete_log = True
                if line.startswith("total:"):
                    line_data = re.split(';|:',line.strip())
                    total_avg_rt = float(line_data[1])
                    total_p95_rt= float(line_data[3])
                    total_p99_rt = float(line_data[4])
                    #if total_avg_rt > 10:
                    #   complete_log = False
                if line.startswith("path0:"):
                    line_data = re.split(';|:',line.strip())
                    path_avg_rt[0] = float(line_data[1])
                    path_p95_rt[0] = float(line_data[3])
                    path_p99_rt[0] = float(line_data[4])
                if line.startswith("path1:"):
                    line_data = re.split(';|:',line.strip())
                    path_avg_rt[1] = float(line_data[1])
                    path_p95_rt[1] = float(line_data[3])
                    path_p99_rt[1] = float(line_data[4])
                if line.startswith("path2:"):
                    line_data = re.split(';|:',line.strip())
                    path_avg_rt[2] = float(line_data[1])
                    path_p95_rt[2] = float(line_data[3])
                    path_p99_rt[2] = float(line_data[4])
                if line.startswith("nginx:"):
                    line_data = re.split(';|:',line.strip())
                    accepted_requests = float(line_data[2])
                    reached_micro_stats = True
                if reached_micro_stats:
                    line_data = re.split(';|:',line.strip())
                    if not re.search(r'\d', line_data[0]):
                        micro_cpu[line_data[0]] = float(line_data[1])*100
                        micro_requests[line_data[0]] = float(line_data[2])
                        micro_avg_rt[line_data[0]] = float(line_data[5])
                        micro_p95_rt[line_data[0]] = float(line_data[6])
                        micro_p99_rt[line_data[0]] = float(line_data[7])
                    

        #load in kilo requests per second
        load = conf_map['kqps']
        deployment = conf_map['deployment']
        threads = {"nginx": conf_map['ngx'], "memcached": conf_map['mmc'], "php": conf_map['php'], "php_io": conf_map['phpio'], "mongodb": conf_map['mongo'], "mongo_io": conf_map['mongoio']}
        replicas = {"nginx": 1, "memcached": 1, "php": 1, "php_io": 1, "mongodb": 1, "mongo_io": 1}
        cores = {"nginx": conf_map['ngxcores'], "memcached": conf_map['mmccores'], "php": conf_map['phpcores'], "php_io": conf_map['phpiocores'], "mongodb": conf_map['mongocores'], "mongo_io": conf_map['mongoiocores']}

        ############TODO######################
        latency_0_2 = conf_map["latencyedgecloud"] if conf_map["latencyedgecloud"] > conf_map["latencyedgefog"] else conf_map["latencyedgefog"]
        latency_1_2 = latency_0_2
        latency_2_4 = conf_map["latencyfogcloud"]
        machine_latencies = {0: {0: 0, 1: 0, 2: latency_0_2, 3: np.inf, 4: np.inf, 5: np.inf}, 1: {0: 0, 1: 0, 2: latency_1_2, 3: np.inf, 4: np.inf, 5: np.inf}, 2: {0: latency_0_2, 1: latency_1_2, 2: 0, 3: 0, 4: latency_2_4, 5: np.inf}, 3: {0: np.inf, 1: np.inf, 2: 0, 3: 0, 4: np.inf, 5: np.inf}, 4: {0: np.inf, 1: np.inf, 2: latency_2_4, 3: np.inf, 4: 0, 5: 0}, 5: {0: np.inf, 1: np.inf, 2: np.inf, 3: np.inf, 4: 0, 5: 0}}
        valid = (accepted_requests / (load*1000)) > (1-rejection_threshold)

        if complete_log and len(path_avg_rt) == 3:
            G = generate_graph(input_graph_dir, load=load, threads=threads, replicas=replicas, cores=cores, machine_latencies=machine_latencies, avg_rt=path_avg_rt, p95_rt=path_p95_rt, p99_rt=path_p99_rt, deployment=deployment, valid=valid, total_avg_rt=total_avg_rt, total_p95_rt=total_p95_rt, total_p99_rt=total_p99_rt, micro_cpu=micro_cpu, micro_requests=micro_requests, micro_avg_rt=micro_avg_rt, micro_p95_rt=micro_p95_rt, micro_p99_rt=micro_p99_rt)
        
            output_file_all = os.path.join(output_dir, f"data_{file_num}.json")
            output_file_valid = os.path.join(output_valid_dir, f"data_{file_num}.json")
            with open(output_file_all, "w") as _f:
                json.dump(json_graph.node_link_data(G), _f)
            if valid:
                with open(output_file_valid, "w") as _f:
                    json.dump(json_graph.node_link_data(G), _f)
            file_num += 1

def join_graphs_into_dataset(files, output_dir, output_file_name="data.json", empty_dirs=False):
    if empty_dirs:
        _empty_dirs(output_dir)
    graphs = [json.load(open(file, "r")) for file in files]
    with open(output_dir / output_file_name, "w") as fp:
        json.dump(graphs, fp)

def split_traing_validation_test(raw_dir, train_dir, validation_dir, test_dir, validation_ratio, test_ratio, empty_dirs=False):
    
    if empty_dirs:
        _empty_dirs([train_dir, validation_dir, test_dir])

    files = np.array(list(Path(raw_dir).glob("*.json")))
    train_samples = int(files.shape[0] * (1 - validation_ratio - test_ratio))
    validation_samples = int(files.shape[0] * validation_ratio)
    test_samples = int(files.shape[0] * test_ratio)
    assert files.shape[0] >= train_samples+validation_samples+test_samples, \
        f"Train + Validation + Test samples {train_samples+validation_samples+test_samples} exceed number of files available {files.shape[0]}."

    np.random.shuffle(files)
    training_files = files[:train_samples]
    validation_files = files[train_samples:train_samples+validation_samples]
    test_files = files[train_samples+validation_samples:]
    
    print(f"Copying training graphs into {raw_dir / 'train'}")
    for file in training_files:
        shutil.copy(file, raw_dir / "train")
    print(f"Joining training graphs into {train_dir}")
    join_graphs_into_dataset(training_files, output_dir=train_dir)

    print(f"Copying validation graphs into {raw_dir / 'validation'}")
    for file in validation_files:
        shutil.copy(file, raw_dir / "validation")
    print(f"Joining validation graphs into {validation_dir}")
    join_graphs_into_dataset(validation_files, output_dir=validation_dir)

    print(f"Coping test graphs into {raw_dir / 'test'}")
    for file in test_files:
        shutil.copy(file, raw_dir / "test")
    print(f"Joining test graphs into {test_dir}")
    join_graphs_into_dataset(test_files, output_dir=test_dir)

if __name__ == "__main__":
    args = parse_args()
    np.random.seed(args.random_seed)
    for _dir in [args.output_dir, args.train_dir, args.validation_dir, args.test_dir, Path(args.output_dir) / "train", Path(args.output_dir) / "validation", Path(args.output_dir) / "test"]:
        os.makedirs(_dir, exist_ok=True)
    for _dir in [args.output_valid_dir, args.train_valid_dir, args.validation_valid_dir, args.test_valid_dir, Path(args.output_valid_dir) / "train", Path(args.output_valid_dir) / "validation", Path(args.output_valid_dir) / "test"]:
        os.makedirs(_dir, exist_ok=True)
    generate_graphs(args.input_graph_dir, args.input_dir, args.output_dir, args.output_valid_dir, args.rejection_threshold)
    split_traing_validation_test(args.output_dir, args.train_dir, args.validation_dir, args.test_dir, args.validation_ratio, args.test_ratio, empty_dirs=True)
    split_traing_validation_test(args.output_valid_dir, args.train_valid_dir, args.validation_valid_dir, args.test_valid_dir, args.validation_ratio, args.test_ratio, empty_dirs=True)