from typing import TypedDict

from .bases import Base
from .models.entities import *
from .models.platforms.chromium import *
from .models.platforms.xenium import *
from .models.processes import *


class OrderedModelDict(TypedDict):
    Institution: type[Institution]
    Person: type[Person]
    Lab: type[Lab]
    Platform: type[Platform]
    Assay: type[Assay]
    ChromiumDataSet: type[ChromiumDataSet]
    ChromiumTag: type[ChromiumTag]
    ChromiumSample: type[ChromiumSample]
    SequencingRun: type[SequencingRun]
    ChromiumLibraryType: type[ChromiumLibraryType]
    ChromiumLibrary: type[ChromiumLibrary]
    XeniumRun: type[XeniumRun]
    XeniumDataSet: type[XeniumDataSet]
    XeniumSample: type[XeniumSample]


ORDERED_MODELS: OrderedModelDict = {
    'Institution': Institution,
    'Person': Person,
    'Lab': Lab,
    'Platform': Platform,
    'Assay': Assay,
    'ChromiumDataSet': ChromiumDataSet,
    'ChromiumTag': ChromiumTag,
    'ChromiumSample': ChromiumSample,
    'SequencingRun': SequencingRun,
    'ChromiumLibraryType': ChromiumLibraryType,
    'ChromiumLibrary': ChromiumLibrary,
    'XeniumRun': XeniumRun,
    'XeniumDataSet': XeniumDataSet,
    'XeniumSample': XeniumSample,
}
__all__ = [
    'Base',
    'Institution',
    'Person',
    'Lab',
    'Platform',
    'Assay',
    'ChromiumDataSet',
    'ChromiumTag',
    'ChromiumSample',
    'SequencingRun',
    'ChromiumLibraryType',
    'ChromiumLibrary',
    'XeniumRun',
    'XeniumDataSet',
    'XeniumSample',
    'ORDERED_MODELS',
]
