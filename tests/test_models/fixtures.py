from pathlib import Path

from pytest import MonkeyPatch, fixture

from scbl_db.models.data import Platform
from scbl_db.models.entities import Institution, Lab, Person


@fixture(scope='class')
def institution() -> Institution:
    """
    Create a valid Institution object for testing.
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
    Create a valid Person object for testing.
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
    """Create a valid Lab object for testing"""
    (
        delivery_parent_dir / f'{person.first_name.lower()}_{person.last_name.lower()}'
    ).mkdir()
    return Lab(institution=institution, pi=person)


@fixture(scope='class')
def platform() -> Platform:
    """
    Create a valid Platform object for testing.
    """
    return Platform(name='Chromium')
