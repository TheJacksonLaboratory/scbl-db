from datetime import date
from pathlib import Path

from pytest import MonkeyPatch, fixture

from scbl_db.models.entities import *
from scbl_db.models.platforms.chromium import *
from scbl_db.models.platforms.xenium import *
from scbl_db.models.something_to_change import *

__all__ = [
    'institution',
    'person',
    'delivery_parent_dir',
    'lab',
    'chromium',
    'xenium',
    'chromium_assay',
    'xenium_assay',
    'chromium_data_set',
    'chromium_sample',
    'chromium_library_type',
    'sequencing_run',
    'chromium_library',
    'chromium_tag',
    'xenium_run',
    'xenium_data_set',
    'xenium_sample',
]


@fixture(scope='class')
def institution() -> Institution:
    """
    Create a valid Institution object for testing dependent models.
    """
    return Institution(
        name='Jackson Laboratory for Genomic Medicine',
        short_name='JAX-GM',
        email_format='{first_name}.{last_name}@jax.org',
        country='US',
        city='Farmington',
        state='CT',
    )


@fixture(scope='class')
def person(institution: Institution) -> Person:
    """
    Create a valid Person object for testing dependent models.
    """
    return Person(
        first_name='ahmed',
        last_name='said',
        email='ahmed.said@jax.org',
        orcid='0009-0008-3754-6150',
        institution=institution,
    )


@fixture(autouse=True)
def delivery_parent_dir(monkeypatch: MonkeyPatch, tmp_path: Path) -> Path:
    """
    Create a temporary delivery parent directory for testing and set
    the environment variable delivery_parent_dir to it. Also change
    the return value of `pathlib.Path.group` to 'test_group' to avoid
    messing with groups on the system.
    """
    delivery_parent_dir = tmp_path / 'delivery'
    delivery_parent_dir.mkdir()

    monkeypatch.setenv('delivery_parent_dir', str(delivery_parent_dir))
    monkeypatch.setattr('pathlib.Path.group', lambda s: 'test_group')

    return delivery_parent_dir


@fixture
def lab(delivery_parent_dir: Path, institution: Institution, person: Person) -> Lab:
    """
    Create a valid Lab object for testing dependent models.
    """
    (
        delivery_parent_dir / f'{person.first_name.lower()}_{person.last_name.lower()}'
    ).mkdir()
    return Lab(institution=institution, pi=person)


@fixture(scope='class')
def chromium() -> Platform:
    """
    Create a valid Chromium platform object for testing dependent models.
    """
    return Platform(name='Chromium')


@fixture(scope='class')
def xenium() -> Platform:
    """
    Create a valid Platform object for testing dependent models.
    """
    return Platform(name='Xenium')


@fixture(scope='class')
def chromium_assay(chromium: Platform) -> Assay:
    """
    Create a valid Assay object for testing dependent models.
    """
    return Assay(name='Single Cell 3\' Gene Expression', platform=chromium)


@fixture(scope='class')
def xenium_assay(xenium: Platform) -> Assay:
    """
    Create a valid Assay object for testing dependent models.
    """
    return Assay(name='Xenium In Situ Gene Expression', platform=xenium)


@fixture
def chromium_data_set(
    chromium_assay: Assay, lab: Lab, person: Person
) -> ChromiumDataSet:
    """
    Create a valid ChromiumDataSet object for testing dependent models.
    """
    return ChromiumDataSet(
        id='SD9900000',
        name='chromium_data_set',
        assay=chromium_assay,
        ilab_request_id='ilab_request',
        date_initialized=date(1999, 1, 1),
        lab=lab,
        submitter=person,
    )


@fixture
def chromium_tag() -> ChromiumTag:
    """
    Create a valid ChromiumTag object for testing dependent models.
    """
    return ChromiumTag(
        id='CMO301',
        name='CMO301',
        type='CellPlex',
        read='R2',
        five_prime_offset=0,
        sequence='ATGAGGAATTCCTGC',
        pattern='5P(BC)',
    )


@fixture
def chromium_sample(chromium_data_set: ChromiumDataSet) -> ChromiumSample:
    """
    Create a valid ChromiumSample object for testing dependent models.
    """
    return ChromiumSample(
        id='SS9900000',
        data_set=chromium_data_set,
        name='chromium_sample',
        date_received=date(1999, 1, 1),
    )


@fixture
def chromium_library_type() -> ChromiumLibraryType:
    """
    Create a valid ChromiumLibraryType object for testing dependent models.
    """
    return ChromiumLibraryType(name='Gene Expression')


@fixture
def sequencing_run() -> SequencingRun:
    """
    Create a valid SequencingRun object for testing dependent models.
    """
    return SequencingRun(id='99-scbct-000', date_begun=date(1999, 1, 1))


@fixture
def chromium_library(
    chromium_data_set: ChromiumDataSet,
    chromium_library_type: ChromiumLibraryType,
    sequencing_run: SequencingRun,
) -> ChromiumLibrary:
    """
    Create a valid ChromiumLibrary object for testing dependent models.
    """
    return ChromiumLibrary(
        id='SC9900000',
        data_set=chromium_data_set,
        date_constructed=date(1999, 1, 1),
        status='status',
        library_type=chromium_library_type,
        sequencing_run=sequencing_run,
    )


@fixture
def xenium_run() -> XeniumRun:
    """
    Create a valid XeniumRun object for testing dependent models.
    """
    return XeniumRun(id='XR99000', date_begun=date(1999, 1, 1))


@fixture
def xenium_data_set(
    xenium_assay: Assay, lab: Lab, person: Person, xenium_run: XeniumRun
) -> XeniumDataSet:
    """
    Create a valid ChromiumDataSet object for testing dependent models.
    """
    return XeniumDataSet(
        id='XD9900000',
        name='xenium_data_set',
        assay=xenium_assay,
        ilab_request_id='ilab_request',
        date_initialized=date(1999, 1, 1),
        lab=lab,
        submitter=person,
        slide_serial_number='0012345',
        slide_name='slide',
        xenium_run=xenium_run,
    )


@fixture
def xenium_sample(xenium_data_set: XeniumDataSet) -> XeniumSample:
    """
    Create a valid XeniumSample object for testing dependent models.
    """
    return XeniumSample(
        id='XE9900000',
        data_set=xenium_data_set,
        name='xenium_sample',
        date_received=date(1999, 1, 1),
    )
