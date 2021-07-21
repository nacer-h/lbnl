import os,sys
from ROOT import TH1F, TH2D, TFile, TCanvas, TFile, gROOT, TLegend, gStyle, TGraphErrors, TMath
from math import sqrt
import numpy as np


# ROOT.gInterpreter.Declare('#include "TH1.h"')
# Make the header known to the interpreter
# ROOT.gInterpreter.ProcessLine('#include "my_header.h"')

# Run ROOT in batch mode to avoid losing focus when plotting
gROOT.SetBatch(True)
# modify title and label sizes
gStyle.SetTitleSize(.06, "xyz")
gStyle.SetTitleOffset(1.3, "y")
gStyle.SetLabelSize(.06, "xyz")
gStyle.SetPadTopMargin(0.12)
gStyle.SetPadBottomMargin(0.16)
gStyle.SetPadRightMargin(0.16) # 2d:0.17 , 1d:0.05
gStyle.SetPadLeftMargin(0.16)  # 2d:0.16, 1d:0.15
gStyle.SetOptStat(0)
gStyle.SetLineWidth(2)

## open the input TTree
treeInput = TFile.Open("$PYJETTY_DIR/pyjetty/sandbox/leadsj_vs_x_bias80.root")
t = treeInput.tlsjvsx

## save plots in ROOT file
outputpath = "~/lbl/analysis/output/"
figOutput = TFile(f'{outputpath}/output.root',"UPDATE")

print("script runing ...")

## plot the average Pt for q and g
c_pt_av = TCanvas("c_pt_av", "c_pt_av", 900, 600)
c_pt_av.cd()
h_pt_q = TH1F("h_pt_q", "z_{r}= sjet01_pt/jet_pt;z_{r};Counts", 200, 0, 1)
t.Project("h_pt_q","sjet01_pt./j_pt.","pquark==1")
h_pt_q.SetFillColorAlpha(4, 0.5)
h_pt_g = TH1F("h_pt_g", "z_{r}= sjet01_pt/jet_pt;z_{r};Counts", 200, 0, 1)
t.Project("h_pt_g","sjet01_pt./j_pt.","pglue==1")
h_pt_g.SetFillColorAlpha(2, 0.5)
h_pt_all = TH1F("h_pt_all", "z_{r}= sjet01_pt/jet_pt;z_{r};Counts", 200, 0, 1)
t.Project("h_pt_all","sjet01_pt./j_pt.","")
h_pt_all.SetFillColorAlpha(3, 0.5)
h_pt_all.Draw("hist")
h_pt_g.Draw("hist same")
h_pt_q.Draw("hist same")
h_pt_q.Write()
h_pt_g.Write()
l_pt = TLegend(0.2, 0.6, 0.4, 0.85)
l_pt.SetTextSize(0.05)
l_pt.SetBorderSize(0)
l_pt.AddEntry(h_pt_all, "all", "f")
l_pt.AddEntry(h_pt_q, "quark", "f")
l_pt.AddEntry(h_pt_g, "gluon", "f")
l_pt.Draw()
c_pt_av.Print("~/lbl/analysis/output/c_pt_av.root", "root")
c_pt_av.Print("~/lbl/analysis/output/c_pt_av.pdf", "pdf")

## normalized subjet ratios for each jet type to the total subjets
c_pt_av_norm = TCanvas("c_pt_av_norm", "c_pt_av_norm", 900, 600)
c_pt_av_norm.cd()
h_pt_q_norm = h_pt_q / h_pt_all
h_pt_g_norm = h_pt_g / h_pt_all
h_pt_q_norm.SetFillColorAlpha(4, 0.5)
h_pt_g_norm.SetFillColorAlpha(2, 0.5)
h_pt_g_norm.Draw("hist ")
h_pt_q_norm.Draw("hist same")
h_pt_g_norm.Write()
h_pt_q_norm.Write()
l_pt_norm = TLegend(0.70, 0.76, 0.80, 0.87)
l_pt_norm.SetTextSize(0.05)
l_pt_norm.SetBorderSize(0)
l_pt_norm.AddEntry(h_pt_q_norm, "quark", "f")
l_pt_norm.AddEntry(h_pt_g_norm, "gluon", "f")
l_pt_norm.Draw()
h_pt_g_norm.SetTitle("Normalized z^{q,g}_{r}/z_{r}")
c_pt_av_norm.Print("~/lbl/analysis/output/c_pt_av_norm.root", "root")
c_pt_av_norm.Print("~/lbl/analysis/output/c_pt_av_norm.pdf", "pdf")

## cumulative distribution of q & g subjet ratios
c_pt_av_norm_cum = TCanvas("c_pt_av_norm_cum", "c_pt_av_norm_cum", 900, 600)
c_pt_av_norm_cum.cd()
h_pt_q_cum = h_pt_q.GetCumulative()
h_pt_g_cum = h_pt_g.GetCumulative()
h_pt_q_cum.Scale(1./h_pt_q.Integral())
h_pt_g_cum.Scale(1./h_pt_g.Integral())
h_pt_q_cum.SetLineColor(4)
h_pt_g_cum.SetLineColor(2)
h_pt_g_cum.Draw("hist ")
h_pt_q_cum.Draw("hist same")
h_pt_g_cum.Write()
h_pt_q_cum.Write()
l_pt_norm_cum = TLegend(0.25, 0.76, 0.4, 0.87)
l_pt_norm_cum.SetTextSize(0.05)
l_pt_norm_cum.SetBorderSize(0)
l_pt_norm_cum.AddEntry(h_pt_q_cum, "quark", "f")
l_pt_norm_cum.AddEntry(h_pt_g_cum, "gluon", "f")
l_pt_norm_cum.Draw()
h_pt_g_cum.SetTitle("Normalized CDF of z^{q,g}_{r}")
c_pt_av_norm_cum.Print("~/lbl/analysis/output/c_pt_av_norm_cum.root", "root")
c_pt_av_norm_cum.Print("~/lbl/analysis/output/c_pt_av_norm_cum.pdf", "pdf")

