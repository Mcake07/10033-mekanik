import uncertainties as unc

a = unc.ufloat(5, 1)
b = unc.ufloat(18, 2)
c = unc.ufloat(12, 1)
t = unc.ufloat(3, 0.5)
m = unc.ufloat(18, 1)

# a)
s = a+b+c
print(s)
print(s.std_dev / s.nominal_value)

# b)
s = a + b - c
print(s)

# c)
s = c * t
print(s)
print(s.std_dev / s.nominal_value)


# d)
s = (m * b) / t
print(s)
print(s.std_dev /s.nominal_value)