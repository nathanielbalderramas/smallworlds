import matplotlib.pyplot as plt

plt.rcParams["axes.facecolor"] = "limegreen"
plt.rcParams["savefig.facecolor"] = "limegreen"


def plot_frame(environment_dims, populations_matrix, symbol_list, epoch_numbrer, time_number):
    data = populations_matrix
    fig, ax = plt.subplots()
    ax.set_xlim(0, environment_dims["x"])
    ax.set_ylim(0, environment_dims["y"])
    for pi, p in enumerate(data):
        try:
            x, y = zip(*p)
            ax.plot(x, y, ls="", **symbol_list[pi])
        except ValueError:
            if len(p) == 0:
                pass
            else:
                raise Exception()


    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.tight_layout()
    plt.savefig(f"vis/e_{epoch_numbrer}_t_{time_number}.png")
    plt.close()