## scatter plot of subjet ratios vs. total jet_Pt
# quark
c_sjet01_pt_q = TCanvas("c_sjet01_pt_q", "c_sjet01_pt_q", 900, 600)
c_sjet01_pt_q.cd()
h2d_sjet01_pt_q = TH2D("h2d_sjet01_pt_q",";P_{t} (GeV/c);z^{q}_{r}",10,80,100,10,0,1)
t.Project("h2d_sjet01_pt_q","sjet01_pt/j_pt:j_pt","pquark==1")
h2d_sjet01_pt_q.Draw("colz")
h2d_sjet01_pt_q.Write()
c_sjet01_pt_q.Print("~/lbl/analysis/output/c_sjet01_pt_q.root", "root")
c_sjet01_pt_q.Print("~/lbl/analysis/output/c_sjet01_pt_q.pdf", "pdf")

# gluon
c_sjet01_pt_g = TCanvas("c_sjet01_pt_g", "c_sjet01_pt_g", 900, 600)
c_sjet01_pt_g.cd()
h2d_sjet01_pt_g = TH2D("h2d_sjet01_pt_g",";P_{t} (GeV/c);z^{g}_{r}",10,80,100,10,0,1)
t.Project("h2d_sjet01_pt_g","sjet01_pt/j_pt:j_pt","pglue==1")
h2d_sjet01_pt_g.Draw("colz")
h2d_sjet01_pt_g.Write()
c_sjet01_pt_g.Print("~/lbl/analysis/output/c_sjet01_pt_g.root", "root")
c_sjet01_pt_g.Print("~/lbl/analysis/output/c_sjet01_pt_g.pdf", "pdf")

## correlation of sof drop (SD) and lund output variables (delta, z) with subjet ratio (zr)

# SD
# z
c_sd_z_zr_all = TCanvas("c_sd_z_zr_all", "c_sd_z_zr_all", 900, 600)
c_sd_z_zr_all.cd()
h2d_sd_z_zr_all = TH2D("h2d_sd_z_zr_all",";z_{r};z_{SD}",10,0,1,10,0.2,0.5)
t.Project("h2d_sd_z_zr_all","sd_z:sjet01_pt/j_pt")
h2d_sd_z_zr_all.Draw("colz")
h2d_sd_z_zr_all.Write()
c_sd_z_zr_all.Print("~/lbl/analysis/output/c_sd_z_zr_all.root", "root")
c_sd_z_zr_all.Print("~/lbl/analysis/output/c_sd_z_zr_all.pdf", "pdf")

# delta
c_sd_delta_zr_all = TCanvas("c_sd_delta_zr_all", "c_sd_delta_zr_all", 900, 600)
c_sd_delta_zr_all.cd()
h2d_sd_delta_zr_all = TH2D("h2d_sd_delta_zr_all",";z_{r};#Delta_{SD}",10,0,1,10,0,0.4)
t.Project("h2d_sd_delta_zr_all","sd_Delta:sjet01_pt/j_pt")
h2d_sd_delta_zr_all.Draw("colz")
h2d_sd_delta_zr_all.Write()
c_sd_delta_zr_all.Print("~/lbl/analysis/output/c_sd_delta_zr_all.root", "root")
c_sd_delta_zr_all.Print("~/lbl/analysis/output/c_sd_delta_zr_all.pdf", "pdf")

# Lund
# z
c_lund_z_zr_all = TCanvas("c_lund_z_zr_all", "c_lund_z_zr_all", 900, 600)
c_lund_z_zr_all.cd()
h2d_lund_z_zr_all = TH2D("h2d_lund_z_zr_all",";z_{r};z_{lund}",10,0,1,10,0,0.5)
t.Project("h2d_lund_z_zr_all","lund_z:sjet01_pt/j_pt")
h2d_lund_z_zr_all.Draw("colz")
h2d_lund_z_zr_all.Write()
c_lund_z_zr_all.Print("~/lbl/analysis/output/c_lund_z_zr_all.root", "root")
c_lund_z_zr_all.Print("~/lbl/analysis/output/c_lund_z_zr_all.pdf", "pdf")

# delta
c_lund_delta_zr_all = TCanvas("c_lund_delta_zr_all", "c_lund_delta_zr_all", 900, 600)
c_lund_delta_zr_all.cd()
h2d_lund_delta_zr_all = TH2D("h2d_lund_delta_zr_all",";z_{r};#Delta_{lund}",10,0,1,10,0,0.4)
t.Project("h2d_lund_delta_zr_all","lund_Delta:sjet01_pt/j_pt")
h2d_lund_delta_zr_all.Draw("colz")
h2d_lund_delta_zr_all.Write()
c_lund_delta_zr_all.Print("~/lbl/analysis/output/c_lund_delta_zr_all.root", "root")
c_lund_delta_zr_all.Print("~/lbl/analysis/output/c_lund_delta_zr_all.pdf", "pdf")

## correlation of Lund output variables for q & g
# lund_Delta vs. lund_z
# quark
c_lund_delta_lund_z_q = TCanvas("c_lund_delta_lund_z_q", "c_lund_delta_lund_z_q", 900, 600)
c_lund_delta_lund_z_q.cd()
h2d_lund_delta_lund_z_q = TH2D("h2d_lund_delta_lund_z_q",";z^{q}_{lund};#Delta^{q}_{lund}",10,0,0.5,10,0,0.4)
t.Project("h2d_lund_delta_lund_z_q","lund_Delta:lund_z","pquark==1")
h2d_lund_delta_lund_z_q.Draw("colz")
h2d_lund_delta_lund_z_q.Write()
c_lund_delta_lund_z_q.Print("~/lbl/analysis/output/c_lund_delta_lund_z_q.root", "root")
c_lund_delta_lund_z_q.Print("~/lbl/analysis/output/c_lund_delta_lund_z_q.pdf", "pdf")

# gluon
c_lund_delta_lund_z_g = TCanvas("c_lund_delta_lund_z_g", "c_lund_delta_lund_z_g", 900, 600)
c_lund_delta_lund_z_g.cd()
h2d_lund_delta_lund_z_g = TH2D("h2d_lund_delta_lund_z_g",";z^{g}_{lund};#Delta^{g}_{lund}",10,0,0.5,10,0,0.4)
t.Project("h2d_lund_delta_lund_z_g","lund_Delta:lund_z","pglue==1")
h2d_lund_delta_lund_z_g.Draw("colz")
h2d_lund_delta_lund_z_g.Write()
c_lund_delta_lund_z_g.Print("~/lbl/analysis/output/c_lund_delta_lund_z_g.root", "root")
c_lund_delta_lund_z_g.Print("~/lbl/analysis/output/c_lund_delta_lund_z_g.pdf", "pdf")

