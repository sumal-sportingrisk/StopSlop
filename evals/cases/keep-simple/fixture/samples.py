def find_sample(samples, sample_id):
    for sample in samples:
        if sample.id == sample_id:
            return sample
    return None
