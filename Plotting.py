import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import boost_histogram as bh
import matplotlib.colors as colors
import pandas as pd


def plt_result(inputs, predictions, target, directory):
    plt.switch_backend('agg')
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.scatter(predictions, target, color='b')
    ax.plot(predictions, predictions, color='r')
    ax.set_xlabel('Grades Range')
    ax.set_ylabel('Grades Scored')
    ax.set_title('scatter plot')
    plt.xlabel('True Energy')
    plt.xlabel('Calibrated energy')
    plt.savefig(directory + "/figures.png")
    plt.close()


def loss_func_ana(history_df, emissions):
    plt.switch_backend('agg')
    trial_columns = history_df.columns
    for column in trial_columns:
        history_df[column].plot(kind="line")
        plt.title("{}".format(column))
        plt.xlabel("Epochs")
        plt.savefig("/{}/{}.png".format(emissions, column))
        plt.close()


def plothist2d(h, Ratio, title, emissions):
    plt.switch_backend('agg')

    fig, ax = plt.subplots(figsize=(16, 8))

    zs = h.view().T  #color info

    # *h.axes.edges.T = defines the two edges for plotting

    pcm = ax.pcolor(*h.axes.edges.T,
                    zs,
                    norm=colors.LogNorm(vmin=1,
                                        vmax=zs.max()))  #log scale of Z

    fig.colorbar(pcm, ax=ax)  #adds the colorbar

    plt.plot(Ratio, color="red", lw=0.5)  #fit
    plt.title(title, fontsize=16)
    plt.xlabel("Cluster Energy [GeV]", fontsize=14)
    plt.ylabel(r"Ratio = $\frac{LCW Calibrated Energy}{Cluster Energy}$",
               fontsize=14)
    plt.xscale("log")  #log scale of X

    plt.xlim([min(h.axes.edges[0]), max(h.axes.edges[0])])
    plt.ylim([0, 2])
    pname = title.replace(" ", "_") + "_plot_performance"
    plt.savefig("/{}/{}.png".format(emissions, pname), dpi=400)
    plt.close()


def Plot_performance(df, title="", emissions=""):
    l_true = df["cluster_ENG_CALIB_TOT"].values
    l_calib = df["CalibratedE"].values
    Ratio = l_calib / l_true

    n1, n2 = len(l_true), len(l_calib)
    n_entries = n1

    MinX = .05
    MaxX = max(l_true)

    MaxY = 2
    MinY = 0

    n_bins = 100

    LogWidth = []
    yWidth = []

    for i in range(n_bins):
        exponent = np.log10(MinX) + (np.log10(MaxX) -
                                     np.log10(MinX)) / float(n_bins) * i
        LogWidth.append(pow(10, exponent))
        yWidth.append(MinY + i * (MaxY - MinY) / n_bins)

    #defines how axes are spaced
    xaxes = bh.axis.Variable(LogWidth, underflow=True, overflow=True)
    yaxes = bh.axis.Variable(yWidth, underflow=True, overflow=True)

    hist = bh.Histogram(xaxes, yaxes)

    values = np.array([l_true, Ratio])

    hist.reset()
    hist.fill(*values)

    plothist2d(hist, Ratio, title, emissions)


def createROOTPlots(df, emissions):
    og_df = df
    em_df = og_df[og_df["truthPDG"] == 111]
    had_df = og_df[og_df["truthPDG"] == 211]
    Plot_performance(og_df, "All Data", emissions)
    Plot_performance(em_df, "EM Tree", emissions)
    Plot_performance(had_df, "Had Tree", emissions)
