set isosamples 40
unset key
set title "Courbe 3D"
set xrange [-10:10]
set yrange [-10:10]
set ztics 1
splot 1.50*exp(-(x**2+y**2)/20)*cos(sqrt(x**2+y**2))
set view 29,53 #Done implicitly by mousing.
