import uncertainties as unc

x = unc.ufloat(95.8,0.1)
y = unc.ufloat(2.30,0.02)

l = x - y

print('a: ', l)


rel_usik = l.std_dev / x.nominal_value

print(rel_usik)