# find optimal zr cut to select q/g

c_zr_cut = TCanvas("c_zr_cut","c_zr_cut",900,600)
c_zr_cut.SetGrid()
gr_zr_cut = TGraphErrors()
gr_zr_cut.SetMinimum(0.)
gr_zr_cut.SetMarkerStyle(20)
gr_zr_cut.GetXaxis().SetNdivisions(515)

zr_min = 0.0 # hdata_postcut.GetXaxis().GetBinLowEdge(1)
zr_max = 1.0 # hdata_postcut.GetXaxis().GetBinUpEdge(200)
zr_step = (zr_max-zr_min) / 40
zr_cut = [zr_min + (i * zr_step) for i in range(40)]
# print(f'zr_cut = {zr_cut}')

h_zr_q = TH1F("h_zr_q", "z_{r}= sjet01_pt/jet_pt;z_{r};Counts", 200, 0, 1)
h_zr_g = TH1F("h_zr_g", "z_{r}= sjet01_pt/jet_pt;z_{r};Counts", 200, 0, 1)

for i in range(len(zr_cut)):
    t.Project("h_zr_q","sjet01_pt./j_pt.", f'pquark==1 && (sjet01_pt./j_pt.)>{zr_cut[i]}')
    t.Project("h_zr_g","sjet01_pt./j_pt.", f'pglue==1 && (sjet01_pt./j_pt.)>{zr_cut[i]}')

    yield_q_err = np.double(0.0)
    yield_g_err = np.double(0.0)
    yield_q = h_zr_q.IntegralAndError(0, h_zr_q.GetNbinsX() + 1, yield_q_err)
    yield_g = h_zr_g.IntegralAndError(0, h_zr_g.GetNbinsX() + 1, yield_g_err)
    q_to_g_ratio = yield_q / yield_g
    q_to_g_ratio_err = q_to_g_ratio * sqrt(((yield_q_err / yield_q) ** 2) + ((yield_g_err / yield_g) ** 2))

    gr_zr_cut.SetPoint(i, zr_cut[i], q_to_g_ratio)
    gr_zr_cut.SetPointError(i, 0, q_to_g_ratio_err)

    # print(f'i = {i} | zr_cut = {zr_cut[i]} | yield_q = {yield_q}\u00B1{yield_q_err} | yield_g = {yield_g}\u00B1{yield_g_err} | significance = {q_to_g_ratio}\u00B1{q_to_g_ratio_err}')

gr_zr_cut.SetTitle("; z_{r} cut; z^{q}_{r}/z^{g}_{r}")
gr_zr_cut.Draw("AP")
gr_zr_cut.Write()
c_zr_cut.Print("~/lbl/analysis/output/c_zr_cut.root", "root")
c_zr_cut.Print("~/lbl/analysis/output/c_zr_cut.pdf", "pdf")

# Soft drop and lund variables after zr cut
# sd_Delta vs. zr
# quark
c_sd_delta_zr_q_postcut = TCanvas("c_sd_delta_zr_q_postcut", "c_sd_delta_zr_q_postcut", 900, 600)
c_sd_delta_zr_q_postcut.cd()
h2d_sd_delta_zr_q_postcut = TH2D("h2d_sd_delta_zr_q_postcut",";z^{q}_{r};#Delta^{q}_{SD}",10,0,1,10,0,0.4)
t.Project("h2d_sd_delta_zr_q_postcut","sd_Delta:sjet01_pt/j_pt","pquark==1 && (sjet01_pt./j_pt.)>0.90")
h2d_sd_delta_zr_q_postcut.Draw("colz")
h2d_sd_delta_zr_q_postcut.Write()
c_sd_delta_zr_q_postcut.Print("~/lbl/analysis/output/c_sd_delta_zr_q_postcut.root", "root")
c_sd_delta_zr_q_postcut.Print("~/lbl/analysis/output/c_sd_delta_zr_q_postcut.pdf", "pdf")

# gluon
c_sd_delta_zr_g_postcut = TCanvas("c_sd_delta_zr_g_postcut", "c_sd_delta_zr_g_postcut", 900, 600)
c_sd_delta_zr_g_postcut.cd()
h2d_sd_delta_zr_g_postcut = TH2D("h2d_sd_delta_zr_g_postcut",";z^{g}_{r};#Delta^{g}_{SD}",10,0,1,10,0,0.4)
t.Project("h2d_sd_delta_zr_g_postcut","sd_Delta:sjet01_pt/j_pt","pglue==1 && (sjet01_pt./j_pt.)<0.90")
h2d_sd_delta_zr_g_postcut.Draw("colz")
h2d_sd_delta_zr_g_postcut.Write()
c_sd_delta_zr_g_postcut.Print("~/lbl/analysis/output/c_sd_delta_zr_g_postcut.root", "root")
c_sd_delta_zr_g_postcut.Print("~/lbl/analysis/output/c_sd_delta_zr_g_postcut.pdf", "pdf")

# lund_Delta vs. lund_z
# quark
c_lund_delta_lund_z_q_postcut = TCanvas("c_lund_delta_lund_z_q_postcut", "c_lund_delta_lund_z_q_postcut", 900, 600)
c_lund_delta_lund_z_q_postcut.cd()
h2d_lund_delta_lund_z_q_postcut = TH2D("h2d_lund_delta_lund_z_q_postcut",";z^{q}_{lund};#Delta^{q}_{lund}",10,0,0.5,10,0,0.4)
t.Project("h2d_lund_delta_lund_z_q_postcut","lund_Delta:lund_z","pquark==1 && (sjet01_pt./j_pt.)>0.90")
h2d_lund_delta_lund_z_q_postcut.Draw("colz")
h2d_lund_delta_lund_z_q_postcut.Write()
c_lund_delta_lund_z_q_postcut.Print("~/lbl/analysis/output/c_lund_delta_lund_z_q_postcut.root", "root")
c_lund_delta_lund_z_q_postcut.Print("~/lbl/analysis/output/c_lund_delta_lund_z_q_postcut.pdf", "pdf")

