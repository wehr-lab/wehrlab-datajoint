import datajoint as dj

from element_lab import lab
from element_animal import subject, genotyping
from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Location, Project
from element_session import session
#from element_array_ephys import ephys_chronic


def activate():
	lab.activate('lab')
	subject.activate('subject', linking_module='wehrdj.elements')
	genotyping.activate('genotyping', 'subject', linking_module='wehrdj.elements')
	session.activate('session', linking_module='wehrdj.elements')
	#ephys_chronic.activate('ephys_chronic', linking_module='wehrdj.elements')

