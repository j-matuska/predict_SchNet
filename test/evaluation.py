#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 00:23:46 2024

@author: jamat
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot


class run_stats:
    def __init__(self, 
                 hyperparameters, 
                 name,
                 original,
                 predicted
                 ):
        self.hyperparameters = hyperparameters
        self.name = np.asarray(name, dtype = np.str_)
        self.original = np.asarray(original, dtype=np.float64)
        self.predicted = np.asarray(predicted, dtype=np.float64)
        #self.calculate_all()
    
    def log_print(self):
        
        print(self.predicted)
        print(self.mse_ds)
        print(self.mse)
        print(self.sigma)
    
    def calculate_MSE(self):
        """
        Calculation of MSE from set.
        
        Parameters
        ----------
        original: array
            Original data
        predicted: array
            Predicted data
    
        Returns
        -------
        mse : float
            Mean square error.
    
        """
        #remove_outliers = np.abs(np.subtract(self.original, self.predicted)) < 200 
        #remove_outliers = np.ones_like(self.original, dtype = np.bool_)
        mse = np.nanmean(np.square(np.subtract(self.original, self.predicted)), axis = 1)

        return mse
        
    def calculate_sigma(self):
        """
        Calculation of standard deviation from set.
        
        Parameters
        ----------
        original: array
            Original data
        predicted: array
            Predicted data
    
        Returns
        -------
        sigma : float
            Standard deviation.
    
        """
        #remove_outliers = np.abs(np.subtract(self.original, self.predicted)) < 200 
        #remove_outliers = np.ones_like(self.original, dtype = np.bool_)
        sigma = np.nanstd(np.subtract(self.original, self.predicted),ddof=1 , axis = 1)
        
        return sigma
    

    def calculate_DS_gaussian(self):
        """
        Calculate data for analysis of the prediction erorrs as a function of docking score (DS).

        Returns
        -------
        intervaly : array
            Bins defining intervals of the DS
        mse_ds : array of shape splits x intervaly.size - 1
            Contains mse calculated on intervals defined above.
        rel_pocet_ds : array of shape intervaly.size - 1
            Relative abundance of molecules in DS intervals.
        mu_ds : array of shape splits x intervaly.size - 1
            Average error of the prediction.
        sigma_ds : array of shape splits x intervaly.size - 1
            Standard deviation of error of prediction.
        fraction_pocet_ds : array of shape splits x intervaly.size - 1
            Fraction of molecules with error above 2 kcal/mol.

        """
        
        AD_min=-15
        AD_max=1
        intervaly = np.linspace(AD_min, AD_max, 9)
        
        error = np.subtract(self.original, self.predicted)
        # MAE
        ae = np.absolute(error)
        
        try: 
            n_splits,n_molecules = error.shape
        except:
            n_splits = 1
        
        
        #print(n_splits,n_molecules)
        
        sigma_ds = np.zeros((n_splits,intervaly.size-1), dtype=np.float_)
        mu_ds = np.zeros((n_splits,intervaly.size-1), dtype=np.float_)
        mse_ds = np.zeros((n_splits,intervaly.size-1), dtype=np.float_)
        pocet_ds = np.zeros((n_splits,intervaly.size-1), dtype=np.int_)
        fraction_pocet_ds = np.zeros((n_splits,intervaly.size-1), dtype=np.float_)
        rel_pocet_ds = np.zeros(intervaly.size-1, dtype=np.float_)
        
        for i in np.arange(intervaly.size-1):
            
            umiestnenie_bool = np.logical_and(self.original > intervaly[i], self.original <= intervaly[i+1])
            if i == 0: # ak menej ako najmenej, tak priradit do najmensej kategorie
                doplnok = (self.original < intervaly[i])
                umiestnenie_bool[doplnok] = True
            if i == intervaly.size-2: #ak viacej ako najviac, tak priradit do najvacsej kategorie
                doplnok = (self.original > intervaly[i+1])
                umiestnenie_bool[doplnok] = True
            umiestnenie = np.where(umiestnenie_bool)
            rel_pocet_ds[i] = np.count_nonzero(umiestnenie_bool)/umiestnenie_bool.size    
            sigma_ds[:,i] = np.nanstd(error[:,umiestnenie[0]], ddof = 0, axis = 1) #zmenil som ddof 1 na 0, lebo to nefungovalo ak tam ostala iba jedna polozka
            mu_ds[:,i] = np.nanmean(error[:,umiestnenie[0]], axis = 1)
            mse_ds[:,i] = np.nanmean(np.square(error[:,umiestnenie[0]]), axis = 1)
            pocet_ds[:,i] = np.count_nonzero(ae[:,umiestnenie[0]] > 2.0, axis = 1)
            fraction_pocet_ds[:,i] = pocet_ds[:,i]/umiestnenie[0].size
     
        return intervaly, mse_ds, rel_pocet_ds, mu_ds, sigma_ds, fraction_pocet_ds
    
    def calculate_all(self, threshold = -8.6):
        """
        Calculate of possible properties of the prediction accuracy.

        Parameters
        ----------
        threshold : float, optional
            Threshold for confution matrix. The default is -8.6.

        Returns
        -------
        None.

        """
        
        #n_split, n_molecules = self.predicted.shape
        #print(n_split, n_molecules)
        
        #mse = []
        #slope = []
        #intercept = []
        #R2 = []
        recall = []
        specificity = []
        precision = []

        #intervaly = []
        #mse_ds = []
        #rel_pocet_ds = []
        #mu_ds = []
        #sigma_ds = []
        #fraction_over_2_ds = []
        
        recall_PRC = []
        precision_PRC = []
        
        self.mse = self.calculate_MSE()
        self.sigma = self.calculate_sigma()
        #slope0, intercept0, R20 = self.calculate_LSQM()
        
        #slope.append(slope0)
        #intercept.append(intercept0)
        #R2.append(R20)
        
        # recall0, specificity0, precision0 = calculate_classification_statistics(o, p, threshold)
        
        # recall.append(recall0)
        # specificity.append(specificity0)
        # precision.append(precision0)
        
        self.intervaly, self.mse_ds, self.rel_pocet_ds, self.mu_ds, self.sigma_ds, self.fraction_over_2_ds = self.calculate_DS_gaussian()
        
        #intervaly.append(intervaly0)
        #mse_ds.append(mse_ds0)
        #rel_pocet_ds.append(rel_pocet_ds0)
        #mu_ds.append(mu_ds0)
        #sigma_ds.append(sigma_ds0)
        #fraction_over_2_ds.append(fraction_over_2_ds0)
        
        #PRC_recall, PRC_precision, baseline =  calculate_PRC(o, p, threshold)
        
        #recall_PRC.append(PRC_recall)
        #precision_PRC.append(PRC_precision)
            
        #self.mse =np.array(mse)
        #self.slope =np.array(slope)
        #self.intercept =np.array(intercept)
        #self.R2 =np.array(R2)
        #self.intervaly = np.array(intervaly)
        #self.mse_ds =np.array(mse_ds)
        #self.rel_pocet_ds =np.array(rel_pocet_ds)
        #self.mu_ds =np.array(mu_ds)
        #self.sigma_ds =np.array(sigma_ds)
        #self.fraction_pocet_ds =np.array(fraction_over_2_ds)
        self.recall = np.array(recall)
        self.specificity = np.array(specificity)
        self.precision = np.array(precision)
        self.recall_thr_dependence =np.array(recall_PRC)
        self.precision_thr_dependence =np.array(precision_PRC)
        #self.baseline = float(baseline)
        
    def get_ensemble_variance(self):
        """
        Calculate mean and variance of docking score prediction for each molecule.

        Returns
        -------
        predicted_mean : array
            Mean of the docking score prediction.
        predicted_var : array
            Variance of the docking score prediction.

        """
        
        print(self.predicted.shape)
        predicted_mean = self.predicted.mean(axis=0)
        predicted_var = self.predicted.var(axis=0, ddof=1)
        print(predicted_mean,predicted_var)
        
        return predicted_mean,predicted_var

