#!/usr/bin/env python3
"""convert pdf to markdown"""
import PyPDF2
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
np.set_printoptions(formatter={'float_kind':'{:f}'.format})
model = hub.load("model/")

def clean_text():
    """returns cleaned text for model"""
    t = ["DIGITAL ADVANCE DIRECTIVE FOR HEALTH CARE", "MEMORIAL SERVICE AND FINAL INSTRUCTIONS", "DURABLE POWER OF ATTORNEY FOR HEALTH CARE"]
    text = []
    txt_list = ["BASE/DIR.txt", "BASE/MEM.txt","BASE/POA.txt"]
    for page, title in zip(txt_list, t):
        with open(page, mode='r') as f:
            text.append(title)
            text.append(f.read())
    text.append("OPTIONAL ADVANCE HEALTH-CARE DIRECTIVE")
    text2 = []
    with open("TEST/1-POA.pdf", mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        for page in reader.pages:
            text2.append(page.extractText())
    word = ""
    for sentence in text2:
        for i, letter in enumerate(sentence):
            if letter != '_':
                word += letter
            if len(word) >= 40 and letter == ' ':
                word = word.replace("\n", "")
                text.append(word)
                word = ""
    return text

def similarity(text):
    """Return similarit between pdf"""
    embed = model(text)
    corr = np.inner(embed, embed)
    score_list = []
    # We use 0 because that is the correlation line
    # that matches our sentence if you were looking
    # at graph with the first index being itself so we must remove it
    
    # for DIR Title
    dt_close = np.argmax(corr[0, 7:])
    dt_perc = corr[0][dt_close + 7]
    # dt_text = text[dt_close + 7]
    # for DIR text
    d_perc = np.mean(corr[1, 7:])
    # d_text = text[d_close + 7]
    dt_alt_close = np.argmax(corr[6, 7:])
    dt_alt_perc = corr[6][dt_alt_close + 7]

    D_alt_score = dt_alt_perc + d_perc
    D_score = dt_perc + d_perc
    if D_alt_score > D_score:
        D_score = D_alt_score
    score_list.append(D_score)

    # for MEM TITLE
    mt_close = np.argmax(corr[2, 7:])
    mt_perc = corr[2][mt_close + 7]
    # mt_text = text[mt_close + 7]
    # for MEM
    m_perc = np.mean(corr[3, 7:])
    # m_text = text[m_close + 7]
    M_score = mt_perc + m_perc
    score_list.append(M_score)

    # for POA TITLE
    pt_close = np.argmax(corr[4, 7:])
    pt_perc = corr[4][pt_close + 7]
    # pt_text = text[pt_close + 7]
    # for POA
    p_perc = np.mean(corr[5, 7:])
    # p_text = text[p_close + 7]
    P_score = pt_perc + p_perc
    score_list.append(P_score)
    index = np.argmax(score_list)
    if score_list[index] >= 0.8:
        if index == 0:
            return "DIR: accuracy={0:.0%}".format(score_list[index])
        elif index == 1:
            return "MEM: accuracy={0:.0%}".format(score_list[index])
        else:
            return "POA: accuracy={0:.0%}".format(score_list[index])
    else:
        return "OTHER FILE"


if __name__ == "__main__":
    text = clean_text()
    sim = similarity(text)
    print(sim)
