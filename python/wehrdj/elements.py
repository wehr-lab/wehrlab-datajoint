"""
Module that contains imports and activations for datajoint elements schemas.

Other schema should be written elsewhere, presumably in a schema module, and
then given a central ``activate`` function..

Don't be fooled by the "module imported but not used" errors your linter will give you,
for some reason you do have to import `Subject` et al even if they aren't used directly.
Don't ask me why.
"""

import datajoint as dj

from element_lab import lab
from element_animal import subject, genotyping
from element_animal.subject import Subject
from element_lab.lab import Source, Lab, Protocol, User, Location, Project
from element_session import session
#from element_array_ephys import ephys_chronic


def activate():
	"""
	Call the activation functions from each of the imported elements.
	Must have already called :func:`wehrdj.connect`

	Currently:

	* element_lab.lab
	* element_animal.subject
	* element_animal.genotyping
	* element_session.session

	It uses ``wehrdj.elements`` as the linking module, which I believe
	is necessary because it looks for a particular context when instantiating
	the schema? Not really sure on that one.


	"""
	lab.activate('lab')
	subject.activate('subject', linking_module='wehrdj.elements')
	genotyping.activate('genotyping', 'subject', linking_module='wehrdj.elements')
	session.activate('session', linking_module='wehrdj.elements')
	#ephys_chronic.activate('ephys_chronic', linking_module='wehrdj.elements')

