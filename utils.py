import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
# from scipy.stats import entropy
# import pandas as pd
# from scipy.special import kl_div

DPI=150 ## for notebook, increase for publication or use PDF

def plot_pc_dist(idx, data):
    data.loc[idx, :].plot(kind="bar", rot=0)


def tpc2npc(tpc):
    steps = list("FCGDAEB")
    pcs = [p * 7 % 12 for p in range(-1, 6)]
    d = {s: p for s, p in zip(steps, pcs)}

    step, acc = tpc[0], tpc[1:]
    if "#" in acc:
        direction = 1
    elif "b" in acc:
        direction = -1
    else:
        direction = 0
    wind = len(acc)
    return (d[step] + (wind * direction)) % 12


def pcs(ordering="chromatic"):
    pcs = np.asarray([k for k in range(12)])
    pcs = pcs if ordering == "chromatic" else pcs * 7 % 12 \
        if ordering == "fifths" else None
    return pcs


# def get_polygon(piece_id, data, ordering="chromatic"):
def get_polygon(values, ordering="chromatic"):  # data,

    values = np.array(values)[pcs(ordering=ordering)]

#     values = data.loc[piece_id, idx].values
    angles = sorted([n / float(12) * 2 * np.pi for n in range(12)])
    angles += angles[:1]

    # close circle
    values = np.append(values, values[0])

    # polar coordinates
    x = values * np.cos(angles)
    y = values * np.sin(angles)

    return values, angles, Polygon(zip(x,y)) 


def plot_area(piece_id, data, ordering="fifths", ax=None, draw=True, fill=True):
    """
    Takes a piece id (index in neutral pitch-class version of TP3C) and 
    returns a radard plot of the pitch-class distribution.
    """
    
    idx = pcs(ordering=ordering)
    
    if ax == None:
        fig, ax = plt.subplots(subplot_kw={"polar": True})

    # title
    ax.set_title(ordering, fontsize=16)
    
    # initialize radar plot
    ax.set_theta_offset(np.pi / 2)  # Put first axis on top
    ax.set_theta_direction(-1)  # clockwise
    
    # set position in degrees (360°) and labels for radial values
    ax.set_rlabel_position(0)
    rlabels = np.linspace(0, 1, 21).round(2)
    ax.set_rticks([lab for lab in rlabels])
    ax.set_rlabel_position(180)
    ax.set_yticklabels(rlabels, fontdict={'fontsize': 13, 'color': '#555555'})

    # data to plot
    values, angles, polygon = get_polygon(
        # , data=data
        data.loc[piece_id, [k for k in range(12)]], ordering=ordering)

    c = "firebrick" if ordering == "chromatic" \
        else "teal" if ordering == "fifths" else "white"

    # area
    if fill:
        ax.fill(angles, values, alpha=.33, c=c,
                label=f"= {round(polygon.area, 4)}")
        ax.legend(loc=1)

    if draw:
        ax.plot(angles, values, c=c, alpha=.33)

    # pitch-class spider
    for i, (theta, r) in enumerate(zip(angles, values)):
        ax.plot([theta, theta], [0, r], color="black", lw=1)
        ax.scatter(x=theta, y=r, color="black")

    # pc labels
    ax.set_xticks(angles)
    idx = np.append(idx, 0)
    ax.set_xticklabels(idx, fontdict={'fontsize': 16})

    return ax


def plot_both_areas(idx, data, fill=True):
    fig, axes = plt.subplots(1,2, figsize=(15, 6), subplot_kw={"polar": True})
    plot_area(idx, data=data, ordering="chromatic", ax=axes[0], fill=fill)
    plot_area(idx, data=data, ordering="fifths", ax=axes[1], fill=fill)

    # ## MEGA HACK BEGIN %%%%%
    # v1, a1, _ = get_polygon(data.loc[idx,[k for k in range(12)]],
    # # ordering="fifths")
    # v2, a2, _ = get_polygon(data.loc[idx,[k for k in range(12)]],
    # ordering="chromatic")
    # vs = (v1[:-1] * v2[:-1])
    # vs = vs / vs.sum()
    # data.loc[len(data.index)] = vs
    # plot_area(data.shape[0]-1,data=data, ordering="fifths", ax=axes[2],
    # fill=fill)
    # data = data.loc[:-1,:]  
    # ## END MEGA HACK %%%%%%

    plt.tight_layout()
    return fig


def pol2cart(magnitude, phase):
    x = magnitude * np.cos(phase)
    y = magnitude * np.sin(phase)
    return complex(x, y)


def cart2pol(real, imag):
    mag = np.sqrt(real**2 + imag**2)
    phase = np.arctan(imag, real)
    return mag, phase


def calculate_features(df):
    from scipy.stats import entropy 
    freqs = df[[k for k in range(12)]]
    
    df["fifths_A"] = freqs.apply(lambda x: get_polygon(x, ordering="fifths")[2].area, axis=1)
    df["chromatic_A"] = freqs[[k for k in range(12)]].apply(lambda x: get_polygon(x, ordering="chromatic")[2].area, axis=1)
    df["entropy"] = freqs.apply(lambda x: entropy(x), axis=1)
    df["ratio_chr/f"] = df["chromatic_A"] / df["fifths_A"]
    df["difference_f-chr"] = df["fifths_A"] - df["chromatic_A"]