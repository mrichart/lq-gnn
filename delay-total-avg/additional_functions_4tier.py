import tensorflow as tf

def normalization(feature, feature_name):
    if feature_name == 'num_threads':
        feature = (feature - 2.73) / 1.82
    elif feature_name == 'num_cores':
        feature = (feature - 2.07) / 1.67
    elif feature_name == 'proc_delay':
        feature = (feature - 244) / 1051
    elif feature_name == 'load':
        feature = (feature - 1740) / 2635
    elif feature_name == 'total_avg_rt':
        feature = tf.math.log(feature)
    return feature


def denormalization(feature, feature_name):
    if feature_name == 'total_avg_rt':
        feature = tf.math.exp(feature)
    return feature
