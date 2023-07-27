import sys
import re
from bootstrap import get_CI, get_CR
import numpy as np




#####################################
########## LOAD INPUT DATA ##########
#####################################

if len(sys.argv) != 11:
    print("\n\nPLEASE, PROVIDE THE NUMBER OF RUN FOLDERS (NAMED RUN1, RUN2, ETC. WHICH HAVE PHI.DAT AND PSI.DAT FILES), ITS TIME RESOLUTION (IN SECONDS), THE LOWER AND THE UPPER TARGET STATE PHI VALUES, THE LOWER AND THE UPPER TARGET STATE PSI VALUES AS COMMAND LINE ARGUMENTS, E.G.:\n\n\t'python get_mfpt.py  5  20e-12  -120.0  -30.0  -90.0  -30.0  -120.0  -30.0  60.0  180.0'\n\n\n")
    sys.exit()
else:
    NumFolders = int(sys.argv[1])
    dt = float(sys.argv[2])
    MinValPhi1 = float(sys.argv[3])
    MaxValPhi1 = float(sys.argv[4])
    MinValPsi1 = float(sys.argv[5])
    MaxValPsi1 = float(sys.argv[6])
    MinValPhi2 = float(sys.argv[7])
    MaxValPhi2 = float(sys.argv[8])
    MinValPsi2 = float(sys.argv[9])
    MaxValPsi2 = float(sys.argv[10])

#####################################






###################################################################
####### DEFINE & LOAD STATES & CALCULATE THE PASSAGE TIMES ########
###################################################################
state_F = [1]              # folded   state definition
state_U = [3]              # unfolded state definition
PT_FU = []                 # passage time F to U
PT_UF = []                 # passage time U to F
for i in range(1, NumFolders+1):
    states = []
    data_phi = []
    data_psi = []
    for line in open("run"+str(i)+"/rmsd_final.dat").readlines() :
        Words = line.split()
        if (len(Words) > 0) and (re.search("\d", Words[0])) :
            data_phi.append(float(Words[1]))
    for line in open("run"+str(i)+"/rg_final.dat").readlines() :
        Words = line.split()
        if (len(Words) > 0) and (re.search("\d", Words[0])) :
            data_psi.append(float(Words[1]))
    for j in range(len(data_phi)):
        if MinValPhi1 <= data_phi[j] <= MaxValPhi1 and MinValPsi1 <= data_psi[j] <= MaxValPsi1:
            states.append(1)		# 'state 1' = folded
        elif MinValPhi2 <= data_phi[j] <= MaxValPhi2 and MinValPsi2 <= data_psi[j] <= MaxValPsi2:
            states.append(3)		# 'state 3' = unfolded
        else:
            states.append(2)		# 'state 2' = transition state
    count = 0  		# first passage time counter
    P_state = "PREVIOUS" 	# previous state
    # loop through all state frames, determine the current state, calculate the passage time
    for frame in states:	
        if frame in state_F:
            state = "F"
        elif frame in state_U:
            state = "U"
        else:
            state = P_state
        if (state == "F") or (state == "U"):
            count += 1
        if P_state == "F" and state == "U":
            PT_FU.append(count)
            count = 0
        elif P_state == "U" and state == "F":
            PT_UF.append(count)
            count = 0
        elif P_state == "PREVIOUS" and (state == "F" or state == "U"):
            count = 0
        P_state = state
#####################################






#####################################
######## CALCULATE THE MFPTs ########
#####################################

# check the existence of passage times
if len(PT_FU) == 0 :
   print("WARNING: No F->U events observed!")
   sys.exit()
if len(PT_UF) == 0 :
   print("WARNING: No U->F events observed!")
   sys.exit() 


# mfpts in seconds
mfpt_FU = float(sum(PT_FU)) / len(PT_FU) * dt
mfpt_FU = 1.0/(mfpt_FU*1e9)
mfpt_UF = float(sum(PT_UF)) / len(PT_UF) * dt
mfpt_UF = 1.0/(mfpt_UF*1e9)


# Bayesian bootstrapping for uncertainty estimation
[PT_FU_CRmin,PT_FU_CRmax] = get_CR(PT_FU, 10000) 
[PT_UF_CRmin,PT_UF_CRmax] = get_CR(PT_UF, 10000)
PT_FU_CRmin *= dt
PT_FU_CRmin = 1.0/(PT_FU_CRmin*1e9)
PT_FU_CRmax *= dt
PT_FU_CRmax = 1.0/(PT_FU_CRmax*1e9)
PT_UF_CRmin *= dt
PT_UF_CRmin = 1.0/(PT_UF_CRmin*1e9)
PT_UF_CRmax *= dt
PT_UF_CRmax = 1.0/(PT_UF_CRmax*1e9)
#####################################






#####################################
######### PRINTING RESULTS ##########
#####################################

print("MFTS (in seconds):") 
print("F-->U: mean = ", mfpt_FU, "\t", "confidence interval =  [", PT_FU_CRmin, ",", PT_FU_CRmax, "]")
print("U-->F: mean = ", mfpt_UF, "\t", "confidence interval =  [", PT_UF_CRmin, ",", PT_UF_CRmax, "]")
 
#####################################