# gluon
c_lund_delta_lund_z_g_postcut = TCanvas("c_lund_delta_lund_z_g_postcut", "c_lund_delta_lund_z_g_postcut", 900, 600)
c_lund_delta_lund_z_g_postcut.cd()
h2d_lund_delta_lund_z_g_postcut = TH2D("h2d_lund_delta_lund_z_g_postcut",";z^{g}_{lund};#Delta^{g}_{lund}",10,0,0.5,10,0,0.4)
t.Project("h2d_lund_delta_lund_z_g_postcut","lund_Delta:lund_z","pglue==1 && (sjet01_pt./j_pt.)<0.90")
h2d_lund_delta_lund_z_g_postcut.Draw("colz")
h2d_lund_delta_lund_z_g_postcut.Write()
c_lund_delta_lund_z_g_postcut.Print("~/lbl/analysis/output/c_lund_delta_lund_z_g_postcut.root", "root")
c_lund_delta_lund_z_g_postcut.Print("~/lbl/analysis/output/c_lund_delta_lund_z_g_postcut.pdf", "pdf")

## check different zr cuts on z_sd, Delta_sd, z_lund and Delta_lund
## z_sd
c_z_sd = TCanvas("c_z_sd", "c_z_sd", 900, 600)
c_z_sd.cd()
h_z_sd_q = TH1F("h_z_sd_q", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_q","sd_z","pquark==1")
h_z_sd_q.SetLineColor(2)
h_z_sd_g = TH1F("h_z_sd_g", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_g","sd_z","pglue==1")
h_z_sd_g.SetLineColor(4)
h_z_sd_all = TH1F("h_z_sd_all", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_all","sd_z","")
h_z_sd_all.SetLineColor(1)
h_z_sd_all.Draw("hist")
h_z_sd_g.Draw("hist same")
h_z_sd_q.Draw("hist same")
h_z_sd_q.Write()
h_z_sd_g.Write()
l_z_sd = TLegend(0.7, 0.7, 0.83, 0.87)
l_z_sd.SetTextSize(0.05)
l_z_sd.SetBorderSize(0)
l_z_sd.AddEntry(h_z_sd_all, "all", "l")
l_z_sd.AddEntry(h_z_sd_q, "quark", "l")
l_z_sd.AddEntry(h_z_sd_g, "gluon", "l")
l_z_sd.Draw()
c_z_sd.Print("~/lbl/analysis/output/c_z_sd.root", "root")
c_z_sd.Print("~/lbl/analysis/output/c_z_sd.pdf", "pdf")

## z_sd post cuts
c_z_sd_cuts = TCanvas("c_z_sd_cuts", "c_z_sd_cuts", 900, 600)
c_z_sd_cuts.cd()
h_z_sd_095 = TH1F("h_z_sd_095", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_095","sd_z","(sjet01_pt./j_pt.)>0.95")
h_z_sd_095.SetLineColor(2)
h_z_sd_09g = TH1F("h_z_sd_09g", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_09g","sd_z","(sjet01_pt./j_pt.)>0.90")
h_z_sd_09g.SetLineColor(3)
h_z_sd_09l = TH1F("h_z_sd_09l", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_09l","sd_z","(sjet01_pt./j_pt.)<0.90")
h_z_sd_09l.SetLineColor(4)
h_z_sd_0709 = TH1F("h_z_sd_0709", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_0709","sd_z","(sjet01_pt./j_pt.)>0.70 && (sjet01_pt./j_pt.)<0.90")
h_z_sd_0709.SetLineColor(46)
h_z_sd_0307 = TH1F("h_z_sd_0307", ";z_{SD};Counts", 200, 0.19, 0.51)
t.Project("h_z_sd_0307","sd_z","(sjet01_pt./j_pt.)>0.30 && (sjet01_pt./j_pt.)<0.70")
h_z_sd_0307.SetLineColor(6)
h_z_sd_all.Draw("hist")
h_z_sd_095.Draw("hist same")
h_z_sd_09g.Draw("hist same")
h_z_sd_09l.Draw("hist same")
h_z_sd_0709.Draw("hist same")
h_z_sd_0307.Draw("hist same")
h_z_sd_all.Write()
h_z_sd_095.Write()
h_z_sd_09g.Write()
h_z_sd_09l.Write()
h_z_sd_0709.Write()
h_z_sd_0307.Write()
l_z_sd = TLegend(0.67, 0.6, 0.78, 0.87)
l_z_sd.SetTextSize(0.05)
l_z_sd.SetBorderSize(0)
l_z_sd.AddEntry(h_z_sd_all, "all", "l")
l_z_sd.AddEntry(h_z_sd_095, "z_{r}>0.95", "l")
l_z_sd.AddEntry(h_z_sd_09g, "z_{r}>0.90", "l")
l_z_sd.AddEntry(h_z_sd_09l, "z_{r}<0.90", "l")
l_z_sd.AddEntry(h_z_sd_0709, "0.7<z_{r}<0.9", "l")
l_z_sd.AddEntry(h_z_sd_0307, "0.3<z_{r}<0.7", "l")
l_z_sd.Draw()
c_z_sd_cuts.Print("~/lbl/analysis/output/c_z_sd_cuts.root", "root")
c_z_sd_cuts.Print("~/lbl/analysis/output/c_z_sd_cuts.pdf", "pdf")

## z_lund
c_z_lund = TCanvas("c_z_lund", "c_z_lund", 900, 600)
c_z_lund.SetLogy()
c_z_lund.cd()
h_z_lund_q = TH1F("h_z_lund_q", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_q","lund_z","pquark==1")
h_z_lund_q.SetLineColor(2)
h_z_lund_g = TH1F("h_z_lund_g", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_g","lund_z","pglue==1")
h_z_lund_g.SetLineColor(4)
h_z_lund_all = TH1F("h_z_lund_all", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_all","lund_z","")
h_z_lund_all.SetLineColor(1)
h_z_lund_all.SetMinimum(1.0)
h_z_lund_all.Draw("hist")
h_z_lund_g.Draw("hist same")
h_z_lund_q.Draw("hist same")
h_z_lund_q.Write()
h_z_lund_g.Write()
l_z_lund = TLegend(0.7, 0.7, 0.83, 0.87)
l_z_lund.SetTextSize(0.05)
l_z_lund.SetBorderSize(0)
l_z_lund.AddEntry(h_z_lund_all, "all", "l")
l_z_lund.AddEntry(h_z_lund_q, "quark", "l")
l_z_lund.AddEntry(h_z_lund_g, "gluon", "l")
l_z_lund.Draw()
c_z_lund.Print("~/lbl/analysis/output/c_z_lund.root", "root")
c_z_lund.Print("~/lbl/analysis/output/c_z_lund.pdf", "pdf")

## z_lund post cuts
c_z_lund_cuts = TCanvas("c_z_lund_cuts", "c_z_lund_cuts", 900, 600)
c_z_lund_cuts.SetLogy()
c_z_lund_cuts.cd()
h_z_lund_095 = TH1F("h_z_lund_095", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_095","lund_z","(sjet01_pt./j_pt.)>0.95")
h_z_lund_095.SetLineColor(2)
h_z_lund_09g = TH1F("h_z_lund_09g", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_09g","lund_z","(sjet01_pt./j_pt.)>0.90")
h_z_lund_09g.SetLineColor(3)
h_z_lund_09l = TH1F("h_z_lund_09l", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_09l","lund_z","(sjet01_pt./j_pt.)<0.90")
h_z_lund_09l.SetLineColor(4)
h_z_lund_0709 = TH1F("h_z_lund_0709", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_0709","lund_z","(sjet01_pt./j_pt.)>0.70 && (sjet01_pt./j_pt.)<0.90")
h_z_lund_0709.SetLineColor(46)
h_z_lund_0307 = TH1F("h_z_lund_0307", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_0307","lund_z","(sjet01_pt./j_pt.)>0.30 && (sjet01_pt./j_pt.)<0.70")
h_z_lund_0307.SetLineColor(6)
h_z_lund_all.SetMinimum(1.0)
h_z_lund_all.Draw("hist")
h_z_lund_095.Draw("hist same")
h_z_lund_09g.Draw("hist same")
h_z_lund_09l.Draw("hist same")
h_z_lund_0709.Draw("hist same")
h_z_lund_0307.Draw("hist same")
h_z_lund_all.Write()
h_z_lund_095.Write()
h_z_lund_09g.Write()
h_z_lund_09l.Write()
h_z_lund_0709.Write()
h_z_lund_0307.Write()
l_z_lund = TLegend(0.67, 0.6, 0.78, 0.87)
l_z_lund.SetTextSize(0.05)
l_z_lund.SetBorderSize(0)
l_z_lund.AddEntry(h_z_lund_all, "all", "l")
l_z_lund.AddEntry(h_z_lund_095, "z_{r}>0.95", "l")
l_z_lund.AddEntry(h_z_lund_09g, "z_{r}>0.90", "l")
l_z_lund.AddEntry(h_z_lund_09l, "z_{r}<0.90", "l")
l_z_lund.AddEntry(h_z_lund_0709, "0.7<z_{r}<0.9", "l")
l_z_lund.AddEntry(h_z_lund_0307, "0.3<z_{r}<0.7", "l")
l_z_lund.Draw()
c_z_lund_cuts.Print("~/lbl/analysis/output/c_z_lund_cuts.root", "root")
c_z_lund_cuts.Print("~/lbl/analysis/output/c_z_lund_cuts.pdf", "pdf")

## Delta_sd
c_Delta_sd = TCanvas("c_Delta_sd", "c_Delta_sd", 900, 600)
c_Delta_sd.cd()
c_Delta_sd.SetLogy()
h_Delta_sd_q = TH1F("h_Delta_sd_q", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_q","sd_Delta","pquark==1")
h_Delta_sd_q.SetLineColor(2)
h_Delta_sd_g = TH1F("h_Delta_sd_g", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_g","sd_Delta","pglue==1")
h_Delta_sd_g.SetLineColor(4)
h_Delta_sd_all = TH1F("h_Delta_sd_all", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_all","sd_Delta","")
h_Delta_sd_all.SetLineColor(1)
h_Delta_sd_all.SetMinimum(1.0)
h_Delta_sd_all.Draw("hist")
h_Delta_sd_g.Draw("hist same")
h_Delta_sd_q.Draw("hist same")
h_Delta_sd_q.Write()
h_Delta_sd_g.Write()
l_Delta_sd = TLegend(0.7, 0.7, 0.83, 0.87)
l_Delta_sd.SetTextSize(0.05)
l_Delta_sd.SetBorderSize(0)
l_Delta_sd.AddEntry(h_Delta_sd_all, "all", "l")
l_Delta_sd.AddEntry(h_Delta_sd_q, "quark", "l")
l_Delta_sd.AddEntry(h_Delta_sd_g, "gluon", "l")
l_Delta_sd.Draw()
c_Delta_sd.Print("~/lbl/analysis/output/c_Delta_sd.root", "root")
c_Delta_sd.Print("~/lbl/analysis/output/c_Delta_sd.pdf", "pdf")

## Delta_sd post cuts
c_Delta_sd_cuts = TCanvas("c_Delta_sd_cuts", "c_Delta_sd_cuts", 900, 600)
c_Delta_sd_cuts.cd()
c_Delta_sd_cuts.SetLogy()
h_Delta_sd_095 = TH1F("h_Delta_sd_095", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_095","sd_Delta","(sjet01_pt./j_pt.)>0.95")
h_Delta_sd_095.SetLineColor(2)
h_Delta_sd_09g = TH1F("h_Delta_sd_09g", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_09g","sd_Delta","(sjet01_pt./j_pt.)>0.90")
h_Delta_sd_09g.SetLineColor(3)
h_Delta_sd_09l = TH1F("h_Delta_sd_09l", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_09l","sd_Delta","(sjet01_pt./j_pt.)<0.90")
h_Delta_sd_09l.SetLineColor(4)
h_Delta_sd_0709 = TH1F("h_Delta_sd_0709", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_0709","sd_Delta","(sjet01_pt./j_pt.)>0.70 && (sjet01_pt./j_pt.)<0.90")
h_Delta_sd_0709.SetLineColor(46)
h_Delta_sd_0307 = TH1F("h_Delta_sd_0307", ";#Delta_{SD};Counts", 200, 0, 0.4)
t.Project("h_Delta_sd_0307","sd_Delta","(sjet01_pt./j_pt.)>0.30 && (sjet01_pt./j_pt.)<0.70")
h_Delta_sd_0307.SetLineColor(6)
h_Delta_sd_all.SetMinimum(1.0)
h_Delta_sd_all.Draw("hist")
h_Delta_sd_095.Draw("hist same")
h_Delta_sd_09g.Draw("hist same")
h_Delta_sd_09l.Draw("hist same")
h_Delta_sd_0709.Draw("hist same")
h_Delta_sd_0307.Draw("hist same")
h_Delta_sd_all.Write()
h_Delta_sd_095.Write()
h_Delta_sd_09g.Write()
h_Delta_sd_09l.Write()
h_Delta_sd_0709.Write()
h_Delta_sd_0307.Write()
l_Delta_sd = TLegend(0.67, 0.6, 0.78, 0.87)
l_Delta_sd.SetTextSize(0.05)
l_Delta_sd.SetBorderSize(0)
l_Delta_sd.AddEntry(h_Delta_sd_all, "all", "l")
l_Delta_sd.AddEntry(h_Delta_sd_095, "z_{r}>0.95", "l")
l_Delta_sd.AddEntry(h_Delta_sd_09g, "z_{r}>0.90", "l")
l_Delta_sd.AddEntry(h_Delta_sd_09l, "z_{r}<0.90", "l")
l_Delta_sd.AddEntry(h_Delta_sd_0709, "0.7<z_{r}<0.9", "l")
l_Delta_sd.AddEntry(h_Delta_sd_0307, "0.3<z_{r}<0.7", "l")
l_Delta_sd.Draw()
c_Delta_sd_cuts.Print("~/lbl/analysis/output/c_Delta_sd_cuts.root", "root")
c_Delta_sd_cuts.Print("~/lbl/analysis/output/c_Delta_sd_cuts.pdf", "pdf")

## Delta_lund
c_Delta_lund = TCanvas("c_Delta_lund", "c_Delta_lund", 900, 600)
c_Delta_lund.cd()
c_Delta_lund.SetLogy()
h_Delta_lund_q = TH1F("h_Delta_lund_q", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_q","lund_Delta","pquark==1")
h_Delta_lund_q.SetLineColor(2)
h_Delta_lund_g = TH1F("h_Delta_lund_g", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_g","lund_Delta","pglue==1")
h_Delta_lund_g.SetLineColor(4)
h_Delta_lund_all = TH1F("h_Delta_lund_all", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_all","lund_Delta","")
h_Delta_lund_all.SetLineColor(1)
h_Delta_lund_all.SetMinimum(1.0)
h_Delta_lund_all.Draw("hist")
h_Delta_lund_g.Draw("hist same")
h_Delta_lund_q.Draw("hist same")
h_Delta_lund_q.Write()
h_Delta_lund_g.Write()
l_Delta_lund = TLegend(0.7, 0.7, 0.83, 0.87)
l_Delta_lund.SetTextSize(0.05)
l_Delta_lund.SetBorderSize(0)
l_Delta_lund.AddEntry(h_Delta_lund_all, "all", "l")
l_Delta_lund.AddEntry(h_Delta_lund_q, "quark", "l")
l_Delta_lund.AddEntry(h_Delta_lund_g, "gluon", "l")
l_Delta_lund.Draw()
c_Delta_lund.Print("~/lbl/analysis/output/c_Delta_lund.root", "root")
c_Delta_lund.Print("~/lbl/analysis/output/c_Delta_lund.pdf", "pdf")

## Delta_lund post cuts
c_Delta_lund_cuts = TCanvas("c_Delta_lund_cuts", "c_Delta_lund_cuts", 900, 600)
c_Delta_lund_cuts.cd()
c_Delta_lund_cuts.SetLogy()
h_Delta_lund_095 = TH1F("h_Delta_lund_095", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_095","lund_Delta","(sjet01_pt./j_pt.)>0.95")
h_Delta_lund_095.SetLineColor(2)
h_Delta_lund_09g = TH1F("h_Delta_lund_09g", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_09g","lund_Delta","(sjet01_pt./j_pt.)>0.90")
h_Delta_lund_09g.SetLineColor(3)
h_Delta_lund_09l = TH1F("h_Delta_lund_09l", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_09l","lund_Delta","(sjet01_pt./j_pt.)<0.90")
h_Delta_lund_09l.SetLineColor(4)
h_Delta_lund_0709 = TH1F("h_Delta_lund_0709", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_0709","lund_Delta","(sjet01_pt./j_pt.)>0.70 && (sjet01_pt./j_pt.)<0.90")
h_Delta_lund_0709.SetLineColor(46)
h_Delta_lund_0307 = TH1F("h_Delta_lund_0307", ";#Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_0307","lund_Delta","(sjet01_pt./j_pt.)>0.30 && (sjet01_pt./j_pt.)<0.70")
h_Delta_lund_0307.SetLineColor(6)
h_Delta_lund_all.SetMinimum(1.0)
h_Delta_lund_all.Draw("hist")
h_Delta_lund_095.Draw("hist same")
h_Delta_lund_09g.Draw("hist same")
h_Delta_lund_09l.Draw("hist same")
h_Delta_lund_0709.Draw("hist same")
h_Delta_lund_0307.Draw("hist same")
h_Delta_lund_all.Write()
h_Delta_lund_095.Write()
h_Delta_lund_09g.Write()
h_Delta_lund_09l.Write()
h_Delta_lund_0709.Write()
h_Delta_lund_0307.Write()
l_Delta_lund = TLegend(0.67, 0.6, 0.78, 0.87)
l_Delta_lund.SetTextSize(0.05)
l_Delta_lund.SetBorderSize(0)
l_Delta_lund.AddEntry(h_Delta_lund_all, "all", "l")
l_Delta_lund.AddEntry(h_Delta_lund_095, "z_{r}>0.95", "l")
l_Delta_lund.AddEntry(h_Delta_lund_09g, "z_{r}>0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_09l, "z_{r}<0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_0709, "0.7<z_{r}<0.9", "l")
l_Delta_lund.AddEntry(h_Delta_lund_0307, "0.3<z_{r}<0.7", "l")
l_Delta_lund.Draw()
c_Delta_lund_cuts.Print("~/lbl/analysis/output/c_Delta_lund_cuts.root", "root")
c_Delta_lund_cuts.Print("~/lbl/analysis/output/c_Delta_lund_cuts.pdf", "pdf")

## selected region/ (all, q, g)
## all
c_Delta_lund_ratio_all_cuts = TCanvas("c_Delta_lund_ratio_all_cuts", "c_Delta_lund_ratio_all_cuts", 900, 600)
c_Delta_lund_ratio_all_cuts.cd()
c_Delta_lund_ratio_all_cuts.SetLogy()
h_Delta_lund_ratio_all_095 = h_Delta_lund_095 / h_Delta_lund_all
h_Delta_lund_ratio_all_095.SetLineColor(2)
h_Delta_lund_ratio_all_09g = h_Delta_lund_09g / h_Delta_lund_all
h_Delta_lund_ratio_all_09g.SetLineColor(3)
h_Delta_lund_ratio_all_09l = h_Delta_lund_09l / h_Delta_lund_all
h_Delta_lund_ratio_all_09l.SetTitle("Total subjets;#Delta_{lund};#Delta^{postcut}_{lund, all}/#Delta_{lund, all}")
h_Delta_lund_ratio_all_09l.SetLineColor(4)
h_Delta_lund_ratio_all_0709 = h_Delta_lund_0709 / h_Delta_lund_all
h_Delta_lund_ratio_all_0709.SetLineColor(46)
h_Delta_lund_ratio_all_0307 = h_Delta_lund_0307 / h_Delta_lund_all
h_Delta_lund_ratio_all_0307.SetLineColor(6)
h_Delta_lund_ratio_all_09l.Draw("hist")
h_Delta_lund_ratio_all_095.Draw("hist same")
h_Delta_lund_ratio_all_09g.Draw("hist same")
h_Delta_lund_ratio_all_0709.Draw("hist same")
h_Delta_lund_ratio_all_0307.Draw("hist same")
h_Delta_lund_ratio_all_095.Write()
h_Delta_lund_ratio_all_09g.Write()
h_Delta_lund_ratio_all_09l.Write()
h_Delta_lund_ratio_all_0709.Write()
h_Delta_lund_ratio_all_0307.Write()
l_Delta_lund = TLegend(0.2, 0.6, 0.4, 0.85)
l_Delta_lund.SetTextSize(0.05)
l_Delta_lund.SetBorderSize(0)
l_Delta_lund.AddEntry(h_Delta_lund_ratio_all_095, "z_{r}>0.95", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_all_09g, "z_{r}>0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_all_09l, "z_{r}<0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_all_0709, "0.7<z_{r}<0.9", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_all_0307, "0.3<z_{r}<0.7", "l")
l_Delta_lund.Draw()
c_Delta_lund_ratio_all_cuts.Print("~/lbl/analysis/output/c_Delta_lund_ratio_all_cuts.root", "root")
c_Delta_lund_ratio_all_cuts.Print("~/lbl/analysis/output/c_Delta_lund_ratio_all_cuts.pdf", "pdf")

## quarks
c_Delta_lund_ratio_q_cuts = TCanvas("c_Delta_lund_ratio_q_cuts", "c_Delta_lund_ratio_q_cuts", 900, 600)
c_Delta_lund_ratio_q_cuts.cd()
# c_Delta_lund_ratio_q_cuts.SetLogy()
h_Delta_lund_ratio_q_095 = h_Delta_lund_095 / h_Delta_lund_q
h_Delta_lund_ratio_q_095.SetLineColor(2)
h_Delta_lund_ratio_q_09g = h_Delta_lund_09g / h_Delta_lund_q
h_Delta_lund_ratio_q_09g.SetLineColor(3)
h_Delta_lund_ratio_q_09l = h_Delta_lund_09l / h_Delta_lund_q
h_Delta_lund_ratio_q_09l.SetTitle("quark subjets;#Delta_{lund};#Delta^{postcut}_{lund,all}/#Delta_{lund,q}")
h_Delta_lund_ratio_q_09l.SetLineColor(4)
h_Delta_lund_ratio_q_0709 = h_Delta_lund_0709 / h_Delta_lund_q
h_Delta_lund_ratio_q_0709.SetLineColor(46)
h_Delta_lund_ratio_q_0307 = h_Delta_lund_0307 / h_Delta_lund_q
h_Delta_lund_ratio_q_0307.SetLineColor(6)
h_Delta_lund_ratio_q_09l.Draw("hist")
h_Delta_lund_ratio_q_095.Draw("hist same")
h_Delta_lund_ratio_q_09g.Draw("hist same")
h_Delta_lund_ratio_q_0709.Draw("hist same")
h_Delta_lund_ratio_q_0307.Draw("hist same")
h_Delta_lund_ratio_q_095.Write()
h_Delta_lund_ratio_q_09g.Write()
h_Delta_lund_ratio_q_09l.Write()
h_Delta_lund_ratio_q_0709.Write()
h_Delta_lund_ratio_q_0307.Write()
l_Delta_lund = TLegend(0.2, 0.6, 0.4, 0.85)
l_Delta_lund.SetTextSize(0.05)
l_Delta_lund.SetBorderSize(0)
l_Delta_lund.AddEntry(h_Delta_lund_ratio_q_095, "z_{r}>0.95", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_q_09g, "z_{r}>0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_q_09l, "z_{r}<0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_q_0709, "0.7<z_{r}<0.9", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_q_0307, "0.3<z_{r}<0.7", "l")
l_Delta_lund.Draw()
c_Delta_lund_ratio_q_cuts.Print("~/lbl/analysis/output/c_Delta_lund_ratio_q_cuts.root", "root")
c_Delta_lund_ratio_q_cuts.Print("~/lbl/analysis/output/c_Delta_lund_ratio_q_cuts.pdf", "pdf")

## gluons
c_Delta_lund_ratio_g_cuts = TCanvas("c_Delta_lund_ratio_g_cuts", "c_Delta_lund_ratio_g_cuts", 900, 600)
c_Delta_lund_ratio_g_cuts.cd()
c_Delta_lund_ratio_g_cuts.SetLogy()
h_Delta_lund_ratio_g_095 = h_Delta_lund_095 / h_Delta_lund_g
h_Delta_lund_ratio_g_095.SetLineColor(2)
h_Delta_lund_ratio_g_09g = h_Delta_lund_09g / h_Delta_lund_g
h_Delta_lund_ratio_g_09g.SetLineColor(3)
h_Delta_lund_ratio_g_09g.SetTitle("gluons subjets;#Delta_{lund};#Delta^{postcut}_{lund,all}/#Delta_{lund,g}")
h_Delta_lund_ratio_g_09l = h_Delta_lund_09l / h_Delta_lund_g
h_Delta_lund_ratio_g_09l.SetLineColor(4)
h_Delta_lund_ratio_g_0709 = h_Delta_lund_0709 / h_Delta_lund_g
h_Delta_lund_ratio_g_0709.SetLineColor(46)
h_Delta_lund_ratio_g_0307 = h_Delta_lund_0307 / h_Delta_lund_g
h_Delta_lund_ratio_g_0307.SetLineColor(6)
h_Delta_lund_ratio_g_09g.Draw("hist")
h_Delta_lund_ratio_g_09l.Draw("hist same")
h_Delta_lund_ratio_g_095.Draw("hist same")
h_Delta_lund_ratio_g_0709.Draw("hist same")
h_Delta_lund_ratio_g_0307.Draw("hist same")
h_Delta_lund_ratio_g_095.Write()
h_Delta_lund_ratio_g_09g.Write()
h_Delta_lund_ratio_g_09l.Write()
h_Delta_lund_ratio_g_0709.Write()
h_Delta_lund_ratio_g_0307.Write()
l_Delta_lund = TLegend(0.67, 0.6, 0.78, 0.87)
l_Delta_lund.SetTextSize(0.05)
l_Delta_lund.SetBorderSize(0)
l_Delta_lund.AddEntry(h_Delta_lund_ratio_g_095, "z_{r}>0.95", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_g_09g, "z_{r}>0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_g_09l, "z_{r}<0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_g_0709, "0.7<z_{r}<0.9", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ratio_g_0307, "0.3<z_{r}<0.7", "l")
l_Delta_lund.Draw()
c_Delta_lund_ratio_g_cuts.Print("~/lbl/analysis/output/c_Delta_lund_ratio_g_cuts.root", "root")
c_Delta_lund_ratio_g_cuts.Print("~/lbl/analysis/output/c_Delta_lund_ratio_g_cuts.pdf", "pdf")

## subjet selection with kt_lund and zr
c_kt = TCanvas("c_kt","c_kt",900,600)
c_kt.cd()
h_kt = TH1F("h_kt",";k_{T};Counts",100, -6, 6)
t.Project("h_kt","lund_kt")
h_kt.Draw()
h_kt.Write()
c_kt.Print("~/lbl/analysis/output/c_kt.root", "root")
c_kt.Print("~/lbl/analysis/output/c_kt.pdf", "pdf")

## z_lund post kt and zr cuts
c_z_lund_cuts_2= TCanvas("c_z_lund_cuts_2", "c_z_lund_cuts_2", 900, 600)
c_z_lund_cuts_2.cd()
c_z_lund_cuts_2.SetLogy()
h_z_lund_ktcut = TH1F("h_z_lund_ktcut", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_ktcut","lund_z","log(lund_kt)>0.0")
h_z_lund_ktcut.SetLineColor(4)
h_z_lund_zrktcut = TH1F("h_z_lund_zrktcut", ";z_{lund};Counts", 200, 0, 0.5)
t.Project("h_z_lund_zrktcut","lund_z","(sjet01_pt./j_pt.)>0.90 && log(lund_kt)>0.0")
h_z_lund_zrktcut.SetLineColor(6)
h_z_lund_all.SetMinimum(1.0)
h_z_lund_all.Draw("hist")
h_z_lund_09g.Draw("hist same")
h_z_lund_ktcut.Draw("hist same")
h_z_lund_zrktcut.Draw("hist same")
h_z_lund_ktcut.Write()
h_z_lund_zrktcut.Write()
l_z_lund = TLegend(0.67, 0.6, 0.78, 0.87)
l_z_lund.SetTextSize(0.05)
l_z_lund.SetBorderSize(0)
l_z_lund.AddEntry(h_z_lund_all, "all", "l")
l_z_lund.AddEntry(h_z_lund_09g, "z_{r}>0.90", "l")
l_z_lund.AddEntry(h_z_lund_ktcut, "ln(k_{T})>0", "l")
l_z_lund.AddEntry(h_z_lund_zrktcut, "z_{r}>0.90 and ln(k_{T})>0", "l")
l_z_lund.Draw()
c_z_lund_cuts_2.Print("~/lbl/analysis/output/c_z_lund_cuts_2.root", "root")
c_z_lund_cuts_2.Print("~/lbl/analysis/output/c_z_lund_cuts_2.pdf", "pdf")

## Delta_lund post kt and zr cuts
c_Delta_lund_cuts_2= TCanvas("c_Delta_lund_cuts_2", "c_Delta_lund_cuts_2", 900, 600)
c_Delta_lund_cuts_2.cd()
c_Delta_lund_cuts_2.SetLogy()
h_Delta_lund_ktcut = TH1F("h_Delta_lund_ktcut", ";Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_ktcut","lund_Delta","log(lund_kt)>0.0")
h_Delta_lund_ktcut.SetLineColor(4)
h_Delta_lund_zrktcut = TH1F("h_Delta_lund_zrktcut", ";Delta_{lund};Counts", 200, 0, 0.4)
t.Project("h_Delta_lund_zrktcut","lund_Delta","(sjet01_pt./j_pt.)>0.90 && log(lund_kt)>0.0")
h_Delta_lund_zrktcut.SetLineColor(6)
h_Delta_lund_all.SetMinimum(1.0)
h_Delta_lund_all.Draw("hist")
h_Delta_lund_09g.Draw("hist same")
h_Delta_lund_ktcut.Draw("hist same")
h_Delta_lund_zrktcut.Draw("hist same")
h_Delta_lund_ktcut.Write()
h_Delta_lund_zrktcut.Write()
l_Delta_lund = TLegend(0.67, 0.6, 0.78, 0.87)
l_Delta_lund.SetTextSize(0.05)
l_Delta_lund.SetBorderSize(0)
l_Delta_lund.AddEntry(h_Delta_lund_all, "all", "l")
l_Delta_lund.AddEntry(h_Delta_lund_09g, "z_{r}>0.90", "l")
l_Delta_lund.AddEntry(h_Delta_lund_ktcut, "ln(k_{T})>0", "l")
l_Delta_lund.AddEntry(h_Delta_lund_zrktcut, "z_{r}>0.90 and ln(k_{T})>0", "l")
l_Delta_lund.Draw()
c_Delta_lund_cuts_2.Print("~/lbl/analysis/output/c_Delta_lund_cuts_2.root", "root")
c_Delta_lund_cuts_2.Print("~/lbl/analysis/output/c_Delta_lund_cuts_2.pdf", "pdf")


