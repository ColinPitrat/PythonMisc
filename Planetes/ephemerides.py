#!/usr/bin/python
# -*- coding: utf8 -*-"

import datetime
import collections
import math
import sympy

fileprefix = "inpop17a_TCB_m100_p100_asc"
abbreviations = {
    "Soleil": "Sun",
    "Mercure": "Mer",
    "Venus": "Ven",
    "Terre": "Ear",
    "Lune": "Moo",
    "Mars": "Mar",
    "Jupiter": "Jup",
    "Saturne": "Sat",
    "Uranus": "Ura",
    "Neptune": "Nep",
    "Pluton": "Plu",
}

X = sympy.symbols('x')
polynomesTchebychev = [ 1, X ]

def PrecomputeTchebychev(n):
    global polynomesTchebychev, X
    for i in range(len(polynomesTchebychev), n+1):
        polynomesTchebychev.append(sympy.simplify(2*X*polynomesTchebychev[i-1] - polynomesTchebychev[i-2]))

def Tchebychev(coeffs):
    global polynomesTchebychev
    if len(coeffs) >= len(polynomesTchebychev):
        PrecomputeTchebychev(len(coeffs))
    R = 0
    for i in range(0, len(coeffs)):
        R += coeffs[i]*polynomesTchebychev[i]
    return sympy.simplify(R)

def Interpolate(coeffs, x):
    t0 = 1
    t1 = x
    r = 0
    for c in coeffs:
        r += c*t0
        #print("r += %s * %s = %s => r = %s" % (c, t0, c*t0, r))
        t2 = 2*t1*x - t0
        t0 = t1
        t1 = t2
    print("T(%s) - %s = %s" % (x, coeffs, r))
    return r

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)

utc = UTC()

def julienToDate(jd):
    # L'origine reelle est le 12 janvier -4713 a 12h, mais datetime ne supporte pas des annees negatives.
    # Le jour julien reduit commence 2400000 jours plus tard.
    # https://en.wikipedia.org/wiki/Julian_day#Variants
    origin = datetime.datetime(year=1858, month=11, day=16, hour=12, tzinfo=utc)
    rjd = jd - 2400000
    return origin + datetime.timedelta(seconds=int(3600*24*rjd))

def dateToJulien(d):
    origin = datetime.datetime(year=1858, month=11, day=16, hour=12, tzinfo=utc)
    td = d - origin
    rjd = td.days + (float(td.seconds)/3600/24)
    return rjd + 2400000

def fichier(info, directory, corps):
    return directory + "/" + fileprefix + "_" + info + "_" + abbreviations[corps] + ".asc"

def fichier_position(directory, corps):
    return fichier("pos", directory, corps)

def fichier_vitesse(directory, corps):
    return fichier("vel", directory, corps)

class Ephemeride(object):

    def __init__(self, corps, info, unite, ordre, duree):
        self.corps = corps
        self.info = info
        self.unite = unite
        self.ordre = ordre
        self.duree = datetime.timedelta(seconds=int(duree*3600*24))
        self.coeffs = collections.OrderedDict()
        self.polynoms = collections.OrderedDict()

    def AddCoeffs(self, axe, debut, coeffs):
        if debut not in self.coeffs:
            self.coeffs[debut] = {}
            self.polynoms[debut] = {}
        self.coeffs[debut][axe] = coeffs

    def ValeurA(self, axe, date):
      debut = self.polynoms.keys()[0]
      val = debut
      while val <= date:
        debut = val
        val += self.duree
      if axe not in self.polynoms[debut]:
        self.polynoms[debut][axe] = Tchebychev(self.coeffs[debut][axe])
      #return Interpolate(self.coeffs[debut][axe], dateToJulien(date)-dateToJulien(debut))
      return self.polynoms[debut][axe].evalf(subs={X: 2*(dateToJulien(date)-dateToJulien(debut))/self.duree.days-1.0})

    def __str__(self):
        print("%s de %s:" % (self.info, self.corps))
        for d, c in self.coeffs.iteritems():
            print("  %s: %s" % (d, c))


