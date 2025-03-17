import tensorflow as tf

def normalization(feature, feature_name):
    if feature_name == 'num_threads':
        feature = (feature - 3.88) / 2.58
    elif feature_name == 'num_cores':
        feature = (feature - 3.63) / 2.64
    elif feature_name == 'proc_delay':
        feature = (feature - 265) / 1254
    elif feature_name == 'load':
        feature = (feature - 1071) / 1810
    elif feature_name == 'total_p95_rt':
        feature = tf.math.log(feature)
    return feature


def denormalization(feature, feature_name):
    if feature_name == 'total_p95_rt':
        feature = tf.math.exp(feature)
    return feature
