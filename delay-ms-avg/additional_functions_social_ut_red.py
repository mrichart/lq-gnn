import tensorflow as tf

def normalization(feature, feature_name):
    if feature_name == 'num_threads':
        feature = (feature - 4.32) / 2.72
    elif feature_name == 'num_cores':
        feature = (feature - 4.32) / 2.79
    elif feature_name == 'proc_delay':
        feature = (feature - 285) / 1322
    elif feature_name == 'load':
        feature = (feature - 601) / 1059
    elif feature_name == 'ms_avg_rt':
        feature = tf.math.log(feature)
    return feature


def denormalization(feature, feature_name):
    if feature_name == 'ms_avg_rt':
        feature = tf.math.exp(feature)
    return feature
