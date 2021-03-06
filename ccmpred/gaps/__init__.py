import numpy as np
import ccmpred.counts

from ccmpred.gaps.cext import remove_gaps_probs, remove_gaps_consensus


def remove_gaps_col_freqs(msa):
    counts = ccmpred.counts.single_counts(msa)
    counts[:, 20] = 0

    counts /= np.sum(counts, axis=1)[:, np.newaxis]

    return remove_gaps_probs(msa, counts)


def backinsert_gapped_positions(x_single, x_pair, gapped_positions):

    for position in gapped_positions:
        x_single = np.insert(x_single,position, [0], axis=0)
        x_pair = np.insert(x_pair,position, [0], axis=0)
        x_pair = np.insert(x_pair,position, [0], axis=1)

    return x_single, x_pair


def remove_gapped_positions(msa, max_gap_percentage):

    if max_gap_percentage >= 100:
        return msa, []

    msa_gap_counts = (msa == 20).sum(0)

    max_gap_count = (max_gap_percentage/100.0 * msa.shape[0])

    ungapped_positions  = np.where(msa_gap_counts <  max_gap_count)
    gapped_positions    = np.where(msa_gap_counts >=  max_gap_count)

    if max_gap_percentage < 100:
        print("Removed {0} alignment positions with > {1} percent gaps.".format(
            len(gapped_positions[0]), max_gap_percentage/100.0))

    return np.ascontiguousarray(msa[:, ungapped_positions[0]]), gapped_positions[0]