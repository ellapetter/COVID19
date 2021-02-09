import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats
from matplotlib.ticker import PercentFormatter
from statannot import add_stat_annotation

def create_rooling_data(data):
    res = None
    
    date = np.datetime64("2020-12-02")
    while date + 7 < np.datetime64("2021-02-01"):
        end_day = date + 7
        d = data[(data["Distribution date"] >= str(date)) & (data["Distribution date"] < str(end_day))]

        print(d["Distribution date"].min(), d["Distribution date"].max())
        d_res = d.groupby("age_group")["Numeric Result"].describe()   
        d_res["start_day"] = str(date + 3)
        res = pd.concat([res, d_res])
        
        date = date + 1

    return res.reset_index()


def plt1(df):
    fig, ax = plt.subplots(1,1, figsize=(30,8))

    sns.lineplot(data= df, x="Week", y = "mean", hue = "age_group", marker = "o", markersize=10, ax = ax, palette=sns.color_palette("Set1")[:2])
    sns.lineplot(data= df, x="Week", y = "CI_l", hue = "age_group", markersize=10, ax = ax, palette=sns.color_palette("Set1")[:2])
    sns.lineplot(data= df, x="Week", y = "CI_h", hue = "age_group",  markersize=10, ax = ax, palette=sns.color_palette("Set1")[:2])

    ax.tick_params(labelrotation=45)

    l1 = ax.lines[4] # blue
    l2 = ax.lines[8]
    l3 = ax.lines[5] # orange
    l4 = ax.lines[9]

    # Get the xy data from the lines so that we can shade
    x1 = l1.get_xydata()[:,0]
    y1 = l1.get_xydata()[:,1]
    x2 = l2.get_xydata()[:,0]
    y2 = l2.get_xydata()[:,1]
    x3 = l3.get_xydata()[:,0]
    y3 = l3.get_xydata()[:,1]
    x4 = l4.get_xydata()[:,0]
    y4 = l4.get_xydata()[:,1]

    ax.fill_between(x2,y2,y1, color=sns.color_palette("Set1")[0], alpha=0.1)
    ax.fill_between(x3,y4,y3, color=sns.color_palette("Set1")[1], alpha=0.1)


    ax.set_ylim(24,30)
    ax.set_xlabel("")
    ax.set_yticks(np.arange(25,31,1))


    ax.axvline(15, ls=":", color="black")
    ax.text(15.1, 29, "Vaccination Drive\n1st dose start" ,rotation=90, fontsize=18)

    ax.axvline(36, ls=":", color="black")
    ax.text(36.1, 29, "Vaccination Drive\n2nd dose start" ,rotation=90, fontsize=18)

    ax.axvline(36+7, ls=":", color="black")
    ax.text(36.1+7, 29.4, "Week after 2nd dose" ,rotation=90, fontsize=18)

    ax.set_ylabel("Average Ct value (95% CI)")
    ax.yaxis.grid()
    ax.get_legend().remove()
    ax.get_xaxis().set_visible(False)
    for ind, label in enumerate(ax.get_xticklabels()):
        if ind % 3 == 2:  # every 3rd label is kept
            label.set_visible(True)
        else:
            label.set_visible(False)
            

def plt2(data):
    sns.set_style("ticks")
    low_age = 40

    ##### Plot
    plt.figure(figsize=(14,6))
    g = sns.boxplot(data = data , y = "Numeric Result", x = "time_cat", hue = "age_cat",\
                    showmeans=True, meanprops={"marker":"o","markerfacecolor":"white", "markeredgecolor":"black","markersize":"7"},\
                    palette=sns.color_palette("Set1"), order=["dec_start","dec_end","jan_start","jan_end"])

    add_stat_annotation(g, data=data, y = "Numeric Result", x = "time_cat", hue = "age_cat",order=["dec_start","dec_end","jan_start","jan_end"],
                        box_pairs=[((("dec_start"),("under 60")), (("dec_start"),("above 60"))),
                                   ((("dec_end"),("under 60")), (("dec_end"),("above 60"))),
                                   ((("jan_start"),("under 60")), (("jan_start"),("above 60"))),
                                   ((("jan_end"),("under 60")), (("jan_end"),("above 60")))
                                  ],
                        test='t-test_ind', text_format='star', loc='inside', verbose=4, fontsize=10)

    plt.ylabel("Ct")
    plt.xlabel("")
    plt.xticks([0,1,2,3],["Dec2-15","Dec15-30","Jan1-15","Jan15-Jan30"])
    plt.yticks(np.arange(5,45,5))
    plt.ylim(0,45)
    plt.gca().legend_.remove()