def read_csv(name_csv):
    """
    Read csv file, extract name, original and predicted score of the molecule.

    Parameters
    ----------
    filename : str
        Filename of the csv file.

    Returns
    -------
    name : array of strings
        Array containing names of the molecules.
    original : array of floats
        Array containing original scores.
    predicted : array of floats
        Array containing original scores.

    """
    
    # Nacitanie a transformovanie dat
    df = pd.read_csv(name_csv, sep=';')
    data = df.values.transpose()

    #print(df.columns[0])

    # Vyberieme stlpce z dat z ktorych sa bude robit graf
    name = data[0] # coumpounds labels
    original = data[1] #np.asarray(data[1], dtype = np.float64)
    predicted = data[2:] #np.asarray(data[2:], dtype = np.float64)
    # predicted = []
    # for i in range(5):
    #     predicted.append(np.asfarray(data[2+i]))

    
    return name, original, predicted

def load_csv_files(name_csv):
    
    r = None
    
    name, original, predicted = read_csv(name_csv)
    
    output = run_stats( r,
                        name,
                        original,
                        predicted
                        )
    
    return output

def load_results(prefix_path_to_result, suffix_path_to_result):
    
    
    adresare = ['01', '02', '03', '04', '05']
    sablona = os.path.join(prefix_path_to_result,suffix_path_to_result)

    meno_all = []
    AD_all = []
    TF_all = []
    
    # data agregation
    
    for adresar in adresare:
        
        meno, AD, TF = read_csv(sablona.replace("XX",adresar))
        meno_all.append(meno)
        AD_all.append(AD)
        TF_all.append(TF[0])
    
    r = None    
    
    output = run_stats(r,
                       meno_all[0],
                       AD_all[0],
                       TF_all)

    return output


