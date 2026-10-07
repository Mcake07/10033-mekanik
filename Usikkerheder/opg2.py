import uncertainties as unc

# a)
v1 = unc.ufloat(14.0, 0.01 * 14.0)
v2 = unc.ufloat(18.0, 0.01 * 18.0)

delta_v = v2 - v1

print(delta_v)
print("Relativ usikkerhed:", delta_v.s / delta_v.n * 100, "%")
# b)
v1 = unc.ufloat(19.0, 0.01 * 19.0)
v2 = unc.ufloat(19.6, 0.01 * 19.6)

delta_v = v2 - v1

print("Relativ usikkerhed:", delta_v.s / delta_v.n * 100, "%") #.n er nominal og .s er stadard deviation