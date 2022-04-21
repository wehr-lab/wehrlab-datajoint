import datajoint as dj

from element_lab import lab
from element_animal import subject, genotyping
from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Location
from element_session import session


def activate():
	lab.activate('lab')
	subject.activate('subject', linking_module='wehrdj.elements')
	genotyping.activate('genotyping', 'subject', linking_module='wehrdj.elements')
	session.activate('session', linking_module='wehrdj.elements')