def main():
    
    prefix_path_to_result = "./reference"
    suffix_path_to_result = "XX/in_vitro_80_XXb_5Ang.csv"
    
    reference = load_results(prefix_path_to_result, suffix_path_to_result)
    
    name_csv = "in_vitro_Schnet20_6_5Ang_train80.csv"
    
    current =  load_csv_files(name_csv)
    
    DS_original_difference = reference.original - current.original
    DS_predicted_difference = reference.predicted - current.predicted
    
    print("Difference of the expected docking score between reference and current. Ideal value is zero.")
    print("Max: ", DS_original_difference.max(), "kcal/mol")
    print("Min: ", DS_original_difference.min(), "kcal/mol")
    
    print("Difference of the predicted docking score between reference and current. Ideal value is zero.")
    print("Max: ", DS_predicted_difference.max(), "kcal/mol")
    print("Min: ", DS_predicted_difference.min(), "kcal/mol")
    print("Everything bellow 1e-4 is good.")
    if np.abs(DS_predicted_difference).max() < 1e-4 :
        print("Success.")
    else:
        print("Something is wrong.")
    #print(reference.predicted.shape)
    #print(reference.predicted, current.predicted)
    #print(DS_predicted_difference)
    
    abundance = []
    intervals = []
    for difference in DS_predicted_difference:
        abundance0, intervals0 = np.histogram(difference, 
                                              bins=50
                                              )
        abundance.append(abundance0)
        intervals.append(intervals0)
    
    for i,a in zip(intervals,abundance):
        matplotlib.pyplot.plot(i[:-1], 
                               a
                               )
        
    png_name = "in_vitro_instalation_test.png"
    matplotlib.pyplot.savefig(png_name, dpi= 300)
    
    print("Distribution of the differences is ploted and saved in file ", png_name)
    
    return 0

if __name__ == "__main__":
   main()
