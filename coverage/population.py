
from matplotlib import rcParams
rcParams['figure.figsize'] = [12,14]
import pylab

from sequana import GenomeCov
print("READING BED files")
b1 = GenomeCov("ERR043367.bed")
print("READING BED files")
b2 = GenomeCov("ERR043371.bed")
print("READING BED files")
b3 = GenomeCov("ERR043375.bed")
print("READING BED files")
b4 = GenomeCov("ERR043379.bed")
print("READING BED files")
b5 = GenomeCov("ERR142616.bed")
print("READING BED files")
b6 = GenomeCov("ERR316404.bed")


# Get all sequana results
import pandas as pd
roi1 = pd.read_csv("roi_ERR043367.csv")
roi2 = pd.read_csv("roi_ERR043371.csv")
roi3 = pd.read_csv("roi_ERR043375.csv")
roi4 = pd.read_csv("roi_ERR043379.csv")   #the one used to plot a coverage signal
roi5 = pd.read_csv("roi_ERR142616.csv")
roi6 = pd.read_csv("roi_ERR316404.csv")


# Get all CNVnator results
from sequana.cnv import CNVnator
all_events = []
sel = ["start", "end", "3"]
all_events.append(CNVnator("events_ERR043367_bin15.txt").df[sel])
all_events.append(CNVnator("events_ERR043371_bin41.txt").df[sel])
all_events.append(CNVnator("events_ERR043375_bin69.txt").df[sel])
all_events.append(CNVnator("events_ERR043379_bin27.txt").df[sel])
all_events.append(CNVnator("events_ERR142616_bin2.txt").df[sel])
all_events.append(CNVnator("events_ERR316404_bin76.txt").df[sel])


# Get all CNOGpro results
# Select events
cnogpro = pd.read_csv('ST1.csv')
cnogpro_events = cnogpro.query("CN_HMM!='1'")
cnogpro_events = cnogpro_events[['Left', 'Right']].values
len(cnogpro_events)


fig, axes = pylab.subplots(6,1, sharex="col")
def plot_all_rois(m1=85000, m2=90000, ymax=500):
    i = 0
    for b, roi,  in zip(
        [b1,b2,b3,b4,b5,b6],
        [roi1, roi2, roi3, roi4, roi5, roi6],
        ):
        print("{}/6".format(i+1))

        color = "red"
        chromosome = b.chr_list[0]
        N = len(chromosome.df)
        chromosome.run(40001, k=2)

        axes[i].plot(chromosome.df['cov'].loc[m1-20000:m2+40000], color="k", lw=2)
        axes[i].set_ylabel("$C_b$", fontsize=18)

        for start, end, cov in zip(roi.start, roi.end, roi.mean_cov):
            if start>m1-20000 and start<m2+40000:
                axes[i].plot([start, end], [cov, cov], lw=2,
                             color=color, marker="o")
        ymax=chromosome.df['cov'].loc[m1-20000:m2+40000].max()*1.2
        axes[i].set_xlim([m1, m2])
        YMAX = axes[i].get_ylim()[1]
        for this in all_events[i].query("start>@m1 and start<@m2+10000").iterrows():
            axes[i].fill_between(this[1][0:2], y1=YMAX, alpha=0.3,
                                 edgecolor="k", lw=2, facecolor="g")
        if i==0:
            axes[i].fill_between([86534,87193] , y1=YMAX/1.5, y2=YMAX, lw=1,
                                edgecolor="k", facecolor="r", alpha=0.3)
            axes[i].fill_between([87194,87231] , y1=YMAX/1.5, y2=YMAX,lw=1,
                                edgecolor="k", facecolor="g", alpha=0.3)
            axes[i].fill_between([87231,89646] , y1=YMAX/1.5, y2=YMAX,lw=1,
                                edgecolor="k", facecolor="r", alpha=0.3)
        i+=1


print("Plotting")
plot_all_rois(86600,89800)
pylab.xlabel("Base position (kbp)", fontsize=18)
pylab.xticks([87000,87500,88000,88500,89000,89500], [87,87.5,88,88.5,89,89.5], fontsize=16)
pylab.tight_layout()
fig.subplots_adjust(hspace=0)

print('saving')
pylab.savefig("test.png", dpi=200)

