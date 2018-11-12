#    This file is part of PyChoReLib.
#
#    PyChoReLib is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    PyChoReLib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyChoReLib; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

from pychore.HelperFunctions import perm
from pychore.Scale import Scale

class Chord(Scale):
        """
        Class to hold a chord consisting of two or more notes 
        Chords are closely related to scales, and can reuse a lot of functionality from scales.
        """
        
        def CreateAllPermutations(self):
                """ Returns all chords that can be formed by permuting itself """
                return perm(self.Notes)

        def FindCanonicForm(self):
                """ Rewrites a chord into its canonical form ("canonical" probably having another meaning outside this software) """
                SimpleChord = self.WithoutDuplicateNotes()
                Permutations = Chord(SimpleChord).CreateAllPermutations() # exhaustive search... how about branch and bound instead?
                IndexOfMinimum, Idx, Minimum = 0, 0, -1
                #the base chord is the one with the minimal energy function
                #the energy function is the sum of the number of half steps between successive notes in the chord
                #hence, base chord is the chord in which the notes lie as closely spaced as possible
                MinimumEnergyChordList = {} 
                PatList = []
                for P in Permutations:
                        Pat = Chord(P).ToIntervalPattern()
                        S = sum( Pat )
                        if (S < Minimum) or (Minimum == -1):
                                #new minimum found => discard what we found up to now
                                Minimum = S
                                MinimumEnergyChordList = {}
                                MinimumEnergyChordList[tuple(Pat)] = P 
                                PatList = [ Pat, ]
                        elif S == Minimum:
                                #chord with minimum energy => add it to the list
                                MinimumEnergyChordList[tuple(Pat)] = P
                                PatList.append(Pat)
                        else:
                                #chord with larger than minimum energy => ignore
                                pass
                #now we face a problem: multiple minimum energy chords can exist if more than 3 notes are present
                #we need a way of picking one chord that will always lead to the same interval pattern, no matter
                #what note names are used. Normal "sort" will sort alphabetically. This is unusable.
                #we need to sort on the interval patterns, but return the chord that corresponds to the pattern instead
                PatList.sort()
                FirstPattern = PatList[0]
                return MinimumEnergyChordList[tuple(FirstPattern)]


