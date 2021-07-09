import matplotlib.pyplot as plt
import numpy as np

# # IBM Verify Credentials
# y1 = np.array([10, 20, 30, 46])     #SIZE    
# y2 = np.array([7, 7, 9, 9])         #LINGUISTIC ASSOCIATION FOUND
t_ibm = np.array([x / 3 for x in [129.3174, 201.5181, 215.1554, 268.8812]])
x_ibm = np.array([10, 20, 30, 46])
t_sov = np.array([x / 3 for x in [41.5221, 103.3790, 158.6173, 205.4211, 369.7658]])
x_sov = np.array([10, 20, 30, 40, 53])
t_upo = np.array([x / 3 for x in [212.9374, 165.6264, 174.3206]])
x_upo = np.array([10, 20, 27])

fig, ax = plt.subplots()

font = {'color':'darkred','size':15}

ax.plot(x_ibm, t_ibm, label="IBM Verify Credentials", marker='*')
ax.plot(x_sov, t_sov, label="Sovrin", marker="*")
ax.plot(x_upo, t_upo, label="uPort", marker='*')
ax.set_title("Analysis time using TEWAF-SSI", fontdict=font)
ax.set_xlabel("Time taken (second)")
ax.set_ylabel("Number of SSI systemic meanings (size of SSI system)")

legend = ax.legend(loc='upper center', shadow=True)

plt.show()

# PIE CHART
# ****************
# y = np.array([495, 913])
# mylabels = ["CWE Entries WITH\n Code Example", "CWE Entries WITHOUT\n Code Example"]
# myexplode = [0.1, 0]

# p, tx, autotexts = plt.pie(y, labels = mylabels, explode = myexplode, autopct="", shadow = True)
# for i, a in enumerate(autotexts):
#     a.set_text("{} Entries".format(y[i]))

# plt.show() 