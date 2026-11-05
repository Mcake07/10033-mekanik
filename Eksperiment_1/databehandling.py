import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import uncertainties as unc
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Indlæs data
m = 0.200  # kg

df = pd.read_csv('Mekanik_forsøg.csv')
df.columns = df.columns.str.strip()

t_raw = df['time'].to_numpy()
F_raw = df['cal[0]'].to_numpy()

# 2. Reducér og udglat data
blok = 46
n = len(df) // blok

t = t_raw[:n*blok].reshape(n, blok).mean(axis=1)
F = F_raw[:n*blok].reshape(n, blok).mean(axis=1)
F = gaussian_filter1d(F, 1.5)

# 3. Find toppe og bunde
dt = np.median(np.diff(t))
afstand = max(1, int(0.6 / dt))

toppe, _ = find_peaks(F, distance=afstand, prominence=0.15)
bunde, _ = find_peaks(-F, distance=afstand, prominence=0.15)

# 4. Beregn amplituder
A = []
t_A = []

for i in range(len(toppe) - 1):
    mellem = bunde[(bunde > toppe[i]) & (bunde < toppe[i+1])]

    if len(mellem) == 1:
        j = mellem[0]
        amplitude = (F[toppe[i]] - F[j]) / 2

        if amplitude > 0:
            A.append(amplitude)
            t_A.append((t[toppe[i]] + t[j]) / 2)

A = np.array(A)
t_A = np.array(t_A)

if len(A) < 3:
    raise ValueError("For få amplituder. Kontrollér toppunkterne.")

# 5. Regression: ln(A) = ln(A0) - lambda*t
def f(t, lnA0, lam):
    return lnA0 - lam*t

param, cov = curve_fit(f, t_A, np.log(A))
delta_param = np.sqrt(np.diag(cov))

lam = unc.ufloat(param[1], delta_param[1])

print(f'Dæmpningskonstant: lambda = {lam:.2u} 1/s')

# 6. Kontrol af regressionen
residualer = np.log(A) - f(t_A, *param)

R2 = 1 - np.sum(residualer**2) / np.sum(
    (np.log(A) - np.mean(np.log(A)))**2
)

print(f'R² = {R2:.4f}')
print(f'Antal amplituder: {len(A)}')

# 7. Sammenlign tre tidsintervaller
lambda_dele = []

for start in [0, 40, 80]:
    valg = (t_A >= start) & (t_A < start + 40)

    param_del, cov_del = curve_fit(
        f, t_A[valg], np.log(A[valg])
    )

    lam_del = unc.ufloat(
        param_del[1], np.sqrt(cov_del[1, 1])
    )

    lambda_dele.append(lam_del.n)
    print(f'{start}-{start+40} s: lambda = {lam_del:.2u} 1/s')

variation = (max(lambda_dele) - min(lambda_dele)) / 2

print(f'Halv spændvidde: {variation:.5f} 1/s')

# 8. Beregn viskøs dæmpningskoefficient
b = 2 * m * lam

print(f'b = {b:.2u} kg/s')

g = 9.82
L_ligevaegt = unc.ufloat(0.101, 0.001)

k = m * g / L_ligevaegt

print(f'Fjederkonstant: k = {k:.2u} N/m')

# 9. Plot regressionen
plt.plot(t_A, np.log(A), '.', label='Målinger')
plt.plot(t_A, f(t_A, *param), '-', label='Regression')

plt.xlabel('Tid (s)')
plt.ylabel('ln(A / 1 N)')
plt.grid()
plt.legend()
plt.show()