def parse_asc(filename):
    ephemeride = None
    with open(filename) as f:
        data = f.readlines()
        version = data[0].split(':')[1].strip()
        #print("Version: %s" % version)
        infos = data[1].split()
        corps = infos[0]
        origine = infos[1]
        info = infos[3]
        unite = infos[4]
        #print("Corps: %s\nOrigine: %s\nInfo: %s\nUnite: %s" % (corps, origine, info, unite))
        if origine != "Barycenter" and origine != 'Geocentric':
            raise ValueError("Ce fichier a une origine '%s' et non 'Barycenter' ou 'Geocentric' !" % origine)
        dimension = int(infos[5])
        ordre = int(infos[6])
        duree = float(infos[7])
        nb_points = int(infos[8])
        #print("Dimension: %s\nOrder: %s\nDuree: %s\nNb points: %s" % (dimension, ordre, duree, nb_points))
        if dimension != 3:
            raise ValueError("Ce fichier est en dimension %s et non 3 (x, y, z) !" % dimension)
        i = 2
        ephemeride = Ephemeride(corps, info, unite, ordre, duree)
        axes = ['x', 'y', 'z']
        while i < len(data):
            valeurs = data[i].split()
            debut = float(valeurs[0])
            fin = float(valeurs[1])
            if fin - debut != duree:
                raise ValueError("Une ligne a une duree de %s alors que le fichier annonce une duree de %s" % (fin-debut, duree))
            coeffs = []
            for j in range(0, ordre):
                coeffs.append(float(valeurs[2+j].replace('D', 'e')))
            ephemeride.AddCoeffs(axes[(i-2)%3], julienToDate(debut), coeffs)
            i += 1
    return ephemeride

def distance_terre_soleil():
    fichier_terre = fichier_position('/home/cpitrat/Downloads', 'Terre')
    fichier_soleil = fichier_position('/home/cpitrat/Downloads', 'Soleil')
    #print("Fichier terre: %s" % fichier_terre)
    #print("Fichier soleil: %s" % fichier_soleil)
    e_terre = parse_asc(fichier_terre)
    e_soleil = parse_asc(fichier_soleil)
    print('date,julien,distance Terre Soleil,Xt,Yt,Zt,Xs,Ys,Zs')
    for t in range(2414105, 2415105):
        d = julienToDate(float(t))
        x_t = e_terre.ValeurA('x', d)
        y_t = e_terre.ValeurA('y', d)
        z_t = e_terre.ValeurA('z', d)
        x_s = e_soleil.ValeurA('x', d)
        y_s = e_soleil.ValeurA('y', d)
        z_s = e_soleil.ValeurA('z', d)
        d_ts = math.sqrt((x_s-x_t)**2 + (y_s-y_t)**2 + (z_s-z_t)**2)
        #print('Le %s (%s), distance Terre-Soleil: %s \t (%s\t%s\t%s)\t(%s\t%s\t%s)' % (d, t, d_ts, x_t, y_t, z_t, x_s, y_s, z_s))
        print('%s,%s,%s,%s,%s,%s,%s,%s,%s' % (d, float(t), d_ts, x_t, y_t, z_t, x_s, y_s, z_s))

def conditions_initiales():
    d = julienToDate(2414105)
    d = julienToDate(2414470)
    print("Le %s:" % d)
    for corps, abbr in abbreviations.iteritems():
        e_pos = parse_asc(fichier_position('/home/cpitrat/Downloads', corps))
        e_vit = parse_asc(fichier_vitesse('/home/cpitrat/Downloads', corps))
        x = e_pos.ValeurA('x', d)*1000
        y = e_pos.ValeurA('y', d)*1000
        z = e_pos.ValeurA('z', d)*1000
        vx = e_vit.ValeurA('x', d)*1000/3600/24
        vy = e_vit.ValeurA('y', d)*1000/3600/24
        vz = e_vit.ValeurA('z', d)*1000/3600/24
        print('%s: pos(%s, %s, %s) - vit(%s, %s, %s)' % (corps, x, y, z, vx, vy, vz))

def main():
    conditions_initiales()

if __name__ == '__main__':
    main()
